from __future__ import annotations

import datetime
import json
import logging
import re
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Literal

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdminAttachment:
    """Structured attachment parsed from DDAttachment or Picture form component."""

    field_name: str  # Form field label (e.g. "附件")
    component_type: str  # "DDAttachment" or "Picture"
    file_id: str = ""
    file_name: str = ""
    file_size: int = 0
    download_url: str = ""
    space_id: str = ""


@dataclass(frozen=True)
class AdminComment:
    """A single comment on an approval instance."""

    comment_id: str
    user_id: str
    content: str
    timestamp: str = ""  # Human-readable ISO string
    attachments: list[AdminAttachment] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CommentFetchResult:
    status: Literal["available", "unavailable", "error"]
    comments: tuple[AdminComment, ...] = ()
    error_type: str = ""
    message: str = ""


@dataclass(frozen=True)
class CapabilityStatus:
    status: Literal["ok", "failed", "unavailable", "not_tested"]
    message: str = ""


@dataclass(frozen=True)
class DingTalkCapabilities:
    token: CapabilityStatus
    approval_detail: CapabilityStatus
    comments: CapabilityStatus


@dataclass(frozen=True)
class ApprovalRemark:
    user_id: str
    timestamp: str
    content: str
    node_name: str = ""
    operation_type: str = ""
    operation_result: str = ""
    comment_id: str = ""
    sources: tuple[str, ...] = ()


def _normalize_remark_content(content: str) -> str:
    normalized = re.sub(r"\s+", " ", content.strip()).casefold()
    return re.sub(r"[。．.!！?？]+$", "", normalized)


def _remark_key(user_id: str, timestamp: str, content: str) -> tuple[str, str, str]:
    return user_id, timestamp[:16], _normalize_remark_content(content)


def merge_approval_remarks(
    operation_records: list[dict],
    comments: list[AdminComment] | tuple[AdminComment, ...],
) -> list[ApprovalRemark]:
    merged: dict[tuple[str, str, str], ApprovalRemark] = {}
    for record in operation_records:
        content = str(record.get("remark", ""))
        if not content.strip():
            continue
        user_id = str(
            record.get("userid")
            or record.get("userId")
            or record.get("creatorUserId")
            or ""
        )
        timestamp = str(record.get("date_formatted") or record.get("date") or "")
        key = _remark_key(user_id, timestamp, content)
        merged[key] = ApprovalRemark(
            user_id=user_id,
            timestamp=timestamp,
            content=content,
            node_name=str(record.get("task_name") or record.get("taskName") or ""),
            operation_type=str(
                record.get("operation_type") or record.get("operationType") or ""
            ),
            operation_result=str(
                record.get("operation_result")
                or record.get("operationResult")
                or record.get("result")
                or ""
            ),
            sources=("operation",),
        )
    for comment in comments:
        key = _remark_key(comment.user_id, comment.timestamp, comment.content)
        existing = merged.get(key)
        if existing:
            merged[key] = ApprovalRemark(
                user_id=existing.user_id,
                timestamp=existing.timestamp,
                content=existing.content,
                node_name=existing.node_name,
                operation_type=existing.operation_type,
                operation_result=existing.operation_result,
                comment_id=comment.comment_id,
                sources=("operation", "comment"),
            )
        else:
            merged[key] = ApprovalRemark(
                user_id=comment.user_id,
                timestamp=comment.timestamp,
                content=comment.content,
                comment_id=comment.comment_id,
                sources=("comment",),
            )
    return list(merged.values())


@dataclass(frozen=True)
class AdminWorkflowDetail:
    """Parsed result from /topapi/processinstance/get."""

    process_instance_id: str
    business_id: str
    title: str
    status: str
    originator_user_id: str
    form_data: dict[str, str] = field(default_factory=dict)
    cc_user_ids: list[str] = field(default_factory=list)
    operation_records: list[dict] = field(default_factory=list)
    attachments: list[AdminAttachment] = field(default_factory=list)
    comments: list[AdminComment] = field(default_factory=list)
    comment_status: str = "available"
    comment_error_type: str = ""
    remarks: list[ApprovalRemark] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass
class BatchFetchResult:
    """Result of a batch approval fetch operation."""

    succeeded: list[AdminWorkflowDetail] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)  # [{"id": str, "error": str}]


@dataclass(frozen=True)
class WorkflowDoc:
    """Template-facing view of a DingTalk approval instance.

    The admin UI renders this shape; it is produced from an
    AdminWorkflowDetail via DingTalkAdminClient.to_workflow().
    """

    title: str
    status: str = ""
    originator: str = ""
    process_instance_id: str = ""
    form_data: dict[str, str] = field(default_factory=dict)
    operation_records: list[dict] = field(default_factory=list)
    attachments: list[dict] = field(default_factory=list)
    comments: list[dict] = field(default_factory=list)
    comment_status: str = "available"
    comment_error_type: str = ""
    remarks: list[dict] = field(default_factory=list)
    raw_json: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DingTalk Admin API client
# ---------------------------------------------------------------------------


class DingTalkAdminClient:
    """Direct client for DingTalk enterprise admin APIs.

    Uses AppKey/AppSecret to get an access_token, then calls
    /topapi/processinstance/* APIs which can access ALL approval instances
    in the organization, regardless of the caller's personal permissions.
    """

    def __init__(self, app_key: str, app_secret: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self._token: str = ""
        self._token_expires: float = 0.0

    # ------------------------------------------------------------------
    # Token management
    # ------------------------------------------------------------------

    def _ensure_token(self) -> str:
        """Get a valid access_token, refreshing if needed."""
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
        body = json.dumps({"appKey": self.app_key, "appSecret": self.app_secret}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        self._token = data["accessToken"]
        self._token_expires = time.time() + data.get("expireIn", 7200)
        logger.info("DingTalk admin access_token refreshed, expires in %ds", data.get("expireIn", 7200))
        return self._token

    # ------------------------------------------------------------------
    # Low-level API call
    # ------------------------------------------------------------------

    def _topapi_post(self, path: str, body: dict) -> dict:
        """Call a /topapi/ endpoint with the admin access_token."""
        token = self._ensure_token()
        url = f"https://oapi.dingtalk.com{path}?access_token={token}"
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_timestamp(ts_ms) -> str:
        """Convert millisecond timestamp to human-readable string."""
        if not ts_ms:
            return ""
        try:
            ms = int(ts_ms)
            return datetime.datetime.fromtimestamp(
                ms / 1000, tz=datetime.timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OSError, TypeError):
            return ""

    # ------------------------------------------------------------------
    # Instance listing
    # ------------------------------------------------------------------

    def list_instance_ids(
        self,
        *,
        process_code: str = "",
        start_time_ms: int = 0,
        end_time_ms: int = 0,
        size: int = 20,
        cursor: int = 0,
    ) -> tuple[list[str], int]:
        """List process instance IDs. Returns (ids, next_cursor)."""
        body: dict = {"size": size, "cursor": cursor}
        if process_code:
            body["process_code"] = process_code
        if start_time_ms:
            body["start_time"] = start_time_ms
        if end_time_ms:
            body["end_time"] = end_time_ms
        data = self._topapi_post("/topapi/processinstance/listids", body)
        if data.get("errcode") != 0:
            raise RuntimeError(f"listids failed: {data.get('errmsg', 'unknown')}")
        result = data.get("result", {})
        return result.get("list", []), result.get("next_cursor", 0)

    # ------------------------------------------------------------------
    # Process code discovery
    # ------------------------------------------------------------------

    def list_process_templates(self) -> list[dict]:
        """List all approval process templates in the organization.

        Uses /topapi/process/listbyuserid which returns all templates
        accessible to the enterprise app, including process_code and name.
        Results are cached for 1 hour.
        """
        cache_key = "_process_templates_cache"
        cached = getattr(self, cache_key, None)
        if cached and time.time() < cached[0]:
            return cached[1]

        templates: list[dict] = []
        cursor = 0
        while True:
            body = {"offset": cursor, "size": 50}
            data = self._topapi_post("/topapi/process/listbyuserid", body)
            if data.get("errcode") != 0:
                logger.warning("listbyuserid failed: %s", data.get("errmsg", ""))
                break
            result = data.get("result", {})
            for p in result.get("process_list", []):
                templates.append({
                    "name": p.get("name", ""),
                    "process_code": p.get("process_code", ""),
                })
            next_cursor = result.get("next_cursor", 0)
            if not next_cursor:
                break
            cursor = next_cursor

        setattr(self, cache_key, (time.time() + 3600, templates))
        logger.info("Discovered %d process templates", len(templates))
        return templates

    def list_process_codes(self) -> list[str]:
        """Get all known process codes from the org's approval templates."""
        return [t["process_code"] for t in self.list_process_templates() if t.get("process_code")]

    # ------------------------------------------------------------------
    # Instance detail
    # ------------------------------------------------------------------

    def get_instance_detail(self, process_instance_id: str) -> dict:
        """Get raw detail from /topapi/processinstance/get."""
        data = self._topapi_post(
            "/topapi/processinstance/get",
            {"process_instance_id": process_instance_id},
        )
        if data.get("errcode") != 0:
            raise RuntimeError(f"get instance failed: {data.get('errmsg', 'unknown')}")
        return data.get("process_instance", {})

    def _parse_form_attachments(
        self, name: str, ctype: str, value: str
    ) -> list[AdminAttachment]:
        """Parse attachment value JSON from DDAttachment/Picture components."""
        results: list[AdminAttachment] = []
        try:
            parsed = json.loads(value) if value else []
        except (json.JSONDecodeError, TypeError):
            parsed = []

        if not isinstance(parsed, list):
            parsed = [parsed] if isinstance(parsed, dict) else []

        for item in parsed:
            if not isinstance(item, dict):
                continue
            results.append(AdminAttachment(
                field_name=name,
                component_type=ctype,
                file_id=item.get("fileId", ""),
                file_name=item.get("fileName", item.get("originalName", name)),
                file_size=item.get("fileSize", 0),
                download_url=item.get("downloadUrl", ""),
                space_id=item.get("spaceId", ""),
            ))

        if not results:
            results.append(AdminAttachment(
                field_name=name,
                component_type=ctype,
                file_name=name,
            ))
        return results

    def parse_detail(self, raw: dict) -> AdminWorkflowDetail:
        """Parse raw process_instance into AdminWorkflowDetail."""
        form_data: dict[str, str] = {}
        attachments: list[AdminAttachment] = []
        form_values = raw.get("formComponentValues") or raw.get("form_component_values") or []
        for fv in form_values:
            name = fv.get("name", "")
            value = str(fv.get("value", "") or "")
            ctype = fv.get("componentType", "") or fv.get("component_type", "")
            if not name:
                continue
            # Attachment / image fields
            if ctype in ("DDAttachment", "Picture") or "附件" in name or "图片" in name:
                attachments.extend(
                    self._parse_form_attachments(name, ctype or "DDAttachment", value)
                )
            elif value and value != "null":
                if value.startswith("[") and value.endswith("]"):
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list):
                            value = ", ".join(str(v) for v in parsed)
                    except json.JSONDecodeError:
                        pass
                form_data[name] = value

        # Enrich operation records with formatted timestamps
        enriched_records: list[dict] = []
        for rec in raw.get("operation_records", []):
            enriched = dict(rec)
            date_ms = rec.get("date", 0)
            if date_ms:
                enriched["date_formatted"] = self._format_timestamp(date_ms)
            enriched_records.append(enriched)

        return AdminWorkflowDetail(
            process_instance_id=raw.get("process_instance_id", ""),
            business_id=raw.get("business_id", ""),
            title=raw.get("title", ""),
            status=raw.get("status", ""),
            originator_user_id=raw.get("originator_userid", ""),
            form_data=form_data,
            cc_user_ids=raw.get("cc_userids", []),
            operation_records=enriched_records,
            attachments=attachments,
            raw=raw,
        )

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------

    def get_comments(self, process_instance_id: str) -> CommentFetchResult:
        """Fetch all comments for an approval instance."""
        comments: list[AdminComment] = []
        cursor = 0
        while True:
            data = self._topapi_post(
                "/topapi/processinstance/comment/list",
                {"process_instance_id": process_instance_id, "cursor": cursor, "size": 20},
            )
            if data.get("errcode") != 0:
                message = str(data.get("errmsg", ""))
                logger.warning(
                    "comment list failed for %s: %s",
                    process_instance_id, message,
                )
                permission_denied = "权限" in message or "permission" in message.lower()
                return CommentFetchResult(
                    status="unavailable" if permission_denied else "error",
                    comments=tuple(comments),
                    error_type="permission_denied" if permission_denied else "api_error",
                    message=message,
                )
            result = data.get("result", {})
            for c in result.get("list", []):
                comments.append(AdminComment(
                    comment_id=str(c.get("id", "")),
                    user_id=c.get("userid", c.get("userId", "")),
                    content=c.get("content", ""),
                    timestamp=self._format_timestamp(c.get("create_time", 0)),
                    raw=c,
                ))
            next_cursor = result.get("next_cursor", 0)
            if not next_cursor:
                break
            cursor = next_cursor
        return CommentFetchResult(status="available", comments=tuple(comments))

    # ------------------------------------------------------------------
    # High-level detail fetch (with comments)
    # ------------------------------------------------------------------

    def get_detail(self, process_instance_id: str) -> AdminWorkflowDetail:
        """Get and parse an approval instance detail, including comments."""
        raw = self.get_instance_detail(process_instance_id)
        detail = self.parse_detail(raw)
        # Fetch comments (graceful: don't block on failure)
        try:
            comment_result = self.get_comments(process_instance_id)
            if isinstance(comment_result, list):
                comment_result = CommentFetchResult(
                    status="available", comments=tuple(comment_result)
                )
        except Exception as exc:
            logger.warning("Failed to fetch comments for %s", process_instance_id, exc_info=True)
            comment_result = CommentFetchResult(
                status="error",
                error_type="transport_error",
                message=str(exc),
            )
        comments = list(comment_result.comments)
        remarks = merge_approval_remarks(detail.operation_records, comments)
        # Return new instance with comments (frozen dataclass).
        # NOTE: /topapi/processinstance/get does NOT echo back process_instance_id,
        # so we set it from the caller's argument (parse_detail leaves it blank).
        return AdminWorkflowDetail(
            process_instance_id=process_instance_id,
            business_id=detail.business_id,
            title=detail.title,
            status=detail.status,
            originator_user_id=detail.originator_user_id,
            form_data=detail.form_data,
            cc_user_ids=detail.cc_user_ids,
            operation_records=detail.operation_records,
            attachments=detail.attachments,
            comments=comments,
            comment_status=comment_result.status,
            comment_error_type=comment_result.error_type,
            remarks=remarks,
            raw=detail.raw,
        )

    # ------------------------------------------------------------------
    # Batch fetch
    # ------------------------------------------------------------------

    def batch_get_details(self, process_instance_ids: list[str]) -> BatchFetchResult:
        """Fetch details for multiple approval instances.

        Includes a small delay between requests to respect DingTalk rate limits.
        """
        result = BatchFetchResult()
        for i, pid in enumerate(process_instance_ids):
            try:
                detail = self.get_detail(pid)
                result.succeeded.append(detail)
            except Exception as exc:
                logger.warning("batch_get_details failed for %s: %s", pid, exc)
                result.failed.append({"id": pid, "error": str(exc)})
            # Rate limit: 50ms delay between requests
            if i < len(process_instance_ids) - 1:
                time.sleep(0.05)
        return result

    # ------------------------------------------------------------------
    # View-model conversion
    # ------------------------------------------------------------------

    @staticmethod
    def to_workflow(detail: AdminWorkflowDetail) -> WorkflowDoc:
        """Convert an AdminWorkflowDetail into the template-facing WorkflowDoc."""
        return WorkflowDoc(
            title=detail.title,
            status=detail.status,
            originator=detail.originator_user_id,
            process_instance_id=detail.process_instance_id,
            form_data=detail.form_data,
            operation_records=detail.operation_records,
            attachments=[
                {
                    "field_name": a.field_name,
                    "file_name": a.file_name,
                    "file_id": a.file_id,
                    "download_url": a.download_url,
                    "file_size": a.file_size,
                    "component_type": a.component_type,
                }
                for a in detail.attachments
            ],
            comments=[
                {"user_id": c.user_id, "content": c.content, "timestamp": c.timestamp}
                for c in detail.comments
            ],
            comment_status=detail.comment_status,
            comment_error_type=detail.comment_error_type,
            remarks=[
                {
                    "user_id": remark.user_id,
                    "timestamp": remark.timestamp,
                    "content": remark.content,
                    "node_name": remark.node_name,
                    "operation_type": remark.operation_type,
                    "operation_result": remark.operation_result,
                    "comment_id": remark.comment_id,
                    "sources": list(remark.sources),
                }
                for remark in detail.remarks
            ],
            raw_json=detail.raw,
        )

    # ------------------------------------------------------------------
    # Business ID resolution
    # ------------------------------------------------------------------

    def resolve_business_id(
        self,
        business_id: str,
        *,
        process_code: str = "",
        start_time_ms: int = 0,
        end_time_ms: int = 0,
    ) -> str | None:
        """Find the processInstanceId for a given businessId."""
        cursor = 0
        while True:
            ids, next_cursor = self.list_instance_ids(
                process_code=process_code,
                start_time_ms=start_time_ms,
                end_time_ms=end_time_ms,
                size=20,
                cursor=cursor,
            )
            if not ids:
                break
            for iid in ids:
                try:
                    raw = self.get_instance_detail(iid)
                    if raw.get("business_id") == business_id:
                        logger.info("Found business_id %s -> %s", business_id, iid)
                        return iid
                except Exception:
                    continue
            if not next_cursor:
                break
            cursor = next_cursor
        return None

    # ------------------------------------------------------------------
    # Business ID date parsing
    # ------------------------------------------------------------------

    # DingTalk listids API lookback limit (empirically tested: 365 days)
    API_LOOKBACK_DAYS = 365

    @staticmethod
    def _parse_business_id_date(business_id: str) -> tuple[int, int] | None:
        """Extract creation date from businessId to narrow search window."""
        if len(business_id) < 8:
            return None
        try:
            date_part = business_id[:8]
            dt = datetime.datetime.strptime(date_part, "%Y%m%d").replace(
                tzinfo=datetime.timezone.utc
            )
            start = int(dt.timestamp() * 1000)
            end = int(dt.replace(hour=23, minute=59, second=59).timestamp() * 1000)
            return start, end
        except (ValueError, OSError):
            return None

    # ------------------------------------------------------------------
    # Fast resolution
    # ------------------------------------------------------------------

    def resolve_business_id_fast(
        self,
        business_id: str,
    ) -> str | None:
        """Resolve business_id intelligently.

        Strategy:
        1. If businessId encodes a date (YYYYMMDD...), check if it falls
           within the DingTalk API's 365-day lookback window.
           If yes, search only that day across all process codes.
        2. Otherwise fall back to scanning recent months (30-day chunks).
        3. Raises ValueError with a helpful message if the date is too old.
        """
        # Pre-check: is the business_id date within API lookback window?
        date_range = self._parse_business_id_date(business_id)
        if date_range:
            start_ms, _ = date_range
            cutoff_ms = int(
                (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=self.API_LOOKBACK_DAYS))
                .timestamp() * 1000
            )
            if start_ms < cutoff_ms:
                date_str = business_id[:4] + "-" + business_id[4:6] + "-" + business_id[6:8]
                raise ValueError(
                    f"工单号创建日期（{date_str}）超出钉钉 API 可查询范围"
                    f"（最近 {self.API_LOOKBACK_DAYS} 天）。"
                    f"请直接使用审批实例 ID 查询。获取方法："
                    f"在钉钉 OA 审批中打开该工单 → 浏览器地址栏中 procInsId= 后面的值"
                    f"即为审批实例 ID。"
                )

        process_codes = self.list_process_codes()
        if not process_codes:
            logger.warning("No process codes discovered; cannot resolve business_id")
            return None

        # Strategy 1: date-aware search (fast path)
        if date_range:
            start_ms, end_ms = date_range
            logger.info(
                "Resolving business_id=%s (date-aware) across %d codes",
                business_id, len(process_codes),
            )
            for pc in process_codes:
                result = self.resolve_business_id(
                    business_id,
                    process_code=pc,
                    start_time_ms=start_ms,
                    end_time_ms=end_ms,
                )
                if result:
                    return result
            return None

        # Strategy 2: scan recent months (30-day chunks, always ≤120 days)
        now = int(time.time() * 1000)
        chunk_ms = 30 * 24 * 3600 * 1000
        for month in range(3):
            end = now - month * chunk_ms
            start = now - (month + 1) * chunk_ms
            for pc in process_codes:
                result = self.resolve_business_id(
                    business_id,
                    process_code=pc,
                    start_time_ms=start,
                    end_time_ms=end,
                )
                if result:
                    return result
        return None

    # ------------------------------------------------------------------
    # Connection health check
    # ------------------------------------------------------------------

    def test_connection(self) -> tuple[bool, str]:
        """Validate AppKey/AppSecret by refreshing the access_token.

        Returns (ok, message). Unlike _ensure_token (which raises), this
        captures errors and reports them as a structured status.
        """
        try:
            self._ensure_token()
            return True, ""
        except Exception as exc:  # noqa: BLE001 — surfaced as connection status
            return False, str(exc)

    def test_capabilities(self, process_instance_id: str = "") -> DingTalkCapabilities:
        try:
            self._ensure_token()
            token = CapabilityStatus(status="ok")
        except Exception as exc:  # noqa: BLE001 - returned as capability status
            failed = CapabilityStatus(status="failed", message=str(exc))
            return DingTalkCapabilities(
                token=failed,
                approval_detail=CapabilityStatus(
                    status="not_tested", message="基础连接失败，未测试审批详情。"
                ),
                comments=CapabilityStatus(
                    status="not_tested", message="基础连接失败，未测试独立评论。"
                ),
            )

        if not process_instance_id:
            not_tested = CapabilityStatus(
                status="not_tested", message="需要审批实例 ID 才能验证。"
            )
            return DingTalkCapabilities(
                token=token,
                approval_detail=not_tested,
                comments=not_tested,
            )

        try:
            self.get_instance_detail(process_instance_id)
            approval_detail = CapabilityStatus(status="ok")
        except Exception as exc:  # noqa: BLE001 - returned as capability status
            approval_detail = CapabilityStatus(status="failed", message=str(exc))

        try:
            result = self.get_comments(process_instance_id)
            comment_status = {
                "available": "ok",
                "unavailable": "unavailable",
                "error": "failed",
            }[result.status]
            comments = CapabilityStatus(status=comment_status, message=result.message)
        except Exception as exc:  # noqa: BLE001 - returned as capability status
            comments = CapabilityStatus(status="failed", message=str(exc))

        return DingTalkCapabilities(
            token=token,
            approval_detail=approval_detail,
            comments=comments,
        )

    # ------------------------------------------------------------------
    # Recent instance listing (approximation of a pending/todo list)
    # ------------------------------------------------------------------

    def list_recent_instances(
        self,
        *,
        days: int = 7,
        limit: int = 50,
    ) -> list[AdminWorkflowDetail]:
        """List recently created approval instances across known process codes.

        DingTalk's /topapi/processinstance/listids is org-wide and scoped by
        process_code + time window — there is no per-user "pending approvals"
        API in this client. This method scans recent instances across all
        discovered process codes and is therefore an APPROXIMATION of the
        list produced by the former DWS `list-pending`/`list-initiated`.

        Results are deduplicated by process_instance_id and capped at *limit*.
        """
        now = int(time.time() * 1000)
        start = now - days * 24 * 3600 * 1000
        seen: set[str] = set()
        details: list[AdminWorkflowDetail] = []

        for code in self.list_process_codes():
            if len(details) >= limit:
                break
            try:
                ids, _ = self.list_instance_ids(
                    process_code=code,
                    start_time_ms=start,
                    end_time_ms=now,
                    size=min(limit, 20),
                )
            except Exception:
                logger.debug("list_instance_ids failed for code %s", code, exc_info=True)
                continue
            for iid in ids:
                if iid in seen:
                    continue
                seen.add(iid)
                try:
                    details.append(self.get_detail(iid))
                except Exception:
                    logger.debug("get_detail failed for %s", iid, exc_info=True)
                if len(details) >= limit:
                    break
        return details
