from __future__ import annotations

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
