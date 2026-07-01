import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sqlalchemy as sa
from fastapi import FastAPI

from inspilot_cloud_baby.db import Base, engine
from inspilot_cloud_baby.routers.admin import router as admin_router
from inspilot_cloud_baby.routers.chat import router as chat_router
from inspilot_cloud_baby.routers.health import router as health_router
from inspilot_cloud_baby.routers.ingest import router as ingest_router
from inspilot_cloud_baby.routers.projects import router as projects_router
from inspilot_cloud_baby.routers.query import router as query_router

logger = logging.getLogger(__name__)


def _init_db() -> None:
    """Auto-create all tables on startup (alpha / PoC convenience)."""
    try:
        with engine.begin() as conn:
            conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))
        Base.metadata.create_all(bind=engine)
        # create_all only builds the HNSW index on a *fresh* knowledge_items table;
        # for an existing table it is a no-op. Ensure it explicitly (idempotent) so
        # existing deployments also get fast ANN search instead of a seq scan.
        try:
            with engine.begin() as conn:
                conn.execute(sa.text(
                    "CREATE INDEX IF NOT EXISTS ix_knowledge_items_embedding_hnsw "
                    "ON knowledge_items USING hnsw (embedding vector_cosine_ops) "
                    "WITH (m = 16, ef_construction = 64)"
                ))
        except Exception:
            logger.warning("Could not ensure HNSW index on knowledge_items.embedding", exc_info=True)
        logger.info("Database tables verified / created")
    except Exception:
        logger.warning("Could not create database tables", exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    _init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="InsPilot Cloud Baby Alpha", lifespan=lifespan)

    app.include_router(health_router)
    app.include_router(projects_router)
    app.include_router(ingest_router)
    app.include_router(chat_router)
    app.include_router(query_router)
    app.include_router(admin_router)
    return app


app = create_app()
