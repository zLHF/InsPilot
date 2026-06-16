import logging

import sqlalchemy as sa
from fastapi import FastAPI

from inspilot_cloud_baby.db import Base, engine
from inspilot_cloud_baby.routers.admin import router as admin_router
from inspilot_cloud_baby.routers.chat import router as chat_router
from inspilot_cloud_baby.routers.health import router as health_router
from inspilot_cloud_baby.routers.ingest import router as ingest_router
from inspilot_cloud_baby.routers.projects import router as projects_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="InsPilot Cloud Baby Alpha")

    @app.on_event("startup")
    def _init_db() -> None:
        """Auto-create all tables on startup (alpha / PoC convenience)."""
        try:
            with engine.begin() as conn:
                conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables verified / created")
        except Exception:
            logger.warning("Could not create database tables", exc_info=True)
    app.include_router(health_router)
    app.include_router(projects_router)
    app.include_router(ingest_router)
    app.include_router(chat_router)
    app.include_router(admin_router)
    return app


app = create_app()
