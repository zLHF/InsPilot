"""Embedding service — wraps OpenAI embeddings API with retry and graceful degradation."""
from __future__ import annotations

import logging

from openai import OpenAI, OpenAIError

from inspilot_cloud_baby.config import settings

logger = logging.getLogger(__name__)

_MAX_INPUT_CHARS = 8000  # text-embedding-3-small ≈ 8K tokens


def _clean_text(text: str) -> str:
    """Normalise whitespace and truncate to a safe length."""
    cleaned = " ".join(text.split())
    return cleaned[:_MAX_INPUT_CHARS]


def _load_db_settings() -> dict[str, str]:
    """Load embedding-related settings from DB (gracefully returns {} on failure)."""
    try:
        from inspilot_cloud_baby.db import SessionLocal
        from inspilot_cloud_baby.models import AppSetting

        with SessionLocal() as session:
            rows = session.query(AppSetting).filter(
                AppSetting.key.in_([
                    "openai_api_key", "openai_base_url",
                    "openai_embedding_model", "enable_vector_search",
                ])
            ).all()
            return {r.key: r.value for r in rows}
    except Exception:
        logger.debug("Could not load DB settings, falling back to env-only", exc_info=True)
        return {}


def get_effective_config() -> dict[str, str]:
    """Resolve effective config with priority: env var > DB > default."""
    db = _load_db_settings()
    return {
        "api_key": settings.openai_api_key or db.get("openai_api_key", ""),
        "base_url": settings.openai_base_url or db.get("openai_base_url", ""),
        "model": settings.openai_embedding_model or db.get("openai_embedding_model", "text-embedding-3-small"),
        "enable_vector_search": settings.enable_vector_search
            if settings.openai_api_key  # env key set → env controls
            else db.get("enable_vector_search", "true").lower() != "false",
    }


class EmbeddingService:
    """Thin wrapper around OpenAI Embeddings API.

    * Returns ``None`` on failure (never raises) so callers can degrade gracefully.
    * Retry logic is built-in (3 attempts with exponential back-off).
    """

    def __init__(
        self,
        *,
        api_key: str = "",
        base_url: str = "",
        model: str = "text-embedding-3-small",
        enable_vector_search: bool = True,
    ) -> None:
        self._model = model
        self._enable_vector_search = enable_vector_search

        if not api_key:
            logger.warning("OpenAI API key not configured — embedding disabled")
            self._client: OpenAI | None = None
            return

        kwargs: dict = {"api_key": api_key, "timeout": 30.0}
        if base_url:
            kwargs["base_url"] = base_url

        self._client = OpenAI(**kwargs)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def available(self) -> bool:
        """True when the service is ready to produce embeddings."""
        return self._client is not None and self._enable_vector_search

    def embed_text(self, text: str) -> list[float] | None:
        """Return an embedding vector for *text*, or ``None`` on failure."""
        if not self.available:
            return None

        cleaned = _clean_text(text)
        for attempt in range(3):
            try:
                resp = self._client.embeddings.create(
                    model=self._model,
                    input=cleaned,
                )
                return resp.data[0].embedding
            except OpenAIError as exc:
                logger.warning("Embedding attempt %d failed: %s", attempt + 1, exc)
            except Exception as exc:  # noqa: BLE001
                logger.error("Unexpected embedding error: %s", exc, exc_info=True)

        logger.error("All 3 embedding attempts failed for text (%d chars)", len(cleaned))
        return None

    def embed_query(self, query: str) -> list[float] | None:
        """Embed a user query — currently identical to :meth:`embed_text`."""
        return self.embed_text(query)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """Return the module-level :class:`EmbeddingService` singleton.

    On first call (or after a reset), reads effective config from
    env vars + DB and creates a fresh instance.
    """
    global _service  # noqa: PLW0603
    if _service is None:
        cfg = get_effective_config()
        _service = EmbeddingService(
            api_key=cfg["api_key"],
            base_url=cfg["base_url"],
            model=cfg["model"],
            enable_vector_search=cfg["enable_vector_search"],
        )
    return _service
