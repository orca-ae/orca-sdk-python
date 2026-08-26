from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .agent_shared import SkillSource

__all__ = ["Skill", "DeletedSkill"]


class Skill(BaseModel):
    id: str

    type: Literal["skill"]

    display_title: Optional[str] = None
    """Present but null when the uploaded bundle declared no title."""

    latest_version: Optional[str] = None
    """Decimal version string, null until the skill has its first version."""

    source: SkillSource
    """Where the skill came from. Values are fixed by the API contract."""

    created_at: str

    updated_at: str


class DeletedSkill(BaseModel):
    id: str

    type: Literal["skill_deleted"]
