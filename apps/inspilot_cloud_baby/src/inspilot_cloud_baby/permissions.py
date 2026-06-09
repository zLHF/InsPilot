from __future__ import annotations

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility


def can_read_knowledge(
    *,
    user: CurrentUser,
    project_id: str | None,
    project_visibility: ProjectVisibility | None,
    sensitivity: KnowledgeSensitivity,
) -> bool:
    if sensitivity == KnowledgeSensitivity.SENSITIVE:
        return user.can_view_sensitive and project_id in user.project_ids

    if sensitivity == KnowledgeSensitivity.PROJECT_RESTRICTED:
        return project_id is not None and project_id in user.project_ids

    if sensitivity == KnowledgeSensitivity.PUBLIC_SUMMARY:
        if project_visibility == ProjectVisibility.COMPANY_VISIBLE:
            return user.is_company_user
        return project_id is not None and project_id in user.project_ids

    return False
