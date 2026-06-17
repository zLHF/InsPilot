import inspilot_cloud_baby.models as models
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility


def test_project_visibility_values_match_prd_terms() -> None:
    assert ProjectVisibility.COMPANY_VISIBLE.value == "company_visible"
    assert ProjectVisibility.PROJECT_MEMBERS.value == "project_members"
    assert ProjectVisibility.RESTRICTED.value == "restricted"


def test_knowledge_sensitivity_values_match_prd_terms() -> None:
    assert KnowledgeSensitivity.PUBLIC_SUMMARY.value == "public_summary"
    assert KnowledgeSensitivity.PROJECT_RESTRICTED.value == "project_restricted"
    assert KnowledgeSensitivity.SENSITIVE.value == "sensitive"


def test_audit_log_model_has_beta_required_fields() -> None:
    assert hasattr(models, "AuditLog")
    AuditLog = models.AuditLog

    assert AuditLog.__tablename__ == "audit_logs"

    assert set(AuditLog.__table__.columns.keys()) == {
        "id",
        "actor_user_id",
        "action",
        "resource_type",
        "resource_id",
        "reason",
        "metadata_json",
        "created_at",
    }
