from __future__ import annotations

import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.chat_service import get_chat_service
from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.models import QueryLog
from inspilot_cloud_baby.retrieval import retrieve_documents_explained

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
    recall_channels: list[str] = Field(default_factory=list)
    matched_fields: list[str] = Field(default_factory=list)
    keyword_rank: int | None = None
    vector_rank: int | None = None
    final_rank: int


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
        results = retrieve_documents_explained(
            query=query, user=_DEFAULT_USER, documents=[], limit=8, db=db, filters=filters,
        )
    finally:
        db.close()
    if not results:
        return [], ""
    parts = []
    for i, explained in enumerate(results, 1):
        doc = explained.document
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
# Prod-DB gate — cheap heuristic pre-filter (NOT semantic routing)
# ---------------------------------------------------------------------------
# 这不是"语义路由"：LLM 仍对如何使用拿到的数据有完全自主权。这里只做一层廉价
# 预过滤——当问题明显与实时数据无关时（纯方案知识库问题），跳过昂贵的 SQL 生成
# LLM 调用 + SQL Server 往返，避免白等。可用 settings.enable_prod_db_gate 关闭，
# 恢复"双通道无脑全跑"的原始行为。
# 注意：避免方案知识库里的高频术语（如"出单"——见费出单/独立出单/出单模式），
# 否则纯知识库问题会被误判为需要实时数据。只保留指向实时查询的明确信号。
_PROD_DB_SIGNALS = (
    "订单", "保单号", "费率", "保费", "缴费", "支付", "金额", "余额",
    "实时", "最新", "当前", "目前", "进度", "今天", "今日", "本月",
    "多少笔", "多少单", "多少钱", "统计", "排名", "排行",
)
_ORDER_NUM_RE = re.compile(r"\d{8,}")


def _needs_prod_db(query: str) -> bool:
    """是否触发生产库通道。门控关闭时恒为 True（恢复双通道全跑）。"""
    if not settings.enable_prod_db_gate:
        return True
    return bool(_ORDER_NUM_RE.search(query)) or any(s in query for s in _PROD_DB_SIGNALS)


# ---------------------------------------------------------------------------
# Channel orchestration + synthesis helpers (shared by /query and /stream)
# ---------------------------------------------------------------------------


def _gather_channels(query: str, manual_filters: dict | None):
    """并行拉取 doc KB 与（按需触发的）prod DB 两个数据通道。

    返回 (doc_results, doc_context, prod_sql, prod_result, prod_rows)。
    两通道互不依赖，并行后总延迟 ≈ max(两者) 而非 sum。
    """
    run_db = _needs_prod_db(query)
    with ThreadPoolExecutor(max_workers=2) as pool:
        doc_future = pool.submit(_fetch_doc_kb, query, manual_filters)
        prod_future = pool.submit(_fetch_prod_db, query) if run_db else None
        doc_results, doc_context = doc_future.result()
        prod_sql, prod_result, prod_rows = (
            prod_future.result() if prod_future else ("", "", 0)
        )
    return doc_results, doc_context, prod_sql, prod_result, prod_rows


def _parse_manual_filters(request: ChatQueryRequest) -> dict | None:
    manual = {
        "region": request.region.strip(),
        "insurer": request.insurer.strip(),
        "integrator": request.integrator.strip(),
    }
    if any(manual.values()):
        return {k: v for k, v in manual.items() if v}
    return None


def _build_sources(doc_results: list) -> list[SourceItem]:
    return [
        SourceItem(
            id=item.document.id,
            title=item.document.title,
            source_type=item.document.source_type,
            region=item.document.metadata.get("region", ""),
            insurer=item.document.metadata.get("insurer", ""),
            integrator=item.document.metadata.get("integrator", ""),
            doc_date=item.document.metadata.get("doc_date", ""),
            recall_channels=list(item.evidence.channels),
            matched_fields=list(item.evidence.matched_fields),
            keyword_rank=item.evidence.keyword_rank,
            vector_rank=item.evidence.vector_rank,
            final_rank=item.evidence.final_rank,
        )
        for item in doc_results
    ]


def _build_synthesis_messages(query, history, doc_results, doc_context, prod_result, prod_rows) -> list[dict]:
    """构建喂给综合 LLM 的 messages（master prompt + 两通道数据 + 多轮历史）。"""
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
    for msg in history[-6:]:
        if msg.role in ("user", "assistant"):
            messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": query})
    return messages


def _sql_details_block(prod_sql: str, prod_rows: int) -> str:
    if not prod_sql:
        return ""
    return (
        f"\n\n<details><summary>📄 生产库 SQL（{prod_rows} 行）</summary>\n\n"
        f"```sql\n{prod_sql}\n```\n\n</details>"
    )


def _degraded_answer(doc_results, sources, prod_result, prod_rows) -> str:
    parts = []
    if doc_results:
        parts.append("**方案知识库：**\n" + "\n".join(f"- {s.title}" for s in sources[:8]))
    if prod_result:
        parts.append(f"**生产数据库（{prod_rows} 行）：**\n```json\n{prod_result[:1000]}\n```")
    return "\n\n".join(parts) or "（无数据）"


def _log_query(query, user_id, doc_results, prod_rows, llm_used, latency_ms) -> None:
    """Persist one retrieval turn to query_logs (best-effort; never breaks the request).

    Zero-result rows are the gold mine: queries users searched but we couldn't answer.
    """
    try:
        db = SessionLocal()
        try:
            db.add(QueryLog(
                query=query[:2000],
                user_id=user_id,
                doc_ids=[d.document.id for d in doc_results],
                doc_count=len(doc_results),
                prod_rows=prod_rows,
                llm_used=llm_used,
                zero_result=(not doc_results and prod_rows == 0),
                latency_ms=latency_ms,
            ))
            db.commit()
        finally:
            db.close()
    except Exception:
        logger.debug("Failed to write query log", exc_info=True)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    """Non-streaming endpoint (kept for compatibility). Streaming lives at /stream."""
    start = time.monotonic()
    manual_filters = _parse_manual_filters(request)
    doc_results, doc_context, prod_sql, prod_result, prod_rows = _gather_channels(
        request.query, manual_filters
    )
    sources = _build_sources(doc_results)
    total_count = len(doc_results) + prod_rows

    def _finish(answer: str, llm_used: bool) -> ChatQueryResponse:
        _log_query(request.query, "alpha", doc_results, prod_rows, llm_used,
                   int((time.monotonic() - start) * 1000))
        return ChatQueryResponse(answer=answer, sources=sources, count=total_count, llm_used=llm_used)

    if not doc_results and prod_rows == 0:
        _log_query(request.query, "alpha", doc_results, prod_rows, False,
                   int((time.monotonic() - start) * 1000))
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的信息（方案知识库和生产数据库均无匹配）。",
            sources=[], count=0, llm_used=False,
        )

    chat_svc = get_chat_service()
    if chat_svc.available:
        messages = _build_synthesis_messages(
            request.query, request.history, doc_results, doc_context, prod_result, prod_rows
        )
        answer = chat_svc.chat(messages)
        if answer:
            return _finish(answer + _sql_details_block(prod_sql, prod_rows), True)
        logger.warning("LLM call failed, returning degraded answer")

    return _finish(_degraded_answer(doc_results, sources, prod_result, prod_rows), False)


def _sse(event: str, data: dict) -> str:
    """Format a Server-Sent Event. JSON-encode data so embedded newlines are safe."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/stream")
def stream_chat(request: ChatQueryRequest) -> StreamingResponse:
    """Streaming version of /query. Pushes sources first, then answer token-by-token.

    SSE events:
      sources {sources:[...], count:N}   — emitted once, before the answer
      token   {t:"..."}                  — incremental answer deltas
      done    {count:N, llm_used:bool}   — terminal
    """

    def gen():
        start = time.monotonic()
        manual_filters = _parse_manual_filters(request)
        doc_results, doc_context, prod_sql, prod_result, prod_rows = _gather_channels(
            request.query, manual_filters
        )
        sources = _build_sources(doc_results)
        total_count = len(doc_results) + prod_rows
        llm_used = False

        try:
            yield _sse("sources", {"sources": [s.model_dump() for s in sources], "count": total_count})

            if not doc_results and prod_rows == 0:
                yield _sse("token", {"t": f"未找到与「{request.query}」相关的信息（方案知识库和生产数据库均无匹配）。"})
                yield _sse("done", {"count": 0, "llm_used": False})
                return

            chat_svc = get_chat_service()
            if chat_svc.available:
                messages = _build_synthesis_messages(
                    request.query, request.history, doc_results, doc_context, prod_result, prod_rows
                )
                got_any = False
                for delta in chat_svc.chat_stream(messages):
                    got_any = True
                    yield _sse("token", {"t": delta})
                if got_any:
                    llm_used = True
                    block = _sql_details_block(prod_sql, prod_rows)
                    if block:
                        yield _sse("token", {"t": block})
                    yield _sse("done", {"count": total_count, "llm_used": True})
                    return
                logger.warning("LLM stream produced nothing, falling back to degraded answer")

            # Degraded (no LLM configured / stream failed before any token)
            yield _sse("token", {"t": _degraded_answer(doc_results, sources, prod_result, prod_rows)})
            yield _sse("done", {"count": total_count, "llm_used": False})
        finally:
            _log_query(request.query, "alpha", doc_results, prod_rows, llm_used,
                       int((time.monotonic() - start) * 1000))

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )
