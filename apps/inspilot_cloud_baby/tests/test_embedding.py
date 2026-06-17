"""Tests for the embedding service."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.embedding import EmbeddingService, get_embedding_service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_service(**overrides):
    """Create an EmbeddingService with sensible test defaults."""
    defaults = {
        "api_key": "sk-test",
        "base_url": "",
        "model": "text-embedding-3-small",
        "enable_vector_search": True,
    }
    defaults.update(overrides)
    return EmbeddingService(**defaults)


# ---------------------------------------------------------------------------
# EmbeddingService tests
# ---------------------------------------------------------------------------


class TestEmbeddingServiceAvailability:
    def test_unavailable_when_no_api_key(self):
        service = _make_service(api_key="")
        assert not service.available

    def test_unavailable_when_disabled(self):
        service = _make_service(enable_vector_search=False)
        assert not service.available

    @patch("inspilot_cloud_baby.embedding.OpenAI")
    def test_available_when_configured(self, mock_openai_cls):
        service = _make_service()
        assert service.available


class TestEmbeddingServiceEmbedText:
    @patch("inspilot_cloud_baby.embedding.OpenAI")
    def test_embed_text_returns_vector(self, mock_openai_cls):
        fake_embedding = [0.1] * 1536
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=fake_embedding)]
        mock_openai_cls.return_value.embeddings.create.return_value = mock_response

        service = _make_service()
        result = service.embed_text("测试文本")
        assert result == fake_embedding

    @patch("inspilot_cloud_baby.embedding.OpenAI")
    def test_embed_text_returns_none_on_api_error(self, mock_openai_cls):
        mock_openai_cls.return_value.embeddings.create.side_effect = Exception("API error")

        service = _make_service()
        result = service.embed_text("测试文本")
        assert result is None

    def test_embed_text_returns_none_when_unavailable(self):
        service = _make_service(api_key="")
        assert service.embed_text("测试") is None

    @patch("inspilot_cloud_baby.embedding.OpenAI")
    def test_embed_text_truncates_long_input(self, mock_openai_cls):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.0] * 1536)]
        mock_openai_cls.return_value.embeddings.create.return_value = mock_response

        service = _make_service()
        long_text = "x" * 20_000
        service.embed_text(long_text)

        call_args = mock_openai_cls.return_value.embeddings.create.call_args
        assert len(call_args.kwargs["input"]) <= 8000

    @patch("inspilot_cloud_baby.embedding.OpenAI")
    def test_embed_query_delegates_to_embed_text(self, mock_openai_cls):
        fake_embedding = [0.5] * 1536
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=fake_embedding)]
        mock_openai_cls.return_value.embeddings.create.return_value = mock_response

        service = _make_service()
        result = service.embed_query("车险费率")
        assert result == fake_embedding


# ---------------------------------------------------------------------------
# Config resolution tests
# ---------------------------------------------------------------------------


class TestEffectiveConfig:
    @patch("inspilot_cloud_baby.embedding._load_db_settings", return_value={})
    def test_env_vars_take_priority(self, _mock_db):
        from inspilot_cloud_baby.embedding import get_effective_config
        with patch.object(settings, "openai_api_key", "sk-env"), \
             patch.object(settings, "openai_base_url", ""), \
             patch.object(settings, "openai_embedding_model", "text-embedding-3-small"):
            cfg = get_effective_config()
            assert cfg["api_key"] == "sk-env"

    @patch("inspilot_cloud_baby.embedding._load_db_settings", return_value={"openai_api_key": "sk-db"})
    def test_db_used_when_env_empty(self, _mock_db):
        from inspilot_cloud_baby.embedding import get_effective_config
        with patch.object(settings, "openai_api_key", ""), \
             patch.object(settings, "openai_base_url", ""), \
             patch.object(settings, "openai_embedding_model", ""):
            cfg = get_effective_config()
            assert cfg["api_key"] == "sk-db"


# ---------------------------------------------------------------------------
# Singleton tests
# ---------------------------------------------------------------------------


class TestGetEmbeddingService:
    def test_returns_same_instance(self):
        import inspilot_cloud_baby.embedding as mod
        mod._service = None

        with patch.object(settings, "openai_api_key", ""), \
             patch.object(settings, "enable_vector_search", True), \
             patch("inspilot_cloud_baby.embedding._load_db_settings", return_value={}):
            s1 = get_embedding_service()
            s2 = get_embedding_service()
            assert s1 is s2

        # Clean up
        mod._service = None
