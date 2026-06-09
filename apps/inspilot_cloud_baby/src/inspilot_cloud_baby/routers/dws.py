from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/dws", tags=["dws"])


class DwsPreviewRequest(BaseModel):
    workflow_id: str


class DwsPreviewResponse(BaseModel):
    workflow_id: str
    status: str


@router.post("/preview", response_model=DwsPreviewResponse)
def preview_dws(request: DwsPreviewRequest) -> DwsPreviewResponse:
    return DwsPreviewResponse(workflow_id=request.workflow_id, status="ready_for_manual_probe")
