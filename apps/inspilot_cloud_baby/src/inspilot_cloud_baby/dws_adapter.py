from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class DwsWorkflow:
    title: str
    fields: dict[str, str]
    comments: list[dict]
    attachments: list[dict]


class DwsAdapter:
    def __init__(self, binary: str = "dws") -> None:
        self.binary = binary

    def build_fetch_workflow_command(self, *, workflow_id: str) -> list[str]:
        return [
            self.binary,
            "oa",
            "process-instance",
            "get",
            "--instance-id",
            workflow_id,
            "--format",
            "json",
        ]

    def fetch_workflow(self, *, workflow_id: str) -> DwsWorkflow:
        completed = subprocess.run(
            self.build_fetch_workflow_command(workflow_id=workflow_id),
            check=True,
            capture_output=True,
            text=True,
        )
        return self.parse_workflow_payload(completed.stdout)

    def parse_workflow_payload(self, raw_json: str) -> DwsWorkflow:
        payload = json.loads(raw_json)
        result = payload["result"]
        return DwsWorkflow(
            title=result.get("title", ""),
            fields={field["name"]: field.get("value", "") for field in result.get("fields", [])},
            comments=result.get("comments", []),
            attachments=result.get("attachments", []),
        )
