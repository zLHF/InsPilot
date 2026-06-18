from unittest.mock import Mock

from inspilot_cloud_baby.audit import ADMIN_WEB_ACTOR, config_change_metadata, write_audit
from inspilot_cloud_baby.models import AuditLog


def test_config_change_metadata_compares_before_and_after_without_secret_values() -> None:
    metadata = config_change_metadata(
        before={
            "dingtalk_app_secret": "old-secret",
            "openai_api_key": "sk-old",
            "chat_model": "old-model",
        },
        after={
            "dingtalk_app_secret": "",
            "openai_api_key": "sk-new",
            "chat_model": "new-model",
        },
    )

    assert metadata == {
        "changed_keys": ["chat_model", "dingtalk_app_secret", "openai_api_key"],
        "secret_keys_changed": ["dingtalk_app_secret", "openai_api_key"],
    }
    serialized = repr(metadata)
    assert "old-secret" not in serialized
    assert "sk-old" not in serialized
    assert "sk-new" not in serialized


def test_config_change_metadata_ignores_unchanged_empty_values() -> None:
    assert config_change_metadata(
        before={"prod_db_password": ""},
        after={"prod_db_password": ""},
    ) == {"changed_keys": [], "secret_keys_changed": []}


def test_write_audit_adds_without_committing() -> None:
    session = Mock()

    row = write_audit(
        session,
        actor_user_id=ADMIN_WEB_ACTOR,
        action="knowledge.create",
        resource_type="knowledge_item",
        resource_id="k1",
        metadata={"source_type": "manual"},
    )

    assert isinstance(row, AuditLog)
    assert row.actor_user_id == "admin:web"
    assert row.metadata_json == {"source_type": "manual"}
    session.add.assert_called_once_with(row)
    session.commit.assert_not_called()
