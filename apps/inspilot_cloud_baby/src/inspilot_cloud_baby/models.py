from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

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

    embedding = mapped_column(Vector(1536), nullable=True)

    project: Mapped[Project | None] = relationship(back_populates="knowledge_items")

    # HNSW 索引：把向量检索从全表暴力扫描（O(n)）变为近似最近邻（O(log n)）。
    # 自动随 Base.metadata.create_all() 创建（需 pgvector 0.5+，pg16 镜像已支持）。
    __table_args__ = (
        Index(
            "ix_knowledge_items_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


class AppSetting(Base):
    """Key-value store for runtime-configurable application settings."""
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class QueryLog(Base):
    """对话检索查询日志 — 发现用户搜索习惯、零结果分析、检索评估的数据来源。

    每次 /chat/query 或 /chat/stream 落一行。重点看 zero_result=True 的行：
    那是用户搜了但召不回的问题，即"你不知道的关键词/黑话"，数据会直接告诉你。
    """
    __tablename__ = "query_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    doc_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)  # 召回的方案 id
    doc_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    prod_rows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    llm_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    zero_result: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """Security and permission audit trail for Beta hardening."""
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    metadata_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
