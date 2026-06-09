import json

from inspilot_cloud_baby.dws_adapter import DwsAdapter


def test_builds_oa_process_instance_command() -> None:
    adapter = DwsAdapter(binary="dws")

    command = adapter.build_fetch_workflow_command(workflow_id="PROC-001")

    assert command == [
        "dws",
        "oa",
        "process-instance",
        "get",
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
    assert parsed.fields["项目"] == "华南车险项目"
    assert parsed.comments[0]["content"] == "需要补充费率"
    assert parsed.attachments[0]["name"] == "费率表.xlsx"
