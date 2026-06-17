"""Knowledge retrieval — vector search with keyword fallback."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import String, func, select

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
    # Optional provenance for richer display (populated for DB-backed results)
    source_type: str = ""
    metadata: dict = field(default_factory=dict)


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
    filters: dict | None = None,
) -> list[KnowledgeDocument]:
    """Retrieve relevant knowledge documents.

    Strategy (degradation chain):
      1. If *db* is provided and the embedding service is available → vector search.
      2. On failure / no results → fall back to keyword search over *documents*.

    *filters* optionally constrains results by metadata (region/insurer/integrator).
    When None, region/insurer/integrator are auto-extracted from *query* text.
    """
    # Auto-extract intent filters from the query text if none were supplied
    if filters is None and db is not None:
        filters = _extract_query_filters(query=query, db=db)

    # --- try vector search first ---
    if db is not None:
        try:
            vector_results = _retrieve_by_vector(
                query=query, user=user, db=db, limit=limit, filters=filters
            )
            if vector_results:
                return vector_results
        except Exception:
            logger.warning("Vector search failed, falling back to keyword search", exc_info=True)

    # --- keyword fallback (original logic) ---
    return _retrieve_by_keyword(query=query, user=user, documents=documents, limit=limit)


# ---------------------------------------------------------------------------
# Query intent extraction — auto-detect region/insurer/integrator in query text
# ---------------------------------------------------------------------------

# Insurer / integrator dictionaries (kept in sync with import_cs3_plans.py)
_INSURERS = [
    "人保", "国寿财", "中华联", "平安", "太平洋", "太保", "阳光",
    "华泰", "安诚", "浙商", "中银", "永安", "紫金", "大家",
]
_INTEGRATORS = [
    "新点", "筑龙", "品茗", "广联达", "政采云", "文锐", "数科", "杰软",
    "杰瑞", "中招", "建网", "移动", "迅捷", "金控", "乐彩云",
]


def _load_known_regions(db: Session) -> list[str]:
    """Return distinct region values from cs3_plan metadata, longest first."""
    try:
        rows = db.execute(
            select(func.distinct(KnowledgeItem.metadata_json["region"]))
            .where(KnowledgeItem.source_type == "cs3_plan")
        ).scalars().all()
        return sorted([r for r in rows if r], key=len, reverse=True)
    except Exception:
        logger.debug("Failed to load known regions", exc_info=True)
        return []


def _extract_query_filters(*, query: str, db: Session) -> dict:
    """Detect region/insurer/integrator intent in a natural-language query.

    Region matching uses the DB's known region values (substring match), so
    "青岛的方案" matches region "青岛". Insurer/integrator use fixed dictionaries.
    Returns a dict like {"region": "青岛", "insurer": "人保"} (only keys that match).
    """
    filters: dict[str, str] = {}

    # Insurer (substring against dictionary)
    for ins in _INSURERS:
        if ins in query:
            filters["insurer"] = ins
            break

    # Integrator (substring against dictionary)
    for integ in _INTEGRATORS:
        if integ in query:
            filters["integrator"] = integ
            break

    # Region (substring against known DB values, longest-first to avoid
    # e.g. "杭州" matching when "杭州市" is the stored value)
    for region in _load_known_regions(db):
        if region and region in query:
            filters["region"] = region
            break

    return filters


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


def _metadata_filter_clauses(filters: dict) -> list:
    """Build SQLAlchemy where-clauses for metadata_json filters (region/insurer/integrator)."""
    clauses = []
    for key in ("region", "insurer", "integrator"):
        val = filters.get(key)
        if val:
            # metadata_json ->> 'key' = 'value'  (JSONB text extraction)
            clauses.append(func.cast(KnowledgeItem.metadata_json.op("->>")(key), String) == val)
    return clauses


def _retrieve_by_vector(
    *,
    query: str,
    user: CurrentUser,
    db: Session,
    limit: int,
    filters: dict | None = None,
) -> list[KnowledgeDocument]:
    from inspilot_cloud_baby.embedding import get_embedding_service  # avoid circular import at module level

    svc = get_embedding_service()
    if not svc.available:
        return []

    query_vec = svc.embed_query(query)
    if query_vec is None:
        return []

    filter_clauses = _metadata_filter_clauses(filters or {})

    def _run(clauses: list) -> list[KnowledgeDocument]:
        stmt = (
            select(KnowledgeItem, Project.visibility)
            .join(Project, KnowledgeItem.project_id == Project.id, isouter=True)
            .where(KnowledgeItem.embedding.isnot(None))
            .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
        )
        for clause in clauses:
            stmt = stmt.where(clause)
        stmt = stmt.order_by(KnowledgeItem.embedding.cosine_distance(query_vec)).limit(limit * 3)

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
                source_type=item.source_type or "",
                metadata=item.metadata_json or {},
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

    # First pass: with filters (auto-extracted or manual)
    if filter_clauses:
        results = _run(filter_clauses)
        if results:
            return results
        # Fallback: filters too strict (e.g. region typo) → relax and re-search
        logger.info("Filtered vector search returned nothing; relaxing filters %s", filters)
        return _run([])

    return _run([])
