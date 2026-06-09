# InsPilot 云小宝 Alpha 阶段实施计划

> **给执行 Agent 的要求：** 实施本计划时必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，逐任务执行并用 checkbox（`- [ ]`）跟踪进度。

**目标：** 实现 InsPilot 云小宝的 Alpha 版本，跑通“文本对话 → 资料投喂 → 权限过滤检索 → 结构化输出 → DWS 钉钉流程导入 PoC”的主链路。

**架构：** Alpha 阶段采用模块化单体，先避免微服务复杂度。后端使用 FastAPI，结构化数据使用 PostgreSQL，附件 Alpha 阶段先落本地文件系统，DWS 通过独立 adapter 封装，知识检索先用可测试的关键词检索，后续再替换为向量检索或混合检索。所有外部能力（DWS、对象存储、向量检索、钉钉提交）都通过接口隔离，方便 PoC 后替换成正式实现。

**技术栈：** Python 3.12、FastAPI、SQLAlchemy 2、Alembic、Pydantic v2、PostgreSQL 16、pytest、Ruff、Jinja2、HTMX、本地文件存储、DWS CLI。

---

## 1. Alpha 范围

Alpha 包含：

- 文本对话入口。
- 附件上传和附件元数据记录。
- Top 10 项目知识库初始化。
- 轻量知识投喂：上传人少填，系统识别，用户确认。
- 项目开放级别：`company_visible`、`project_members`、`restricted`。
- 知识敏感级别：`public_summary`、`project_restricted`、`sensitive`。
- 按权限过滤的项目知识检索。
- 三类结构化输出：`change_request`、`new_requirement`、`system_issue`。
- DWS 按钉钉流程 ID / 工单号导入历史流程的 PoC。
- 最小后台页面：项目、知识投喂、DWS 导入结果。

Alpha 不包含：

- 语音、OCR、视频解析、ASR。
- 完整向量数据库和 embedding 管道。
- 生产级钉钉提交流转。
- 完整组织架构管理。
- 精准字段自动晋升事实。

## 2. 代码目录规划

当前仓库只有文档，没有应用代码。Alpha 工程新建在：

```text
apps/inspilot_cloud_baby/
```

目标目录：

```text
apps/inspilot_cloud_baby/
  pyproject.toml
  README.md
  alembic.ini
  alembic/
    env.py
    versions/
  src/inspilot_cloud_baby/
    __init__.py
    main.py
    config.py
    db.py
    models.py
    schemas.py
    auth.py
    permissions.py
    storage.py
    retrieval.py
    output_builder.py
    dws_adapter.py
    ingest/
      __init__.py
      classifier.py
      service.py
    routers/
      __init__.py
      health.py
      projects.py
      knowledge.py
      ingest.py
      chat.py
      dws.py
      admin.py
    templates/
      base.html
      projects.html
      knowledge.html
      ingest.html
      dws.html
  tests/
    conftest.py
    test_health.py
    test_models.py
    test_permissions.py
    test_ingest_classifier.py
    test_storage.py
    test_retrieval.py
    test_output_builder.py
    test_dws_adapter.py
    test_api_routes.py
    test_admin_pages.py
    test_alpha_contract.py
```

模块职责：

- `models.py`：SQLAlchemy 持久化模型。
- `schemas.py`：API 请求/响应 DTO 和枚举。
- `permissions.py`：项目开放级别 + 知识敏感级别的可见性判断。
- `storage.py`：附件存储抽象，Alpha 先使用本地文件。
- `retrieval.py`：Alpha 阶段关键词检索 + 权限过滤。
- `output_builder.py`：结构化输出 JSON 生成。
- `dws_adapter.py`：封装 DWS CLI 调用和结果解析。
- `ingest/classifier.py`：上传资料的规则分类器。
- `routers/*`：API 和后台页面路由。

## 3. 任务拆分

### Task 1：创建 Alpha 工程骨架

**目标：** 建立 FastAPI 工程、健康检查接口和测试框架。

**文件：**

- 新建：`apps/inspilot_cloud_baby/pyproject.toml`
- 新建：`apps/inspilot_cloud_baby/README.md`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/__init__.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/config.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/health.py`
- 新建：`apps/inspilot_cloud_baby/tests/conftest.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_health.py`

- [ ] **Step 1：创建 `pyproject.toml`**

```toml
[project]
name = "inspilot-cloud-baby"
version = "0.1.0"
description = "Alpha implementation of InsPilot Cloud Baby"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.0",
  "uvicorn[standard]>=0.30.0",
  "sqlalchemy>=2.0.30",
  "alembic>=1.13.0",
  "psycopg[binary]>=3.2.0",
  "pydantic-settings>=2.4.0",
  "jinja2>=3.1.0",
  "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.2.0",
  "httpx>=0.27.0",
  "ruff>=0.5.0",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py312"
```

- [ ] **Step 2：创建 FastAPI 入口**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`：

```python
from fastapi import FastAPI

from inspilot_cloud_baby.routers.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="InsPilot Cloud Baby Alpha")
    app.include_router(health_router)
    return app


app = create_app()
```

- [ ] **Step 3：创建配置文件**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/config.py`：

```python
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BUSINESS_ROBOT_", env_file=".env")

    database_url: str = "postgresql+psycopg://inspilot_cloud_baby:inspilot_cloud_baby@localhost:5432/inspilot_cloud_baby"
    attachment_root: Path = Path("./var/attachments")
    dws_binary: str = "dws"


settings = Settings()
```

- [ ] **Step 4：创建健康检查路由**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/health.py`：

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 5：创建健康检查测试**

`apps/inspilot_cloud_baby/tests/test_health.py`：

```python
from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_health_returns_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 6：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_health.py -v
```

期望：`1 passed`。

- [ ] **Step 7：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "chore: scaffold inspilot cloud baby alpha app"
```

### Task 2：实现核心数据模型

**目标：** 建立项目、项目成员、知识条目、开放级别、敏感级别等 Alpha 核心模型。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/db.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/models.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/schemas.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_models.py`

- [ ] **Step 1：创建数据库基础类**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/db.py`：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from inspilot_cloud_baby.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

- [ ] **Step 2：创建模型**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/models.py`：

```python
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

    memberships: Mapped[list["ProjectMember"]] = relationship(back_populates="project")
    knowledge_items: Mapped[list["KnowledgeItem"]] = relationship(back_populates="project")


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
```

- [ ] **Step 3：创建 DTO**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/schemas.py`：

```python
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectVisibilityDto(StrEnum):
    COMPANY_VISIBLE = "company_visible"
    PROJECT_MEMBERS = "project_members"
    RESTRICTED = "restricted"


class KnowledgeSensitivityDto(StrEnum):
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
```

- [ ] **Step 4：创建模型测试**

`apps/inspilot_cloud_baby/tests/test_models.py`：

```python
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility


def test_project_visibility_values_match_prd_terms() -> None:
    assert ProjectVisibility.COMPANY_VISIBLE.value == "company_visible"
    assert ProjectVisibility.PROJECT_MEMBERS.value == "project_members"
    assert ProjectVisibility.RESTRICTED.value == "restricted"


def test_knowledge_sensitivity_values_match_prd_terms() -> None:
    assert KnowledgeSensitivity.PUBLIC_SUMMARY.value == "public_summary"
    assert KnowledgeSensitivity.PROJECT_RESTRICTED.value == "project_restricted"
    assert KnowledgeSensitivity.SENSITIVE.value == "sensitive"
```

- [ ] **Step 5：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_models.py -v
```

期望：`2 passed`。

- [ ] **Step 6：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add alpha domain models"
```

### Task 3：实现知识可见性判断

**目标：** 实现“项目开放级别 + 知识敏感级别 + 用户项目关系”的读取权限判断。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/auth.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/permissions.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_permissions.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_permissions.py`：

```python
from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.permissions import can_read_knowledge


def test_company_user_can_read_public_summary_in_company_visible_project() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())

    assert can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
    )


def test_company_user_cannot_read_restricted_item_without_membership() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())

    assert not can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
    )


def test_project_member_can_read_project_restricted_item() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})

    assert can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.PROJECT_MEMBERS,
        sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
    )


def test_sensitive_item_requires_explicit_sensitive_grant() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})

    assert not can_read_knowledge(
        user=user,
        project_id="p1",
        project_visibility=ProjectVisibility.COMPANY_VISIBLE,
        sensitivity=KnowledgeSensitivity.SENSITIVE,
    )
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_permissions.py -v
```

期望：因为 `auth.py` 或 `permissions.py` 不存在而失败。

- [ ] **Step 3：实现用户上下文和权限判断**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/auth.py`：

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CurrentUser:
    user_id: str
    is_company_user: bool
    project_ids: set[str] = field(default_factory=set)
    can_view_sensitive: bool = False
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/permissions.py`：

```python
from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility


def can_read_knowledge(
    *,
    user: CurrentUser,
    project_id: str | None,
    project_visibility: ProjectVisibility | None,
    sensitivity: KnowledgeSensitivity,
) -> bool:
    if sensitivity == KnowledgeSensitivity.SENSITIVE:
        return user.can_view_sensitive and project_id in user.project_ids

    if sensitivity == KnowledgeSensitivity.PROJECT_RESTRICTED:
        return project_id is not None and project_id in user.project_ids

    if sensitivity == KnowledgeSensitivity.PUBLIC_SUMMARY:
        if project_visibility == ProjectVisibility.COMPANY_VISIBLE:
            return user.is_company_user
        return project_id is not None and project_id in user.project_ids

    return False
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_permissions.py -v
```

期望：`4 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add knowledge permission filtering"
```

### Task 4：实现轻量资料投喂分类器

**目标：** 上传资料后，系统自动给出资料类型、建议归属、敏感级别和敏感命中项。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/ingest/__init__.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/ingest/classifier.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_ingest_classifier.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_ingest_classifier.py`：

```python
from inspilot_cloud_baby.ingest.classifier import classify_material


def test_classifies_fee_table_as_project_restricted() -> None:
    result = classify_material(
        filename="华南车险项目费率表.xlsx",
        text="机构类型：经纪公司\n付费类型：平台代收\n费率：2.5%\n接口编号：POLICY_001",
    )

    assert result.material_type == "rate_table"
    assert result.suggested_scope == "project"
    assert result.sensitivity == "project_restricted"
    assert "费率" in result.detected_sensitive_terms
    assert "接口编号" in result.detected_sensitive_terms


def test_classifies_common_template_as_public_candidate() -> None:
    result = classify_material(
        filename="需求提单模板.md",
        text="本模板用于描述背景、目标、影响范围、验收标准。",
    )

    assert result.material_type == "operation_guide"
    assert result.suggested_scope == "public"
    assert result.sensitivity == "public_summary"


def test_detects_pii_as_sensitive() -> None:
    result = classify_material(
        filename="问题截图说明.txt",
        text="客户手机号 13800138000，身份证号 110101199001011234。",
    )

    assert result.sensitivity == "sensitive"
    assert "手机号" in result.detected_sensitive_terms
    assert "身份证号" in result.detected_sensitive_terms
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_ingest_classifier.py -v
```

期望：因为 `inspilot_cloud_baby.ingest.classifier` 不存在而失败。

- [ ] **Step 3：实现分类器**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/ingest/__init__.py`：

```python
"""Knowledge ingestion helpers."""
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/ingest/classifier.py`：

```python
from pydantic import BaseModel


class ClassificationResult(BaseModel):
    material_type: str
    suggested_scope: str
    sensitivity: str
    detected_sensitive_terms: list[str]


SENSITIVE_PATTERNS = {
    "手机号": ["手机号", "手机", "138", "139", "137"],
    "身份证号": ["身份证", "110101", "证件"],
    "费率": ["费率", "%"],
    "接口编号": ["接口编号", "API", "回调"],
    "合同": ["合同", "协议"],
    "聊天记录": ["聊天记录", "群聊"],
}


def classify_material(*, filename: str, text: str) -> ClassificationResult:
    combined = f"{filename}\n{text}"
    detected = [
        label
        for label, patterns in SENSITIVE_PATTERNS.items()
        if any(pattern in combined for pattern in patterns)
    ]

    if "费率" in combined or "接口编号" in combined:
        material_type = "rate_table"
        suggested_scope = "project"
    elif "模板" in combined or "标准" in combined:
        material_type = "operation_guide"
        suggested_scope = "public"
    elif "技术方案" in combined or "直连" in combined or "跳转" in combined:
        material_type = "technical_solution"
        suggested_scope = "project"
    else:
        material_type = "project_note"
        suggested_scope = "project"

    if "手机号" in detected or "身份证号" in detected:
        sensitivity = "sensitive"
    elif detected:
        sensitivity = "project_restricted"
    else:
        sensitivity = "public_summary" if suggested_scope == "public" else "project_restricted"

    return ClassificationResult(
        material_type=material_type,
        suggested_scope=suggested_scope,
        sensitivity=sensitivity,
        detected_sensitive_terms=detected,
    )
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_ingest_classifier.py -v
```

期望：`3 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: classify uploaded knowledge materials"
```

### Task 5：实现附件本地存储

**目标：** Alpha 阶段先把附件安全写到配置目录，避免路径穿越。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/storage.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_storage.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_storage.py`：

```python
from pathlib import Path

from inspilot_cloud_baby.storage import LocalAttachmentStorage


def test_local_storage_writes_file_under_root(tmp_path: Path) -> None:
    storage = LocalAttachmentStorage(root=tmp_path)

    stored = storage.save(filename="需求说明.txt", content=b"hello")

    assert stored.path.exists()
    assert stored.path.read_bytes() == b"hello"
    assert stored.original_filename == "需求说明.txt"


def test_local_storage_removes_path_separators(tmp_path: Path) -> None:
    storage = LocalAttachmentStorage(root=tmp_path)

    stored = storage.save(filename="../secret.txt", content=b"safe")

    assert stored.path.parent == tmp_path
    assert stored.path.name.endswith("secret.txt")
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_storage.py -v
```

期望：因为 `inspilot_cloud_baby.storage` 不存在而失败。

- [ ] **Step 3：实现本地存储**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/storage.py`：

```python
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoredAttachment:
    original_filename: str
    path: Path


class LocalAttachmentStorage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, *, filename: str, content: bytes) -> StoredAttachment:
        safe_name = Path(filename).name
        target = self.root / f"{uuid.uuid4()}-{safe_name}"
        target.write_bytes(content)
        return StoredAttachment(original_filename=filename, path=target)
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_storage.py -v
```

期望：`2 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add alpha attachment storage"
```

### Task 6：实现 DWS 钉钉流程导入 PoC Adapter

**目标：** 封装 DWS CLI，支持按流程 ID 获取表单字段、评论、附件元数据。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dws_adapter.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_dws_adapter.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_dws_adapter.py`：

```python
import json

from inspilot_cloud_baby.dws_adapter import DwsAdapter


def test_builds_oa_process_instance_command() -> None:
    adapter = DwsAdapter(binary="dws")

    command = adapter.build_fetch_workflow_command(workflow_id="PROC-001")

    assert command == [
        "dws",
        "oa",
        "process-instance",
        "get",
        "--instance-id",
        "PROC-001",
        "--format",
        "json",
    ]


def test_parses_workflow_json() -> None:
    adapter = DwsAdapter(binary="dws")
    raw = json.dumps(
        {
            "result": {
                "title": "变更需求",
                "fields": [{"name": "项目", "value": "华南车险项目"}],
                "comments": [{"creator": "u1", "content": "需要补充费率"}],
                "attachments": [{"name": "费率表.xlsx", "downloadUrl": "https://example.test/file"}],
            }
        }
    )

    parsed = adapter.parse_workflow_payload(raw)

    assert parsed.title == "变更需求"
    assert parsed.fields["项目"] == "华南车险项目"
    assert parsed.comments[0]["content"] == "需要补充费率"
    assert parsed.attachments[0]["name"] == "费率表.xlsx"
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_dws_adapter.py -v
```

期望：因为 `inspilot_cloud_baby.dws_adapter` 不存在而失败。

- [ ] **Step 3：实现 DWS adapter**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/dws_adapter.py`：

```python
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
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_dws_adapter.py -v
```

期望：`2 passed`。

- [ ] **Step 5：人工验证 DWS 命令**

企业管理员授权后运行：

```bash
dws auth login
dws schema oa --format json
dws oa process-instance get --instance-id "PROC-EXAMPLE-001" --format json
```

期望：

- `dws auth login` 完成企业授权。
- `dws schema oa --format json` 能列出 OA 相关命令。
- 流程实例命令返回 JSON，包含表单字段、状态、评论或操作记录、附件元数据。
- 如果实际命令和计划假设不同，以 `dws schema oa --format json` 为准，更新 `DwsAdapter.build_fetch_workflow_command()` 和测试。

- [ ] **Step 6：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add dws workflow import adapter"
```

### Task 7：实现权限感知检索

**目标：** Alpha 先实现关键词检索，并在返回前应用知识可见性过滤。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_retrieval.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_retrieval.py`：

```python
from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.retrieval import KnowledgeDocument, retrieve_documents


def test_retrieval_filters_invisible_sensitive_documents() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())
    docs = [
        KnowledgeDocument(
            id="k1",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
            title="华南车险项目背景",
            body="项目采用跳转模式，适合快速上线。",
        ),
        KnowledgeDocument(
            id="k2",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.SENSITIVE,
            title="华南车险项目费率",
            body="详细费率 2.5%。",
        ),
    ]

    results = retrieve_documents(query="华南 车险 项目", user=user, documents=docs)

    assert [doc.id for doc in results] == ["k1"]


def test_retrieval_scores_matching_documents_first() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})
    docs = [
        KnowledgeDocument(
            id="k1",
            project_id="p1",
            project_visibility=ProjectVisibility.PROJECT_MEMBERS,
            sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
            title="系统问题",
            body="按钮不好找。",
        ),
        KnowledgeDocument(
            id="k2",
            project_id="p1",
            project_visibility=ProjectVisibility.PROJECT_MEMBERS,
            sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
            title="直连方案",
            body="直连 API 包含支付回调和出单回调。",
        ),
    ]

    results = retrieve_documents(query="直连 回调", user=user, documents=docs)

    assert [doc.id for doc in results] == ["k2", "k1"]
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_retrieval.py -v
```

期望：因为 `inspilot_cloud_baby.retrieval` 不存在而失败。

- [ ] **Step 3：实现检索**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/retrieval.py`：

```python
from dataclasses import dataclass

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.permissions import can_read_knowledge


@dataclass(frozen=True)
class KnowledgeDocument:
    id: str
    project_id: str | None
    project_visibility: ProjectVisibility | None
    sensitivity: KnowledgeSensitivity
    title: str
    body: str


def retrieve_documents(
    *, query: str, user: CurrentUser, documents: list[KnowledgeDocument], limit: int = 5
) -> list[KnowledgeDocument]:
    terms = [term for term in query.lower().split() if term]
    visible_docs = [
        document
        for document in documents
        if can_read_knowledge(
            user=user,
            project_id=document.project_id,
            project_visibility=document.project_visibility,
            sensitivity=document.sensitivity,
        )
    ]
    scored = sorted(
        visible_docs,
        key=lambda document: _score(document=document, terms=terms),
        reverse=True,
    )
    return scored[:limit]


def _score(*, document: KnowledgeDocument, terms: list[str]) -> int:
    text = f"{document.title} {document.body}".lower()
    return sum(1 for term in terms if term in text)
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_retrieval.py -v
```

期望：`2 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add permission-aware alpha retrieval"
```

### Task 8：实现结构化输出生成

**目标：** 支持三类 Alpha 输出 JSON：历史变更、新需求、系统问题。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/output_builder.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_output_builder.py`

- [ ] **Step 1：创建测试**

`apps/inspilot_cloud_baby/tests/test_output_builder.py`：

```python
from inspilot_cloud_baby.output_builder import build_structured_output


def test_builds_system_issue_output() -> None:
    output = build_structured_output(
        output_type="system_issue",
        confirmed={
            "project_name": "华南车险项目",
            "page": "保单查询页",
            "actual_result": "点击查询后报错",
            "expected_result": "返回保单列表",
        },
        pending=["复现账号", "错误截图原图"],
        sources=["knowledge:k1", "attachment:a1"],
    )

    assert output["output_type"] == "system_issue"
    assert output["confirmed"]["project_name"] == "华南车险项目"
    assert output["pending"] == ["复现账号", "错误截图原图"]
    assert output["sources"] == ["knowledge:k1", "attachment:a1"]
    assert output["schema_version"] == "1.0.0"


def test_rejects_unknown_output_type() -> None:
    try:
        build_structured_output(output_type="unknown", confirmed={}, pending=[], sources=[])
    except ValueError as exc:
        assert "unsupported output_type" in str(exc)
    else:
        raise AssertionError("expected ValueError")
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_output_builder.py -v
```

期望：因为 `inspilot_cloud_baby.output_builder` 不存在而失败。

- [ ] **Step 3：实现输出生成器**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/output_builder.py`：

```python
from typing import Any


SUPPORTED_OUTPUT_TYPES = {"change_request", "new_requirement", "system_issue"}


def build_structured_output(
    *, output_type: str, confirmed: dict[str, Any], pending: list[str], sources: list[str]
) -> dict[str, Any]:
    if output_type not in SUPPORTED_OUTPUT_TYPES:
        raise ValueError(f"unsupported output_type: {output_type}")

    return {
        "schema_version": "1.0.0",
        "output_type": output_type,
        "confirmed": confirmed,
        "pending": pending,
        "sources": sources,
    }
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_output_builder.py -v
```

期望：`2 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: build alpha structured outputs"
```

### Task 9：实现 Alpha API

**目标：** 暴露项目列表、投喂预览、聊天查询、DWS 导入预览接口。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/projects.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/ingest.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/dws.py`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_api_routes.py`

- [ ] **Step 1：创建 API 测试**

`apps/inspilot_cloud_baby/tests/test_api_routes.py`：

```python
from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_ingest_preview_returns_classification() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/ingest/preview",
        json={"filename": "需求提单模板.md", "text": "本模板用于描述背景、目标、影响范围。"},
    )

    assert response.status_code == 200
    assert response.json()["suggested_scope"] == "public"


def test_chat_query_returns_alpha_response() -> None:
    client = TestClient(create_app())

    response = client.post("/chat/query", json={"query": "华南车险项目是什么模式"})

    assert response.status_code == 200
    assert "answer" in response.json()
    assert response.json()["sources"] == []


def test_dws_preview_requires_workflow_id() -> None:
    client = TestClient(create_app())

    response = client.post("/dws/preview", json={})

    assert response.status_code == 422
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_api_routes.py -v
```

期望：因为路由不存在而失败。

- [ ] **Step 3：实现路由**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/ingest.py`：

```python
from pydantic import BaseModel
from fastapi import APIRouter

from inspilot_cloud_baby.ingest.classifier import ClassificationResult, classify_material

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestPreviewRequest(BaseModel):
    filename: str
    text: str


@router.post("/preview", response_model=ClassificationResult)
def preview_ingest(request: IngestPreviewRequest) -> ClassificationResult:
    return classify_material(filename=request.filename, text=request.text)
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/chat.py`：

```python
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatQueryRequest(BaseModel):
    query: str


class ChatQueryResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest) -> ChatQueryResponse:
    return ChatQueryResponse(
        answer=f"Alpha 已收到问题：{request.query}。知识库接入后将返回带来源的回答。",
        sources=[],
    )
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/dws.py`：

```python
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/dws", tags=["dws"])


class DwsPreviewRequest(BaseModel):
    workflow_id: str


class DwsPreviewResponse(BaseModel):
    workflow_id: str
    status: str


@router.post("/preview", response_model=DwsPreviewResponse)
def preview_dws(request: DwsPreviewRequest) -> DwsPreviewResponse:
    return DwsPreviewResponse(workflow_id=request.workflow_id, status="ready_for_manual_probe")
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/projects.py`：

```python
from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def list_projects() -> list[dict[str, str]]:
    return []
```

修改 `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`：

```python
from fastapi import FastAPI

from inspilot_cloud_baby.routers.chat import router as chat_router
from inspilot_cloud_baby.routers.dws import router as dws_router
from inspilot_cloud_baby.routers.health import router as health_router
from inspilot_cloud_baby.routers.ingest import router as ingest_router
from inspilot_cloud_baby.routers.projects import router as projects_router


def create_app() -> FastAPI:
    app = FastAPI(title="InsPilot Cloud Baby Alpha")
    app.include_router(health_router)
    app.include_router(projects_router)
    app.include_router(ingest_router)
    app.include_router(chat_router)
    app.include_router(dws_router)
    return app


app = create_app()
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_api_routes.py -v
```

期望：`3 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: expose alpha api routes"
```

### Task 10：实现最小后台页面

**目标：** 提供资料投喂页和 DWS 导入页，方便 Alpha 演示。

**文件：**

- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/base.html`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/ingest.html`
- 新建：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/dws.html`
- 修改：`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`
- 新建：`apps/inspilot_cloud_baby/tests/test_admin_pages.py`

- [ ] **Step 1：创建页面测试**

`apps/inspilot_cloud_baby/tests/test_admin_pages.py`：

```python
from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_ingest_admin_page_renders() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/ingest")

    assert response.status_code == 200
    assert "资料投喂" in response.text


def test_dws_admin_page_renders() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/dws")

    assert response.status_code == 200
    assert "DWS 流程导入" in response.text
```

- [ ] **Step 2：确认测试失败**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_admin_pages.py -v
```

期望：因为页面不存在而失败。

- [ ] **Step 3：实现后台路由和模板**

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/routers/admin.py`：

```python
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ingest")
def ingest_page(request: Request):
    return templates.TemplateResponse("ingest.html", {"request": request})


@router.get("/dws")
def dws_page(request: Request):
    return templates.TemplateResponse("dws.html", {"request": request})
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/base.html`：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>InsPilot 云小宝 Alpha</title>
  </head>
  <body>
    <main>
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/ingest.html`：

```html
{% extends "base.html" %}
{% block content %}
<h1>资料投喂</h1>
<form>
  <label>资料归属</label>
  <select name="scope">
    <option value="unknown">不确定，让系统识别</option>
    <option value="project">项目</option>
    <option value="public">公共</option>
    <option value="private">个人</option>
  </select>
  <label>备注</label>
  <textarea name="note"></textarea>
</form>
{% endblock %}
```

`apps/inspilot_cloud_baby/src/inspilot_cloud_baby/templates/dws.html`：

```html
{% extends "base.html" %}
{% block content %}
<h1>DWS 流程导入</h1>
<form>
  <label>钉钉流程 ID 或工单号</label>
  <input name="workflow_id">
</form>
{% endblock %}
```

修改 `apps/inspilot_cloud_baby/src/inspilot_cloud_baby/main.py`，引入 `admin_router`：

```python
from fastapi import FastAPI

from inspilot_cloud_baby.routers.admin import router as admin_router
from inspilot_cloud_baby.routers.chat import router as chat_router
from inspilot_cloud_baby.routers.dws import router as dws_router
from inspilot_cloud_baby.routers.health import router as health_router
from inspilot_cloud_baby.routers.ingest import router as ingest_router
from inspilot_cloud_baby.routers.projects import router as projects_router


def create_app() -> FastAPI:
    app = FastAPI(title="InsPilot Cloud Baby Alpha")
    app.include_router(health_router)
    app.include_router(projects_router)
    app.include_router(ingest_router)
    app.include_router(chat_router)
    app.include_router(dws_router)
    app.include_router(admin_router)
    return app


app = create_app()
```

- [ ] **Step 4：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest tests/test_admin_pages.py -v
```

期望：`2 passed`。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "feat: add alpha admin pages"
```

### Task 11：增加 Alpha 演示契约

**目标：** 用一个契约测试证明 Alpha 主入口都存在。

**文件：**

- 新建：`apps/inspilot_cloud_baby/scripts/alpha_demo.sh`
- 新建：`apps/inspilot_cloud_baby/tests/test_alpha_contract.py`

- [ ] **Step 1：创建契约测试**

`apps/inspilot_cloud_baby/tests/test_alpha_contract.py`：

```python
from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_alpha_contract_core_routes_exist() -> None:
    client = TestClient(create_app())

    assert client.get("/health").status_code == 200
    assert client.get("/projects").status_code == 200
    assert client.get("/admin/ingest").status_code == 200
    assert client.get("/admin/dws").status_code == 200
    assert client.post(
        "/ingest/preview",
        json={"filename": "技术方案.md", "text": "直连 API，支付回调，出单回调。"},
    ).status_code == 200
    assert client.post("/chat/query", json={"query": "直连方案怎么做"}).status_code == 200
```

- [ ] **Step 2：创建演示脚本**

`apps/inspilot_cloud_baby/scripts/alpha_demo.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python -m pytest tests/test_alpha_contract.py -v
python -m uvicorn inspilot_cloud_baby.main:app --host 127.0.0.1 --port 8000
```

- [ ] **Step 3：设置脚本权限**

```bash
chmod +x apps/inspilot_cloud_baby/scripts/alpha_demo.sh
```

- [ ] **Step 4：运行全量测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest -v
```

期望：全部测试通过。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby
git commit -m "test: add alpha demo contract"
```

### Task 12：Alpha 验证与运行说明

**目标：** 补充 README，给出本地运行、测试、DWS PoC 验证方法。

**文件：**

- 新建或修改：`apps/inspilot_cloud_baby/README.md`

- [ ] **Step 1：写入 README**

`apps/inspilot_cloud_baby/README.md`：

````markdown
# InsPilot 云小宝 Alpha

## 运行测试

```bash
python -m pytest -v
```

## 启动开发服务

```bash
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000
```

打开：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/admin/ingest`
- `http://127.0.0.1:8000/admin/dws`

## DWS PoC

企业管理员授权后运行：

```bash
dws auth login
dws schema oa --format json
dws oa process-instance get --instance-id "PROC-EXAMPLE-001" --format json
```

实际 OA 命令必须以 `dws schema oa --format json` 返回结果为准。如果命令名或参数不同，更新 `inspilot_cloud_baby.dws_adapter.DwsAdapter` 和对应测试。
````

- [ ] **Step 2：运行 lint**

```bash
cd apps/inspilot_cloud_baby
python -m ruff check .
```

期望：`All checks passed!`

- [ ] **Step 3：运行测试**

```bash
cd apps/inspilot_cloud_baby
python -m pytest -v
```

期望：全部测试通过。

- [ ] **Step 4：人工验证页面**

```bash
cd apps/inspilot_cloud_baby
python -m uvicorn inspilot_cloud_baby.main:app --reload --host 127.0.0.1 --port 8000
```

打开：

- `http://127.0.0.1:8000/admin/ingest`
- `http://127.0.0.1:8000/admin/dws`

期望：

- 资料投喂页包含“不确定，让系统识别 / 项目 / 公共 / 个人”选项。
- DWS 页面包含“钉钉流程 ID 或工单号”输入框。

- [ ] **Step 5：提交**

```bash
git add apps/inspilot_cloud_baby docs/superpowers/plans/2026-06-08-inspilot-cloud-baby-alpha.md
git commit -m "docs: add alpha implementation runbook"
```

## 4. Alpha 验收清单

- [ ] 文本对话 API 存在：`/chat/query`。
- [ ] 附件存储抽象存在，文件写入配置目录。
- [ ] 投喂分类器能识别公共候选、项目受限资料、敏感资料。
- [ ] 项目开放级别和知识敏感级别已进入代码模型。
- [ ] 权限过滤能阻止普通公司用户查看项目敏感资料。
- [ ] 检索只返回当前用户可见的知识。
- [ ] 结构化输出支持 `change_request`、`new_requirement`、`system_issue`。
- [ ] DWS adapter 能构造流程导入命令并解析流程 JSON。
- [ ] 企业授权后，已用一个真实钉钉流程实例验证 DWS 命令。
- [ ] 后台页面包含资料投喂和 DWS 导入入口。
- [ ] `python -m pytest -v` 全部通过。
- [ ] `python -m ruff check .` 通过。

## 5. 自检说明

PRD 覆盖关系：

- V2.4 的项目开放与敏感分层：Task 2、Task 3、Task 7、Task 9。
- 轻量知识投喂：Task 4、Task 5、Task 9、Task 10。
- DWS 历史流程导入 PoC：Task 6、Task 10。
- 结构化输出：Task 8。
- 最小后台页面：Task 10。

已明确排除：

- 语音、OCR、视频、多模态解析。
- 生产级钉钉提交流转。
- 完整向量检索。
- 完整组织架构管理。

主要风险：

- DWS 的真实 OA 命令可能与计划中的命令名不同。执行时必须先跑 `dws schema oa --format json`，再调整 adapter 和测试。
- 当前仓库没有应用代码，所以 Task 1 从零创建 `apps/inspilot_cloud_baby`。
