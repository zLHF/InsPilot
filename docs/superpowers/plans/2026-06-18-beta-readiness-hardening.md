# Beta Readiness Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the audit, retrieval explainability, and DingTalk comment-permission gates required before InsPilot enters Beta.

**Architecture:** Keep the FastAPI modular monolith and current PostgreSQL + pgvector retrieval stack. Add a transaction-scoped audit service, return internal retrieval evidence from always-on dual-channel recall while preserving keyword-first ranking, and model DingTalk comment fetch status explicitly so imports can degrade to operation records without hiding permission failures.

**Tech Stack:** Python 3.10+, FastAPI, SQLAlchemy 2, PostgreSQL 16, pgvector, Pydantic v2, Jinja2/HTMX, pytest, Ruff.

**Design:** `docs/superpowers/specs/2026-06-18-beta-readiness-hardening-design.md`

---

## File Map

- Create `src/inspilot_cloud_baby/audit.py`: audit action constants, secret-safe metadata helpers, and transaction-scoped audit writes.
- Create `src/inspilot_cloud_baby/retrieval_evidence.py`: retrieval candidate/evidence types and deterministic keyword-first fusion.
- Create `src/inspilot_cloud_baby/scripts/verify_beta_readiness.py`: read-only Beta gate verification.
- Modify `src/inspilot_cloud_baby/routers/admin.py`: connect audit writes, expose DingTalk capability status, and persist DingTalk provenance.
- Modify `src/inspilot_cloud_baby/retrieval.py`: remove keyword short-circuit, capture both recall channels, and return explained results.
- Modify `src/inspilot_cloud_baby/routers/chat.py`: expose safe retrieval evidence to the admin search console.
- Modify `src/inspilot_cloud_baby/dingtalk_admin.py`: explicit comment fetch status, normalization, deduplication, and capability checks.
- Modify `src/inspilot_cloud_baby/templates/search.html`: render recall channel, matched fields, and ranks.
- Modify `src/inspilot_cloud_baby/templates/settings.html`: accept a non-persisted test approval instance ID.
- Modify `src/inspilot_cloud_baby/templates/partials/_settings_test.html`: render three independent DingTalk capability states.
- Add focused tests under `tests/`; use PostgreSQL for audit transaction and secret persistence assertions.

## Task 1: Transaction-Scoped Audit Service

**Files:**
- Create: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/audit.py`
- Create: `apps/inspilot_cloud_baby/tests/test_audit.py`
- Create: `apps/inspilot_cloud_baby/tests/test_audit_integration.py`

- [ ] **Step 1: Write failing unit tests for audit construction and secret-safe configuration metadata**

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

- [ ] **Step 2: Run the unit tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_audit.py -v`

Expected: FAIL because `inspilot_cloud_baby.audit` does not exist.

- [ ] **Step 3: Implement the audit service**

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

- [ ] **Step 4: Add a real PostgreSQL rollback test**

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

- [ ] **Step 5: Run audit tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_audit.py tests/test_audit_integration.py -v`

Expected: PASS. If PostgreSQL is unavailable, fix the local Docker dependency; do not replace this test with a mock.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/audit.py apps/inspilot_cloud_baby/tests/test_audit.py apps/inspilot_cloud_baby/tests/test_audit_integration.py
git commit -m "feat: add transaction-scoped audit service"
```

## Task 2: Audit Knowledge, Project, and DingTalk Import Operations

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **Step 1: Write failing route tests that capture `AuditLog` objects added to the same session**

Add a reusable fake session that records both business rows and audit rows, then assert these actions:

```python
assert_audit(response, added, "knowledge.create", "knowledge_item")
assert_audit(response, added, "project.create", "project")
assert_audit(response, added, "knowledge.status.update", "knowledge_item")
assert_audit(response, added, "knowledge.visibility.update", "knowledge_item")
assert_audit(response, added, "knowledge.delete", "knowledge_item")
assert_audit(response, added, "dingtalk.import", "knowledge_item")
assert_audit(response, added, "dingtalk.batch_import", "knowledge_batch")
```

The helper must verify `actor_user_id == "admin:web"`, and the visibility/status tests must assert `metadata_json` contains `before` and `after` summaries without body content.

- [ ] **Step 2: Run focused admin tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py -k audit -v`

Expected: FAIL because the routes do not add audit rows.

- [ ] **Step 3: Add audit writes before each existing `session.commit()`**

Use this pattern for every covered operation:

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

For updates, capture enum/ID values before mutation. For delete, write the audit row before `session.delete(item)` and include only title, source type, project ID, sensitivity, and status. For batch import, use one transaction for all successfully built items, write one summary audit row with `requested_count`, `success_count`, and `failure_count`, and commit once; do not increment success count when `_db_query` returned `None`.

- [ ] **Step 4: Persist DingTalk provenance needed by the Beta verifier**

Both single and batch imports must include:

```python
metadata_json={
    "workflow_id": workflow.process_instance_id,
    "business_id": detail.business_id,
    "workflow_status": workflow.status,
    "originator": workflow.originator,
    "form_fields": list(workflow.form_data.keys()),
}
```

- [ ] **Step 5: Run route and integration tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit_integration.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: audit admin knowledge and import operations"
```

## Task 3: Audit Configuration Updates and Pre-Save Tests

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_admin_pages.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_audit_integration.py`

- [ ] **Step 1: Write failing tests for distinct action codes and secret redaction**

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

Extend the PostgreSQL integration test to load configured secrets from `app_settings`, scan serialized audit metadata, and assert none of the non-empty secret values occurs.

- [ ] **Step 2: Run focused tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit_integration.py -k 'config or secret' -v`

Expected: FAIL because no configuration audit exists.

- [ ] **Step 3: Implement update and test audit helpers**

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

Call this helper on every return path of embedding, chat, DingTalk, and production DB test endpoints. In `settings_save`, build the submitted value mapping, call `config_change_metadata`, write `config.update` in the existing save transaction, then commit once.

- [ ] **Step 4: Run admin and audit tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_admin_pages.py tests/test_audit.py tests/test_audit_integration.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py apps/inspilot_cloud_baby/tests/test_audit_integration.py
git commit -m "feat: audit configuration changes and tests"
```

## Task 4: Retrieval Evidence and Deterministic Dual-Channel Fusion

**Files:**
- Create: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval_evidence.py`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_retrieval.py`

- [ ] **Step 1: Write failing evidence and ranking tests**

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

Also cover title/metadata/body field priority, dual-channel tie-breaking, vector-only distance ordering, vector-unavailable status, deduplication, and stable document-ID tie-breaking.

- [ ] **Step 2: Run retrieval tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_retrieval.py -v`

Expected: FAIL because explained retrieval and fusion types do not exist.

- [ ] **Step 3: Implement focused evidence types and fusion**

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

Use an internal mutable candidate while merging. Its sort key must be exactly:

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

- [ ] **Step 4: Refactor recall functions to return rankable candidates**

`_retrieve_by_db_keyword` must inspect title, body, and stringified scalar metadata values, count distinct matched query terms, and return matched fields plus keyword rank. `_retrieve_by_vector` must select cosine distance as a labeled column so each permitted result retains its numeric distance and rank. Both functions must apply `can_read_knowledge` before constructing evidence.

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

Keep the existing no-DB in-memory fallback and convert it to keyword evidence. Vector API/DB failures must not discard valid keyword candidates.

- [ ] **Step 5: Run retrieval tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_retrieval.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval_evidence.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py apps/inspilot_cloud_baby/tests/test_retrieval.py
git commit -m "feat: explain hybrid retrieval ranking"
```

## Task 5: Expose Safe Retrieval Evidence in the Search Console

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/search.html`
- Create: `apps/inspilot_cloud_baby/tests/test_chat_search.py`

- [ ] **Step 1: Write failing response-contract tests**

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

The test must also assert an unauthorized result mocked below the retrieval boundary is rejected before serialization, or preferably cannot be produced by the retrieval fixture.

- [ ] **Step 2: Run the contract test and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_chat_search.py -v`

Expected: FAIL because `SourceItem` lacks evidence fields.

- [ ] **Step 3: Extend the admin-facing source contract**

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

Make `_fetch_doc_kb` call `retrieve_documents_explained`; use only `.document` for Prompt context and use `.evidence` for source serialization. Do not expose vector distance in the HTTP response.

- [ ] **Step 4: Render compact diagnostic rows in `search.html`**

For each source, append escaped text nodes showing final rank, channel labels, matched fields, keyword rank, and vector rank. Keep the title link as the primary element and use existing 12px source typography. Do not use `innerHTML` with API-provided values.

- [ ] **Step 5: Run chat and UI contract tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_chat_search.py tests/test_api_routes.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/search.html apps/inspilot_cloud_baby/tests/test_chat_search.py
git commit -m "feat: show retrieval evidence in admin search"
```

## Task 6: DingTalk Comment Status, Normalization, and Deduplication

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **Step 1: Write failing tests for available, unavailable, error, and duplicate comments**

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

Normalization tests must cover trimmed/collapsed whitespace, case folding, trailing Chinese/English punctuation, and minute-level timestamps while preserving original display text.

- [ ] **Step 2: Run DingTalk tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -k 'comment or approval_chain' -v`

Expected: FAIL because the client returns a list and has no merged remark model.

- [ ] **Step 3: Implement explicit fetch and merged remark models**

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

Map DingTalk permission error codes/messages to `unavailable`; map transport and unexpected API errors to `error`. `get_detail` must preserve the result status instead of converting every failure into an empty comment list.

- [ ] **Step 4: Implement normalization and merge priority**

Use `(user_id, timestamp[:16], normalized_content)` as the fallback cross-source key. Prefer operation-record node/type/result fields and supplement comment ID/original comment content. Add `comment_status`, `comment_error_type`, and merged remarks to `AdminWorkflowDetail` and `WorkflowDoc`.

Update `_build_dingtalk_knowledge_body` to render one `审批意见` section from merged remarks rather than separate duplicate chain/comment text, while retaining operation records with no remark as approval-chain events. Add an explicit degraded note when comment status is unavailable/error.

- [ ] **Step 5: Run DingTalk and admin tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: merge dingtalk comments with approval remarks"
```

## Task 7: Three-Part DingTalk Capability Test

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/settings.html`
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/partials/_settings_test.html`
- Modify: `apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **Step 1: Write failing capability tests**

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

- [ ] **Step 2: Run focused tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -k capabilit -v`

Expected: FAIL because capability models and UI are absent.

- [ ] **Step 3: Implement capability results**

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

`test_capabilities(process_instance_id)` must test token first. If no instance ID is supplied, return `not_tested` for detail/comments with a clear message. If supplied, call detail and comment APIs independently so one failure does not overwrite another.

- [ ] **Step 4: Update settings UI and endpoint**

Add a `process_instance_id` input labeled `测试审批实例 ID（不保存）`. Include it in `testDingTalk()`'s `X-Test-Body`. Render the three statuses as a compact list in the existing test-result partial. Audit only service name, overall status, and capability status codes; never audit credentials or the instance ID.

- [ ] **Step 5: Run tests**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_dingtalk_admin.py tests/test_admin_pages.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dingtalk_admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/settings.html apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/partials/_settings_test.html apps/inspilot_cloud_baby/tests/test_dingtalk_admin.py apps/inspilot_cloud_baby/tests/test_admin_pages.py
git commit -m "feat: report dingtalk capability status"
```

## Task 8: Read-Only Beta Gate Verification and Documentation

**Files:**
- Create: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/scripts/verify_beta_readiness.py`
- Create: `apps/inspilot_cloud_baby/tests/test_verify_beta_readiness.py`
- Modify: `apps/inspilot_cloud_baby/README.md`
- Modify: `docs/superpowers/plans/2026-06-18-beta-readiness-hardening.md`

- [ ] **Step 1: Write failing verifier tests**

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

- [ ] **Step 2: Run verifier tests and verify failure**

Run: `cd apps/inspilot_cloud_baby && DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_verify_beta_readiness.py -v`

Expected: FAIL because the verifier does not exist.

- [ ] **Step 3: Implement the read-only verifier**

The script must:

1. Locate one active `dingtalk_approval` by `metadata_json.business_id`.
2. Fail with `fixture_missing` if it or its embedding is absent.
3. Run `西宁市`, `浙江华重融资担保`, `华重担保`, and the business ID through `retrieve_documents_explained(limit=8)`.
4. Require target rank, channels, matched fields, and final rank.
5. Count audit actions.
6. Load non-empty configured secret values and scan audit `metadata_json` serialization for exact matches.
7. Emit JSON containing statuses and record IDs only; never emit secret values.

Expose:

```bash
python -m inspilot_cloud_baby.scripts.verify_beta_readiness --business-id 202605281923000432811
```

Exit `0` only when every automated gate passes; exit `1` for fixture, retrieval, evidence, or secret failures.

- [ ] **Step 4: Run all automated verification**

Run:

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest -v
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m ruff check .
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m inspilot_cloud_baby.scripts.verify_beta_readiness --business-id 202605281923000432811
git diff --check
```

Expected: tests PASS, Ruff reports `All checks passed!`, verifier exits 0 with four Top-8 explained results and no secret leaks, and `git diff --check` emits no output.

- [ ] **Step 5: Run real DingTalk and browser regression**

Use `/admin/settings` with the known process instance ID for the business ID and verify three capability rows. Then use `/admin/dws` to preview/import and `/admin/search` for all four queries. Record whether independent comments are `ok` or degraded; approval operation records must remain present in either case. Confirm each search source row shows channel, matched field, and final rank and completes within 5 seconds.

- [ ] **Step 6: Update README and mark plan checkboxes from actual results**

Document the audit actor limitation (`admin:web` until SSO), retrieval ranking rule, DingTalk capability result, verifier command, real work-order outcome, and measured query timings. Do not mark external comment permission as passed if it remains unavailable.

- [ ] **Step 7: Commit**

```bash
git add apps/inspilot_cloud_baby/src/inspilot_cloud_baby/scripts/verify_beta_readiness.py apps/inspilot_cloud_baby/tests/test_verify_beta_readiness.py apps/inspilot_cloud_baby/README.md docs/superpowers/plans/2026-06-18-beta-readiness-hardening.md
git commit -m "test: verify beta readiness gates"
```

## Final Review

- Confirm every requirement in the design has a corresponding task and test.
- Confirm no audit metadata includes request bodies, knowledge bodies, API keys, secrets, passwords, or DingTalk test instance IDs.
- Confirm the public chat response exposes ranks and matched-field labels only, not vector distances or filtered-document details.
- Confirm the retrieval implementation always attempts both DB channels but degrades cleanly when embedding/vector search is unavailable.
- Confirm no Elasticsearch/OpenSearch, multimodal input, or follow-up-question functionality was introduced.
