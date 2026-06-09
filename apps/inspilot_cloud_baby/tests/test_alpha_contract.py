from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_alpha_contract_core_routes_exist() -> None:
    client = TestClient(create_app())

    assert client.get("/health").status_code == 200
    assert client.get("/projects").status_code == 200
    assert client.get("/admin/ingest").status_code == 200
    assert client.get("/admin/dws").status_code == 200
    assert client.post(
        "/ingest/preview",
        json={"filename": "技术方案.md", "text": "直连 API，支付回调，出单回调。"},
    ).status_code == 200
    assert client.post("/chat/query", json={"query": "直连方案怎么做"}).status_code == 200
