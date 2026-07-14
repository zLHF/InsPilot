"""Tests for knowledge retrieval (keyword + vector fallback)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.retrieval import (
    KnowledgeDocument,
    _extract_query_filters,
    _query_terms,
    retrieve_documents,
    retrieve_documents_explained,
)
from inspilot_cloud_baby.retrieval_evidence import RetrievalCandidate, fuse_candidates


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def company_user() -> CurrentUser:
    return CurrentUser(user_id="u1", is_company_user=True, project_ids=set())


@pytest.fixture()
def project_member() -> CurrentUser:
    return CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})


@pytest.fixture()
def sample_docs() -> list[KnowledgeDocument]:
    return [
        KnowledgeDocument(
            id="k1",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
            title="华南车险项目背景",
            body="项目采用跳转模式，适合快速上线。",
        ),
        KnowledgeDocument(
            id="k2",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.SENSITIVE,
            title="华南车险项目费率",
            body="详细费率 2.5%。",
        ),
    ]


# ---------------------------------------------------------------------------
# Keyword search tests (original behaviour, preserved)
# ---------------------------------------------------------------------------


class TestKeywordRetrieval:
    def test_query_terms_segments_chinese_into_matchable_words(self):
        # jieba segments the phrase into independently-matchable words (old behavior
        # kept the whole sentence as one term, which an ilike almost never matched).
        terms = _query_terms("浙江华重融资担保")
        assert "浙江" in terms and "融资" in terms and "担保" in terms
        # Region word from a space-separated multi-entity query is still recovered.
        assert "西宁市" in _query_terms("西宁市 浙江华重融资担保")

    def test_query_filter_extraction_ignores_polluted_non_region_values(self):
        mock_db = MagicMock()
        with patch(
            "inspilot_cloud_baby.retrieval._load_known_regions",
            return_value=["山西省平台（PDF）顺欣担保", "担保", "详情页", "西宁市"],
        ):
            assert _extract_query_filters(query="浙江华重融资担保", db=mock_db) == {}
            assert _extract_query_filters(query="西宁市项目", db=mock_db) == {"region": "西宁市"}

    def test_filters_invisible_sensitive_documents(self, company_user, sample_docs):
        results = retrieve_documents(query="华南 车险 项目", user=company_user, documents=sample_docs)
        assert [doc.id for doc in results] == ["k1"]

    def test_scores_matching_documents_first(self, project_member):
        docs = [
            KnowledgeDocument(
                id="k1",
                project_id="p1",
                project_visibility=ProjectVisibility.PROJECT_MEMBERS,
                sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                title="系统问题",
                body="按钮不好找。",
            ),
            KnowledgeDocument(
                id="k2",
                project_id="p1",
                project_visibility=ProjectVisibility.PROJECT_MEMBERS,
                sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
                title="直连方案",
                body="直连 API 包含支付回调和出单回调。",
            ),
        ]

        results = retrieve_documents(query="直连 回调", user=project_member, documents=docs)
        assert [doc.id for doc in results] == ["k2", "k1"]

    def test_returns_empty_when_no_visible_docs(self, company_user):
        docs = [
            KnowledgeDocument(
                id="k1",
                project_id="p1",
                project_visibility=ProjectVisibility.PROJECT_MEMBERS,
                sensitivity=KnowledgeSensitivity.SENSITIVE,
                title="机密文档",
                body="不可见内容",
            ),
        ]
        results = retrieve_documents(query="机密", user=company_user, documents=docs)
        assert results == []

    def test_respects_limit(self, project_member):
        docs = [
            KnowledgeDocument(
                id=f"k{i}",
                project_id="p1",
                project_visibility=ProjectVisibility.COMPANY_VISIBLE,
                sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
                title="测试文档",
                body="内容",
            )
            for i in range(10)
        ]
        results = retrieve_documents(query="测试", user=project_member, documents=docs, limit=3)
        assert len(results) == 3


# ---------------------------------------------------------------------------
# Vector search fallback tests
# ---------------------------------------------------------------------------


class TestVectorFallback:
    def test_falls_back_to_keyword_when_no_db(self, company_user, sample_docs):
        """When db=None, vector search is skipped entirely → keyword results."""
        results = retrieve_documents(query="华南", user=company_user, documents=sample_docs, db=None)
        assert len(results) >= 1
        assert results[0].id == "k1"

    @patch("inspilot_cloud_baby.embedding.get_embedding_service")
    def test_falls_back_to_keyword_when_service_unavailable(self, mock_get_svc, company_user, sample_docs):
        """When the embedding service is unavailable, fall back to keyword search."""
        mock_svc = MagicMock()
        mock_svc.available = False
        mock_get_svc.return_value = mock_svc

        mock_db = MagicMock()
        results = retrieve_documents(query="华南", user=company_user, documents=sample_docs, db=mock_db)
        # Should still get keyword results
        assert len(results) >= 1

    @patch("inspilot_cloud_baby.embedding.get_embedding_service")
    def test_falls_back_to_keyword_on_vector_error(self, mock_get_svc, company_user, sample_docs):
        """When vector search raises, degrade gracefully to keyword search."""
        mock_svc = MagicMock()
        mock_svc.available = True
        mock_svc.embed_query.return_value = [0.1] * 1536
        mock_get_svc.return_value = mock_svc

        mock_db = MagicMock()
        mock_db.execute.side_effect = Exception("DB connection lost")

        results = retrieve_documents(query="华南", user=company_user, documents=sample_docs, db=mock_db)
        # Keyword fallback kicks in
        assert len(results) >= 1
        assert results[0].id == "k1"

    @patch("inspilot_cloud_baby.embedding.get_embedding_service")
    def test_falls_back_when_embedding_returns_none(self, mock_get_svc, company_user, sample_docs):
        """When embed_query returns None, fall back to keyword search."""
        mock_svc = MagicMock()
        mock_svc.available = True
        mock_svc.embed_query.return_value = None
        mock_get_svc.return_value = mock_svc

        mock_db = MagicMock()
        results = retrieve_documents(query="华南", user=company_user, documents=sample_docs, db=mock_db)
        assert len(results) >= 1


def _candidate(
    document: KnowledgeDocument,
    *,
    keyword_score: int = 0,
    keyword_rank: int | None = None,
    vector_distance: float | None = None,
    vector_rank: int | None = None,
    matched_fields: tuple[str, ...] = (),
) -> RetrievalCandidate:
    return RetrievalCandidate(
        document=document,
        keyword_score=keyword_score,
        keyword_rank=keyword_rank,
        vector_distance=vector_distance,
        vector_rank=vector_rank,
        matched_fields=matched_fields,
    )


class TestRetrievalEvidence:
    def test_keyword_candidate_ranks_before_closer_vector_only_candidate(self, sample_docs):
        fused = fuse_candidates(
            keyword=[
                _candidate(
                    sample_docs[0],
                    keyword_score=1,
                    keyword_rank=1,
                    matched_fields=("body",),
                )
            ],
            vector=[
                _candidate(
                    sample_docs[1],
                    vector_distance=0.01,
                    vector_rank=1,
                )
            ],
            limit=8,
        )

        assert [item.document.id for item in fused] == ["k1", "k2"]
        assert fused[0].evidence.channels == ("keyword",)
        assert fused[0].evidence.final_rank == 1

    def test_dual_channel_candidate_is_merged_and_explained(self, sample_docs):
        fused = fuse_candidates(
            keyword=[
                _candidate(
                    sample_docs[0],
                    keyword_score=1,
                    keyword_rank=1,
                    matched_fields=("title",),
                )
            ],
            vector=[
                _candidate(sample_docs[0], vector_distance=0.2, vector_rank=2)
            ],
            limit=8,
        )

        assert len(fused) == 1
        assert fused[0].evidence.channels == ("keyword", "vector")
        assert fused[0].evidence.vector_rank == 2
        assert fused[0].evidence.vector_distance == 0.2

    def test_explained_retrieval_attempts_vector_when_keyword_fills_limit(
        self, monkeypatch, company_user, sample_docs
    ):
        calls = {"vector": 0}
        keyword = [_candidate(sample_docs[0], keyword_score=1, keyword_rank=1)]

        monkeypatch.setattr(
            "inspilot_cloud_baby.retrieval._retrieve_by_db_keyword_candidates",
            lambda **kwargs: keyword,
        )

        def vector_recall(**kwargs):
            calls["vector"] += 1
            return []

        monkeypatch.setattr(
            "inspilot_cloud_baby.retrieval._retrieve_by_vector_candidates", vector_recall
        )

        results = retrieve_documents_explained(
            query="华南", user=company_user, documents=[], limit=1, db=MagicMock()
        )

        assert calls["vector"] == 1
        assert results[0].document.id == "k1"
