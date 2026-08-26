from __future__ import annotations

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SkillVersion", "DeletedSkillVersion"]


class SkillVersion(BaseModel):
    id: str

    type: Literal["skill_version"]

    skill_id: str

    name: str

    description: str

    directory: str
    """Bundle directory the version was packaged from."""

    version: str
    """Decimal version string, the same value used in the version path segment."""

    created_at: str


class DeletedSkillVersion(BaseModel):
    id: str
    """The version string, not the `skill_version` object id.

    A version is addressed by its number everywhere, so the tombstone echoes that
    rather than the surrogate id carried by `SkillVersion.id`.
    """

    type: Literal["skill_version_deleted"]
