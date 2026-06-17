import uuid

from fastapi.testclient import TestClient

from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.main import create_app
from inspilot_cloud_baby.dingtalk_admin import WorkflowDoc
from inspilot_cloud_baby.models import AppSetting, KnowledgeItem, KnowledgeSensitivity, KnowledgeStatus
from inspilot_cloud_baby.routers import admin


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


def test_settings_page_renders_dingtalk_credentials_form() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/settings")

    assert response.status_code == 200
    assert "钉钉开放平台配置" in response.text
    assert 'name="dingtalk_app_key"' in response.text
    assert 'name="dingtalk_app_secret"' in response.text
    assert "testDingTalk()" in response.text
    assert 'id="test-dingtalk"' in response.text


def test_settings_save_persists_dingtalk_credentials(monkeypatch) -> None:
    saved: dict[str, AppSetting] = {}

    class FakeSession:
        def __init__(self):
            self.scalar_calls = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, model, key):
            return saved.get(key)

        def add(self, row):
            saved[row.key] = row

        def commit(self):
            return None

    monkeypatch.setattr(admin, "SessionLocal", lambda: FakeSession())
    client = TestClient(create_app())

    response = client.post(
        "/admin/settings",
        data={
            "dingtalk_app_key": "ding-key",
            "dingtalk_app_secret": "ding-secret",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert saved["dingtalk_app_key"].value == "ding-key"
    assert saved["dingtalk_app_secret"].value == "ding-secret"


def test_dingtalk_admin_client_uses_db_credentials_when_env_empty(monkeypatch) -> None:
    monkeypatch.setattr(settings, "dingtalk_app_key", "")
    monkeypatch.setattr(settings, "dingtalk_app_secret", "")
    monkeypatch.setattr(
        admin,
        "_load_db_settings",
        lambda: {
            "dingtalk_app_key": "db-key",
            "dingtalk_app_secret": "db-secret",
        },
    )

    client = admin._admin_client()

    assert client is not None
    assert client.app_key == "db-key"
    assert client.app_secret == "db-secret"


def test_dingtalk_settings_test_uses_current_form_values(monkeypatch) -> None:
    seen: dict[str, str] = {}

    class FakeDingTalkClient:
        def __init__(self, app_key: str, app_secret: str) -> None:
            seen["app_key"] = app_key
            seen["app_secret"] = app_secret

        def test_connection(self) -> tuple[bool, str]:
            return True, ""

    monkeypatch.setattr(admin, "DingTalkAdminClient", FakeDingTalkClient)
    client = TestClient(create_app())

    response = client.post(
        "/admin/settings/dingtalk-test",
        headers={
            "X-Test-Body": '{"app_key":"form-key","app_secret":"form-secret"}',
        },
        json={},
    )

    assert response.status_code == 200
    assert "连接成功" in response.text
    assert seen == {"app_key": "form-key", "app_secret": "form-secret"}


def test_dingtalk_settings_test_requires_credentials(monkeypatch) -> None:
    monkeypatch.setattr(settings, "dingtalk_app_key", "")
    monkeypatch.setattr(settings, "dingtalk_app_secret", "")
    monkeypatch.setattr(admin, "_load_db_settings", lambda: {})
    client = TestClient(create_app())

    response = client.post("/admin/settings/dingtalk-test", headers={"X-Test-Body": "{}"}, json={})

    assert response.status_code == 200
    assert "未配置钉钉 AppKey 或 AppSecret" in response.text


def test_knowledge_row_renders_project_and_sensitivity_editor(monkeypatch) -> None:
    item = KnowledgeItem(
        id=uuid.uuid4(),
        title="[钉钉审批] 测试审批",
        body="审批内容",
        source_type="dingtalk_approval",
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
        status=KnowledgeStatus.ACTIVE,
        metadata_json={},
        created_by="dingtalk_import",
    )

    class ItemsScalarResult:
        def all(self):
            return [item]

    class EmptyScalarResult:
        def all(self):
            return []

    class FakeSession:
        def __init__(self):
            self.scalar_calls = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def scalars(self, statement):
            self.scalar_calls += 1
            if self.scalar_calls == 1:
                return ItemsScalarResult()
            return EmptyScalarResult()

        def scalar(self, statement):
            return 1

    monkeypatch.setattr(admin, "SessionLocal", lambda: FakeSession())
    client = TestClient(create_app())

    response = client.get("/admin/knowledge")

    assert response.status_code == 200
    assert 'name="project_id"' in response.text
    assert 'name="sensitivity"' in response.text
    assert "/admin/knowledge/" in response.text
    assert "/visibility" in response.text


def test_knowledge_visibility_update_can_make_unassigned_dingtalk_item_public(monkeypatch) -> None:
    item = KnowledgeItem(
        id=uuid.uuid4(),
        title="[钉钉审批] 测试审批",
        body="审批内容",
        source_type="dingtalk_approval",
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
        status=KnowledgeStatus.ACTIVE,
        metadata_json={},
        created_by="dingtalk_import",
    )

    class FakeScalarResult:
        def all(self):
            return []

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, model, key):
            if model is KnowledgeItem:
                return item
            return None

        def scalars(self, statement):
            return FakeScalarResult()

        def commit(self):
            return None

    monkeypatch.setattr(admin, "SessionLocal", lambda: FakeSession())
    client = TestClient(create_app())

    response = client.put(
        f"/admin/knowledge/{item.id}/visibility",
        data={"project_id": "", "sensitivity": "public_summary"},
    )

    assert response.status_code == 200
    assert item.project_id is None
    assert item.sensitivity == KnowledgeSensitivity.PUBLIC_SUMMARY
    assert "公开摘要" in response.text


def test_dingtalk_knowledge_body_includes_approval_chain_details() -> None:
    workflow = WorkflowDoc(
        title="测试审批",
        status="RUNNING",
        originator="originator-user",
        form_data={"费率": "0.3"},
        operation_records=[
            {
                "userid": "approver-1",
                "operation_type": "EXECUTE_TASK_NORMAL",
                "operation_result": "AGREE",
                "remark": "同意",
                "date": "2026-05-28 20:02:57",
            },
            {
                "userid": "bpms_system",
                "operation_type": "EXECUTE_TASK_NORMAL",
                "operation_result": "AGREE",
                "remark": "[未找到审批人](https://example.test)，已自动通过",
                "date": "2026-05-31 19:40:25",
            },
        ],
    )

    body = admin._build_dingtalk_knowledge_body(workflow)

    assert "**费率**: 0.3" in body
    assert "approver-1" in body
    assert "EXECUTE_TASK_NORMAL" in body
    assert "AGREE" in body
    assert "同意" in body
    assert "2026-05-28 20:02:57" in body
    assert "未找到审批人" in body
