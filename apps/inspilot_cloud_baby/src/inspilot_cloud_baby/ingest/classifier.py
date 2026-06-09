from __future__ import annotations

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
