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


class ChatQueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    db: Session = SessionLocal()
    try:
        results = retrieve_documents(
            query=request.query,
            user=_DEFAULT_USER,
            documents=[],  # vector search queries DB directly
            limit=5,
            db=db,
        )
    finally:
        db.close()

    if not results:
        return ChatQueryResponse(
            answer=f"未找到与「{request.query}」相关的知识条目。",
            sources=[],
        )

    sources = [doc.title for doc in results]
    preview = results[0].body[:200]
    return ChatQueryResponse(
        answer=f"找到 {len(results)} 条相关知识：\n{preview}",
        sources=sources,
    )
