# Beta 准入硬化实施计划

> **给执行 Agent 的要求：** 必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，逐任务执行本计划，并使用 checkbox（`- [ ]`）跟踪进度。

**目标：** 补齐 InsPilot 进入 Beta 前所需的审计、检索可解释性和钉钉评论权限门槛。

**架构：** 保持 FastAPI 模块化单体和现有 PostgreSQL + pgvector 检索栈。新增事务内审计服务；检索始终执行双通道召回并返回内部证据，同时保持关键词优先排序；显式建模钉钉评论获取状态，使导入可降级到审批操作记录，但不隐藏权限失败。

**技术栈：** Python 3.10+、FastAPI、SQLAlchemy 2、PostgreSQL 16、pgvector、Pydantic v2、Jinja2/HTMX、pytest、Ruff。

**设计文档：** `docs/superpowers/specs/2026-06-18-beta-readiness-hardening-design.md`

---

## 文件规划

- 新建 `src/inspilot_cloud_baby/audit.py`：审计动作常量、秘密安全的元数据助手及事务内审计写入。
- 新建 `src/inspilot_cloud_baby/retrieval_evidence.py`：检索候选/证据类型及确定性的关键词优先融合。
- 新建 `src/inspilot_cloud_baby/scripts/verify_beta_readiness.py`：只读 Beta 门槛验证。
- 修改 `src/inspilot_cloud_baby/routers/admin.py`：接入审计写入、暴露钉钉能力状态并保存钉钉来源信息。
- 修改 `src/inspilot_cloud_baby/retrieval.py`：移除关键词短路、捕获两个召回通道并返回可解释结果。
- 修改 `src/inspilot_cloud_baby/routers/chat.py`：向后台搜索台暴露安全的检索证据。
- 修改 `src/inspilot_cloud_baby/dingtalk_admin.py`：显式评论状态、规范化、去重和能力检查。
- 修改 `src/inspilot_cloud_baby/templates/search.html`：展示召回渠道、命中字段和排名。
- 修改 `src/inspilot_cloud_baby/templates/settings.html`：接收但不保存测试审批实例 ID。
- 修改 `src/inspilot_cloud_baby/templates/partials/_settings_test.html`：展示三项独立钉钉能力状态。
- 在 `tests/` 增加聚焦测试；审计事务与秘密落库断言使用 PostgreSQL。

## 任务 1：事务内审计服务

**文件：**
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/audit.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_audit.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_audit_integration.py`

- [ ] **步骤 1：为审计构造和秘密安全的配置元数据编写失败测试**

```python
from inspilot_cloud_baby.audit import ADMIN_WEB_ACTOR, config_change_metadata, write_audit
from inspilot_cloud_baby.models import AuditLog


def test_config_change_metadata_never_contains_secret_values() -> None:
    metadata = config_change_metadata(
        {
            "dingtalk_app_secret": "ding-secret",
            "openai_api_key": "sk-secret",
            "prod_db_password": "db-secret",
            "chat_model": "deepseek-chat",
        }
    )
    serialized = repr(metadata)
    assert metadata["changed_keys"] == [
        "chat_model", "dingtalk_app_secret", "openai_api_key", "prod_db_password"
    ]
    assert metadata["secret_keys_changed"] == [
        "dingtalk_app_secret", "openai_api_key", "prod_db_password"
    ]
    assert "ding-secret" not in serialized
    assert "sk-secret" not in serialized
    assert "db-secret" not in serialized


def test_write_audit_adds_without_committing(mocker) -> None:
    session = mocker.Mock()
    row = write_audit(
        session,
        actor_user_id=ADMIN_WEB_ACTOR,
        action="knowledge.create",
        resource_type="knowledge_item",
        resource_id="k1",
        metadata={"source_type": "manual"},
    )
    assert isinstance(row, AuditLog)
    session.add.assert_called_once_with(row)
    session.commit.assert_not_called()
```

- [ ] **步骤 2：运行单元测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_audit.py -v`

预期：失败，因为 `inspilot_cloud_baby.audit` 尚不存在。

- [ ] **步骤 3：实现审计服务**

```python
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Session

from inspilot_cloud_baby.models import AuditLog

ADMIN_WEB_ACTOR = "admin:web"
SECRET_SETTING_KEYS = frozenset(
    {"dingtalk_app_secret", "openai_api_key", "chat_api_key", "prod_db_password"}
)


def config_change_metadata(values: Mapping[str, str]) -> dict[str, list[str]]:
    changed = sorted(key for key, value in values.items() if value != "")
    return {
        "changed_keys": changed,
        "secret_keys_changed": sorted(key for key in changed if key in SECRET_SETTING_KEYS),
    }


def write_audit(
    session: Session,
    *,
    actor_user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    reason: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> AuditLog:
    row = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        reason=reason,
        metadata_json=dict(metadata or {}),
    )
    session.add(row)
    return row
```

- [ ] **步骤 4：增加真实 PostgreSQL 回滚测试**

```python
import uuid

import pytest
from sqlalchemy import event, select

from inspilot_cloud_baby.audit import ADMIN_WEB_ACTOR, write_audit
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.models import AuditLog, Project, ProjectVisibility


def test_audit_flush_failure_rolls_back_business_change() -> None:
    project_id = uuid.uuid4()
    session = SessionLocal()

    @event.listens_for(session, "before_flush")
    def fail_audit_flush(current_session, _flush_context, _instances) -> None:
        if any(isinstance(obj, AuditLog) for obj in current_session.new):
            raise RuntimeError("audit write failed")

    try:
        project = Project(
            id=project_id,
            name=f"audit-rollback-{project_id}",
            visibility=ProjectVisibility.RESTRICTED,
            summary="",
        )
        session.add(project)
        write_audit(
            session,
            actor_user_id=ADMIN_WEB_ACTOR,
            action="project.create",
            resource_type="project",
            resource_id=str(project_id),
        )
        with pytest.raises(RuntimeError, match="audit write failed"):
            session.commit()
        session.rollback()
    finally:
        event.remove(session, "before_flush", fail_audit_flush)
        session.close()

    with SessionLocal() as verify:
        assert verify.scalar(select(Project).where(Project.id == project_id)) is None
```

- [ ] **步骤 5：运行审计测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_audit.py tests/test_audit_integration.py -v`

预期：通过。如果 PostgreSQL 不可用，修复本地 Docker 依赖，不得用 mock 替代该测试。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/audit.py apps/inspilot_cloud_baby/tests/test_audit.py apps/inspilot_cloud_baby/tests/test_audit_integration.py
git commit -m "feat: add transaction-scoped audit service"
```

## 任务 2：审计知识、项目和钉钉导入操作

**文件：**
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **步骤 1：编写失败的路由测试，捕获同一会话中新增的 `AuditLog` 对象**

增加可复用的伪会话，同时记录业务行和审计行，并断言以下动作：

```python
assert_audit(response, added, "knowledge.create", "knowledge_item")
assert_audit(response, added, "project.create", "project")
assert_audit(response, added, "knowledge.status.update", "knowledge_item")
assert_audit(response, added, "knowledge.visibility.update", "knowledge_item")
assert_audit(response, added, "knowledge.delete", "knowledge_item")
assert_audit(response, added, "dingtalk.import", "knowledge_item")
assert_audit(response, added, "dingtalk.batch_import", "knowledge_batch")
```

测试助手必须验证 `actor_user_id == "admin:web"`；可见性/状态测试必须断言 `metadata_json` 包含 `before`、`after` 摘要且不含正文。

- [ ] **步骤 2：运行聚焦的后台测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py -k audit -v`

预期：失败，因为路由尚未新增审计行。

- [ ] **步骤 3：在每个现有 `session.commit()` 前增加审计写入**

所有覆盖操作均使用以下模式：

```python
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
```

更新前先保存枚举/ID 旧值。删除时，在 `session.delete(item)` 前写审计，仅包含标题、来源类型、项目 ID、敏感级别和状态。批量导入对所有成功构建的条目使用一个事务，写一条包含 `requested_count`、`success_count`、`failure_count` 的汇总审计并只提交一次；`_db_query` 返回 `None` 时不得增加成功数。

- [ ] **步骤 4：保存 Beta 验证器所需的钉钉来源信息**

单条和批量导入都必须包含：

```python
metadata_json={
    "workflow_id": workflow.process_instance_id,
    "business_id": detail.business_id,
    "workflow_status": workflow.status,
    "originator": workflow.originator,
    "form_fields": list(workflow.form_data.keys()),
}
```

- [ ] **步骤 5：运行路由和集成测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit_integration.py -v`

预期：通过。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: audit admin knowledge and import operations"
```

## 任务 3：审计配置更新和保存前测试

**文件：**
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_admin_pages.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_audit_integration.py`

- [ ] **步骤 1：为独立动作码和秘密脱敏编写失败测试**

```python
def test_settings_save_writes_redacted_config_update_audit(audit_client, added):
    # POST secrets and a model name.
    audit = next(row for row in added if isinstance(row, AuditLog))
    assert audit.action == "config.update"
    assert audit.actor_user_id == "admin:web"
    serialized = repr(audit.metadata_json)
    assert "dingtalk_app_secret" in serialized
    assert "ding-secret" not in serialized


def test_dingtalk_pre_save_test_writes_config_test_audit(audit_client, added):
    # The test action uses a separate SessionLocal transaction.
    assert audit.action == "config.test"
    assert audit.metadata_json == {"service": "dingtalk", "ok": True, "error_type": ""}
```

扩展 PostgreSQL 集成测试：从 `app_settings` 读取已配置秘密，扫描序列化审计元数据，并断言任何非空秘密值都未出现。

- [ ] **步骤 2：运行聚焦测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit_integration.py -k 'config or secret' -v`

预期：失败，因为配置审计尚不存在。

- [ ] **步骤 3：实现配置更新和测试审计助手**

```python
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
```

Embedding、对话、钉钉和生产库测试端点的每条返回路径都调用该助手。在 `settings_save` 中构造提交值映射，调用 `config_change_metadata`，在现有保存事务中写入 `config.update`，然后只提交一次。

- [ ] **步骤 4：运行后台和审计测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit.py tests/test_audit_integration.py -v`

预期：通过。

- [ ] **步骤 5：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py apps/inspilot_cloud_baby/tests/test_audit_integration.py
git commit -m "feat: audit configuration changes and tests"
```

## 任务 4：检索证据与确定性双通道融合

**文件：**
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval_evidence.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_retrieval.py`

- [ ] **步骤 1：编写失败的证据与排序测试**

```python
def test_keyword_results_do_not_short_circuit_vector_recall(
    company_user, mock_db, vector_recall
):
    explained = retrieve_documents_explained(
        query="西宁市", user=company_user, documents=[], limit=2, db=mock_db
    )
    vector_recall.assert_called_once()
    assert explained[0].evidence.channels == ("keyword", "vector")


def test_keyword_candidates_rank_before_vector_only_candidates() -> None:
    fused = fuse_candidates(
        keyword=[candidate("exact", keyword_score=1, keyword_rank=1, fields=("body",))],
        vector=[candidate("semantic", vector_distance=0.01, vector_rank=1)],
        limit=8,
    )
    assert [item.document.id for item in fused] == ["exact", "semantic"]


def test_unauthorized_document_never_appears_in_evidence(company_user, mock_db):
    results = retrieve_documents_explained(
        query="受限内容", user=company_user, documents=[], limit=8, db=mock_db
    )
    serialized = repr(results)
    assert "restricted-title" not in serialized
    assert "restricted-body" not in serialized
```

同时覆盖标题/元数据/正文的字段优先级、双通道平分处理、仅向量距离排序、向量不可用状态、去重和稳定的文档 ID 平分处理。

- [ ] **步骤 2：运行检索测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_retrieval.py -v`

预期：失败，因为可解释检索和融合类型尚不存在。

- [ ] **步骤 3：实现聚焦的证据类型和融合逻辑**

```python
@dataclass(frozen=True)
class RetrievalEvidence:
    channels: tuple[str, ...]
    matched_fields: tuple[str, ...] = ()
    keyword_score: int = 0
    keyword_rank: int | None = None
    vector_distance: float | None = None
    vector_rank: int | None = None
    final_rank: int = 0
    vector_status: str = "available"


@dataclass(frozen=True)
class ExplainedDocument:
    document: KnowledgeDocument
    evidence: RetrievalEvidence
```

融合时使用内部可变候选对象，其排序键必须严格为：

```python
(
    0 if candidate.keyword_rank is not None else 1,
    -candidate.keyword_score,
    -int("title" in candidate.matched_fields),
    -int("metadata" in candidate.matched_fields),
    -int("body" in candidate.matched_fields),
    -int(candidate.keyword_rank is not None and candidate.vector_rank is not None),
    candidate.keyword_rank or 10**9,
    candidate.vector_rank or 10**9,
    candidate.document.id,
)
```

- [ ] **步骤 4：重构召回函数以返回可排序候选**

`_retrieve_by_db_keyword` 必须检查标题、正文及字符串化的标量元数据值，统计命中的不同查询词，并返回命中字段和关键词排名。`_retrieve_by_vector` 必须将余弦距离作为带标签列查询，使每条获准结果保留数值距离和排名。两个函数都必须在构造证据前执行 `can_read_knowledge`。

Add:

```python
def retrieve_documents_explained(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int = 5,
    db: Session | None = None,
    filters: dict | None = None,
) -> list[ExplainedDocument]:
    # Always attempt DB keyword and vector recall when db is available.
    # Fuse available candidates and return safe evidence.


def retrieve_documents(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int = 5,
    db: Session | None = None,
    filters: dict | None = None,
) -> list[KnowledgeDocument]:
    return [
        item.document
        for item in retrieve_documents_explained(
            query=query,
            user=user,
            documents=documents,
            limit=limit,
            db=db,
            filters=filters,
        )
    ]
```

保留现有无数据库的内存降级路径，并转换为关键词证据。向量 API/数据库失败不得丢弃有效关键词候选。

- [ ] **步骤 5：运行检索测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_retrieval.py -v`

预期：通过。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval_evidence.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py apps/inspilot_cloud_baby/tests/test_retrieval.py
git commit -m "feat: explain hybrid retrieval ranking"
```

## 任务 5：在搜索后台展示安全的检索证据

**文件：**
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/search.html`
- 新建：`apps/inspilot_cloud_baby/tests/test_chat_search.py`

- [ ] **步骤 1：编写失败的响应契约测试**

```python
def test_chat_source_exposes_safe_retrieval_evidence(monkeypatch) -> None:
    response = client.post("/chat/query", json={"query": "西宁市"})
    source = response.json()["sources"][0]
    assert source["recall_channels"] == ["keyword", "vector"]
    assert source["matched_fields"] == ["body"]
    assert source["keyword_rank"] == 1
    assert source["vector_rank"] == 2
    assert source["final_rank"] == 1
    assert "vector_distance" not in source
```

测试还必须断言：在检索边界下方模拟的未授权结果会在序列化前被拒绝；更优做法是让检索 fixture 根本无法产生该结果。

- [ ] **步骤 2：运行契约测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_chat_search.py -v`

预期：失败，因为 `SourceItem` 缺少证据字段。

- [ ] **步骤 3：扩展面向后台的来源契约**

```python
class SourceItem(BaseModel):
    id: str
    title: str
    source_type: str = ""
    region: str = ""
    insurer: str = ""
    integrator: str = ""
    doc_date: str = ""
    recall_channels: list[str] = []
    matched_fields: list[str] = []
    keyword_rank: int | None = None
    vector_rank: int | None = None
    final_rank: int
```

让 `_fetch_doc_kb` 调用 `retrieve_documents_explained`；Prompt 上下文只使用 `.document`，来源序列化使用 `.evidence`。HTTP 响应不得暴露向量距离。

- [ ] **步骤 4：在 `search.html` 中渲染紧凑诊断行**

为每个来源追加经过转义的文本节点，展示最终排名、渠道标签、命中字段、关键词排名和向量排名。标题链接保持主元素，沿用现有 12px 来源字号。API 返回值不得通过 `innerHTML` 写入。

- [ ] **步骤 5：运行对话和界面契约测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_chat_search.py tests/test_api_routes.py -v`

预期：通过。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/search.html apps/inspilot_cloud_baby/tests/test_chat_search.py
git commit -m "feat: show retrieval evidence in admin search"
```

## 任务 6：钉钉评论状态、规范化与去重

**文件：**
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **步骤 1：为评论可用、不可用、异常和重复场景编写失败测试**

```python
def test_comment_permission_error_is_not_reported_as_empty_success(client, permission_error):
    result = client.get_comments("PROC-1")
    assert result.status == "unavailable"
    assert result.comments == ()
    assert result.error_type == "permission_denied"


def test_duplicate_comment_merges_into_operation_record() -> None:
    merged = merge_approval_remarks(operation_records, comments)
    assert len(merged) == 1
    assert merged[0].node_name == "专项负责人"
    assert merged[0].comment_id == "c1"
    assert merged[0].sources == ("operation", "comment")
```

规范化测试必须覆盖首尾/连续空白、大小写折叠、中英文末尾标点和分钟级时间，同时保留原始展示文本。

- [ ] **步骤 2：运行钉钉测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -k 'comment or approval_chain' -v`

预期：失败，因为客户端当前返回列表，且没有归并意见模型。

- [ ] **步骤 3：实现显式获取结果和归并意见模型**

```python
@dataclass(frozen=True)
class CommentFetchResult:
    status: Literal["available", "unavailable", "error"]
    comments: tuple[AdminComment, ...] = ()
    error_type: str = ""
    message: str = ""


@dataclass(frozen=True)
class ApprovalRemark:
    user_id: str
    timestamp: str
    content: str
    node_name: str = ""
    operation_type: str = ""
    operation_result: str = ""
    comment_id: str = ""
    sources: tuple[str, ...] = ()
```

将钉钉权限错误码/消息映射为 `unavailable`，传输及非预期 API 错误映射为 `error`。`get_detail` 必须保留结果状态，不能把所有失败都转成空评论列表。

- [ ] **步骤 4：实现规范化和归并优先级**

使用 `(user_id, timestamp[:16], normalized_content)` 作为跨来源降级键。优先保留操作记录的节点/类型/结果字段，再补充评论 ID 和评论原文。在 `AdminWorkflowDetail`、`WorkflowDoc` 中增加 `comment_status`、`comment_error_type` 和归并意见。

更新 `_build_dingtalk_knowledge_body`：根据归并意见只渲染一个“审批意见”章节，不再分别渲染重复的审批链/评论文本；无意见的操作记录仍作为审批链事件保留。评论状态为不可用/异常时，增加明确降级说明。

- [ ] **步骤 5：运行钉钉和后台测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -v`

预期：通过。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: merge dingtalk comments with approval remarks"
```

## 任务 7：钉钉三项能力测试

**文件：**
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/settings.html`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/partials/_settings_test.html`
- 修改：`apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py`
- 修改：`apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **步骤 1：编写失败的能力测试**

```python
def test_dingtalk_capabilities_report_independent_states(client, permission_error):
    result = client.test_capabilities("PROC-1")
    assert result.token.ok is True
    assert result.approval_detail.ok is True
    assert result.comments.ok is False
    assert result.comments.status == "unavailable"


def test_dingtalk_settings_test_does_not_persist_test_instance_id(web, saved_settings):
    response = web.post(
        "/admin/settings/dingtalk-test",
        headers={"X-Test-Body": json.dumps({
            "app_key": "key", "app_secret": "secret", "process_instance_id": "PROC-1"
        })},
    )
    assert "基础连接" in response.text
    assert "审批详情" in response.text
    assert "独立评论" in response.text
    assert "PROC-1" not in saved_settings
```

- [ ] **步骤 2：运行聚焦测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -k capabilit -v`

预期：失败，因为能力模型和界面尚不存在。

- [ ] **步骤 3：实现能力测试结果**

```python
@dataclass(frozen=True)
class CapabilityStatus:
    status: Literal["ok", "failed", "unavailable", "not_tested"]
    message: str = ""


@dataclass(frozen=True)
class DingTalkCapabilities:
    token: CapabilityStatus
    approval_detail: CapabilityStatus
    comments: CapabilityStatus
```

`test_capabilities(process_instance_id)` 必须先测试 token。未提供实例 ID 时，详情/评论返回 `not_tested` 并给出明确说明；提供后，详情和评论 API 独立调用，任一失败不得覆盖另一项结果。

- [ ] **步骤 4：更新配置界面和端点**

增加标签为“测试审批实例 ID（不保存）”的 `process_instance_id` 输入，并纳入 `testDingTalk()` 的 `X-Test-Body`。在现有测试结果局部模板中以紧凑列表展示三项状态。审计只记录服务名、整体状态和能力状态码，绝不记录凭据或实例 ID。

- [ ] **步骤 5：运行测试**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -v`

预期：通过。

- [ ] **步骤 6：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/settings.html apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/partials/_settings_test.html apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: report dingtalk capability status"
```

## 任务 8：只读 Beta 门槛验证与文档

**文件：**
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/scripts/verify_beta_readiness.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_verify_beta_readiness.py`
- 修改：`apps/inspilot_cloud_baby/README.md`
- 修改：`docs/superpowers/plans/2026-06-18-beta-readiness-hardening.md`

- [ ] **步骤 1：编写失败的验证器测试**

```python
def test_verifier_stops_when_fixture_is_missing(session):
    report = verify_beta_readiness(business_id="202605281923000432811", db=session)
    assert report.ok is False
    assert report.errors == ("fixture_missing",)


def test_verifier_requires_top8_and_complete_evidence(session, seeded_dingtalk_knowledge):
    report = verify_beta_readiness(business_id="202605281923000432811", db=session)
    assert report.ok is True
    assert all(query.target_rank <= 8 for query in report.queries)
    assert all(query.channels and query.matched_fields for query in report.queries)


def test_verifier_reports_secret_record_ids_without_secret_values(session, configured_secrets):
    report = scan_audit_secrets(session)
    assert report.leaked_record_ids == ()
    assert "actual-secret" not in report.to_json()
```

- [ ] **步骤 2：运行验证器测试并确认失败**

运行：`cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_verify_beta_readiness.py -v`

预期：失败，因为验证器尚不存在。

- [ ] **步骤 3：实现只读验证器**

脚本必须：

1. 按 `metadata_json.business_id` 定位一条已生效的 `dingtalk_approval`。
2. 目标记录或 embedding 缺失时，以 `fixture_missing` 失败。
3. 将 `西宁市`、`浙江华重融资担保`、`华重担保` 和业务编号传入 `retrieve_documents_explained(limit=8)`。
4. 检查目标排名、召回渠道、命中字段和最终排名。
5. 统计审计动作。
6. 读取非空配置秘密值，精确扫描审计 `metadata_json` 序列化内容。
7. 仅输出包含状态和记录 ID 的 JSON，绝不输出秘密值。

提供命令：

```bash
python -m inspilot_cloud_baby.scripts.verify_beta_readiness --business-id 202605281923000432811
```

仅当所有自动门槛通过时退出码为 `0`；fixture、检索、证据或秘密检查失败时退出码为 `1`。

- [ ] **步骤 4：运行全部自动验证**

运行：

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest -v
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m ruff check .
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m inspilot_cloud_baby.scripts.verify_beta_readiness --business-id 202605281923000432811
git diff --check
```

预期：测试通过；Ruff 输出 `All checks passed!`；验证器以 0 退出，四个查询均有 Top 8 可解释结果且无秘密泄露；`git diff --check` 无输出。

- [ ] **步骤 5：运行真实钉钉和浏览器回归**

在 `/admin/settings` 使用该业务编号对应的已知流程实例 ID，验证三项能力状态。随后在 `/admin/dws` 预览/导入，并在 `/admin/search` 执行四个查询。记录独立评论为 `ok` 还是降级；无论哪种情况，审批操作记录都必须存在。确认每条搜索来源展示渠道、命中字段和最终排名，并在 5 秒内完成。

- [ ] **步骤 6：更新 README，并按实际结果勾选计划**

记录审计操作者限制（接入 SSO 前为 `admin:web`）、检索排序规则、钉钉能力结果、验证器命令、真实工单结果和实测查询耗时。独立评论权限仍不可用时，不得标记为通过。

- [ ] **步骤 7：提交**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/scripts/verify_beta_readiness.py apps/inspilot_cloud_baby/tests/test_verify_beta_readiness.py apps/inspilot_cloud_baby/README.md docs/superpowers/plans/2026-06-18-beta-readiness-hardening.md
git commit -m "test: verify beta readiness gates"
```

## 最终复核

- 确认设计中的每项要求都有对应任务和测试。
- 确认审计元数据不含请求正文、知识正文、API Key、Secret、密码或钉钉测试实例 ID。
- 确认公开对话响应只暴露排名和命中字段标签，不暴露向量距离或被过滤文档详情。
- 确认检索始终尝试两个数据库渠道，并在 embedding/向量检索不可用时正常降级。
- 确认未引入 Elasticsearch/OpenSearch、多模态输入或追问补全功能。
