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

# Max chars of each retrieved plan fed to the LLM (keeps prompt bounded)
_CONTEXT_MAX_CHARS = 1500


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


_SYSTEM_PROMPT = (
    "你是 InsPilot 云小宝的知识助手，专门帮助保险业务人员解答方案相关问题。\n"
    "请基于下面提供的知识库内容回答用户问题。要求：\n"
    "1. 回答要准确、具体，直接引用知识库中的关键信息。\n"
    "2. 如果涉及多个方案，用列表或对比表格清晰呈现。\n"
    "3. 如果知识库中没有相关信息，如实说明'知识库中暂无相关内容'，不要编造。\n"
    "4. 回答用中文，使用 Markdown 格式（标题、列表、表格等）。"
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

    db: Session = SessionLocal()
    try:
        results = retrieve_documents(
            query=request.query,
            user=_DEFAULT_USER,
            documents=[],
            limit=8,
            db=db,
            filters=manual_filters,
        )
    finally:
        db.close()

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
        for doc in results
    ]

    if not results:
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的知识条目。换个关键词或去掉筛选条件试试？",
            sources=[],
            count=0,
            llm_used=False,
        )

    # --- RAG: ask the LLM to answer based on retrieved context ---
    chat_svc = get_chat_service()
    if chat_svc.available:
        context = _build_context(results)
        messages: list[dict] = [
            {"role": "system", "content": _SYSTEM_PROMPT + "\n\n## 知识库内容\n\n" + context},
        ]
        # Carry prior turns (cap at last 6 messages to bound tokens)
        for msg in request.history[-6:]:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": request.query})

        answer = chat_svc.chat(messages)
        if answer:
            return ChatQueryResponse(answer=answer, sources=sources, count=len(results), llm_used=True)
        # LLM call failed → fall through to degraded answer
        logger.warning("LLM call failed, returning degraded answer")

    # Degraded: no LLM configured or call failed
    titles = "\n".join(f"- {s.title}" for s in sources[:8])
    return ChatQueryResponse(
        answer=f"找到 {len(results)} 条相关知识（对话模型未配置或调用失败，仅返回标题列表）：\n\n{titles}",
        sources=sources,
        count=len(results),
        llm_used=False,
    )
