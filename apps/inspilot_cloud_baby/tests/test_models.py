from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility


def test_project_visibility_values_match_prd_terms() -> None:
    assert ProjectVisibility.COMPANY_VISIBLE.value == "company_visible"
    assert ProjectVisibility.PROJECT_MEMBERS.value == "project_members"
    assert ProjectVisibility.RESTRICTED.value == "restricted"


def test_knowledge_sensitivity_values_match_prd_terms() -> None:
    assert KnowledgeSensitivity.PUBLIC_SUMMARY.value == "public_summary"
    assert KnowledgeSensitivity.PROJECT_RESTRICTED.value == "project_restricted"
    assert KnowledgeSensitivity.SENSITIVE.value == "sensitive"
