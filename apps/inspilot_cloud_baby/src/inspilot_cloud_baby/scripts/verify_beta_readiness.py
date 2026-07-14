from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass, field

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from inspilot_cloud_baby.audit import SECRET_SETTING_KEYS
from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.models import AppSetting, AuditLog, KnowledgeItem, KnowledgeStatus
from inspilot_cloud_baby.retrieval import retrieve_documents_explained

FIXED_QUERIES = ("西宁市", "浙江华重融资担保", "华重担保")


@dataclass(frozen=True)
class QueryVerification:
    query: str
    target_rank: int | None
    channels: tuple[str, ...] = ()
    matched_fields: tuple[str, ...] = ()
    elapsed_ms: int = 0


@dataclass(frozen=True)
class SecretScanReport:
    leaked_record_ids: tuple[str, ...] = ()

    def to_json(self) -> str:
        return json.dumps(
            {"leaked_record_ids": list(self.leaked_record_ids)},
            ensure_ascii=False,
        )


@dataclass(frozen=True)
class BetaReadinessReport:
    ok: bool
    business_id: str
    knowledge_id: str = ""
    errors: tuple[str, ...] = ()
    queries: tuple[QueryVerification, ...] = ()
    leaked_audit_record_ids: tuple[str, ...] = ()
    audit_action_counts: dict[str, int] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


def _rows(result):
    if hasattr(result, "scalars"):
        return result.scalars().all()
    return list(result)


def scan_audit_secrets(db: Session) -> SecretScanReport:
    setting_rows = list(
        db.execute(
            select(AppSetting.key, AppSetting.value).where(
                AppSetting.key.in_(SECRET_SETTING_KEYS)
            )
        )
    )
    secrets = [value for _key, value in setting_rows if value]
    audit_rows = _rows(db.execute(select(AuditLog)))
    leaked: list[str] = []
    for row in audit_rows:
        serialized = json.dumps(row.metadata_json or {}, ensure_ascii=False, default=str)
        if any(secret in serialized for secret in secrets):
            leaked.append(str(row.id))
    return SecretScanReport(leaked_record_ids=tuple(leaked))


def _audit_action_counts(db: Session) -> dict[str, int]:
    rows = _rows(db.execute(select(AuditLog)))
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.action] = counts.get(row.action, 0) + 1
    return counts


def verify_beta_readiness(*, business_id: str, db: Session) -> BetaReadinessReport:
    fixture = db.scalar(
        select(KnowledgeItem)
        .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
        .where(KnowledgeItem.source_type == "dingtalk_approval")
        .where(
            or_(
                KnowledgeItem.metadata_json["business_id"].as_string() == business_id,
                KnowledgeItem.title.ilike(f"%{business_id}%"),
                KnowledgeItem.body.ilike(f"%{business_id}%"),
            )
        )
    )
    if fixture is None:
        return BetaReadinessReport(
            ok=False,
            business_id=business_id,
            errors=("fixture_missing",),
        )
    if fixture.embedding is None:
        return BetaReadinessReport(
            ok=False,
            business_id=business_id,
            knowledge_id=str(fixture.id),
            errors=("embedding_missing",),
        )

    user = CurrentUser(user_id="system:beta-verifier", is_company_user=True)
    checks: list[QueryVerification] = []
    errors: list[str] = []
    for query in (*FIXED_QUERIES, business_id):
        started = time.perf_counter()
        results = retrieve_documents_explained(
            query=query,
            user=user,
            documents=[],
            limit=8,
            db=db,
        )
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        target = next((item for item in results if item.document.id == str(fixture.id)), None)
        check = QueryVerification(
            query=query,
            target_rank=target.evidence.final_rank if target else None,
            channels=target.evidence.channels if target else (),
            matched_fields=target.evidence.matched_fields if target else (),
            elapsed_ms=elapsed_ms,
        )
        checks.append(check)
        if target is None:
            errors.append(f"retrieval_missing:{query}")
        elif not check.channels or not check.matched_fields:
            errors.append(f"evidence_missing:{query}")
        if elapsed_ms > 5000:
            errors.append(f"latency_exceeded:{query}")

    secret_report = scan_audit_secrets(db)
    if secret_report.leaked_record_ids:
        errors.append("audit_secret_leak")
    return BetaReadinessReport(
        ok=not errors,
        business_id=business_id,
        knowledge_id=str(fixture.id),
        errors=tuple(errors),
        queries=tuple(checks),
        leaked_audit_record_ids=secret_report.leaked_record_ids,
        audit_action_counts=_audit_action_counts(db),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 InsPilot Beta 准入门槛")
    parser.add_argument("--business-id", required=True)
    args = parser.parse_args()
    with SessionLocal() as session:
        report = verify_beta_readiness(business_id=args.business_id, db=session)
    print(report.to_json())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
