from __future__ import annotations

import enum
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectVisibilityDto(str, enum.Enum):
    COMPANY_VISIBLE = "company_visible"
    PROJECT_MEMBERS = "project_members"
    RESTRICTED = "restricted"


class KnowledgeSensitivityDto(str, enum.Enum):
    PUBLIC_SUMMARY = "public_summary"
    PROJECT_RESTRICTED = "project_restricted"
    SENSITIVE = "sensitive"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    visibility: ProjectVisibilityDto = ProjectVisibilityDto.COMPANY_VISIBLE
    summary: str = ""


class ProjectRead(BaseModel):
    id: UUID
    name: str
    visibility: ProjectVisibilityDto
    summary: str
