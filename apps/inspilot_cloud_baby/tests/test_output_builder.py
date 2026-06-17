from inspilot_cloud_baby.output_builder import build_structured_output


def test_builds_system_issue_output() -> None:
    output = build_structured_output(
        output_type="system_issue",
        confirmed={
            "project_name": "华南车险项目",
            "page": "保单查询页",
            "actual_result": "点击查询后报错",
            "expected_result": "返回保单列表",
        },
        pending=["复现账号", "错误截图原图"],
        sources=["knowledge:k1", "attachment:a1"],
    )

    assert output["output_type"] == "system_issue"
    assert output["confirmed"]["project_name"] == "华南车险项目"
    assert output["pending"] == ["复现账号", "错误截图原图"]
    assert output["sources"] == ["knowledge:k1", "attachment:a1"]
    assert output["schema_version"] == "1.0.0"


def test_rejects_unknown_output_type() -> None:
    try:
        build_structured_output(output_type="unknown", confirmed={}, pending=[], sources=[])
    except ValueError as exc:
        assert "unsupported output_type" in str(exc)
    else:
        raise AssertionError("expected ValueError")
