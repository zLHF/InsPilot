from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def list_projects() -> list[dict[str, str]]:
    return []
