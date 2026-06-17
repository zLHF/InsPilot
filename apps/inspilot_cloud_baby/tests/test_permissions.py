from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.permissions import can_read_knowledge


def test_company_user_can_read_public_summary_in_company_visible_project() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())

    assert can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
    )


def test_company_user_cannot_read_restricted_item_without_membership() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())

    assert not can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
    )


def test_project_member_can_read_project_restricted_item() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})

    assert can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.PROJECT_MEMBERS,
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
    )


def test_sensitive_item_requires_explicit_sensitive_grant() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})

    assert not can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.SENSITIVE,
    )
