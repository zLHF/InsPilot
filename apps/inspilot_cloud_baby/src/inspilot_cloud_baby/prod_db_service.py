"""Production database service — read-only SQL Server connection for NL2SQL.

Mirrors chat_service.py: lazy singleton, env>DB config merge, graceful disable.
Uses pymssql (pure-Python, no ODBC needed). ALL queries are read-only with
strict safety guards (SELECT-only, forced LIMIT, timeout).
"""
from __future__ import annotations

import logging
import re

from inspilot_cloud_baby.config import settings

logger = logging.getLogger(__name__)

# Safety: reject any SQL that contains write/dangerous keywords
_FORBIDDEN_RE = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|exec|execute|"
    r"merge|grant|revoke|backup|restore|sp_|xp_|shutdown)\b",
    re.IGNORECASE,
)
_MAX_ROWS = 50


def _load_db_settings() -> dict[str, str]:
    """Load prod DB config from the app_settings table."""
    try:
        from inspilot_cloud_baby.db import SessionLocal
        from inspilot_cloud_baby.models import AppSetting

        with SessionLocal() as session:
            rows = session.query(AppSetting).filter(
                AppSetting.key.in_([
                    "prod_db_host", "prod_db_port", "prod_db_name",
                    "prod_db_user", "prod_db_password",
                ])
            ).all()
            return {r.key: r.value for r in rows}
    except Exception:
        logger.debug("Failed to load prod DB settings from DB", exc_info=True)
        return {}


def get_prod_db_config() -> dict:
    """Merge env > DB > default for prod DB config."""
    db = _load_db_settings()
    port = db.get("prod_db_port", "").strip() or settings.prod_db_port
    return {
        "host": settings.prod_db_host or db.get("prod_db_host", ""),
        "port": int(port) if port else 1433,
        "database": settings.prod_db_name or db.get("prod_db_name", ""),
        "user": settings.prod_db_user or db.get("prod_db_user", ""),
        "password": settings.prod_db_password or db.get("prod_db_password", ""),
    }


class ProdDBService:
    """Read-only SQL Server (pymssql) connection wrapper."""

    def __init__(self, *, host: str, port: int, database: str, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        if not host or not database or not user:
            logger.warning("ProdDBService created without full config — disabled")
            self._conn_params = None
        else:
            self._conn_params = {
                "server": host,
                "port": port,
                "database": database,
                "user": user,
                "password": password,
                "timeout": 10,        # connection timeout (seconds)
                "login_timeout": 10,
                "charset": "utf8",
                "as_dict": True,
            }

    @property
    def available(self) -> bool:
        return self._conn_params is not None

    def test_connection(self) -> tuple[bool, str]:
        """Test connectivity with a simple SELECT 1."""
        if not self.available:
            return False, "数据库连接未配置"
        try:
            import pymssql
            with pymssql.connect(**self._conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 AS ok")
                    row = cur.fetchone()
                    if row and row.get("ok") == 1:
                        return True, f"连接成功。服务器 {self._host}:{self._port}，数据库 {self._database}"
        except Exception as exc:  # noqa: BLE001 — surfaced to user
            return False, f"连接失败：{exc}"
        return False, "未知错误"

    def execute_query(self, sql: str, *, max_rows: int = _MAX_ROWS) -> list[dict]:
        """Execute a read-only SELECT query and return rows as dicts.

        Safety: rejects non-SELECT statements, forces TOP clause to limit rows.
        Raises ValueError for unsafe SQL.
        """
        if not self.available:
            raise RuntimeError("数据库未配置")

        sql_stripped = sql.strip().rstrip(";")

        # Safety: reject forbidden keywords
        if _FORBIDDEN_RE.search(sql_stripped):
            raise ValueError("SQL 包含禁止的关键词，只允许 SELECT 查询")

        # Safety: must start with SELECT (after optional WITH for CTE)
        if not re.match(r"^(select|with)\b", sql_stripped, re.IGNORECASE):
            raise ValueError("只允许 SELECT 查询")

        # Inject TOP clause if not present (SQL Server syntax)
        if not re.search(r"\btop\b", sql_stripped, re.IGNORECASE):
            # Insert TOP N after SELECT
            sql_stripped = re.sub(r"^(select)\b", "SELECT TOP " + str(max_rows), sql_stripped, count=1, flags=re.IGNORECASE)

        logger.info("Executing prod DB query: %s", sql_stripped[:200])
        try:
            import pymssql
            with pymssql.connect(**self._conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_stripped)
                    rows = cur.fetchall()
            return rows[:max_rows]
        except Exception as exc:
            logger.error("Prod DB query failed: %s", exc, exc_info=True)
            raise


_service: ProdDBService | None = None


def get_prod_db_service() -> ProdDBService:
    """Lazy singleton — reset _service to None to force reload after config change."""
    global _service
    if _service is None:
        cfg = get_prod_db_config()
        _service = ProdDBService(
            host=cfg["host"],
            port=cfg["port"],
            database=cfg["database"],
            user=cfg["user"],
            password=cfg["password"],
        )
    return _service
