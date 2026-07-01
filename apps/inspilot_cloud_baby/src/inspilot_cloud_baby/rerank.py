"""Rerank service — cross-encoder reranking via an OpenAI-compatible /rerank endpoint.

Mirrors embedding.py: lazy singleton, env config, graceful degradation. Works with
Jina / Cohere / SiliconFlow style `/rerank` APIs that accept
{model, query, documents[, top_n]} and return {results: [{index, relevance_score}]}.

Returns None on any failure so callers fall back to the original ordering.
"""
from __future__ import annotations

import logging

import httpx

from inspilot_cloud_baby.config import settings

logger = logging.getLogger(__name__)


class RerankService:
    """Thin client for an OpenAI-compatible rerank endpoint."""

    def __init__(self, *, api_key: str, base_url: str, model: str, enabled: bool = True) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._enabled = enabled and bool(api_key) and bool(base_url) and bool(model)

    @property
    def available(self) -> bool:
        return self._enabled

    def rerank(self, query: str, documents: list[str], *, top_n: int | None = None) -> list[tuple[int, float]] | None:
        """Return [(original_index, relevance_score), ...] sorted desc, or None on failure."""
        if not self.available or not documents:
            return None
        payload: dict = {"model": self._model, "query": query, "documents": documents}
        if top_n:
            payload["top_n"] = top_n
        url = f"{self._base_url}/rerank"
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        for attempt in range(3):
            try:
                resp = httpx.post(url, json=payload, headers=headers, timeout=15.0)
                resp.raise_for_status()
                results = resp.json().get("results", [])
                ranked = [
                    (r["index"], float(r.get("relevance_score", 0.0)))
                    for r in results
                    if isinstance(r.get("index"), int)
                ]
                ranked.sort(key=lambda x: x[1], reverse=True)
                return ranked
            except Exception as exc:  # noqa: BLE001
                logger.warning("Rerank attempt %d/3 failed: %s", attempt + 1, exc)
        logger.error("Rerank failed after 3 attempts")
        return None


_service: RerankService | None = None


def get_rerank_service() -> RerankService:
    """Lazy singleton — reset _service to None to force reload after config change."""
    global _service  # noqa: PLW0603
    if _service is None:
        _service = RerankService(
            api_key=settings.rerank_api_key,
            base_url=settings.rerank_base_url,
            model=settings.rerank_model,
            enabled=settings.enable_rerank,
        )
    return _service
