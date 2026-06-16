import json

from inspilot_cloud_baby.dws_adapter import DwsAdapter


def test_builds_approval_detail_command() -> None:
    adapter = DwsAdapter(binary="dws")

    command = adapter.build_fetch_workflow_command(workflow_id="PROC-001")

    assert command == [
        "dws",
        "oa",
        "approval",
        "detail",
        "--instance-id",
        "PROC-001",
        "--format",
        "json",
    ]


def test_builds_records_command() -> None:
    adapter = DwsAdapter(binary="dws")

    command = adapter.build_fetch_records_command(workflow_id="PROC-001")

    assert command == [
        "dws",
        "oa",
        "approval",
        "records",
        "--instance-id",
        "PROC-001",
        "--format",
        "json",
    ]


def test_parses_workflow_json() -> None:
    adapter = DwsAdapter(binary="dws")
    raw = json.dumps(
        {
            "result": {
                "title": "变更需求",
                "fields": [{"name": "项目", "value": "华南车险项目"}],
                "comments": [{"creator": "u1", "content": "需要补充费率"}],
                "attachments": [{"name": "费率表.xlsx", "downloadUrl": "https://example.test/file"}],
            }
        }
    )

    parsed = adapter.parse_workflow_payload(raw)

    assert parsed.title == "变更需求"
    assert parsed.form_data["项目"] == "华南车险项目"
    assert parsed.operation_records[0]["content"] == "需要补充费率"
    assert parsed.attachments[0]["name"] == "费率表.xlsx"
