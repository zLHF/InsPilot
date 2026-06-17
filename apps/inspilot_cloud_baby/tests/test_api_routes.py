from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_ingest_preview_returns_classification() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/ingest/preview",
        json={"filename": "需求提单模板.md", "text": "本模板用于描述背景、目标、影响范围。"},
    )

    assert response.status_code == 200
    assert response.json()["suggested_scope"] == "public"


def test_chat_query_returns_alpha_response() -> None:
    client = TestClient(create_app())

    response = client.post("/chat/query", json={"query": "华南车险项目是什么模式"})

    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    # sources is a list of knowledge-item titles (may be non-empty when the
    # knowledge base has data); just assert the shape is stable.
    assert isinstance(body["sources"], list)
