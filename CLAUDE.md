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
docs/superpowers/
  specs/                       # PRD documents (current: V2.4)
  plans/                       # Implementation plans
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

Stack: Python 3.10+, FastAPI, SQLAlchemy 2, Pydantic v2, PostgreSQL 16 + pgvector, OpenAI embeddings, pytest, Ruff, HTMX.

```bash
cd apps/inspilot_cloud_baby
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -v            # Run all tests (42 tests)
python -m ruff check .         # Lint
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000  # Dev server
```

**Note**: Homebrew Python 3.12 on this machine has a libexpat incompatibility. Always prefix commands with `DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib` when running outside the venv (e.g. `DYLD_LIBRARY_PATH=/usr/local/opt/expat/lib .venv/bin/python -m pytest`).

### Database

PostgreSQL 16 runs in Docker container `inspilot-postgres` (port 5432, user/pass/db: `inspilot_cloud_baby`).
Requires **pgvector** extension (`CREATE EXTENSION IF NOT EXISTS vector` — auto-created on startup).
Tables auto-create on startup via `main.py` `on_event("startup")` → `Base.metadata.create_all()`.
Connection: `postgresql+psycopg://inspilot_cloud_baby:inspilot_cloud_baby@localhost:5432/inspilot_cloud_baby`

### Architecture

Modular monolith. All external capabilities (DingTalk approval API, object storage, vector search) isolated behind interfaces for post-PoC replacement.

Key modules: `models.py` (SQLAlchemy), `schemas.py` (Pydantic DTOs), `permissions.py` (visibility logic), `ingest/classifier.py` (material classification), `retrieval.py` (vector search + keyword fallback), `embedding.py` (OpenAI embedding service), `output_builder.py` (structured JSON), `dingtalk_admin.py` (DingTalk enterprise admin API client — direct Open Platform API, no external CLI), `routers/` (API + admin pages).

### Vector Search (`embedding.py` + `retrieval.py`)

- **Storage**: pgvector extension on `KnowledgeItem.embedding` column (Vector(1536), nullable)
- **Embedding service**: `embedding.py` wraps OpenAI `text-embedding-3-small` API with retry (3 attempts) and graceful degradation
- **Retrieval**: `retrieval.py` uses degradation chain — vector cosine distance search first, falls back to keyword matching on API/DB failure
- **Auto-embed**: Knowledge items get embeddings generated at creation time via `_attach_embedding()` in `routers/admin.py`
- **Migration**: `python -m inspilot_cloud_baby.scripts.migrate_embeddings` backfills embeddings for existing items
- **Config**: `BUSINESS_ROBOT_OPENAI_API_KEY`, `BUSINESS_ROBOT_ENABLE_VECTOR_SEARCH` (toggle), `BUSINESS_ROBOT_OPENAI_BASE_URL` (proxy support)

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
- **Knowledge** (`/admin/knowledge`) — CRUD + status workflow (待审核 → 已生效 → 已归档)
- **Projects** (`/admin/projects`) — project management with visibility settings
- **DingTalk Approval Import** (`/admin/dws`) — single + batch DingTalk approval import (direct Open Platform API) with progress indicator
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
