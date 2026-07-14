from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True)
class RetrievalCandidate:
    document: Any
    matched_fields: tuple[str, ...] = ()
    keyword_score: int = 0
    keyword_rank: int | None = None
    vector_distance: float | None = None
    vector_rank: int | None = None
    vector_status: str = "available"


@dataclass(frozen=True)
class RetrievalEvidence:
    channels: tuple[str, ...]
    matched_fields: tuple[str, ...] = ()
    keyword_score: int = 0
    keyword_rank: int | None = None
    vector_distance: float | None = None
    vector_rank: int | None = None
    final_rank: int = 0
    vector_status: str = "available"


@dataclass(frozen=True)
class ExplainedDocument:
    document: Any
    evidence: RetrievalEvidence


def _merge_candidate(
    keyword: RetrievalCandidate | None,
    vector: RetrievalCandidate | None,
) -> RetrievalCandidate:
    base = keyword or vector
    if base is None:
        raise ValueError("at least one candidate is required")
    return replace(
        base,
        vector_distance=vector.vector_distance if vector else None,
        vector_rank=vector.vector_rank if vector else None,
        vector_status=vector.vector_status if vector else base.vector_status,
    )


def _sort_key(candidate: RetrievalCandidate) -> tuple:
    return (
        0 if candidate.keyword_rank is not None else 1,
        -candidate.keyword_score,
        -int("title" in candidate.matched_fields),
        -int("metadata" in candidate.matched_fields),
        -int("body" in candidate.matched_fields),
        -int(candidate.keyword_rank is not None and candidate.vector_rank is not None),
        candidate.keyword_rank or 10**9,
        candidate.vector_rank or 10**9,
        candidate.document.id,
    )


def fuse_candidates(
    *,
    keyword: list[RetrievalCandidate],
    vector: list[RetrievalCandidate],
    limit: int,
) -> list[ExplainedDocument]:
    keyword_by_id = {candidate.document.id: candidate for candidate in keyword}
    vector_by_id = {candidate.document.id: candidate for candidate in vector}
    ids = keyword_by_id.keys() | vector_by_id.keys()
    merged = [
        _merge_candidate(keyword_by_id.get(document_id), vector_by_id.get(document_id))
        for document_id in ids
    ]
    merged.sort(key=_sort_key)

    explained: list[ExplainedDocument] = []
    for final_rank, candidate in enumerate(merged[:limit], 1):
        channels = tuple(
            channel
            for channel, rank in (
                ("keyword", candidate.keyword_rank),
                ("vector", candidate.vector_rank),
            )
            if rank is not None
        )
        explained.append(
            ExplainedDocument(
                document=candidate.document,
                evidence=RetrievalEvidence(
                    channels=channels,
                    matched_fields=candidate.matched_fields,
                    keyword_score=candidate.keyword_score,
                    keyword_rank=candidate.keyword_rank,
                    vector_distance=candidate.vector_distance,
                    vector_rank=candidate.vector_rank,
                    final_rank=final_rank,
                    vector_status=candidate.vector_status,
                ),
            )
        )
    return explained
