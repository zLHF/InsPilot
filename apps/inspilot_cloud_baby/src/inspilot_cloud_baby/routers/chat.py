from __future__ import annotations

import logging

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.chat_service import get_chat_service
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.retrieval import retrieve_documents

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Alpha default user — replace with real auth when available
_DEFAULT_USER = CurrentUser(user_id="alpha", is_company_user=True, project_ids=set())

# Max chars of each retrieved plan fed to the LLM. Plans are 8K-12K chars;
# 6000 covers the key sections (话术/单证说明/费率/保额/收款/退保) while
# keeping total prompt bounded (~48K chars for 8 plans ≈ 24K tokens).
_CONTEXT_MAX_CHARS = 6000


class HistoryMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatQueryRequest(BaseModel):
    query: str
    history: list[HistoryMessage] = []
    region: str = ""
    insurer: str = ""
    integrator: str = ""


class SourceItem(BaseModel):
    """One retrieved knowledge source shown to the user."""

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
# System prompt for the final cross-referenced answer
# ---------------------------------------------------------------------------

_FINAL_PROMPT = (
    "你是 InsPilot 云小宝的知识助手，专门帮助保险业务人员解答方案相关问题。\n\n"
    "你将收到来自两个数据源的信息：\n"
    "1. **方案知识库**：项目接入或变更初期的方案文档（可能含过时信息）。\n"
    "2. **生产数据库**：实际运行中的最新业务数据（最准确、最实时）。\n\n"
    "回答规则：\n"
    "1. **以生产数据库为准**——当两个来源有冲突时，生产库的数据是正确的。\n"
    "2. 综合两个来源的信息，给出完整、准确的回答。\n"
    "3. 如果涉及多个条目，用列表或对比表格清晰呈现。\n"
    "4. 某个来源没有相关信息时，基于另一个来源回答即可。\n"
    "5. 如果两个来源都没有相关信息，如实说明，不要编造。\n"
    "6. 回答用中文，使用 Markdown 格式。"
)


def _build_context(results) -> str:
    """Build a knowledge-context string from retrieved documents for the LLM."""
    parts = []
    for i, doc in enumerate(results, 1):
        body = doc.body[:_CONTEXT_MAX_CHARS]
        meta_bits = []
        m = doc.metadata
        for label, key in (("地区", "region"), ("保司", "insurer"), ("集成商", "integrator")):
            if m.get(key):
                meta_bits.append(f"{label}={m[key]}")
        meta_str = f"（{'，'.join(meta_bits)}）" if meta_bits else ""
        parts.append(f"【方案{i}】{doc.title}{meta_str}\n{body}")
    return "\n\n---\n\n".join(parts)


def _fetch_doc_kb(query: str, filters: dict | None) -> tuple[list, str]:
    """Query the document knowledge base (RAG). Returns (docs, context_text)."""
    db: Session = SessionLocal()
    try:
        results = retrieve_documents(
            query=query,
            user=_DEFAULT_USER,
            documents=[],
            limit=8,
            db=db,
            filters=filters,
        )
    finally:
        db.close()

    if not results:
        return [], ""
    return results, _build_context(results)


def _fetch_prod_db(query: str) -> tuple[str, str, int]:
    """Query the production DB (NL2SQL). Returns (sql, result_text, row_count)."""
    from inspilot_cloud_baby.prod_db_service import get_prod_db_service
    from inspilot_cloud_baby.routers.query import _SCHEMA_SUMMARY, _extract_sql
    import json

    db_svc = get_prod_db_service()
    if not db_svc.available:
        return "", "", 0

    chat_svc = get_chat_service()
    if not chat_svc.available:
        return "", "", 0

    # Step 1: LLM generates SQL
    sql_system = (
        "你是一个 SQL 生成助手。根据用户的问题和下面的数据库表结构，生成一条 SQL Server (T-SQL) 查询语句。\n"
        "规则：\n"
        "1. 只能生成 SELECT 语句。\n"
        "2. 查询结果不要超过 100 行（用 TOP 100）。\n"
        "3. 只返回 SQL 语句本身，不要加任何解释或 markdown 标记。\n"
        "4. 用中文列名做别名（AS）方便阅读。\n\n"
        + _SCHEMA_SUMMARY
    )
    sql_raw = chat_svc.chat(
        [{"role": "system", "content": sql_system}, {"role": "user", "content": query}],
        temperature=0.0,
    )
    if not sql_raw:
        return "", "", 0

    sql = _extract_sql(sql_raw)

    # Step 2: Execute
    try:
        rows = db_svc.execute_query(sql)
    except (ValueError, Exception) as exc:  # noqa: BLE001
        logger.warning("Prod DB query failed: %s", exc)
        return sql, "", 0

    if not rows:
        return sql, "（查询结果为空）", 0

    compact = [{k: (str(v)[:80] if v is not None else "") for k, v in r.items()} for r in rows[:20]]
    return sql, json.dumps(compact, ensure_ascii=False, default=str), len(rows)


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    # Build manual filters from request (only non-empty values)
    manual_filters: dict | None = None
    manual = {
        "region": request.region.strip(),
        "insurer": request.insurer.strip(),
        "integrator": request.integrator.strip(),
    }
    if any(manual.values()):
        manual_filters = {k: v for k, v in manual.items() if v}

    # === Dual-source fetch: query BOTH data sources ===
    doc_results, doc_context = _fetch_doc_kb(request.query, manual_filters)
    prod_sql, prod_result, prod_rows = _fetch_prod_db(request.query)

    # Build source list from doc KB (for the citation cards)
    sources = [
        SourceItem(
            id=doc.id,
            title=doc.title,
            source_type=doc.source_type,
            region=doc.metadata.get("region", ""),
            insurer=doc.metadata.get("insurer", ""),
            integrator=doc.metadata.get("integrator", ""),
            doc_date=doc.metadata.get("doc_date", ""),
        )
        for doc in doc_results
    ]

    total_count = len(doc_results) + prod_rows

    # Both sources empty?
    if not doc_results and prod_rows == 0:
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的信息（方案知识库和生产数据库均无匹配）。",
            sources=[],
            count=0,
            llm_used=False,
        )

    # === Cross-reference: feed both sources to LLM for a unified answer ===
    chat_svc = get_chat_service()
    if chat_svc.available:
        sections = []
        if doc_context:
            sections.append(f"## 方案知识库（{len(doc_results)} 条相关方案）\n\n{doc_context}")
        if prod_result:
            sections.append(f"## 生产数据库（实时数据，{prod_rows} 行）\n\n查询结果：\n```json\n{prod_result}\n```")
        combined_context = "\n\n---\n\n".join(sections)

        messages: list[dict] = [
            {"role": "system", "content": _FINAL_PROMPT + "\n\n" + combined_context},
        ]
        for msg in request.history[-6:]:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": request.query})

        answer = chat_svc.chat(messages)
        if answer:
            # Append SQL detail if prod DB was used
            sql_block = ""
            if prod_sql:
                sql_block = f"\n\n<details><summary>📄 生产库 SQL（{prod_rows} 行）</summary>\n\n```sql\n{prod_sql}\n```\n\n</details>"
            return ChatQueryResponse(
                answer=answer + sql_block,
                sources=sources,
                count=total_count,
                llm_used=True,
            )
        logger.warning("LLM call failed, returning degraded answer")

    # Degraded: no LLM — return what we have as text
    parts = []
    if doc_results:
        parts.append("**方案知识库：**\n" + "\n".join(f"- {s.title}" for s in sources[:8]))
    if prod_result:
        parts.append(f"**生产数据库（{prod_rows} 行）：**\n```json\n{prod_result[:1000]}\n```")
    return ChatQueryResponse(
        answer="\n\n".join(parts) or "（无数据）",
        sources=sources,
        count=total_count,
        llm_used=False,
    )
