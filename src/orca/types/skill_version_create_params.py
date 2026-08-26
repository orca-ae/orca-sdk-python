from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes, SequenceNotStr

__all__ = ["SkillVersionCreateParams"]


class SkillVersionCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """The skill bundle files for the new version.

    Sent as `multipart/form-data`; a version is always a whole bundle, never a patch
    against the previous one.
    """
