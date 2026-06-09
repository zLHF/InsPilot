from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CurrentUser:
    user_id: str
    is_company_user: bool
    project_ids: set[str] = field(default_factory=set)
    can_view_sensitive: bool = False
