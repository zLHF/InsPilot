from __future__ import annotations

import logging

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.retrieval import retrieve_documents

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Alpha default user — replace with real auth when available
_DEFAULT_USER = CurrentUser(user_id="alpha", is_company_user=True, project_ids=set())


class ChatQueryRequest(BaseModel):
    query: str


class SourceItem(BaseModel):
    """One retrieved knowledge source shown to the user."""

    id: str
    title: str
    source_type: str = ""
    region: str = ""
    insurer: str = ""
    integrator: str = ""
    doc_date: str = ""
    preview: str = ""


class ChatQueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    count: int = 0


def _preview(body: str, query: str, width: int = 240) -> str:
    """Return a snippet of *body* around the first query-term match, else the head."""
    if not body:
        return ""
    text = " ".join(body.split())
    idx = -1
    for term in query.split():
        pos = text.find(term)
        if pos >= 0:
            idx = pos
            break
    if idx < 0:
        return text[:width]
    start = max(0, idx - 40)
    snippet = text[start : start + width]
    return ("…" if start > 0 else "") + snippet + ("…" if start + width < len(text) else "")


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    db: Session = SessionLocal()
    try:
        results = retrieve_documents(
            query=request.query,
            user=_DEFAULT_USER,
            documents=[],  # vector search queries DB directly
            limit=8,
            db=db,
        )
    finally:
        db.close()

    if not results:
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的知识条目。",
            sources=[],
            count=0,
        )

    sources = [
        SourceItem(
            id=doc.id,
            title=doc.title,
            source_type=doc.source_type,
            region=doc.metadata.get("region", ""),
            insurer=doc.metadata.get("insurer", ""),
            integrator=doc.metadata.get("integrator", ""),
            doc_date=doc.metadata.get("doc_date", ""),
            preview=_preview(doc.body, request.query),
        )
        for doc in results
    ]
    return ChatQueryResponse(
        answer=f"找到 {len(results)} 条相关知识",
        sources=sources,
        count=len(results),
    )
