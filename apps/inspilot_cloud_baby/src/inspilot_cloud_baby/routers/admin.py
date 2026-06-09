from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ingest")
def ingest_page(request: Request):
    return templates.TemplateResponse(request, "ingest.html")


@router.get("/dws")
def dws_page(request: Request):
    return templates.TemplateResponse(request, "dws.html")
