"""Knowledge retrieval — vector search with keyword fallback."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import (
    KnowledgeItem,
    KnowledgeSensitivity,
    KnowledgeStatus,
    Project,
    ProjectVisibility,
)
from inspilot_cloud_baby.permissions import can_read_knowledge

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class KnowledgeDocument:
    id: str
    project_id: str | None
    project_visibility: ProjectVisibility | None
    sensitivity: KnowledgeSensitivity
    title: str
    body: str


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def retrieve_documents(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int = 5,
    db: Session | None = None,
) -> list[KnowledgeDocument]:
    """Retrieve relevant knowledge documents.

    Strategy (degradation chain):
      1. If *db* is provided and the embedding service is available → vector search.
      2. On failure / no results → fall back to keyword search over *documents*.
    """
    # --- try vector search first ---
    if db is not None:
        try:
            vector_results = _retrieve_by_vector(query=query, user=user, db=db, limit=limit)
            if vector_results:
                return vector_results
        except Exception:
            logger.warning("Vector search failed, falling back to keyword search", exc_info=True)

    # --- keyword fallback (original logic) ---
    return _retrieve_by_keyword(query=query, user=user, documents=documents, limit=limit)


# ---------------------------------------------------------------------------
# Keyword search (unchanged from original)
# ---------------------------------------------------------------------------


def _retrieve_by_keyword(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int,
) -> list[KnowledgeDocument]:
    terms = [term for term in query.lower().split() if term]
    visible_docs = [
        document
        for document in documents
        if can_read_knowledge(
            user=user,
            project_id=document.project_id,
            project_visibility=document.project_visibility,
            sensitivity=document.sensitivity,
        )
    ]
    scored = sorted(
        visible_docs,
        key=lambda document: _score(document=document, terms=terms),
        reverse=True,
    )
    return scored[:limit]


def _score(*, document: KnowledgeDocument, terms: list[str]) -> int:
    text = f"{document.title} {document.body}".lower()
    return sum(1 for term in terms if term in text)


# ---------------------------------------------------------------------------
# Vector search via pgvector
# ---------------------------------------------------------------------------


def _retrieve_by_vector(
    *,
    query: str,
    user: CurrentUser,
    db: Session,
    limit: int,
) -> list[KnowledgeDocument]:
    from inspilot_cloud_baby.embedding import get_embedding_service  # avoid circular import at module level

    svc = get_embedding_service()
    if not svc.available:
        return []

    query_vec = svc.embed_query(query)
    if query_vec is None:
        return []

    # Build ORM query: cosine-distance ordering, fetch extra rows for permission filtering
    stmt = (
        select(KnowledgeItem, Project.visibility)
        .join(Project, KnowledgeItem.project_id == Project.id, isouter=True)
        .where(KnowledgeItem.embedding.isnot(None))
        .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
        .order_by(KnowledgeItem.embedding.cosine_distance(query_vec))
        .limit(limit * 3)
    )

    rows = db.execute(stmt).all()

    documents: list[KnowledgeDocument] = []
    for item, visibility in rows:
        doc = KnowledgeDocument(
            id=str(item.id),
            project_id=str(item.project_id) if item.project_id else None,
            project_visibility=visibility,
            sensitivity=item.sensitivity,
            title=item.title,
            body=item.body,
        )
        if can_read_knowledge(
            user=user,
            project_id=doc.project_id,
            project_visibility=doc.project_visibility,
            sensitivity=doc.sensitivity,
        ):
            documents.append(doc)
        if len(documents) >= limit:
            break

    return documents
