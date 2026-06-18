from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app
from inspilot_cloud_baby.models import KnowledgeSensitivity
from inspilot_cloud_baby.retrieval import KnowledgeDocument
from inspilot_cloud_baby.retrieval_evidence import ExplainedDocument, RetrievalEvidence
from inspilot_cloud_baby.routers import chat


def test_chat_source_exposes_safe_retrieval_evidence(monkeypatch) -> None:
    document = KnowledgeDocument(
        id="k1",
        project_id=None,
        project_visibility=None,
        sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
        title="西宁市项目",
        body="浙江华重融资担保",
        source_type="dingtalk_approval",
    )
    explained = ExplainedDocument(
        document=document,
        evidence=RetrievalEvidence(
            channels=("keyword", "vector"),
            matched_fields=("body",),
            keyword_score=1,
            keyword_rank=1,
            vector_distance=0.123,
            vector_rank=2,
            final_rank=1,
        ),
    )
    monkeypatch.setattr(chat, "_fetch_doc_kb", lambda query, filters: ([explained], "上下文"))
    monkeypatch.setattr(chat, "_fetch_prod_db", lambda query: ("", "", 0))

    class UnavailableChat:
        available = False

    monkeypatch.setattr(chat, "get_chat_service", lambda: UnavailableChat())

    response = TestClient(create_app()).post("/chat/query", json={"query": "西宁市"})

    assert response.status_code == 200
    source = response.json()["sources"][0]
    assert source["recall_channels"] == ["keyword", "vector"]
    assert source["matched_fields"] == ["body"]
    assert source["keyword_rank"] == 1
    assert source["vector_rank"] == 2
    assert source["final_rank"] == 1
    assert "vector_distance" not in source
