from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.chat_service import get_chat_service
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.retrieval import retrieve_documents

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

_DEFAULT_USER = CurrentUser(user_id="alpha", is_company_user=True, project_ids=set())

# Load the master prompt from docs/rag-prompt.md (single source of truth for AI behavior)
_PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "rag-prompt.md"


def _load_master_prompt() -> str:
    """Load the RAG prompt file. Falls back to a minimal inline prompt if missing."""
    try:
        return _PROMPT_PATH.read_text(encoding="utf-8")
    except Exception:
        logger.warning("Could not load %s, using fallback prompt", _PROMPT_PATH)
        return "你是 InsPilot 云小宝的知识助手。基于提供的信息回答用户问题。"


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatQueryRequest(BaseModel):
    query: str
    history: list[HistoryMessage] = []
    region: str = ""
    insurer: str = ""
    integrator: str = ""


class SourceItem(BaseModel):
    id: str
    title: str
    source_type: str = ""
    region: str = ""
    insurer: str = ""
    integrator: str = ""
    doc_date: str = ""


class ChatQueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    count: int = 0
    llm_used: bool = False


# ---------------------------------------------------------------------------
# Data-channel helpers — just fetch raw data, no routing/decision logic
# ---------------------------------------------------------------------------

_CONTEXT_MAX_CHARS = 6000


def _fetch_doc_kb(query: str, filters: dict | None) -> tuple[list, str]:
    """Channel 1: retrieve relevant scheme documents via vector search."""
    db: Session = SessionLocal()
    try:
        results = retrieve_documents(
            query=query, user=_DEFAULT_USER, documents=[], limit=8, db=db, filters=filters,
        )
    finally:
        db.close()
    if not results:
        return [], ""
    parts = []
    for i, doc in enumerate(results, 1):
        body = doc.body[:_CONTEXT_MAX_CHARS]
        m = doc.metadata
        meta_bits = [f"{lab}={m.get(k)}" for lab, k in (("地区", "region"), ("保司", "insurer"), ("集成商", "integrator")) if m.get(k)]
        meta_str = f"（{'，'.join(meta_bits)}）" if meta_bits else ""
        parts.append(f"【方案{i}】{doc.title}{meta_str}\n{body}")
    return results, "\n\n---\n\n".join(parts)


def _fetch_prod_db(query: str) -> tuple[str, str, int]:
    """Channel 2: generate SQL via LLM, execute on prod DB, return (sql, result_json, row_count)."""
    from inspilot_cloud_baby.prod_db_service import get_prod_db_service
    from inspilot_cloud_baby.routers.query import _SCHEMA_SUMMARY

    db_svc = get_prod_db_service()
    if not db_svc.available:
        return "", "", 0

    chat_svc = get_chat_service()
    if not chat_svc.available:
        return "", "", 0

    # Focused SQL-generation prompt (schema only, no general chat instructions)
    sql_system = (
        "你是 SQL 生成助手。根据用户的问题，生成一条 SQL Server (T-SQL) 查询语句。\n"
        "严格规则：\n"
        "1. 只能生成 SELECT 语句。\n"
        "2. 结果不超过 100 行（用 TOP 100）。\n"
        "3. 只返回 SQL 本身，不加任何解释、不加 markdown 标记。\n"
        "4. 必须用真实的表名和列名（见下方表结构），不要编造。\n"
        "5. 用中文列名做别名（AS）。\n"
        "6. 结果必须包含机构名称列。\n"
        "7. 机构名匹配：用户给全称，订单表 cInsuranceCompany 存简称。提取关键词（去掉有限公司/融资/担保/非融资性），用 LIKE '%关键词%' 匹配。\n\n"
        + _SCHEMA_SUMMARY
    )
    sql_raw = chat_svc.chat(
        [
            {"role": "system", "content": sql_system},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
    )
    if not sql_raw:
        return "", "", 0

    sql = _extract_sql(sql_raw)
    try:
        rows = db_svc.execute_query(sql)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Prod DB query failed: %s", exc)
        return sql, "", 0

    if not rows:
        return sql, "（查询结果为空）", 0
    compact = [{k: (str(v)[:80] if v is not None else "") for k, v in r.items()} for r in rows[:20]]
    return sql, json.dumps(compact, ensure_ascii=False, default=str), len(rows)


def _extract_sql(text: str) -> str:
    """Extract SQL from LLM output (strip markdown fences / trailing prose)."""
    text = text.strip()
    if text.startswith("```"):
        lines = [ln for ln in text.split("\n") if not ln.strip().startswith("```")]
        text = "\n".join(lines).strip()
    if ";" in text:
        text = text.split(";")[0]
    return text.strip()


# ---------------------------------------------------------------------------
# Main endpoint — fetch both channels, let the LLM synthesize
# ---------------------------------------------------------------------------

@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    # Build optional manual filters
    manual_filters: dict | None = None
    manual = {"region": request.region.strip(), "insurer": request.insurer.strip(), "integrator": request.integrator.strip()}
    if any(manual.values()):
        manual_filters = {k: v for k, v in manual.items() if v}

    # === Fetch BOTH channels — no routing, no decisions ===
    doc_results, doc_context = _fetch_doc_kb(request.query, manual_filters)
    prod_sql, prod_result, prod_rows = _fetch_prod_db(request.query)

    sources = [
        SourceItem(
            id=doc.id, title=doc.title, source_type=doc.source_type,
            region=doc.metadata.get("region", ""), insurer=doc.metadata.get("insurer", ""),
            integrator=doc.metadata.get("integrator", ""), doc_date=doc.metadata.get("doc_date", ""),
        )
        for doc in doc_results
    ]

    total_count = len(doc_results) + prod_rows

    if not doc_results and prod_rows == 0:
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的信息（方案知识库和生产数据库均无匹配）。",
            sources=[], count=0, llm_used=False,
        )

    # === Synthesize: feed master prompt + both channel results to LLM ===
    chat_svc = get_chat_service()
    if chat_svc.available:
        master = _load_master_prompt()
        sections = []
        if doc_context:
            sections.append(f"## 方案知识库（{len(doc_results)} 条相关方案）\n\n{doc_context}")
        if prod_result:
            sections.append(f"## 生产数据库（实时数据，{prod_rows} 行）\n\n```json\n{prod_result}\n```")
        combined = "\n\n---\n\n".join(sections)

        messages: list[dict] = [
            {"role": "system", "content": master + "\n\n## 本轮获取到的数据\n\n" + combined},
        ]
        for msg in request.history[-6:]:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": request.query})

        answer = chat_svc.chat(messages)
        if answer:
            sql_block = f"\n\n<details><summary>📄 生产库 SQL（{prod_rows} 行）</summary>\n\n```sql\n{prod_sql}\n```\n\n</details>" if prod_sql else ""
            return ChatQueryResponse(answer=answer + sql_block, sources=sources, count=total_count, llm_used=True)
        logger.warning("LLM call failed, returning degraded answer")

    # Degraded (no LLM)
    parts = []
    if doc_results:
        parts.append("**方案知识库：**\n" + "\n".join(f"- {s.title}" for s in sources[:8]))
    if prod_result:
        parts.append(f"**生产数据库（{prod_rows} 行）：**\n```json\n{prod_result[:1000]}\n```")
    return ChatQueryResponse(answer="\n\n".join(parts) or "（无数据）", sources=sources, count=total_count, llm_used=False)
