from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from inspilot_cloud_baby.ingest.classifier import ClassificationResult, classify_material

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestPreviewRequest(BaseModel):
    filename: str
    text: str


@router.post("/preview", response_model=ClassificationResult)
def preview_ingest(request: IngestPreviewRequest) -> ClassificationResult:
    return classify_material(filename=request.filename, text=request.text)
