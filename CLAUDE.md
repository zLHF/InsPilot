# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**InsPilot 云小宝** — a multimodal AI business assistant for insurance industry front-line workers (market, operations, business lines). Users express problems/needs via natural language + multimodal input; the bot handles scene recognition, follow-up questions, knowledge retrieval, and structured output that flows into DingTalk (钉钉) processes.

The product targets **public cloud SaaS, publicly accessible**, with DingTalk as the primary entry point and downstream channel.

## Repository Structure

```
apps/
  inspilot_mobile_prototype/   # React mobile prototype (Vite)
  inspilot_cloud_baby/         # Alpha backend (FastAPI)
docs/
  prod-db-dictionary.md        # Production SQL Server DB schema (436 tables)
  superpowers/
    specs/                     # PRD documents (current: V2.4)
    plans/                     # Implementation plans
```

## Mobile Prototype (`apps/inspilot_mobile_prototype/`)

Stack: React 19, Vite 6, no router/state lib — single-file component architecture (`App.jsx`).

```bash
npm run dev        # Start dev server at 127.0.0.1
npm run build      # Production build
npm run test       # Run tests (node --test)
npm run preview    # Preview production build
```

Tests live in `tests/` and use Node.js built-in test runner (`node:test` + `node:assert/strict`), asserting against source file contents via regex matching.

The prototype renders a 390px mobile shell with three tabs (对话/记录/我的), covering four core scenarios: 历史知识、项目变更、需求提炼、系统问题.

Per `AGENTS.md`: run the dev server yourself rather than giving instructions. Treat selected generated mock images as source of truth for layout/spacing/color/typography.

## Alpha Backend (`apps/inspilot_cloud_baby/`)

Stack: Python 3.10+, FastAPI, SQLAlchemy 2, Pydantic v2, PostgreSQL 16 + pgvector, OpenAI embeddings + chat, pymssql (SQL Server), pytest, Ruff, HTMX.

```bash
cd apps/inspilot_cloud_baby
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -v            # Run all tests (45 tests)
python -m ruff check .         # Lint
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000  # Dev server
```

**Note**: Homebrew Python 3.12 on this machine has a libexpat incompatibility. Always prefix commands with `DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib` when running outside the venv (e.g. `DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest`).

### Database

PostgreSQL 16 runs in Docker container `inspilot-postgres` (port 5432, user/pass/db: `inspilot_cloud_baby`). Uses the `pgvector/pgvector:pg16` image (not plain postgres — the pgvector extension is required).
**Requires Docker Desktop running** — if settings/data appear "missing", check `docker ps` first; the container may be stopped (data is safe in the volume).
Requires **pgvector** extension (`CREATE EXTENSION IF NOT EXISTS vector` — auto-created on startup).
Tables auto-create on startup via `main.py` `on_event("startup")` → `Base.metadata.create_all()`.
Connection: `postgresql+psycopg://inspilot_cloud_baby:inspilot_cloud_baby@localhost:5432/inspilot_cloud_baby`

### Architecture

Modular monolith. All external capabilities (DingTalk approval API, object storage, vector search) isolated behind interfaces for post-PoC replacement.

Key modules: `models.py` (SQLAlchemy), `schemas.py` (Pydantic DTOs), `permissions.py` (visibility logic — PUBLIC_SUMMARY with no project is company-readable for shared scheme libraries), `ingest/classifier.py` (material classification), `retrieval.py` (vector search + keyword fallback + query-intent extraction + province→city expansion), `embedding.py` (OpenAI embedding service), `rerank.py` (cross-encoder rerank client, graceful degradation), `chat_service.py` (LLM chat service for RAG — `chat()` + `chat_stream()`), `prod_db_service.py` (read-only SQL Server connection for NL2SQL), `output_builder.py` (structured JSON), `dingtalk_admin.py` (DingTalk enterprise admin API client — direct Open Platform API, no external CLI), `routers/` (API + admin pages: `chat.py` (dual-source RAG + NL2SQL, fully autonomous), `query.py` (NL2SQL schema + SQL endpoints), `admin.py`, `health.py`, `ingest.py`, `projects.py`).

**AI behavior is fully externalized**: `docs/rag-prompt.md` is the single source of truth for how the LLM behaves (which channels to use, schema reference, lessons learned). Edit that file to tune behavior — no code changes needed. The LLM owns *synthesis* (how to use the data); the code makes no semantic routing decisions. The one exception is a cheap **performance gate** (`_needs_prod_db`, toggleable) that skips the prod-DB channel for questions with no real-time signal — it changes *whether a slow round-trip runs*, not how the answer is composed.

### Vector Search (`embedding.py` + `retrieval.py`)

- **Storage**: pgvector extension on `KnowledgeItem.embedding` column (Vector(1536), nullable)
- **Embedding service**: `embedding.py` wraps OpenAI `text-embedding-3-small` API with retry (3 attempts) and graceful degradation
- **Retrieval**: `retrieval.py` runs a **hybrid pipeline** — keyword (jieba 中文分词) + vector recall over a wider candidate pool → **RRF fusion** (`_rrf_fuse`) → optional **cross-encoder rerank** → trim to top-k. Each stage degrades gracefully (a failing channel is skipped; both empty → in-memory keyword fallback). Optional LLM query-rewrite (`_maybe_rewrite_query`, off by default — adds a round-trip).
- **ANN index**: `KnowledgeItem.embedding` has an **HNSW** index (`vector_cosine_ops`), defined in the model and ensured idempotently on startup (`CREATE INDEX IF NOT EXISTS`) — turns vector search from a full-table seq scan into O(log n).
- **Rerank** (`rerank.py`): calls an OpenAI-compatible `/rerank` endpoint (Jina / Cohere / SiliconFlow); no key configured → graceful no-op (keeps fused order).
- **Auto-embed**: Knowledge items get embeddings generated at creation time via `_attach_embedding()` in `routers/admin.py`
- **Migration**: `python -m inspilot_cloud_baby.scripts.migrate_embeddings` backfills embeddings for existing items
- **Eval harness** (`scripts/eval_retrieval.py`): recall@k / MRR over a labeled or auto-generated query set — the "ruler" for A/B-testing retrieval changes (rerank on/off, hybrid on/off, etc.)
- **Config**: `BUSINESS_ROBOT_OPENAI_API_KEY`, `BUSINESS_ROBOT_ENABLE_VECTOR_SEARCH` (toggle), `BUSINESS_ROBOT_OPENAI_BASE_URL` (proxy); `BUSINESS_ROBOT_RERANK_API_KEY/BASE_URL/MODEL` + `BUSINESS_ROBOT_ENABLE_RERANK`; `BUSINESS_ROBOT_ENABLE_HYBRID_SEARCH`, `BUSINESS_ROBOT_ENABLE_QUERY_REWRITE`

### Conversational RAG Search (`chat.py` + `chat_service.py`)

- **Search console** at `/admin/search` — full chat interface (bubbles, markdown rendering via marked.js, multi-turn history, quick-question chips), consumes the streaming endpoint
- **Streaming**: `POST /chat/stream` (SSE) pushes `sources` first, then answer token-by-token, then `done` — first byte in ~1-2s instead of waiting for the full answer. `POST /chat/query` kept as the non-streaming equivalent.
- **Parallel channels**: `_gather_channels()` fetches doc KB ‖ prod DB concurrently (ThreadPoolExecutor) — total latency ≈ max(both) not sum.
- **RAG flow**: user question → `retrieve_documents()` (hybrid + region filter) → retrieved plans fed as context to LLM (6K chars/plan) → LLM generates structured answer
- **Chat service**: `chat_service.py` wraps OpenAI-compatible `chat.completions.create()` (OpenRouter / DeepSeek / OpenAI), `chat()` (3-retry) + `chat_stream()` (streaming, no retry), lazy singleton with hot-reload
- **Prod-DB gate** (`_needs_prod_db`): cheap heuristic pre-filter — only generate+run SQL when the question hits real-time signals (order/rate/number…), so pure-KB questions skip the SQL round-trip. This is a *performance* pre-filter, NOT semantic routing (the LLM still owns how to use the data). Toggle with `BUSINESS_ROBOT_ENABLE_PROD_DB_GATE` (default on; off = both channels always run).
- **Query log** (`QueryLog` table): every turn is logged (query, recalled doc_ids, zero_result flag, latency). Zero-result rows surface the keywords/黑话 users search but you can't answer — the data-driven way to find what to improve.
- **Config**: `BUSINESS_ROBOT_CHAT_API_KEY`, `BUSINESS_ROBOT_CHAT_BASE_URL`, `BUSINESS_ROBOT_CHAT_MODEL`, `BUSINESS_ROBOT_ENABLE_PROD_DB_GATE`
- **Degraded mode**: if no chat model configured, returns title list instead of LLM answer

### CS3.0 Scheme Import (`scripts/import_cs3_plans.py`)

- Parses 794 self-contained HTML scheme files (strip tags → plain text + dimensions)
- **Dimension extraction**: dual-source — title line (primary) + filename (fallback); substring-matches insurer/integrator, derives region from residual text
- **Province→city expansion**: `_PROVINCE_CITIES` mapping in `retrieval.py` — searching a province (浙江) auto-includes its cities (杭州/温州/湖州…)
- **Region matching**: prefix match (衢州 → 衢州市/衢州常山) at the SQL layer
- 697 plans imported with embeddings; `source_type="cs3_plan"`, `metadata_json` holds region/insurer/integrator/doc_date
- Idempotent (dedupes by `metadata.original_file`)

### NL2SQL — Production DB Queries (`routers/query.py` + `prod_db_service.py`)

- **Purpose**: query live production data (rates, orders, platform config) that's more current than the scheme documents
- **Flow**: user question → LLM generates SQL (guided by trimmed core-table schema) → safety check → execute read-only → LLM answers from rows
- **ProdDBService**: pymssql connection to SQL Server (YDB_GeneralSystemDB). Safety: SELECT-only regex guard, forced TOP 50, 10s timeout
- **Data dictionary**: `docs/prod-db-dictionary.md` (436 tables, 5567 fields) — regenerate when prod schema changes
- **Config**: `BUSINESS_ROBOT_PROD_DB_HOST/PORT/NAME/USER/PASSWORD` (use a read-only account)
- **Test endpoint**: `POST /admin/settings/db-test` (pre-save connection test)

### Plan Detail Page (`/admin/knowledge/{id}`)

- Structured rendering of scheme body via `format_plan_body()` — known section titles → sub-headings, `《...》` doc names → h4, key:value lines → definition rows
- Metadata header (region/insurer/integrator/date badges), source filename, copy-all button

### Settings Page (`/admin/settings`)

Three configurable services, each with a **pre-save test button** (tests current input-box values before committing):
- **🔑 OpenAI Embedding** — API key / base URL / model + vector search toggle
- **🤖 对话模型** — API key / base URL / model (for RAG chat)
- **🗄️ 生产数据库** — SQL Server host/port/db/user/password (for NL2SQL)
- All saved to `app_settings` table; hot-reload via singleton reset; env vars override DB

### DingTalk Admin API (`dingtalk_admin.py`)

Direct client for the DingTalk Open Platform (`/topapi/processinstance/*`), using an enterprise internal app's AppKey/AppSecret for org-wide access. **No external CLI/binary is used** (the former `dws_adapter.py` that shelled out to a `dws` binary has been removed). Key capabilities:
- **Process code discovery**: `list_process_templates()` via `/topapi/process/listbyuserid` — discovers all org approval templates
- **Business ID resolution**: `resolve_business_id_fast()` — parses `YYYYMMDD` from business_id for date-aware 1-day window search across all process codes
- **Detail fetch**: `get_detail()` — fetches instance detail + comments + structured attachments
- **Batch fetch**: `batch_get_details()` — rate-limited (50ms) batch operation
- **Connection check**: `test_connection()` — validates AppKey/AppSecret without raising
- **Recent instances**: `list_recent_instances()` — approximate recent-instance list (DingTalk has no per-user pending-approval API)
- **View model**: `to_workflow()` converts an `AdminWorkflowDetail` into a `WorkflowDoc` for the admin templates
- **Config**: `BUSINESS_ROBOT_DINGTALK_APP_KEY`, `BUSINESS_ROBOT_DINGTALK_APP_SECRET`
- **API limits** (empirically verified):
  - `listids` max time range width: **120 days**
  - `listids` max lookback: **365 days** (older dates return "时间戳无效")
  - Comment API requires separate permission (`dingtalk.oapi.processinstance.comment.list`)

### Admin Pages (`routers/admin.py`)

HTMX-driven admin UI at `/admin/*`:
- **Dashboard** (`/admin`) — project/knowledge stats
- **Ingest** (`/admin/ingest`) — text-based knowledge import with auto-classification
- **Knowledge** (`/admin/knowledge`) — CRUD + status workflow (待审核 → 已生效 → 已归档), pagination (20/page default, 50/100 options, pager top+bottom)
- **Plan Detail** (`/admin/knowledge/{id}`) — structured read-only view of a scheme
- **Search Console** (`/admin/search`) — conversational RAG chat interface
- **Projects** (`/admin/projects`) — project management with visibility settings
- **DingTalk Approval Import** (`/admin/dws`) — single + batch DingTalk approval import (direct Open Platform API) with progress indicator
- **Settings** (`/admin/settings`) — embedding + chat model + prod DB config with pre-save test buttons
- Templates in `templates/` with HTMX partials in `templates/partials/`

## Key Domain Concepts

- **Scenarios**: 历史知识查询, 项目变更, 需求提炼, 系统问题 — the four core use cases the bot recognizes
- **Structured output**: Three output types — `change_request`, `new_requirement`, `system_issue` with versioned optimistic locking
- **Knowledge layers**: 事实层 (fact), 候选层 (candidate), 参考层 (reference) — outputs always show source and confidence
- **Permission model**: Project visibility (`company_visible` / `project_members` / `restricted`) + knowledge sensitivity (`public_summary` / `project_restricted` / `sensitive`)
- **PII handling**: Three-tier processing on public cloud, masked by default, audit-trail for authorized view
- **DingTalk integration**: Primary entry point and downstream flow channel for both issues and requirements

## PRD

Current PRD is `docs/superpowers/specs/2026-06-06-inspilot-cloud-baby-prd-v2.4.md`. Version history runs from V1.4 through V2.4 — always reference the latest version for product requirements.
