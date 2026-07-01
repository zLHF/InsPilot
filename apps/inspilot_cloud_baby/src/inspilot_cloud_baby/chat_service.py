"""Chat / LLM service — OpenAI-compatible chat completions for RAG answers.

Mirrors embedding.py: lazy singleton, env>DB config merge, 3-retry, graceful
disable when unconfigured. Uses the openai SDK (works with OpenRouter and any
OpenAI-compatible endpoint via base_url).
"""
from __future__ import annotations

import logging
from collections.abc import Iterator

from openai import OpenAI, OpenAIError

from inspilot_cloud_baby.config import settings

logger = logging.getLogger(__name__)


def _load_db_settings() -> dict[str, str]:
    """Load chat config from the app_settings table."""
    try:
        from inspilot_cloud_baby.db import SessionLocal
        from inspilot_cloud_baby.models import AppSetting

        with SessionLocal() as session:
            rows = session.query(AppSetting).filter(
                AppSetting.key.in_(["chat_api_key", "chat_base_url", "chat_model"])
            ).all()
            return {r.key: r.value for r in rows}
    except Exception:
        logger.debug("Failed to load chat settings from DB", exc_info=True)
        return {}


def get_chat_config() -> dict[str, str]:
    """Merge env > DB > default for chat model config."""
    db = _load_db_settings()
    return {
        "api_key": settings.chat_api_key or db.get("chat_api_key", ""),
        "base_url": settings.chat_base_url or db.get("chat_base_url", ""),
        "model": settings.chat_model or db.get("chat_model", ""),
    }


class ChatService:
    """OpenAI-compatible chat completion client (OpenRouter / OpenAI / compatible)."""

    def __init__(self, *, api_key: str, base_url: str, model: str) -> None:
        self._model = model
        if not api_key:
            logger.warning("ChatService created without api_key — LLM disabled")
            self._client = None
            return
        kwargs: dict = {"api_key": api_key, "timeout": 60.0}
        if base_url:
            kwargs["base_url"] = base_url
        self._client = OpenAI(**kwargs)

    @property
    def available(self) -> bool:
        return self._client is not None and bool(self._model)

    def chat(self, messages: list[dict], *, temperature: float = 0.3) -> str | None:
        """Send messages and return the assistant reply text, or None on failure."""
        if not self.available:
            return None
        for attempt in range(3):
            try:
                resp = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=temperature,
                )
                return resp.choices[0].message.content
            except OpenAIError as exc:
                logger.warning("Chat API error (attempt %d/3): %s", attempt + 1, exc)
            except Exception:
                logger.error("Chat unexpected error (attempt %d/3)", attempt + 1, exc_info=True)
        logger.error("Chat failed after 3 attempts")
        return None

    def chat_stream(self, messages: list[dict], *, temperature: float = 0.3) -> Iterator[str]:
        """Yield assistant reply text incrementally (token deltas).

        Unlike `chat()`, streaming cannot be retried mid-flight (partial tokens
        already emitted), so on error it simply stops yielding. Callers should
        treat an empty stream as failure and fall back accordingly.
        """
        if not self.available:
            return
        try:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except OpenAIError as exc:
            logger.warning("Chat stream API error: %s", exc)
        except Exception:
            logger.error("Chat stream unexpected error", exc_info=True)


_service: ChatService | None = None


def get_chat_service() -> ChatService:
    """Lazy singleton — reset _service to None to force reload after config change."""
    global _service
    if _service is None:
        cfg = get_chat_config()
        _service = ChatService(
            api_key=cfg["api_key"],
            base_url=cfg["base_url"],
            model=cfg["model"],
        )
    return _service
