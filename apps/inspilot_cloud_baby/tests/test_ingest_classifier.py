from inspilot_cloud_baby.ingest.classifier import classify_material


def test_classifies_fee_table_as_project_restricted() -> None:
    result = classify_material(
        filename="华南车险项目费率表.xlsx",
        text="机构类型：经纪公司\n付费类型：平台代收\n费率：2.5%\n接口编号：POLICY_001",
    )

    assert result.material_type == "rate_table"
    assert result.suggested_scope == "project"
    assert result.sensitivity == "project_restricted"
    assert "费率" in result.detected_sensitive_terms
    assert "接口编号" in result.detected_sensitive_terms


def test_classifies_common_template_as_public_candidate() -> None:
    result = classify_material(
        filename="需求提单模板.md",
        text="本模板用于描述背景、目标、影响范围、验收标准。",
    )

    assert result.material_type == "operation_guide"
    assert result.suggested_scope == "public"
    assert result.sensitivity == "public_summary"


def test_detects_pii_as_sensitive() -> None:
    result = classify_material(
        filename="问题截图说明.txt",
        text="客户手机号 13800138000，身份证号 110101199001011234。",
    )

    assert result.sensitivity == "sensitive"
    assert "手机号" in result.detected_sensitive_terms
    assert "身份证号" in result.detected_sensitive_terms
