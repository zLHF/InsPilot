from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inspilot_cloud_baby.db import Base


class ProjectVisibility(str, enum.Enum):
    COMPANY_VISIBLE = "company_visible"
    PROJECT_MEMBERS = "project_members"
    RESTRICTED = "restricted"


class KnowledgeSensitivity(str, enum.Enum):
    PUBLIC_SUMMARY = "public_summary"
    PROJECT_RESTRICTED = "project_restricted"
    SENSITIVE = "sensitive"


class KnowledgeStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    ACTIVE = "active"
    ARCHIVED = "archived"
    CONFLICT = "conflict"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    visibility: Mapped[ProjectVisibility] = mapped_column(
        Enum(ProjectVisibility), nullable=False, default=ProjectVisibility.COMPANY_VISIBLE
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    memberships: Mapped[list[ProjectMember]] = relationship(back_populates="project")
    knowledge_items: Mapped[list[KnowledgeItem]] = relationship(back_populates="project")


class ProjectMember(Base):
    __tablename__ = "project_members"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    project_role: Mapped[str] = mapped_column(String(50), nullable=False)

    project: Mapped[Project] = relationship(back_populates="memberships")


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(80), nullable=False)
    sensitivity: Mapped[KnowledgeSensitivity] = mapped_column(Enum(KnowledgeSensitivity), nullable=False)
    status: Mapped[KnowledgeStatus] = mapped_column(Enum(KnowledgeStatus), nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped[Project | None] = relationship(back_populates="knowledge_items")
