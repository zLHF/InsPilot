from __future__ import annotations

import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from inspilot_cloud_baby.audit import (
    ADMIN_WEB_ACTOR,
    config_change_metadata,
    write_audit,
)
from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.dingtalk_admin import DingTalkAdminClient, WorkflowDoc
from inspilot_cloud_baby.embedding import get_embedding_service
from inspilot_cloud_baby.ingest.classifier import classify_material
from inspilot_cloud_baby.models import (
    AppSetting,
    KnowledgeItem,
    KnowledgeSensitivity,
    KnowledgeStatus,
    Project,
    ProjectVisibility,
)

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter(prefix="/admin", tags=["admin"])

# ---------------------------------------------------------------------------
# Mapping helpers for template display
# ---------------------------------------------------------------------------


def _attach_embedding(item: KnowledgeItem) -> None:
    """Generate and attach an embedding vector to a newly created KnowledgeItem."""
    svc = get_embedding_service()
    if not svc.available:
        return
    vector = svc.embed_text(f"{item.title}\n{item.body}")
    if vector is not None:
        item.embedding = vector

VISIBILITY_LABELS = {
    ProjectVisibility.COMPANY_VISIBLE: "公司可见",
    ProjectVisibility.PROJECT_MEMBERS: "项目成员",
    ProjectVisibility.RESTRICTED: "受限",
}

SENSITIVITY_LABELS = {
    KnowledgeSensitivity.PUBLIC_SUMMARY: "公开摘要",
    KnowledgeSensitivity.PROJECT_RESTRICTED: "项目受限",
    KnowledgeSensitivity.SENSITIVE: "敏感",
}

STATUS_LABELS = {
    KnowledgeStatus.DRAFT: "草稿",
    KnowledgeStatus.PENDING_REVIEW: "待审核",
    KnowledgeStatus.ACTIVE: "已生效",
    KnowledgeStatus.ARCHIVED: "已归档",
    KnowledgeStatus.CONFLICT: "冲突",
}

STATUS_COLORS = {
    KnowledgeStatus.DRAFT: "gray",
    KnowledgeStatus.PENDING_REVIEW: "amber",
    KnowledgeStatus.ACTIVE: "green",
    KnowledgeStatus.ARCHIVED: "slate",
    KnowledgeStatus.CONFLICT: "red",
}

PROJECT_OPTIONS_LABEL = "— 不指定项目 —"

MATERIAL_TYPE_LABELS = {
    "rate_table": "费率表",
    "operation_guide": "操作指南",
    "technical_solution": "技术方案",
    "project_note": "项目笔记",
}

SCOPE_LABELS = {
    "project": "项目",
    "public": "公共",
    "private": "个人",
    "unknown": "待识别",
}


# ---------------------------------------------------------------------------
# Template context helper
# ---------------------------------------------------------------------------

def _ctx(request: Request, **extra: object) -> dict:
    ctx = {"request": request}
    ctx.update(extra)
    return ctx


def _knowledge_row_context(
    request: Request,
    *,
    item: KnowledgeItem,
    project_name: str = "",
    projects: list[Project] | None = None,
) -> dict:
    return _ctx(
        request,
        item=item,
        project_name=project_name,
        projects=projects or [],
        project_options_label=PROJECT_OPTIONS_LABEL,
        status_labels=STATUS_LABELS,
        status_colors=STATUS_COLORS,
        sensitivity_labels=SENSITIVITY_LABELS,
        material_type_labels=MATERIAL_TYPE_LABELS,
    )


def _format_operation_record(rec: dict) -> str:
    user_id = rec.get("userid") or rec.get("userId") or rec.get("creatorUserId") or "未知"
    op_type = rec.get("operation_type") or rec.get("operationType") or ""
    result = rec.get("operation_result") or rec.get("operationResult") or rec.get("result", "")
    remark = rec.get("remark", "")
    date = rec.get("date_formatted") or rec.get("date", "")
    parts = [str(v) for v in (date, user_id, op_type, result, remark) if v]
    return " / ".join(parts) if parts else "未知"


def _build_dingtalk_knowledge_body(workflow: WorkflowDoc) -> str:
    body_parts = [f"# {workflow.title or workflow.process_instance_id}"]
    if workflow.status:
        body_parts.append(f"\n**审批状态**: {workflow.status}")
    if workflow.originator:
        body_parts.append(f"**发起人**: {workflow.originator}")

    if workflow.form_data:
        body_parts.append("\n## 表单字段")
        for name, value in workflow.form_data.items():
            body_parts.append(f"- **{name}**: {value}")

    if workflow.operation_records:
        body_parts.append("\n## 审批链条")
        for rec in workflow.operation_records:
            if workflow.remarks and str(rec.get("remark", "")).strip():
                continue
            body_parts.append(f"- {_format_operation_record(rec)}")

    if workflow.remarks:
        body_parts.append("\n## 审批意见")
        for remark in workflow.remarks:
            details = [
                remark.get("timestamp", ""),
                remark.get("user_id", "未知"),
                remark.get("node_name", ""),
                remark.get("operation_result", ""),
            ]
            prefix = " / ".join(str(value) for value in details if value)
            body_parts.append(f"- {prefix}: {remark.get('content', '')}")
    elif workflow.comments:
        body_parts.append("\n## 审批意见")
        for comment in workflow.comments:
            body_parts.append(
                f"- **{comment.get('user_id', '未知')}**"
                f"{' @ ' + comment.get('timestamp', '') if comment.get('timestamp') else ''}: "
                f"{comment.get('content', '')}"
            )

    if workflow.comment_status in {"unavailable", "error"}:
        body_parts.append(
            "\n> 独立评论接口不可用，审批意见已按审批操作记录降级导入。"
        )

    if workflow.attachments:
        body_parts.append("\n## 附件")
        for att in workflow.attachments:
            body_parts.append(f"- {att.get('file_name', att.get('field_name', '附件'))}")

    return "\n".join(body_parts)


def _get_dingtalk_config() -> dict[str, str]:
    db_settings = _load_db_settings()
    return {
        "app_key": settings.dingtalk_app_key or db_settings.get("dingtalk_app_key", ""),
        "app_secret": settings.dingtalk_app_secret or db_settings.get("dingtalk_app_secret", ""),
    }


def _has_admin_credentials() -> bool:
    """Check if enterprise admin credentials are configured."""
    cfg = _get_dingtalk_config()
    return bool(cfg["app_key"] and cfg["app_secret"])


def _admin_client() -> DingTalkAdminClient | None:
    """Return a DingTalkAdminClient if credentials are configured."""
    cfg = _get_dingtalk_config()
    if cfg["app_key"] and cfg["app_secret"]:
        return DingTalkAdminClient(cfg["app_key"], cfg["app_secret"])
    return None


# ---------------------------------------------------------------------------
# DB session helper — graceful fallback when DB is unavailable
# ---------------------------------------------------------------------------

def _db_query(func, *args, **kwargs):
    """Execute a DB query function, returning None on failure."""
    try:
        return func(*args, **kwargs)
    except Exception:
        logger.warning("Database query failed, using empty data", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@router.get("")
def dashboard(request: Request):
    def _query():
        with SessionLocal() as session:
            return {
                "project_count": session.scalar(select(func.count()).select_from(Project)) or 0,
                "knowledge_count": session.scalar(select(func.count()).select_from(KnowledgeItem)) or 0,
                "pending_count": session.scalar(
                    select(func.count())
                    .select_from(KnowledgeItem)
                    .where(KnowledgeItem.status == KnowledgeStatus.PENDING_REVIEW)
                ) or 0,
                "active_count": session.scalar(
                    select(func.count())
                    .select_from(KnowledgeItem)
                    .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
                ) or 0,
            }
    stats = _db_query(_query) or {"project_count": 0, "knowledge_count": 0, "pending_count": 0, "active_count": 0}
    return templates.TemplateResponse(request, "dashboard.html", _ctx(request, **stats))


@router.get("/ingest")
def ingest_page(request: Request):
    def _query():
        with SessionLocal() as session:
            return list(session.scalars(select(Project).order_by(Project.name)).all())
    projects = _db_query(_query) or []
    return templates.TemplateResponse(request, "ingest.html", _ctx(request, projects=projects))


@router.get("/knowledge")
def knowledge_page(
    request: Request,
    status: str = Query(""),
    project_id: str = Query(""),
    sensitivity: str = Query(""),
    q: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):

    def _query():
        with SessionLocal() as session:
            stmt = select(KnowledgeItem).order_by(KnowledgeItem.created_at.desc())
            if status:
                try:
                    stmt = stmt.where(KnowledgeItem.status == KnowledgeStatus(status))
                except ValueError:
                    pass
            if project_id:
                stmt = stmt.where(KnowledgeItem.project_id == uuid.UUID(project_id))
            if sensitivity:
                try:
                    stmt = stmt.where(KnowledgeItem.sensitivity == KnowledgeSensitivity(sensitivity))
                except ValueError:
                    pass
            if q:
                stmt = stmt.where(KnowledgeItem.title.ilike(f"%{q}%"))
            # Total count (before pagination)
            total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
            # Paginated slice
            items = list(session.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all())
            projects = list(session.scalars(select(Project).order_by(Project.name)).all())
            return items, projects, total
    result = _db_query(_query) or ([], [], 0)
    items, projects, total = result
    project_names = {str(p.id): p.name for p in projects}
    total_pages = max(1, (total + page_size - 1) // page_size)
    # Build a query-string prefix that carries active filters (for pager links)
    filter_qs_parts = []
    if q:
        filter_qs_parts.append(f"q={q}")
    if status:
        filter_qs_parts.append(f"status={status}")
    if project_id:
        filter_qs_parts.append(f"project_id={project_id}")
    if sensitivity:
        filter_qs_parts.append(f"sensitivity={sensitivity}")
    if page_size != 20:
        filter_qs_parts.append(f"page_size={page_size}")
    filter_qs = "&".join(filter_qs_parts)
    return templates.TemplateResponse(
        request,
        "knowledge.html",
        _ctx(
            request,
            items=items,
            projects=projects,
            project_names=project_names,
            current_status=status,
            current_project=project_id,
            current_sensitivity=sensitivity,
            current_query=q,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            filter_qs=filter_qs,
            status_labels=STATUS_LABELS,
            status_colors=STATUS_COLORS,
            sensitivity_labels=SENSITIVITY_LABELS,
            material_type_labels=MATERIAL_TYPE_LABELS,
            project_options_label=PROJECT_OPTIONS_LABEL,
        ),
    )


@router.get("/projects")
def projects_page(request: Request):
    def _query():
        with SessionLocal() as session:
            projects = list(session.scalars(select(Project).order_by(Project.name)).all())
            counts = dict(
                session.execute(
                    select(KnowledgeItem.project_id, func.count())
                    .group_by(KnowledgeItem.project_id)
                ).all()
            )
            return projects, counts
    result = _db_query(_query) or ([], {})
    projects, counts = result
    return templates.TemplateResponse(
        request,
        "projects.html",
        _ctx(request, projects=projects, counts=counts, visibility_labels=VISIBILITY_LABELS),
    )


@router.get("/dws")
def dws_page(request: Request):
    return templates.TemplateResponse(request, "dws.html", _ctx(request))


@router.get("/search")
def search_page(request: Request):
    return templates.TemplateResponse(request, "search.html", _ctx(request))


@router.get("/search/facets")
def search_facets():
    """Return distinct region/insurer/integrator values for filter dropdowns."""
    from fastapi.responses import JSONResponse

    # Noise region values from functional pages (not real regions)
    _region_noise = {
        "ca授权签章", "ca登录", "ok", "‼️发票申请", "CS3.0", "三方平台方案模板",
        "签章", "发票", "流程图", "付款通知书", "退保", "出单", "打款", "中心",
    }

    def _clean(values):
        return sorted(v for v in values if v and v not in _region_noise and len(v) >= 2)

    def _query():
        with SessionLocal() as session:
            regions = _clean(session.execute(
                select(func.distinct(KnowledgeItem.metadata_json["region"]))
                .where(KnowledgeItem.source_type == "cs3_plan")
            ).scalars().all())
            insurers = _clean(session.execute(
                select(func.distinct(KnowledgeItem.metadata_json["insurer"]))
                .where(KnowledgeItem.source_type == "cs3_plan")
            ).scalars().all())
            integrators = _clean(session.execute(
                select(func.distinct(KnowledgeItem.metadata_json["integrator"]))
                .where(KnowledgeItem.source_type == "cs3_plan")
            ).scalars().all())
            return {"regions": regions, "insurers": insurers, "integrators": integrators}

    facets = _db_query(_query) or {"regions": [], "insurers": [], "integrators": []}
    return JSONResponse(facets)


# ---------------------------------------------------------------------------
# Plan detail — structured rendering of a scheme's body
# ---------------------------------------------------------------------------

# Known section titles inside a CS3.0 plan body (rendered as sub-headings).
_PLAN_SECTIONS = {
    "密文话术模板", "明文话术模板", "客户端退保说明", "业务模式说明",
    "中心对接标准", "平台对接模式", "平台对接", "客户端配置说明",
    "收款账户", "保司端方案说明", "项目基础信息", "操作记录",
    "退保审批单", "转账授权书", "专票确认函", "投保单模板",
    "关闭诉求1", "关闭诉求2", "单证说明", "方案依据", "方案说明",
    "中心平台操作页面流程", "平台订单申请调研", "中心平台功能调研",
}


def _is_section_title(line: str) -> bool:
    """True if a line is a known plan section heading (exact-ish match)."""
    return line in _PLAN_SECTIONS or any(line.startswith(s) for s in _PLAN_SECTIONS)


def format_plan_body(body: str) -> str:
    """Convert a plan's plain-text body into structured HTML for display.

    Rules:
      - known section titles → <h3> heading
      - 《...》 document names → heading
      - "key：value" (key ≤ 12 chars) → definition row
      - everything else → paragraph
    """
    import html as html_mod
    import re

    if not body:
        return ""

    # Split into lines, drop empty/BOM noise
    raw_lines = body.split("\n")
    lines = [ln.strip() for ln in raw_lines if ln.strip() and ln.strip() != "\ufeff"]

    out: list[str] = []
    kv_re = re.compile(r"^(.{1,12})[：:](.+)$")
    doc_re = re.compile(r"^《.+》")

    for ln in lines:
        esc = html_mod.escape(ln)
        if _is_section_title(ln):
            out.append(f'<h3 class="plan-section">{esc}</h3>')
        elif doc_re.match(ln):
            out.append(f'<h4 class="plan-doc">{esc}</h4>')
        else:
            m = kv_re.match(ln)
            if m and not _is_section_title(m.group(1)):
                key = html_mod.escape(m.group(1))
                val = html_mod.escape(m.group(2).strip())
                out.append(f'<div class="plan-kv"><span class="plan-k">{key}：</span><span class="plan-v">{val}</span></div>')
            else:
                out.append(f"<p>{esc}</p>")

    return "\n".join(out)


@router.get("/knowledge/{item_id}")
def knowledge_detail(request: Request, item_id: str):
    """Read-only detail view of a single knowledge item / scheme."""
    import uuid as uuid_mod

    def _query():
        with SessionLocal() as session:
            return session.get(KnowledgeItem, uuid_mod.UUID(item_id))

    item = _db_query(_query)
    if not item:
        return templates.TemplateResponse(
            request,
            "knowledge_detail.html",
            _ctx(request, item=None, item_id=item_id, body_html=""),
            status_code=404,
        )

    body_html = format_plan_body(item.body)
    return templates.TemplateResponse(
        request,
        "knowledge_detail.html",
        _ctx(
            request,
            item=item,
            item_id=item_id,
            body_html=body_html,
            meta=item.metadata_json or {},
        ),
    )


# ---------------------------------------------------------------------------
# HTMX partials / API
# ---------------------------------------------------------------------------

@router.post("/ingest/preview")
def ingest_preview(request: Request, text: str = Form(""), filename: str = Form("")):
    """Run classifier on submitted text and return preview card."""
    result = classify_material(filename=filename, text=text)

    def _query():
        with SessionLocal() as session:
            return list(session.scalars(select(Project).order_by(Project.name)).all())

    projects = _db_query(_query) or []
    return templates.TemplateResponse(
        request,
        "partials/_ingest_preview.html",
        _ctx(
            request,
            filename=filename,
            text_preview=text[:500],
            result=result,
            projects=projects,
            scope_labels=SCOPE_LABELS,
            material_type_labels=MATERIAL_TYPE_LABELS,
            sensitivity_labels=SENSITIVITY_LABELS,
        ),
    )


@router.post("/ingest/confirm")
def ingest_confirm(
    request: Request,
    title: str = Form(""),
    scope: str = Form("project"),
    project_id: str = Form(""),
    material_type: str = Form(""),
    sensitivity: str = Form(""),
    note: str = Form(""),
    original_text: str = Form(""),
):
    """Save the knowledge item to database."""
    item_id = None

    def _query():
        with SessionLocal() as session:
            item = KnowledgeItem(
                title=title or "未命名资料",
                body=original_text,
                source_type=material_type or "manual",
                sensitivity=KnowledgeSensitivity(sensitivity)
                if sensitivity
                else KnowledgeSensitivity.PROJECT_RESTRICTED,
                status=KnowledgeStatus.PENDING_REVIEW,
                project_id=uuid.UUID(project_id) if project_id else None,
                metadata_json={"note": note, "scope": scope},
                created_by="admin",
            )
            session.add(item)
            _attach_embedding(item)
            session.flush()
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="knowledge.create",
                resource_type="knowledge_item",
                resource_id=str(item.id),
                metadata={"source_type": item.source_type, "status": item.status.value},
            )
            session.commit()
            return item.id

    item_id = _db_query(_query)
    return templates.TemplateResponse(
        request,
        "partials/_ingest_success.html",
        _ctx(request, item_id=item_id, title=title or "未命名资料"),
    )


@router.post("/projects/create")
def project_create(
    request: Request,
    name: str = Form(""),
    visibility: str = Form("company_visible"),
    summary: str = Form(""),
):
    """Create a new project."""
    def _query():
        with SessionLocal() as session:
            project = Project(
                name=name,
                visibility=ProjectVisibility(visibility),
                summary=summary,
            )
            session.add(project)
            session.flush()
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="project.create",
                resource_type="project",
                resource_id=str(project.id),
                metadata={"name": project.name, "visibility": project.visibility.value},
            )
            session.commit()
            return project

    project = _db_query(_query)
    if not project:
        return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))
    return templates.TemplateResponse(
        request,
        "partials/_project_row.html",
        _ctx(request, project=project, item_count=0, visibility_labels=VISIBILITY_LABELS),
    )


@router.put("/knowledge/{item_id}/status")
def knowledge_update_status(request: Request, item_id: str, status: str = Form(...)):
    """Update knowledge item status."""
    def _query():
        with SessionLocal() as session:
            item = session.get(KnowledgeItem, uuid.UUID(item_id))
            if not item:
                return None
            before = item.status.value
            item.status = KnowledgeStatus(status)
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="knowledge.status.update",
                resource_type="knowledge_item",
                resource_id=str(item.id),
                metadata={"before": {"status": before}, "after": {"status": item.status.value}},
            )
            session.commit()
            project_name = ""
            if item.project_id:
                proj = session.get(Project, item.project_id)
                if proj:
                    project_name = proj.name
            projects = list(session.scalars(select(Project).order_by(Project.name)).all())
            return item, project_name, projects

    result = _db_query(_query)
    if not result:
        return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))
    item, project_name, projects = result
    return templates.TemplateResponse(
        request,
        "partials/_knowledge_row.html",
        _knowledge_row_context(request, item=item, project_name=project_name, projects=projects),
    )


@router.put("/knowledge/{item_id}/visibility")
def knowledge_update_visibility(
    request: Request,
    item_id: str,
    project_id: str = Form(""),
    sensitivity: str = Form(...),
):
    """Update knowledge item project assignment and sensitivity."""
    def _query():
        with SessionLocal() as session:
            item = session.get(KnowledgeItem, uuid.UUID(item_id))
            if not item:
                return None
            before = {
                "project_id": str(item.project_id) if item.project_id else None,
                "sensitivity": item.sensitivity.value,
            }
            item.project_id = uuid.UUID(project_id) if project_id else None
            item.sensitivity = KnowledgeSensitivity(sensitivity)
            after = {
                "project_id": str(item.project_id) if item.project_id else None,
                "sensitivity": item.sensitivity.value,
            }
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="knowledge.visibility.update",
                resource_type="knowledge_item",
                resource_id=str(item.id),
                metadata={"before": before, "after": after},
            )
            session.commit()

            project_name = ""
            if item.project_id:
                proj = session.get(Project, item.project_id)
                if proj:
                    project_name = proj.name
            projects = list(session.scalars(select(Project).order_by(Project.name)).all())
            return item, project_name, projects

    result = _db_query(_query)
    if not result:
        return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))
    item, project_name, projects = result
    return templates.TemplateResponse(
        request,
        "partials/_knowledge_row.html",
        _knowledge_row_context(request, item=item, project_name=project_name, projects=projects),
    )


@router.delete("/knowledge/{item_id}")
def knowledge_delete(request: Request, item_id: str):
    """Delete a knowledge item."""
    def _query():
        with SessionLocal() as session:
            item = session.get(KnowledgeItem, uuid.UUID(item_id))
            if item:
                write_audit(
                    session,
                    actor_user_id=ADMIN_WEB_ACTOR,
                    action="knowledge.delete",
                    resource_type="knowledge_item",
                    resource_id=str(item.id),
                    metadata={
                        "title": item.title,
                        "source_type": item.source_type,
                        "project_id": str(item.project_id) if item.project_id else None,
                        "sensitivity": item.sensitivity.value,
                        "status": item.status.value,
                    },
                )
                session.delete(item)
                session.commit()

    _db_query(_query)
    return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))


@router.get("/dws/status")
def dws_status(request: Request):
    """Check DingTalk admin API connection status."""
    admin_ok = False
    admin_error = ""
    if _has_admin_credentials():
        admin = _admin_client()
        if admin:
            admin_ok, admin_error = admin.test_connection()
    return templates.TemplateResponse(
        request,
        "partials/_dws_status.html",
        _ctx(request, has_admin=_has_admin_credentials(), admin_ok=admin_ok, admin_error=admin_error),
    )


@router.get("/dws/list")
def dws_list(request: Request):
    """List recent approval instances accessible to the enterprise app.

    Note: DingTalk has no per-user pending-approval API in this client, so this
    scans recent instances across known process codes (an approximation).
    """
    admin = _admin_client()
    if not admin:
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error="需要配置企业管理 API（AppKey/AppSecret）", workflow_id=""),
        )
    try:
        details = admin.list_recent_instances(days=7, limit=50)
    except Exception as exc:  # noqa: BLE001 — surfaced to the user
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=str(exc), workflow_id=""),
        )
    approvals = [DingTalkAdminClient.to_workflow(d) for d in details]
    return templates.TemplateResponse(
        request,
        "partials/_dws_list.html",
        _ctx(request, approvals=approvals),
    )


@router.post("/dws/preview")
def dws_preview(request: Request, workflow_id: str = Form("")):
    """Preview an approval instance via the DingTalk admin API."""
    # Fetch projects for the import form dropdown
    def _query():
        with SessionLocal() as session:
            return list(session.scalars(select(Project).order_by(Project.name)).all())
    projects = _db_query(_query) or []

    admin = _admin_client()
    if not admin:
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error="需要配置企业管理 API（AppKey/AppSecret）", workflow_id=workflow_id),
        )

    # If it looks like a businessId (all digits), resolve it first
    instance_id = workflow_id
    if workflow_id.isdigit():
        try:
            resolved = admin.resolve_business_id_fast(workflow_id)
        except ValueError as e:
            return templates.TemplateResponse(
                request,
                "partials/_dws_error.html",
                _ctx(request, error=str(e), workflow_id=workflow_id),
            )
        if resolved:
            instance_id = resolved
        else:
            return templates.TemplateResponse(
                request,
                "partials/_dws_error.html",
                _ctx(request, error=f"企业管理 API 未找到工单号 {workflow_id} 对应的审批实例", workflow_id=workflow_id),
            )

    try:
        detail = admin.get_detail(instance_id)
    except Exception as exc:  # noqa: BLE001 — surfaced to the user
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=str(exc), workflow_id=workflow_id),
        )
    workflow = DingTalkAdminClient.to_workflow(detail)
    return templates.TemplateResponse(
        request,
        "partials/_dws_preview.html",
        _ctx(request, workflow=workflow, workflow_id=instance_id, projects=projects),
    )


@router.post("/dws/import")
def dws_import(
    request: Request,
    workflow_id: str = Form(""),
    title: str = Form(""),
    project_id: str = Form(""),
):
    """Import an approval instance as a knowledge item via the DingTalk admin API."""
    admin = _admin_client()
    if not admin:
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error="需要配置企业管理 API（AppKey/AppSecret）", workflow_id=workflow_id),
        )

    try:
        detail = admin.get_detail(workflow_id)
    except Exception as exc:  # noqa: BLE001 — surfaced to the user
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=str(exc), workflow_id=workflow_id),
        )
    workflow = DingTalkAdminClient.to_workflow(detail)

    body = _build_dingtalk_knowledge_body(workflow)

    # Save to database
    item_id = None

    def _query():
        with SessionLocal() as session:
            item = KnowledgeItem(
                title=f"[钉钉审批] {workflow.title or title or workflow_id}",
                body=body,
                source_type="dingtalk_approval",
                sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                status=KnowledgeStatus.PENDING_REVIEW,
                project_id=uuid.UUID(project_id) if project_id else None,
                metadata_json={
                    "workflow_id": detail.process_instance_id,
                    "business_id": detail.business_id,
                    "workflow_status": workflow.status,
                    "originator": workflow.originator,
                    "form_fields": list(workflow.form_data.keys()),
                },
                created_by="dingtalk_import",
            )
            session.add(item)
            _attach_embedding(item)
            session.flush()
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="dingtalk.import",
                resource_type="knowledge_item",
                resource_id=str(item.id),
                metadata={
                    "workflow_id": detail.process_instance_id,
                    "business_id": detail.business_id,
                },
            )
            session.commit()
            return item.id

    item_id = _db_query(_query)
    return templates.TemplateResponse(
        request,
        "partials/_dws_success.html",
        _ctx(request, item_id=item_id, title=workflow.title or title or workflow_id),
    )


# ---------------------------------------------------------------------------
# Batch DingTalk approval operations
# ---------------------------------------------------------------------------


@router.post("/dws/batch-preview")
def dws_batch_preview(request: Request, workflow_ids: str = Form("")):
    """Batch preview multiple approval instances."""
    ids = [line.strip() for line in workflow_ids.replace(",", "\n").splitlines() if line.strip()]
    if not ids:
        return templates.TemplateResponse(
            request, "partials/_dws_error.html",
            _ctx(request, error="请输入至少一个审批实例 ID 或工单号", workflow_id=""),
        )

    def _query():
        with SessionLocal() as session:
            return list(session.scalars(select(Project).order_by(Project.name)).all())
    projects = _db_query(_query) or []

    admin = _admin_client()
    if not admin:
        return templates.TemplateResponse(
            request, "partials/_dws_error.html",
            _ctx(request, error="批量查询需要配置企业管理 API（AppKey/AppSecret）", workflow_id=""),
        )

    # Resolve business IDs to instance IDs
    resolved_ids: list[str] = []
    resolve_errors: list[dict] = []
    for raw_id in ids:
        if raw_id.isdigit():
            try:
                resolved = admin.resolve_business_id_fast(raw_id)
                resolved_ids.append(resolved or raw_id)
            except ValueError as e:
                resolve_errors.append({"id": raw_id, "error": str(e)})
                resolved_ids.append(raw_id)
        else:
            resolved_ids.append(raw_id)

    # Batch fetch
    result = admin.batch_get_details(resolved_ids)
    workflows = [DingTalkAdminClient.to_workflow(d) for d in result.succeeded]

    # Merge resolve errors with fetch errors
    all_failed = resolve_errors + result.failed

    return templates.TemplateResponse(
        request, "partials/_dws_batch_preview.html",
        _ctx(request, workflows=workflows, failed=all_failed,
             instance_ids=resolved_ids, projects=projects),
    )


@router.post("/dws/batch-import")
def dws_batch_import(
    request: Request,
    workflow_ids: str = Form(""),
    project_id: str = Form(""),
):
    """Import multiple workflows as knowledge items."""
    ids = [line.strip() for line in workflow_ids.replace(",", "\n").splitlines() if line.strip()]
    if not ids:
        return templates.TemplateResponse(
            request, "partials/_dws_error.html",
            _ctx(request, error="没有可导入的流程 ID", workflow_id=""),
        )

    admin = _admin_client()
    if not admin:
        return templates.TemplateResponse(
            request, "partials/_dws_error.html",
            _ctx(request, error="批量导入需要企业管理 API", workflow_id=""),
        )

    result = admin.batch_get_details(ids)
    imported_count = 0
    errors: list[dict] = list(result.failed)

    try:
        with SessionLocal() as session:
            imported_ids: list[str] = []
            for detail in result.succeeded:
                workflow = DingTalkAdminClient.to_workflow(detail)
                body = _build_dingtalk_knowledge_body(workflow)
                item = KnowledgeItem(
                    title=f"[钉钉审批] {detail.title or detail.process_instance_id}",
                    body=body,
                    source_type="dingtalk_approval",
                    sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                    status=KnowledgeStatus.PENDING_REVIEW,
                    project_id=uuid.UUID(project_id) if project_id else None,
                    metadata_json={
                        "workflow_id": detail.process_instance_id,
                        "business_id": detail.business_id,
                        "workflow_status": detail.status,
                        "originator": detail.originator_user_id,
                        "form_fields": list(detail.form_data.keys()),
                    },
                    created_by="dingtalk_batch_import",
                )
                session.add(item)
                _attach_embedding(item)
                session.flush()
                imported_ids.append(str(item.id))
            imported_count = len(imported_ids)
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="dingtalk.batch_import",
                resource_type="knowledge_batch",
                resource_id=",".join(imported_ids),
                metadata={
                    "requested_count": len(ids),
                    "success_count": imported_count,
                    "failure_count": len(errors),
                },
            )
            session.commit()
    except Exception as exc:  # noqa: BLE001 - returned in the batch result
        imported_count = 0
        errors.append({"id": "database", "error": str(exc)})

    return templates.TemplateResponse(
        request, "partials/_dws_batch_success.html",
        _ctx(request, imported_count=imported_count, total=len(ids), errors=errors),
    )


# ---------------------------------------------------------------------------
# System Settings
# ---------------------------------------------------------------------------

_SETTINGS_KEYS = [
    "dingtalk_app_key",
    "dingtalk_app_secret",
    "openai_api_key",
    "openai_base_url",
    "openai_embedding_model",
    "enable_vector_search",
    "chat_api_key",
    "chat_base_url",
    "chat_model",
    "prod_db_host",
    "prod_db_port",
    "prod_db_name",
    "prod_db_user",
    "prod_db_password",
]


def _load_settings(session: Session) -> dict[str, str]:
    """Load settings from DB, keyed by setting key."""
    rows = session.query(AppSetting).filter(AppSetting.key.in_(_SETTINGS_KEYS)).all()
    return {r.key: r.value for r in rows}


def _save_setting(session: Session, key: str, value: str) -> None:
    """Upsert a single setting row."""
    row = session.get(AppSetting, key)
    if row:
        row.value = value
    else:
        session.add(AppSetting(key=key, value=value))


def _settings_snapshot(session: Session) -> dict[str, str]:
    return {
        key: row.value
        for key in _SETTINGS_KEYS
        if (row := session.get(AppSetting, key)) is not None
    }


def _record_config_test(*, service: str, ok: bool, error_type: str = "") -> None:
    with SessionLocal() as session:
        write_audit(
            session,
            actor_user_id=ADMIN_WEB_ACTOR,
            action="config.test",
            resource_type="integration_config",
            resource_id=service,
            metadata={"service": service, "ok": ok, "error_type": error_type},
        )
        session.commit()


@router.get("/settings")
def settings_page(request: Request, saved: str = ""):
    """System settings page — shows current config and status."""
    from inspilot_cloud_baby.embedding import get_embedding_service

    db_settings: dict[str, str] = _db_query(lambda: _load_db_settings()) or {}

    # Determine API key source
    if settings.openai_api_key:
        api_key_source = "env"
        api_key_hint = "当前使用环境变量配置"
    elif db_settings.get("openai_api_key"):
        api_key_source = "db"
        api_key_hint = "sk-****" + db_settings["openai_api_key"][-4:]
    else:
        api_key_source = "none"
        api_key_hint = "未配置"

    # Embedding service status
    svc = get_embedding_service()
    service_available = svc.available

    # Knowledge embedding stats
    stats = _db_query(_count_embedding_stats) or {"embedded": 0, "total": 0}

    # Resolve effective values (env > db > default)
    vector_enabled = settings.enable_vector_search
    current_base_url = db_settings.get("openai_base_url", "")
    current_model = db_settings.get("openai_embedding_model", settings.openai_embedding_model)

    # Chat model status
    from inspilot_cloud_baby.chat_service import get_chat_service
    chat_svc = get_chat_service()
    if settings.chat_api_key:
        chat_key_source, chat_key_hint = "env", "当前使用环境变量配置"
    elif db_settings.get("chat_api_key"):
        chat_key_source, chat_key_hint = "db", "****" + db_settings["chat_api_key"][-4:]
    else:
        chat_key_source, chat_key_hint = "none", "未配置"

    if settings.dingtalk_app_key:
        dingtalk_key_source, dingtalk_key_hint = "env", "当前使用环境变量配置"
    elif db_settings.get("dingtalk_app_key"):
        dingtalk_key_source = "db"
        dingtalk_key_hint = "****" + db_settings["dingtalk_app_key"][-4:]
    else:
        dingtalk_key_source, dingtalk_key_hint = "none", "未配置"

    return templates.TemplateResponse(
        request, "settings.html",
        _ctx(
            request,
            saved=bool(saved),
            service_available=service_available,
            vector_enabled=vector_enabled,
            api_key_source=api_key_source,
            api_key_hint=api_key_hint,
            current_base_url=current_base_url,
            current_model=current_model,
            embedded_count=stats["embedded"],
            total_count=stats["total"],
            chat_available=chat_svc.available,
            chat_key_source=chat_key_source,
            chat_key_hint=chat_key_hint,
            chat_base_url=db_settings.get("chat_base_url", ""),
            chat_model=db_settings.get("chat_model", ""),
            dingtalk_available=bool(
                (settings.dingtalk_app_key or db_settings.get("dingtalk_app_key"))
                and (settings.dingtalk_app_secret or db_settings.get("dingtalk_app_secret"))
            ),
            dingtalk_key_source=dingtalk_key_source,
            dingtalk_key_hint=dingtalk_key_hint,
            prod_db_host=db_settings.get("prod_db_host", ""),
            prod_db_port=db_settings.get("prod_db_port", "1433"),
            prod_db_name=db_settings.get("prod_db_name", ""),
            prod_db_user=db_settings.get("prod_db_user", ""),
            prod_db_available=bool(db_settings.get("prod_db_host")),
        ),
    )


@router.post("/settings")
def settings_save(
    request: Request,
    dingtalk_app_key: str = Form(""),
    dingtalk_app_secret: str = Form(""),
    openai_api_key: str = Form(""),
    openai_base_url: str = Form(""),
    openai_embedding_model: str = Form(""),
    enable_vector_search: str = Form(""),
    chat_api_key: str = Form(""),
    chat_base_url: str = Form(""),
    chat_model: str = Form(""),
    prod_db_host: str = Form(""),
    prod_db_port: str = Form(""),
    prod_db_name: str = Form(""),
    prod_db_user: str = Form(""),
    prod_db_password: str = Form(""),
):
    """Save settings to DB and reload embedding + chat services.

    Unlike most admin handlers, this does NOT swallow DB errors — if the save
    fails the user is shown the error so it isn't silently lost.
    """

    def _query():
        with SessionLocal() as session:
            before = _settings_snapshot(session)
            if dingtalk_app_key.strip():
                _save_setting(session, "dingtalk_app_key", dingtalk_app_key.strip())
            if dingtalk_app_secret.strip():
                _save_setting(session, "dingtalk_app_secret", dingtalk_app_secret.strip())
            if openai_api_key.strip():
                _save_setting(session, "openai_api_key", openai_api_key.strip())
            if openai_base_url.strip():
                _save_setting(session, "openai_base_url", openai_base_url.strip())
            elif openai_base_url == "" and not settings.openai_base_url:
                # Only clear if env var doesn't override
                row = session.get(AppSetting, "openai_base_url")
                if row:
                    row.value = ""
            if openai_embedding_model.strip():
                _save_setting(session, "openai_embedding_model", openai_embedding_model.strip())
            _save_setting(session, "enable_vector_search", "true" if enable_vector_search else "false")
            # Chat model settings
            if chat_api_key.strip():
                _save_setting(session, "chat_api_key", chat_api_key.strip())
            if chat_base_url.strip():
                _save_setting(session, "chat_base_url", chat_base_url.strip())
            if chat_model.strip():
                _save_setting(session, "chat_model", chat_model.strip())
            # Production DB settings
            if prod_db_host.strip():
                _save_setting(session, "prod_db_host", prod_db_host.strip())
            if prod_db_port.strip():
                _save_setting(session, "prod_db_port", prod_db_port.strip())
            if prod_db_name.strip():
                _save_setting(session, "prod_db_name", prod_db_name.strip())
            if prod_db_user.strip():
                _save_setting(session, "prod_db_user", prod_db_user.strip())
            if prod_db_password.strip():
                _save_setting(session, "prod_db_password", prod_db_password.strip())
            after = _settings_snapshot(session)
            write_audit(
                session,
                actor_user_id=ADMIN_WEB_ACTOR,
                action="config.update",
                resource_type="integration_config",
                resource_id="settings",
                metadata=config_change_metadata(before=before, after=after),
            )
            session.commit()

    try:
        _query()
    except Exception as exc:  # noqa: BLE001 — surfaced to the user
        logger.error("Failed to save settings: %s", exc, exc_info=True)
        return templates.TemplateResponse(
            request,
            "settings.html",
            _settings_ctx(request, error=f"保存失败：{exc}"),
        )

    # Hot-reload: reset singletons so next call picks up new config
    import inspilot_cloud_baby.chat_service as chat_mod
    import inspilot_cloud_baby.embedding as emb_mod
    import inspilot_cloud_baby.prod_db_service as db_mod
    chat_mod._service = None
    emb_mod._service = None
    db_mod._service = None

    # Redirect to GET to show the saved state (PRG pattern)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/settings?saved=1", status_code=303)


def _settings_ctx(request: Request, error: str = "") -> dict:
    """Build the settings-page context (shared by GET and the save-error path)."""
    from inspilot_cloud_baby.embedding import get_embedding_service

    db_settings: dict[str, str] = _db_query(lambda: _load_db_settings()) or {}

    if settings.openai_api_key:
        api_key_source, api_key_hint = "env", "当前使用环境变量配置"
    elif db_settings.get("openai_api_key"):
        api_key_source, api_key_hint = "db", "sk-****" + db_settings["openai_api_key"][-4:]
    else:
        api_key_source, api_key_hint = "none", "未配置"

    svc = get_embedding_service()
    stats = _db_query(_count_embedding_stats) or {"embedded": 0, "total": 0}

    # Chat model config for display
    from inspilot_cloud_baby.chat_service import get_chat_service
    chat_svc = get_chat_service()
    if settings.chat_api_key:
        chat_key_source, chat_key_hint = "env", "当前使用环境变量配置"
    elif db_settings.get("chat_api_key"):
        chat_key_source, chat_key_hint = "db", "****" + db_settings["chat_api_key"][-4:]
    else:
        chat_key_source, chat_key_hint = "none", "未配置"

    if settings.dingtalk_app_key:
        dingtalk_key_source, dingtalk_key_hint = "env", "当前使用环境变量配置"
    elif db_settings.get("dingtalk_app_key"):
        dingtalk_key_source, dingtalk_key_hint = "db", "****" + db_settings["dingtalk_app_key"][-4:]
    else:
        dingtalk_key_source, dingtalk_key_hint = "none", "未配置"

    return _ctx(
        request,
        saved=False,
        error=error,
        service_available=svc.available,
        vector_enabled=settings.enable_vector_search,
        api_key_source=api_key_source,
        api_key_hint=api_key_hint,
        current_base_url=db_settings.get("openai_base_url", ""),
        current_model=db_settings.get("openai_embedding_model", settings.openai_embedding_model),
        embedded_count=stats["embedded"],
        total_count=stats["total"],
        chat_available=chat_svc.available,
        chat_key_source=chat_key_source,
        chat_key_hint=chat_key_hint,
        chat_base_url=db_settings.get("chat_base_url", ""),
        chat_model=db_settings.get("chat_model", ""),
        dingtalk_available=bool(
            (settings.dingtalk_app_key or db_settings.get("dingtalk_app_key"))
            and (settings.dingtalk_app_secret or db_settings.get("dingtalk_app_secret"))
        ),
        dingtalk_key_source=dingtalk_key_source,
        dingtalk_key_hint=dingtalk_key_hint,
        prod_db_host=db_settings.get("prod_db_host", ""),
        prod_db_port=db_settings.get("prod_db_port", "1433"),
        prod_db_name=db_settings.get("prod_db_name", ""),
        prod_db_user=db_settings.get("prod_db_user", ""),
        prod_db_available=bool(db_settings.get("prod_db_host")),
    )


@router.post("/settings/test")
def settings_test(request: Request):
    """Test the embedding API with the CURRENT FORM values (pre-save).

    Accepts JSON {api_key, base_url, model}. Empty fields fall back to the
    currently saved config so the user can test without re-entering the key.
    """
    from inspilot_cloud_baby.embedding import EmbeddingService, get_effective_config

    import json

    try:
        body = json.loads(request.headers.get("x-test-body", "{}"))
    except Exception:
        body = {}
    saved = get_effective_config()
    api_key = body.get("api_key", "").strip() or saved["api_key"]
    base_url = body.get("base_url", "").strip() or saved["base_url"]
    model = body.get("model", "").strip() or saved["model"]

    if not api_key:
        _record_config_test(
            service="embedding", ok=False, error_type="missing_configuration"
        )
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(request, test_ok=False, test_message="未配置 API Key，无法测试。请先填写 API Key。"),
        )

    svc = EmbeddingService(api_key=api_key, base_url=base_url, model=model, enable_vector_search=True)
    vector = svc.embed_text("测试连接")

    if vector is not None:
        _record_config_test(service="embedding", ok=True)
        dim = len(vector)
        endpoint = base_url or "https://api.openai.com/v1 (官方)"
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(
                request,
                test_ok=True,
                test_message=f"✅ 连接成功。模型 {model} 返回 {dim} 维向量。",
                test_endpoint=endpoint,
            ),
        )

    endpoint = base_url or "https://api.openai.com/v1 (官方)"
    _record_config_test(service="embedding", ok=False, error_type="connection_failed")
    return templates.TemplateResponse(
        request,
        "partials/_settings_test.html",
        _ctx(
            request,
            test_ok=False,
            test_message="❌ 连接失败。请检查 API Key、Base URL、模型名是否正确。",
            test_endpoint=endpoint,
            test_model=model,
        ),
    )


@router.post("/settings/chat-test")
def settings_chat_test(request: Request):
    """Test the chat model with the CURRENT FORM values (pre-save)."""
    from inspilot_cloud_baby.chat_service import ChatService, get_chat_config

    import json

    try:
        body = json.loads(request.headers.get("x-test-body", "{}"))
    except Exception:
        body = {}
    saved = get_chat_config()
    api_key = body.get("api_key", "").strip() or saved["api_key"]
    base_url = body.get("base_url", "").strip() or saved["base_url"]
    model = body.get("model", "").strip() or saved["model"]

    if not api_key:
        _record_config_test(service="chat", ok=False, error_type="missing_configuration")
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(request, test_ok=False, test_message="未配置对话模型 API Key。请先填写。"),
        )
    if not model:
        _record_config_test(service="chat", ok=False, error_type="missing_configuration")
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(request, test_ok=False, test_message="未配置对话模型名称。请先填写。"),
        )

    svc = ChatService(api_key=api_key, base_url=base_url, model=model)
    reply = svc.chat([{"role": "user", "content": "你好，请回复「连接正常」。"}])

    endpoint = base_url or "https://api.openai.com/v1 (官方)"
    if reply:
        _record_config_test(service="chat", ok=True)
        snippet = reply.strip()[:60]
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(
                request, test_ok=True,
                test_message=f"✅ 连接成功。模型 {model} 回复：{snippet}",
                test_endpoint=endpoint,
            ),
        )
    _record_config_test(service="chat", ok=False, error_type="connection_failed")
    return templates.TemplateResponse(
        request,
        "partials/_settings_test.html",
        _ctx(
            request, test_ok=False,
            test_message="❌ 连接失败。请检查 API Key、Base URL、模型名是否正确。",
            test_endpoint=endpoint,
            test_model=model,
        ),
    )


@router.post("/settings/dingtalk-test")
def settings_dingtalk_test(request: Request):
    """Test DingTalk AppKey/AppSecret with CURRENT FORM values (pre-save)."""
    import json

    try:
        body = json.loads(request.headers.get("x-test-body", "{}"))
    except Exception:
        body = {}
    saved = _get_dingtalk_config()
    app_key = body.get("app_key", "").strip() or saved["app_key"]
    app_secret = body.get("app_secret", "").strip() or saved["app_secret"]
    process_instance_id = body.get("process_instance_id", "").strip()

    if not app_key or not app_secret:
        _record_config_test(
            service="dingtalk", ok=False, error_type="missing_configuration"
        )
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(request, test_ok=False, test_message="未配置钉钉 AppKey 或 AppSecret。请先填写。"),
        )

    capabilities = DingTalkAdminClient(app_key, app_secret).test_capabilities(
        process_instance_id
    )
    ok = capabilities.token.status == "ok" and capabilities.approval_detail.status in {
        "ok",
        "not_tested",
    }
    error_type = ""
    if capabilities.token.status != "ok":
        error_type = "connection_failed"
    elif capabilities.approval_detail.status == "failed":
        error_type = "approval_detail_failed"
    elif capabilities.comments.status in {"failed", "unavailable"}:
        error_type = "comments_unavailable"
    _record_config_test(
        service="dingtalk",
        ok=ok,
        error_type=error_type,
    )
    return templates.TemplateResponse(
        request,
        "partials/_settings_test.html",
        _ctx(
            request,
            test_ok=ok,
            test_message="钉钉开放平台能力测试完成。",
            capability_results=[
                ("基础连接", capabilities.token.status, capabilities.token.message),
                (
                    "审批详情",
                    capabilities.approval_detail.status,
                    capabilities.approval_detail.message,
                ),
                ("独立评论", capabilities.comments.status, capabilities.comments.message),
            ],
        ),
    )


@router.post("/settings/db-test")
def settings_db_test(request: Request):
    """Test the production DB connection with CURRENT FORM values (pre-save)."""
    from inspilot_cloud_baby.prod_db_service import ProdDBService

    import json

    try:
        body = json.loads(request.headers.get("x-test-body", "{}"))
    except Exception:
        body = {}
    host = body.get("host", "").strip()
    port = body.get("port", "").strip() or "1433"
    database = body.get("database", "").strip()
    user = body.get("user", "").strip()
    password = body.get("password", "").strip()

    if not host:
        _record_config_test(
            service="production_db", ok=False, error_type="missing_configuration"
        )
        return templates.TemplateResponse(
            request,
            "partials/_settings_test.html",
            _ctx(request, test_ok=False, test_message="未配置数据库地址。"),
        )

    svc = ProdDBService(host=host, port=int(port), database=database, user=user, password=password)
    ok, msg = svc.test_connection()
    _record_config_test(
        service="production_db",
        ok=ok,
        error_type="" if ok else "connection_failed",
    )
    return templates.TemplateResponse(
        request,
        "partials/_settings_test.html",
        _ctx(request, test_ok=ok, test_message=msg),
    )


def _load_db_settings() -> dict[str, str]:
    with SessionLocal() as session:
        return _load_settings(session)


def _count_embedding_stats() -> dict[str, int]:
    with SessionLocal() as session:
        total = session.query(KnowledgeItem).filter(
            KnowledgeItem.status == KnowledgeStatus.ACTIVE
        ).count()
        embedded = session.query(KnowledgeItem).filter(
            KnowledgeItem.status == KnowledgeStatus.ACTIVE,
            KnowledgeItem.embedding.isnot(None),
        ).count()
        return {"embedded": embedded, "total": total}
