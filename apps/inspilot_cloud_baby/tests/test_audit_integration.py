import uuid

import pytest
from sqlalchemy import event, select

from inspilot_cloud_baby.audit import ADMIN_WEB_ACTOR, write_audit
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.models import AuditLog, Project, ProjectVisibility


def test_audit_flush_failure_rolls_back_business_change() -> None:
    project_id = uuid.uuid4()
    session = SessionLocal()

    @event.listens_for(session, "before_flush")
    def fail_audit_flush(current_session, _flush_context, _instances) -> None:
        if any(isinstance(obj, AuditLog) for obj in current_session.new):
            raise RuntimeError("audit write failed")

    try:
        project = Project(
            id=project_id,
            name=f"audit-rollback-{project_id}",
            visibility=ProjectVisibility.RESTRICTED,
            summary="",
        )
        session.add(project)
        write_audit(
            session,
            actor_user_id=ADMIN_WEB_ACTOR,
            action="project.create",
            resource_type="project",
            resource_id=str(project_id),
        )
        with pytest.raises(RuntimeError, match="audit write failed"):
            session.commit()
        session.rollback()
    finally:
        event.remove(session, "before_flush", fail_audit_flush)
        session.close()

    with SessionLocal() as verify:
        assert verify.scalar(select(Project).where(Project.id == project_id)) is None
