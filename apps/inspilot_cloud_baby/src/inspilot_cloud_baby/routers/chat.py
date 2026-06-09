from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatQueryRequest(BaseModel):
    query: str


class ChatQueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    return ChatQueryResponse(
        answer=f"Alpha 已收到问题：{request.query}。知识库接入后将返回带来源的回答。",
        sources=[],
    )
