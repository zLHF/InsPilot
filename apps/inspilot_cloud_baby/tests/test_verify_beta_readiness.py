import json
from types import SimpleNamespace
from unittest.mock import Mock

from inspilot_cloud_baby.scripts.verify_beta_readiness import (
    scan_audit_secrets,
    verify_beta_readiness,
)


def test_verifier_stops_when_fixture_is_missing() -> None:
    session = Mock()
    session.scalar.return_value = None

    report = verify_beta_readiness(
        business_id="202605281923000432811",
        db=session,
    )

    assert report.ok is False
    assert report.errors == ("fixture_missing",)


def test_secret_scan_reports_ids_without_secret_values() -> None:
    secret = "never-print-this-secret"
    session = Mock()
    session.execute.side_effect = [
        [("openai_api_key", secret)],
        [
            SimpleNamespace(id="safe", metadata_json={"changed_keys": ["openai_api_key"]}),
            SimpleNamespace(id="leaked", metadata_json={"value": secret}),
        ],
    ]

    report = scan_audit_secrets(session)
    payload = report.to_json()

    assert report.leaked_record_ids == ("leaked",)
    assert secret not in payload
    assert json.loads(payload)["leaked_record_ids"] == ["leaked"]
