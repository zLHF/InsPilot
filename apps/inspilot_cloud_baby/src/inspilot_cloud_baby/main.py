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
