"""Tests for the direct DingTalk admin API client (dingtalk_admin.py)."""
from __future__ import annotations

from unittest.mock import patch

from inspilot_cloud_baby.dingtalk_admin import (
    AdminAttachment,
    AdminComment,
    AdminWorkflowDetail,
    DingTalkAdminClient,
    WorkflowDoc,
)


def _sample_detail() -> AdminWorkflowDetail:
    return AdminWorkflowDetail(
        process_instance_id="PROC-001",
        business_id="202606101118000214667",
        title="车险费率变更申请",
        status="COMPLETED",
        originator_user_id="user-001",
        form_data={"机构类型": "经纪公司", "费率": "0.85"},
        cc_user_ids=["user-002"],
        operation_records=[{"userId": "user-001", "remark": "发起", "date_formatted": "2026-06-10"}],
        attachments=[AdminAttachment(field_name="附件", component_type="DDAttachment", file_name="方案.pdf")],
        comments=[AdminComment(comment_id="c1", user_id="user-003", content="已确认")],
    )


def test_to_workflow_maps_all_fields() -> None:
    detail = _sample_detail()

    doc = DingTalkAdminClient.to_workflow(detail)

    assert isinstance(doc, WorkflowDoc)
    assert doc.title == "车险费率变更申请"
    assert doc.status == "COMPLETED"
    assert doc.originator == "user-001"
    assert doc.process_instance_id == "PROC-001"
    assert doc.form_data == {"机构类型": "经纪公司", "费率": "0.85"}
    assert len(doc.operation_records) == 1
    assert doc.attachments[0]["file_name"] == "方案.pdf"
    assert doc.comments[0]["content"] == "已确认"


def test_get_detail_preserves_caller_id_when_api_omits_it() -> None:
    """Regression: /topapi/processinstance/get does not return process_instance_id,
    so get_detail must set it from the caller's argument, not the (empty) raw payload."""
    client = DingTalkAdminClient("key", "secret")
    # Raw payload as returned by DingTalk — note: NO process_instance_id field
    raw_without_id = {"title": "测试审批", "status": "COMPLETED", "business_id": "BIZ-1"}

    with (
        patch.object(DingTalkAdminClient, "get_instance_detail", return_value=raw_without_id),
        patch.object(DingTalkAdminClient, "get_comments", return_value=[]),
    ):
        detail = client.get_detail("THE-REAL-ID")

    assert detail.process_instance_id == "THE-REAL-ID"
    assert detail.title == "测试审批"
    # And to_workflow propagates it through to the view model
    assert DingTalkAdminClient.to_workflow(detail).process_instance_id == "THE-REAL-ID"


def test_to_workflow_is_idempotent_on_empty_detail() -> None:
    detail = AdminWorkflowDetail(
        process_instance_id="",
        business_id="",
        title="",
        status="",
        originator_user_id="",
    )
    doc = DingTalkAdminClient.to_workflow(detail)

    assert doc.title == ""
    assert doc.form_data == {}
    assert doc.attachments == []
    assert doc.comments == []


def test_parse_detail_accepts_dingtalk_snake_case_form_fields() -> None:
    client = DingTalkAdminClient("key", "secret")
    raw = {
        "title": "王国通提交的项目评估申请+项目实施",
        "status": "RUNNING",
        "business_id": "202605281923000432811",
        "originator_userid": "0649510929152648",
        "form_component_values": [
            {
                "component_type": "TextField",
                "name": "维格表RECORDID",
                "value": "rech35DRMYFck",
            },
            {
                "component_type": "DDSelectField",
                "name": "产品类型（险种/产品）",
                "value": "投标",
            },
            {
                "component_type": "DDMultiSelectField",
                "name": "业务平台所属省市",
                "value": '["青海省","西宁市"]',
            },
            {
                "component_type": "TextField",
                "name": "空字段",
                "value": "null",
            },
        ],
    }

    detail = client.parse_detail(raw)

    assert detail.form_data["维格表RECORDID"] == "rech35DRMYFck"
    assert detail.form_data["产品类型（险种/产品）"] == "投标"
    assert detail.form_data["业务平台所属省市"] == "青海省, 西宁市"
    assert "空字段" not in detail.form_data


def test_parse_detail_null_attachment_value_yields_no_placeholder() -> None:
    """Regression: when an attachment field's value is the literal string "null"
    (DingTalk returns this when no file was uploaded / for client-side local
    uploads), parse_detail must NOT fabricate a placeholder attachment.

    Before the fix, a phantom "附件" appeared in the UI that couldn't be opened.
    """
    client = DingTalkAdminClient("key", "secret")
    raw = {
        "title": "无附件工单",
        "status": "RUNNING",
        "business_id": "202603170904000148843",
        "originator_userid": "u1",
        "form_component_values": [
            {
                "component_type": "DDAttachment",
                "id": "DDAttachment_1ZG45MOQV7UO0",
                "name": "附件",
                "value": "null",
            },
        ],
    }
    detail = client.parse_detail(raw)
    assert detail.attachments == []


def test_parse_detail_real_attachment_value_is_parsed() -> None:
    """A populated attachment field should yield one AdminAttachment per file,
    preserving fileId / fileName / fileSize / fileType."""
    client = DingTalkAdminClient("key", "secret")
    raw = {
        "title": "有附件工单",
        "status": "COMPLETED",
        "business_id": "BIZ-2",
        "originator_userid": "u1",
        "form_component_values": [
            {
                "component_type": "DDAttachment",
                "name": "更新包上传",
                "value": (
                    '[{"spaceId":"1764121318","fileName":"app.exe",'
                    '"fileSize":316416,"fileType":"exe","fileId":"225597627427"}]'
                ),
            },
        ],
    }
    detail = client.parse_detail(raw)
    assert len(detail.attachments) == 1
    att = detail.attachments[0]
    assert att.file_id == "225597627427"
    assert att.file_name == "app.exe"
    assert att.file_size == 316416
    assert att.file_type == "exe"
    assert att.space_id == "1764121318"


def test_test_connection_ok_when_token_refresh_succeeds() -> None:
    client = DingTalkAdminClient("key", "secret")

    with patch.object(DingTalkAdminClient, "_ensure_token", return_value="token") as mock:
        ok, message = client.test_connection()

    assert ok is True
    assert message == ""
    mock.assert_called_once()


def test_test_connection_reports_failure_when_token_refresh_raises() -> None:
    client = DingTalkAdminClient("bad-key", "bad-secret")

    with patch.object(
        DingTalkAdminClient, "_ensure_token", side_effect=RuntimeError("invalid appKey")
    ):
        ok, message = client.test_connection()

    assert ok is False
    assert "invalid appKey" in message


def test_list_recent_instances_aggregates_details_within_limit() -> None:
    client = DingTalkAdminClient("key", "secret")
    detail = _sample_detail()

    with (
        patch.object(DingTalkAdminClient, "list_process_codes", return_value=["PROC-A"]),
        patch.object(
            DingTalkAdminClient,
            "list_instance_ids",
            return_value=(["i1", "i2", "i3"], 0),
        ),
        patch.object(DingTalkAdminClient, "get_detail", return_value=detail) as mock_detail,
    ):
        results = client.list_recent_instances(days=7, limit=2)

    assert len(results) == 2  # capped at limit
    assert all(r.title == "车险费率变更申请" for r in results)
    assert mock_detail.call_count == 2


def test_list_recent_instances_skips_detail_errors() -> None:
    client = DingTalkAdminClient("key", "secret")
    detail = _sample_detail()

    with (
        patch.object(DingTalkAdminClient, "list_process_codes", return_value=["PROC-A"]),
        patch.object(
            DingTalkAdminClient,
            "list_instance_ids",
            return_value=(["good", "bad"], 0),
        ),
        patch.object(
            DingTalkAdminClient,
            "get_detail",
            side_effect=[detail, RuntimeError("not found")],
        ),
    ):
        results = client.list_recent_instances(days=7, limit=5)

    # "good" succeeded, "bad" raised and was skipped — only 1 result
    assert len(results) == 1
    assert results[0].title == "车险费率变更申请"
