# Alpha Hardening and Beta Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Alpha closure for InsPilot 云小宝 and add the minimum hardening needed before Beta work begins.

**Architecture:** Keep the current FastAPI modular monolith. Treat the existing Alpha backend as the source of truth, then harden it by removing stale DWS CLI assumptions, moving startup initialization to FastAPI lifespan, adding an audit-log persistence foundation, and defining the manual real DingTalk validation gate.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2, PostgreSQL 16 + pgvector, pytest, Ruff, Jinja2, HTMX, DingTalk Open Platform API.

---

## File Structure

- Modify: `docs/superpowers/plans/2026-06-08-inspilot-cloud-baby-alpha.md`
  - Mark the old DWS CLI snippets as historical design notes and keep the remaining real DingTalk validation item visible.
- Modify: `apps/inspilot_cloud_baby/README.md`
  - Add Alpha closure status, real DingTalk validation steps, and current known hardening gates.
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`
  - Replace deprecated `@app.on_event("startup")` with a FastAPI lifespan context manager.
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/models.py`
  - Add a minimal `AuditLog` model for Beta permission/security auditing.
- Modify: `apps/inspilot_cloud_baby/tests/test_health.py`
  - Add a regression test proving the app uses lifespan instead of deprecated startup handlers.
- Modify: `apps/inspilot_cloud_baby/tests/test_models.py`
  - Add a model-level contract test for the audit log table and required fields.

## Task 1: Alpha Closure Documentation

**Files:**
- Modify: `docs/superpowers/plans/2026-06-08-inspilot-cloud-baby-alpha.md`
- Modify: `apps/inspilot_cloud_baby/README.md`

- [x] **Step 1: Mark legacy DWS CLI sections as historical**

Update the Alpha plan so sections that mention `dws_adapter.py`, `routers/dws.py`, or `dws auth login` are clearly labeled as historical design content superseded by `dingtalk_admin.py`.

- [x] **Step 2: Add real DingTalk validation checklist**

Add a short checklist to the backend README:

```markdown
## Alpha 封板验证

- [x] 已配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_KEY`
- [x] 已配置企业内部应用 `BUSINESS_ROBOT_DINGTALK_APP_SECRET`
- [x] `/admin/dws/status` 返回连接成功
- [x] 用真实审批工单号完成 `/admin/dws/preview`
- [x] 用同一审批实例完成 `/admin/dws/import`
- [x] 导入后的知识条目进入 `pending_review`，人工审核后为 `active`
- [x] 已人工核对表单字段、审批链条操作记录和导入来源标识
```

- [x] **Step 3: Verify docs contain no active DWS CLI instructions**

Run:

```bash
rg -n "dws auth login|dws schema oa|dws oa process-instance|dws_adapter|routers/dws" docs/superpowers/plans/2026-06-08-inspilot-cloud-baby-alpha.md apps/inspilot_cloud_baby/README.md
```

Expected: matches are either absent from README or explicitly inside historical-note context in the Alpha plan.

## Task 2: FastAPI Lifespan Migration

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_health.py`

- [x] **Step 1: Write failing lifespan regression test**

Add:

```python
def test_app_uses_lifespan_instead_of_deprecated_startup_handlers() -> None:
    app = create_app()

    assert app.router.on_startup == []
    assert app.router.lifespan_context is not None
```

- [x] **Step 2: Run test to verify failure**

Run:

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_health.py::test_app_uses_lifespan_instead_of_deprecated_startup_handlers -v
```

Expected: FAIL because the app still registers a startup handler.

- [x] **Step 3: Implement lifespan initialization**

Move database initialization into a small helper and register it via `FastAPI(lifespan=lifespan)`.

- [x] **Step 4: Verify targeted test passes**

Run the same pytest command. Expected: PASS.

## Task 3: Minimal Audit Log Foundation

**Files:**
- Modify: `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/models.py`
- Modify: `apps/inspilot_cloud_baby/tests/test_models.py`

- [x] **Step 1: Write failing audit model contract test**

Add a test that asserts `AuditLog.__tablename__ == "audit_logs"` and that the table has these columns:

```python
{
    "id",
    "actor_user_id",
    "action",
    "resource_type",
    "resource_id",
    "reason",
    "metadata_json",
    "created_at",
}
```

- [x] **Step 2: Run test to verify failure**

Run:

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest tests/test_models.py::test_audit_log_model_has_beta_required_fields -v
```

Expected: FAIL because `AuditLog` does not exist.

- [x] **Step 3: Implement `AuditLog` model**

Add a SQLAlchemy model with UUID primary key, actor, action, resource identity, optional reason, JSON metadata, and timestamp.

- [x] **Step 4: Verify targeted test passes**

Run the same pytest command. Expected: PASS.

## Task 4: Verification

**Files:**
- No new files.

- [x] **Step 1: Run full backend tests**

Run:

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest -v
```

Expected: all tests pass.

- [x] **Step 2: Run Ruff**

Run:

```bash
cd apps/inspilot_cloud_baby
DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m ruff check .
```

Expected: `All checks passed!`

## Task 5: Real DingTalk Validation Gate

**Files:**
- Modify: `apps/inspilot_cloud_baby/README.md`
- Modify: `docs/superpowers/plans/2026-06-08-inspilot-cloud-baby-alpha.md`

- [x] **Step 1: Confirm real DingTalk validation inputs**

Validated inputs:

```text
BUSINESS_ROBOT_DINGTALK_APP_KEY configured in settings or environment
BUSINESS_ROBOT_DINGTALK_APP_SECRET configured in settings or environment
Business ID: 202605281923000432811
Resolved process instance ID: pqolozaASbajK5D54JpIPg00861779967423
```

- [x] **Step 2: Run real validation**

Backend validation command:

```bash
cd apps/inspilot_cloud_baby
curl -sS http://127.0.0.1:8000/admin/dws/status
curl -sS -X POST http://127.0.0.1:8000/admin/dws/preview \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'workflow_id=202605281923000432811'
```

Observed result:

- `/admin/dws/status` returned connected with valid access token.
- `/admin/dws/preview` resolved the business ID to the process instance ID and rendered the real approval.
- Preview parsed 29 form fields and 14 operation records.
- Imported knowledge item `46010940-b027-4771-9608-932cf479a34a` is now reviewed as `active`.
- `/chat/query` can retrieve the imported knowledge by `西宁市`, `浙江华重融资担保`, and `华重担保`.

Remaining limitation:

- DingTalk standalone comment API currently returns an unavailable/permission error; approval-chain remarks are still captured through operation records. Beta should re-check the `dingtalk.oapi.processinstance.comment.list` permission if independent comment lists become a requirement.

---

## Beta Search Architecture Note

**Decision:** Do not treat the vector database as the only search engine. InsPilot search must use hybrid retrieval.

**Current Alpha posture:** Keep the lightweight in-process stack:

- PostgreSQL exact keyword recall over title/body for field-like queries such as city, institution, approval ID, business ID, and DingTalk form values.
- pgvector semantic recall for fuzzy business questions and similar scheme discovery.
- Merge and deduplicate recall results before applying LLM synthesis.
- Keep permission/status filtering in the retrieval path before results are exposed to the prompt.

**Reason:** DingTalk approvals and insurance project documents contain many exact business identifiers, including city names, institution names, rates, product types, record IDs, and approval-chain remarks. Vector similarity alone is not reliable enough for these exact-match requirements, and prompt changes cannot recover records that were never retrieved into context.

**Beta trigger for Elasticsearch/OpenSearch:** Introduce Elasticsearch/OpenSearch as the first retrieval channel when any of these become material:

- Knowledge volume grows enough that PostgreSQL `ILIKE` recall is slow or hard to rank.
- Users need highlighted snippets, Chinese word segmentation, synonyms, field boosting, or typo tolerance.
- Search needs richer structured filters across source type, region, institution, product type, approval status, date range, and project visibility.
- Reranking needs a broader candidate pool than PostgreSQL + pgvector can cheaply provide.

**Target Beta+ shape:**

```text
Query
  -> Elasticsearch/OpenSearch exact + full-text recall
  -> pgvector semantic recall
  -> merge + dedupe
  -> rerank
  -> permission/status filtering
  -> RAG prompt synthesis
```

Open question for Beta planning: decide whether to use self-hosted Elasticsearch/OpenSearch, managed cloud search, or PostgreSQL full-text search as an intermediate step before introducing another service.

---

## Self-Review

- Spec coverage: This plan covers the remaining Alpha manual gate and the first Beta readiness foundations from PRD v2.4: hardening, auditability, and safer runtime initialization.
- Placeholder scan: No task contains TBD/TODO/fill-in-later language. The DingTalk real validation gate explicitly lists the required external inputs.
- Type consistency: `AuditLog`, `metadata_json`, and lifespan terminology are consistent across tasks.
