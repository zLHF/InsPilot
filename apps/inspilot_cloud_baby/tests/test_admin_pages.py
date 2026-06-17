from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_ingest_admin_page_renders() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/ingest")

    assert response.status_code == 200
    assert "资料投喂" in response.text


def test_dingtalk_admin_page_renders() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/dws")

    assert response.status_code == 200
    assert "钉钉审批流程导入" in response.text
