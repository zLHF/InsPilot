from __future__ import annotations

import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.dingtalk_admin import DingTalkAdminClient
from inspilot_cloud_baby.dws_adapter import DwsAdapter, DwsWorkflow
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


def _has_admin_credentials() -> bool:
    """Check if enterprise admin credentials are configured."""
    return bool(settings.dws_client_id and settings.dws_client_secret)


def _admin_client() -> DingTalkAdminClient | None:
    """Return a DingTalkAdminClient if credentials are configured."""
    if _has_admin_credentials():
        return DingTalkAdminClient(settings.dws_client_id, settings.dws_client_secret)
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
            items = list(session.scalars(stmt.limit(100)).all())
            projects = list(session.scalars(select(Project).order_by(Project.name)).all())
            return items, projects
    result = _db_query(_query) or ([], [])
    items, projects = result
    # Build project name lookup for row template
    project_names = {str(p.id): p.name for p in projects}
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
            status_labels=STATUS_LABELS,
            status_colors=STATUS_COLORS,
            sensitivity_labels=SENSITIVITY_LABELS,
            material_type_labels=MATERIAL_TYPE_LABELS,
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
    return templates.TemplateResponse(
        request, "dws.html", _ctx(request, settings_dws_binary=settings.dws_binary)
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
            item.status = KnowledgeStatus(status)
            session.commit()
            project_name = ""
            if item.project_id:
                proj = session.get(Project, item.project_id)
                if proj:
                    project_name = proj.name
            return item, project_name

    result = _db_query(_query)
    if not result:
        return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))
    item, project_name = result
    return templates.TemplateResponse(
        request,
        "partials/_knowledge_row.html",
        _ctx(
            request,
            item=item,
            project_name=project_name,
            status_labels=STATUS_LABELS,
            status_colors=STATUS_COLORS,
            sensitivity_labels=SENSITIVITY_LABELS,
            material_type_labels=MATERIAL_TYPE_LABELS,
        ),
    )


@router.delete("/knowledge/{item_id}")
def knowledge_delete(request: Request, item_id: str):
    """Delete a knowledge item."""
    def _query():
        with SessionLocal() as session:
            item = session.get(KnowledgeItem, uuid.UUID(item_id))
            if item:
                session.delete(item)
                session.commit()

    _db_query(_query)
    return templates.TemplateResponse(request, "partials/_empty.html", _ctx(request))


@router.get("/dws/status")
def dws_status(request: Request):
    """Check DWS CLI connection and auth status."""
    adapter = DwsAdapter(binary=settings.dws_binary, client_id=settings.dws_client_id, client_secret=settings.dws_client_secret)
    conn = adapter.test_connection()
    admin_ok = False
    admin_error = ""
    if _has_admin_credentials():
        try:
            admin = _admin_client()
            admin._ensure_token()
            admin_ok = True
        except Exception as exc:
            admin_error = str(exc)
    return templates.TemplateResponse(
        request,
        "partials/_dws_status.html",
        _ctx(request, conn=conn, has_admin=_has_admin_credentials(), admin_ok=admin_ok, admin_error=admin_error),
    )


@router.get("/dws/list")
def dws_list(request: Request):
    """List all accessible approval instances for the current user."""
    adapter = DwsAdapter(binary=settings.dws_binary, client_id=settings.dws_client_id, client_secret=settings.dws_client_secret)
    conn = adapter.test_connection()
    if not conn.success:
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=conn.error, workflow_id=""),
        )
    approvals = adapter.list_approvals()
    return templates.TemplateResponse(
        request,
        "partials/_dws_list.html",
        _ctx(request, approvals=approvals),
    )


@router.post("/dws/preview")
def dws_preview(request: Request, workflow_id: str = Form("")):
    """Preview DWS workflow data — uses enterprise admin API if configured."""
    # Fetch projects for the import form dropdown
    def _query():
        with SessionLocal() as session:
            return list(session.scalars(select(Project).order_by(Project.name)).all())
    projects = _db_query(_query) or []

    # Try enterprise admin API first (can access ALL instances)
    admin = _admin_client()
    if admin:
        try:
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
            detail = admin.get_detail(instance_id)
            # Convert AdminWorkflowDetail to DwsWorkflow for template compatibility
            workflow = DwsWorkflow(
                title=detail.title,
                status=detail.status,
                originator=detail.originator_user_id,
                form_data=detail.form_data,
                operation_records=detail.operation_records,
                attachments=[
                    {"field_name": a.field_name, "file_name": a.file_name,
                     "file_id": a.file_id, "download_url": a.download_url,
                     "file_size": a.file_size, "component_type": a.component_type}
                    for a in detail.attachments
                ],
                comments=[
                    {"user_id": c.user_id, "content": c.content, "timestamp": c.timestamp}
                    for c in detail.comments
                ],
                raw_json=detail.raw,
            )
            return templates.TemplateResponse(
                request,
                "partials/_dws_preview.html",
                _ctx(request, workflow=workflow, workflow_id=instance_id, projects=projects),
            )
        except Exception as exc:
            logger.warning("Admin API failed, falling back to DWS CLI: %s", exc)

    # Fallback to DWS CLI (personal OAuth mode)
    adapter = DwsAdapter(binary=settings.dws_binary, client_id=settings.dws_client_id, client_secret=settings.dws_client_secret)
    conn = adapter.test_connection()
    if not conn.success:
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=conn.error, workflow_id=workflow_id),
        )
    result = adapter.fetch_workflow_safe(workflow_id=workflow_id)
    if isinstance(result, str):
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=result, workflow_id=workflow_id),
        )
    return templates.TemplateResponse(
        request,
        "partials/_dws_preview.html",
        _ctx(request, workflow=result, workflow_id=workflow_id, projects=projects),
    )


@router.post("/dws/import")
def dws_import(
    request: Request,
    workflow_id: str = Form(""),
    title: str = Form(""),
    project_id: str = Form(""),
):
    """Import a DWS workflow as a knowledge item."""
    adapter = DwsAdapter(binary=settings.dws_binary, client_id=settings.dws_client_id, client_secret=settings.dws_client_secret)
    result = adapter.fetch_workflow_safe(workflow_id=workflow_id)

    if isinstance(result, str):
        return templates.TemplateResponse(
            request,
            "partials/_dws_error.html",
            _ctx(request, error=result, workflow_id=workflow_id),
        )

    workflow: DwsWorkflow = result

    # Build the knowledge body from workflow data
    body_parts = [f"# {workflow.title or title or workflow_id}"]
    if workflow.status:
        body_parts.append(f"\n**审批状态**: {workflow.status}")
    if workflow.originator:
        body_parts.append(f"**发起人**: {workflow.originator}")

    if workflow.form_data:
        body_parts.append("\n## 表单字段")
        for name, value in workflow.form_data.items():
            body_parts.append(f"- **{name}**: {value}")

    if workflow.operation_records:
        body_parts.append("\n## 操作记录")
        for rec in workflow.operation_records:
            body_parts.append(
                f"- {rec.get('creatorUserId', rec.get('userId', '未知'))}: "
                f"{rec.get('remark', rec.get('result', ''))}"
            )

    if workflow.attachments:
        body_parts.append("\n## 附件")
        for att in workflow.attachments:
            body_parts.append(f"- {att.get('name', '附件')}")

    body = "\n".join(body_parts)

    # Save to database
    item_id = None

    def _query():
        with SessionLocal() as session:
            item = KnowledgeItem(
                title=f"[DWS] {workflow.title or title or workflow_id}",
                body=body,
                source_type="dws_workflow",
                sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                status=KnowledgeStatus.PENDING_REVIEW,
                project_id=uuid.UUID(project_id) if project_id else None,
                metadata_json={
                    "workflow_id": workflow_id,
                    "workflow_status": workflow.status,
                    "originator": workflow.originator,
                    "form_fields": list(workflow.form_data.keys()),
                },
                created_by="dws_import",
            )
            session.add(item)
            _attach_embedding(item)
            session.commit()
            return item.id

    item_id = _db_query(_query)
    return templates.TemplateResponse(
        request,
        "partials/_dws_success.html",
        _ctx(request, item_id=item_id, title=workflow.title or title or workflow_id),
    )


# ---------------------------------------------------------------------------
# Batch DWS operations
# ---------------------------------------------------------------------------

def _admin_detail_to_workflow(detail) -> DwsWorkflow:
    """Convert AdminWorkflowDetail to DwsWorkflow for template use."""
    return DwsWorkflow(
        title=detail.title,
        status=detail.status,
        originator=detail.originator_user_id,
        form_data=detail.form_data,
        operation_records=detail.operation_records,
        attachments=[
            {"field_name": a.field_name, "file_name": a.file_name,
             "file_id": a.file_id, "download_url": a.download_url,
             "file_size": a.file_size, "component_type": a.component_type}
            for a in detail.attachments
        ],
        comments=[
            {"user_id": c.user_id, "content": c.content, "timestamp": c.timestamp}
            for c in detail.comments
        ],
        raw_json=detail.raw,
    )


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
    workflows = [_admin_detail_to_workflow(d) for d in result.succeeded]

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
    errors: list[dict] = []

    for detail in result.succeeded:
        try:
            # Build markdown body
            body_parts = [f"# {detail.title or detail.process_instance_id}"]
            if detail.status:
                body_parts.append(f"\n**审批状态**: {detail.status}")
            if detail.originator_user_id:
                body_parts.append(f"**发起人**: {detail.originator_user_id}")

            if detail.form_data:
                body_parts.append("\n## 表单字段")
                for name, value in detail.form_data.items():
                    body_parts.append(f"- **{name}**: {value}")

            if detail.operation_records:
                body_parts.append("\n## 操作记录")
                for rec in detail.operation_records:
                    body_parts.append(
                        f"- {rec.get('creatorUserId', rec.get('userId', '未知'))}: "
                        f"{rec.get('remark', rec.get('result', ''))}"
                    )

            if detail.comments:
                body_parts.append("\n## 评论")
                for c in detail.comments:
                    body_parts.append(f"- **{c.user_id}**: {c.content}")

            if detail.attachments:
                body_parts.append("\n## 附件")
                for a in detail.attachments:
                    body_parts.append(f"- {a.file_name or a.field_name}")

            body = "\n".join(body_parts)

            def _query(pid=detail.process_instance_id, b=body, t=detail.title, st=detail.status):
                with SessionLocal() as session:
                    item = KnowledgeItem(
                        title=f"[DWS] {t or pid}",
                        body=b,
                        source_type="dws_workflow",
                        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                        status=KnowledgeStatus.PENDING_REVIEW,
                        project_id=uuid.UUID(project_id) if project_id else None,
                        metadata_json={
                            "workflow_id": pid,
                            "workflow_status": st,
                            "originator": detail.originator_user_id,
                            "form_fields": list(detail.form_data.keys()),
                        },
                        created_by="dws_batch_import",
                    )
                    session.add(item)
                    _attach_embedding(item)
                    session.commit()
                    return item.id

            _db_query(_query)
            imported_count += 1
        except Exception as exc:
            errors.append({"id": detail.process_instance_id, "error": str(exc)})

    errors.extend(result.failed)
    return templates.TemplateResponse(
        request, "partials/_dws_batch_success.html",
        _ctx(request, imported_count=imported_count, total=len(ids), errors=errors),
    )


# ---------------------------------------------------------------------------
# System Settings
# ---------------------------------------------------------------------------

_SETTINGS_KEYS = [
    "openai_api_key",
    "openai_base_url",
    "openai_embedding_model",
    "enable_vector_search",
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
        ),
    )


@router.post("/settings")
def settings_save(
    request: Request,
    openai_api_key: str = Form(""),
    openai_base_url: str = Form(""),
    openai_embedding_model: str = Form(""),
    enable_vector_search: str = Form(""),
):
    """Save settings to DB and reload embedding service."""

    def _query():
        with SessionLocal() as session:
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
            session.commit()

    _db_query(_query)

    # Hot-reload: reset the singleton so next call picks up new config
    import inspilot_cloud_baby.embedding as emb_mod
    emb_mod._service = None

    # Redirect to GET to show the saved state (PRG pattern)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/settings?saved=1", status_code=303)


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
