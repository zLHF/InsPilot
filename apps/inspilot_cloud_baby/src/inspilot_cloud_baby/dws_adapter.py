from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DwsWorkflow:
    title: str
    status: str = ""
    originator: str = ""
    form_data: dict[str, str] = field(default_factory=dict)
    operation_records: list[dict] = field(default_factory=list)
    attachments: list[dict] = field(default_factory=list)
    comments: list[dict] = field(default_factory=list)
    raw_json: dict = field(default_factory=dict)


@dataclass(frozen=True)
class DwsAuthStatus:
    authenticated: bool
    message: str = ""


@dataclass(frozen=True)
class DwsApprovalSummary:
    """A single approval instance from list-pending or list-initiated."""
    process_instance_id: str
    title: str
    process_name: str
    status: str
    modified_time: str = ""
    accessible: bool = True


@dataclass(frozen=True)
class DwsConnectionResult:
    success: bool
    authenticated: bool
    binary_found: bool
    error: str = ""


class DwsAdapter:
    def __init__(
        self,
        binary: str = "dws",
        client_id: str = "",
        client_secret: str = "",
    ) -> None:
        self.binary = binary
        self.client_id = client_id
        self.client_secret = client_secret

    def _cmd(self, base_args: list[str]) -> list[str]:
        """Build a DWS command with optional client credentials."""
        cmd = [self.binary] + base_args
        if self.client_id:
            cmd += ["--client-id", self.client_id]
        if self.client_secret:
            cmd += ["--client-secret", self.client_secret]
        return cmd

    # ------------------------------------------------------------------
    # Connection & auth
    # ------------------------------------------------------------------

    def check_binary(self) -> bool:
        """Check if the DWS CLI binary exists and is executable."""
        try:
            result = subprocess.run(
                self._cmd(["--help"]),
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def check_auth(self) -> DwsAuthStatus:
        """Check the DWS CLI authentication status."""
        try:
            result = subprocess.run(
                self._cmd(["auth", "status", "--format", "json"]),
                capture_output=True,
                text=True,
                timeout=15,
            )
            payload = json.loads(result.stdout)
            return DwsAuthStatus(
                authenticated=payload.get("authenticated", False),
                message=payload.get("message", ""),
            )
        except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
            logger.warning("DWS auth check failed: %s", exc)
            return DwsAuthStatus(authenticated=False, message=str(exc))

    def test_connection(self) -> DwsConnectionResult:
        """Full connection test: binary + auth."""
        if not self.check_binary():
            return DwsConnectionResult(
                success=False,
                authenticated=False,
                binary_found=False,
                error=f"DWS CLI 工具未找到：请确认 '{self.binary}' 已安装并在 PATH 中",
            )
        auth = self.check_auth()
        if not auth.authenticated:
            return DwsConnectionResult(
                success=False,
                authenticated=False,
                binary_found=True,
                error=f"DWS CLI 未认证：{auth.message}。请运行 `dws auth login` 完成登录。",
            )
        return DwsConnectionResult(
            success=True,
            authenticated=True,
            binary_found=True,
        )

    # ------------------------------------------------------------------
    # List accessible approvals
    # ------------------------------------------------------------------

    def list_approvals(self) -> list[DwsApprovalSummary]:
        """List all approval instances accessible to the current user.

        Combines results from list-pending and list-initiated.
        Filters out items where detail API access fails (e.g. past approval nodes).
        Returns a list of DwsApprovalSummary objects.
        """
        results = []
        seen_ids = set()
        for cmd_name in ("list-pending", "list-initiated"):
            try:
                result = subprocess.run(
                    self._cmd(["oa", "approval", cmd_name, "--format", "json", "--size", "50"]),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    continue
                payload = json.loads(result.stdout)
                items = payload.get("result", {}).get("processInstanceList", [])
                for item in items:
                    iid = item.get("processInstanceId", "")
                    if not iid or iid in seen_ids:
                        continue
                    seen_ids.add(iid)
                    # Format timestamp
                    ts = item.get("gmtModified", 0)
                    modified = ""
                    if ts:
                        from datetime import datetime, timezone
                        try:
                            modified = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
                        except (ValueError, OSError):
                            pass
                    # Verify we can actually access the detail for this instance
                    # Some items appear in the list but detail API rejects them
                    # (e.g. approval has moved to a different node)
                    accessible = self._check_detail_accessible(iid)
                    results.append(DwsApprovalSummary(
                        process_instance_id=iid,
                        title=item.get("processInstanceTitle", ""),
                        process_name=item.get("processName", ""),
                        status=item.get("processInstanceStatus", ""),
                        modified_time=modified,
                        accessible=accessible,
                    ))
            except Exception:
                logger.warning("Failed to list approvals via %s", cmd_name, exc_info=True)
        return results

    def _check_detail_accessible(self, instance_id: str) -> bool:
        """Quick check if the detail API accepts this instance ID."""
        try:
            result = subprocess.run(
                self.build_fetch_workflow_command(workflow_id=instance_id),
                capture_output=True,
                text=True,
                timeout=15,
            )
            return result.returncode == 0
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Workflow fetching
    # ------------------------------------------------------------------

    def build_fetch_workflow_command(self, *, workflow_id: str) -> list[str]:
        """Build the CLI command to fetch an OA approval instance."""
        return self._cmd([
            "oa", "approval", "detail",
            "--instance-id", workflow_id,
            "--format", "json",
        ])

    def build_fetch_records_command(self, *, workflow_id: str) -> list[str]:
        """Build the CLI command to fetch operation records for an instance."""
        return self._cmd([
            "oa", "approval", "records",
            "--instance-id", workflow_id,
            "--format", "json",
        ])

    def fetch_workflow(self, *, workflow_id: str) -> DwsWorkflow:
        """Fetch an OA approval instance from DWS.

        Accepts either a processInstanceId (e.g. Uh6LpPqiSEiailbBafHsGw00...)
        or a businessId / 工单号 (e.g. 202511051648000128619).
        When a businessId is provided, it will search pending/initiated lists
        to resolve the corresponding processInstanceId.
        """
        # Step 1: Try directly as processInstanceId
        try:
            return self._fetch_by_instance_id(workflow_id)
        except Exception:
            pass

        # Step 2: If it looks like a business ID (all digits), search lists
        if workflow_id.isdigit():
            instance_id = self._resolve_business_id(workflow_id)
            if instance_id:
                return self._fetch_by_instance_id(instance_id)
            raise RuntimeError(
                f"未找到工单号 {workflow_id} 对应的审批实例。"
                f"请在钉钉 OA 中确认该工单号是否正确，或直接使用审批实例 ID。"
            )

        raise RuntimeError(f"DWS 获取流程详情失败: 流程 ID「{workflow_id}」不存在或无权限查看")

    def _fetch_by_instance_id(self, workflow_id: str) -> DwsWorkflow:
        """Fetch workflow detail + records by processInstanceId."""
        detail_result = subprocess.run(
            self.build_fetch_workflow_command(workflow_id=workflow_id),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if detail_result.returncode != 0:
            error_msg = self._parse_error(detail_result.stdout, detail_result.stderr)
            raise RuntimeError(f"DWS 获取流程详情失败: {error_msg}")

        detail_payload = json.loads(detail_result.stdout)

        # Also fetch operation records (which also contains the title)
        records_title = ""
        records_data = []
        try:
            records_result = subprocess.run(
                self.build_fetch_records_command(workflow_id=workflow_id),
                capture_output=True,
                text=True,
                timeout=30,
            )
            if records_result.returncode == 0:
                records_payload = json.loads(records_result.stdout)
                rec_result = records_payload.get("result", {})
                if isinstance(rec_result, dict):
                    records_title = rec_result.get("processInstanceTitle", "")
                    records_data = rec_result.get("operationRecords", [])
        except Exception:
            logger.warning("Failed to fetch operation records for %s", workflow_id, exc_info=True)

        return self._parse_detail(detail_payload, records_data, records_title)

    def _resolve_business_id(self, business_id: str) -> str | None:
        """Search pending and initiated lists to find processInstanceId by businessId."""
        for cmd_name in ("list-pending", "list-initiated"):
            try:
                result = subprocess.run(
                    self._cmd(["oa", "approval", cmd_name, "--format", "json"]),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    continue
                payload = json.loads(result.stdout)
                items = payload.get("result", {}).get("processInstanceList", [])
                for item in items:
                    inst_id = item.get("processInstanceId", "")
                    if not inst_id:
                        continue
                    # Fetch detail to check businessId
                    try:
                        detail = subprocess.run(
                            self.build_fetch_workflow_command(workflow_id=inst_id),
                            capture_output=True,
                            text=True,
                            timeout=15,
                        )
                        if detail.returncode == 0:
                            detail_data = json.loads(detail.stdout)
                            if detail_data.get("result", {}).get("businessId") == business_id:
                                return inst_id
                    except Exception:
                        continue
            except Exception:
                continue
        return None

    def fetch_workflow_safe(self, *, workflow_id: str) -> DwsWorkflow | str:
        """Fetch workflow, returning either the parsed workflow or an error message string."""
        try:
            return self.fetch_workflow(workflow_id=workflow_id)
        except Exception as exc:
            logger.error("DWS fetch failed for %s: %s", workflow_id, exc)
            return str(exc)

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_detail(self, payload: dict, records: list[dict], records_title: str = "") -> DwsWorkflow:
        """Parse the detail + records payload into a DwsWorkflow."""
        result = payload.get("result", {})

        # result might be a list (from mock) or dict
        if isinstance(result, list):
            if not result:
                return DwsWorkflow(title="(空结果)", raw_json=payload)
            result = result[0] if isinstance(result[0], dict) else {}

        # Title: prefer detail, fall back to records title
        title = result.get("title") or records_title or ""

        # Status
        status = result.get("status", "")

        # Originator
        originator = result.get("originatorUserId", "")

        # Extract form fields — handle both real format (formValueVOS) and test format (formComponentValues)
        form_values = result.get("formValueVOS", result.get("formComponentValues", []))
        form_data = {}
        attachments = []
        for fv in form_values:
            name = fv.get("name", fv.get("id", ""))
            value = fv.get("value", "")
            ctype = fv.get("componentType", "")
            if not name:
                continue
            # Extract attachments (DDAttachment type or name containing "附件")
            if ctype == "DDAttachment" or "附件" in name:
                attachments.append({
                    "name": name,
                    "componentType": ctype,
                    "value": str(value)[:500] if value else "",
                })
            elif value:
                # Clean up JSON array values for display
                if value.startswith("[") and value.endswith("]"):
                    try:
                        parsed = json.loads(value)
                        if isinstance(parsed, list):
                            value = ", ".join(str(v) for v in parsed)
                    except json.JSONDecodeError:
                        pass
                form_data[name] = value

        return DwsWorkflow(
            title=title,
            status=status,
            originator=originator,
            form_data=form_data,
            operation_records=records,
            attachments=attachments,
            raw_json=payload,
        )

    def _parse_error(self, stdout: str, stderr: str) -> str:
        """Extract a human-readable error from DWS CLI output."""
        try:
            payload = json.loads(stdout)
            err = payload.get("error", {})
            return err.get("message", err.get("hint", stdout[:200]))
        except json.JSONDecodeError:
            return stderr[:200] if stderr else stdout[:200]

    def parse_workflow_payload(self, raw_json: str) -> DwsWorkflow:
        """Parse a raw JSON string into a DwsWorkflow (for testing)."""
        payload = json.loads(raw_json)
        result = payload.get("result", {})
        return DwsWorkflow(
            title=result.get("title", ""),
            form_data={field["name"]: field.get("value", "") for field in result.get("fields", [])},
            operation_records=result.get("comments", []),
            attachments=result.get("attachments", []),
            raw_json=payload,
        )
