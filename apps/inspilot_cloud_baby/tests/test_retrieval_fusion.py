"""Unit tests for retrieval-quality helpers (no DB / no external calls)."""
from __future__ import annotations

from inspilot_cloud_baby.models import KnowledgeSensitivity
from inspilot_cloud_baby.retrieval import KnowledgeDocument, _query_terms, _rrf_fuse
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


# --- RRF fusion ------------------------------------------------------------


def test_rrf_fuse_rewards_cross_channel_agreement():
    # doc "2" ranks high in both lists → should win after fusion.
    vector = [_doc("1"), _doc("2"), _doc("3")]
    keyword = [_doc("2"), _doc("4"), _doc("1")]
    fused = _rrf_fuse([vector, keyword])
    assert fused[0].id == "2"
    assert {d.id for d in fused} == {"1", "2", "3", "4"}


def test_rrf_fuse_dedups_by_id():
    a = [_doc("1"), _doc("2")]
    b = [_doc("1"), _doc("2")]
    fused = _rrf_fuse([a, b])
    assert [d.id for d in fused] == ["1", "2"]


def test_rrf_fuse_handles_empty_lists():
    assert _rrf_fuse([[], []]) == []
    single = _rrf_fuse([[_doc("9")], []])
    assert [d.id for d in single] == ["9"]


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
