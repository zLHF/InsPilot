"""Unit tests for retrieval-quality helpers (no DB / no external calls)."""
from __future__ import annotations

from inspilot_cloud_baby.models import KnowledgeSensitivity
from inspilot_cloud_baby.retrieval import KnowledgeDocument, _query_terms
from inspilot_cloud_baby.retrieval_evidence import RetrievalCandidate, fuse_candidates
from inspilot_cloud_baby.routers.chat import _needs_prod_db


def _doc(doc_id: str) -> KnowledgeDocument:
    return KnowledgeDocument(
        id=doc_id,
        project_id=None,
        project_visibility=None,
        sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
        title=f"title-{doc_id}",
        body=f"body-{doc_id}",
    )


def _candidate(
    doc_id: str, *, keyword_rank=None, keyword_score=0, vector_rank=None, vector_distance=None
) -> RetrievalCandidate:
    return RetrievalCandidate(
        document=_doc(doc_id),
        keyword_rank=keyword_rank,
        keyword_score=keyword_score,
        vector_rank=vector_rank,
        vector_distance=vector_distance,
    )


# --- evidence-carrying fusion (RRF's successor) -----------------------------


def test_fuse_candidates_rewards_cross_channel_agreement():
    # doc "2" ranks high in both channels → should win after fusion.
    keyword = [
        _candidate("2", keyword_rank=1, keyword_score=1),
        _candidate("4", keyword_rank=2, keyword_score=1),
    ]
    vector = [
        _candidate("2", vector_rank=1),
        _candidate("1", vector_rank=2),
    ]
    fused = fuse_candidates(keyword=keyword, vector=vector, limit=10)
    assert fused[0].document.id == "2"
    assert fused[0].evidence.channels == ("keyword", "vector")
    assert {item.document.id for item in fused} == {"1", "2", "4"}


def test_fuse_candidates_dedups_by_id():
    keyword = [
        _candidate("1", keyword_rank=1, keyword_score=1),
        _candidate("2", keyword_rank=2, keyword_score=1),
    ]
    vector = [
        _candidate("1", vector_rank=1),
        _candidate("2", vector_rank=2),
    ]
    fused = fuse_candidates(keyword=keyword, vector=vector, limit=10)
    assert [item.document.id for item in fused] == ["1", "2"]


def test_fuse_candidates_handles_empty_lists():
    assert fuse_candidates(keyword=[], vector=[], limit=10) == []
    single = fuse_candidates(keyword=[], vector=[_candidate("9", vector_rank=1)], limit=10)
    assert [item.document.id for item in single] == ["9"]


# --- jieba query tokenization ---------------------------------------------


def test_query_terms_segments_chinese_and_drops_stopwords():
    terms = _query_terms("衢州有哪些方案")
    assert "衢州" in terms
    assert "方案" in terms
    assert "有" not in terms      # stopword
    assert "哪些" not in terms    # stopword


def test_query_terms_dedup_and_lowercase():
    terms = _query_terms("CA签章 CA配置")
    assert terms == list(dict.fromkeys(terms))   # no duplicates, order preserved
    assert all(t == t.lower() for t in terms)


def test_query_terms_empty():
    assert _query_terms("") == []


# --- prod-DB gate heuristic ------------------------------------------------


def test_needs_prod_db_triggers_on_realtime_signals():
    assert _needs_prod_db("最新费率是多少")
    assert _needs_prod_db("订单12345678的状态")   # keyword + long number
    assert _needs_prod_db("本月出单数量")


def test_needs_prod_db_skips_pure_knowledge_questions():
    assert not _needs_prod_db("衢州有哪些方案")
    assert not _needs_prod_db("独立出单模式是什么")
