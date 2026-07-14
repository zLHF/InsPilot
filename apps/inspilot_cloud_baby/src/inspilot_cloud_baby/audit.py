from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Session

from inspilot_cloud_baby.models import AuditLog

ADMIN_WEB_ACTOR = "admin:web"
SECRET_SETTING_KEYS = frozenset(
    {"dingtalk_app_secret", "openai_api_key", "chat_api_key", "prod_db_password"}
)


def config_change_metadata(
    *,
    before: Mapping[str, str],
    after: Mapping[str, str],
) -> dict[str, list[str]]:
    """Describe changed setting keys without retaining any setting values."""
    changed = sorted(
        key for key in before.keys() | after.keys() if before.get(key, "") != after.get(key, "")
    )
    return {
        "changed_keys": changed,
        "secret_keys_changed": sorted(key for key in changed if key in SECRET_SETTING_KEYS),
    }


def write_audit(
    session: Session,
    *,
    actor_user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    reason: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> AuditLog:
    """Add an audit row to the caller's transaction without committing it."""
    row = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        reason=reason,
        metadata_json=dict(metadata or {}),
    )
    session.add(row)
    return row
