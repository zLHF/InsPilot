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

Stack: Python 3.10+, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, PostgreSQL 16, pytest, Ruff, HTMX.

```bash
cd apps/inspilot_cloud_baby
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -v            # Run all tests (24 tests)
python -m ruff check .         # Lint
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000  # Dev server
```

Architecture: Modular monolith. All external capabilities (DWS, object storage, vector search, DingTalk submission) isolated behind interfaces for post-PoC replacement.

Key modules: `models.py` (SQLAlchemy), `schemas.py` (Pydantic DTOs), `permissions.py` (visibility logic), `ingest/classifier.py` (material classification), `retrieval.py` (keyword search + permission filter), `output_builder.py` (structured JSON), `dws_adapter.py` (DingTalk workflow CLI), `routers/` (API + admin pages).

## Key Domain Concepts

- **Scenarios**: 历史知识查询, 项目变更, 需求提炼, 系统问题 — the four core use cases the bot recognizes
- **Structured output**: Three output types — `change_request`, `new_requirement`, `system_issue` with versioned optimistic locking
- **Knowledge layers**: 事实层 (fact), 候选层 (candidate), 参考层 (reference) — outputs always show source and confidence
- **Permission model**: Project visibility (`company_visible` / `project_members` / `restricted`) + knowledge sensitivity (`public_summary` / `project_restricted` / `sensitive`)
- **PII handling**: Three-tier processing on public cloud, masked by default, audit-trail for authorized view
- **DingTalk integration**: Primary entry point and downstream flow channel for both issues and requirements

## PRD

Current PRD is `docs/superpowers/specs/2026-06-06-inspilot-cloud-baby-prd-v2.4.md`. Version history runs from V1.4 through V2.4 — always reference the latest version for product requirements.
