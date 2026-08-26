from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes, SequenceNotStr

__all__ = ["SkillCreateParams"]


class SkillCreateParams(TypedDict, total=False):
    files: Required[SequenceNotStr[FileTypes]]
    """The skill bundle files.

    Sent as `multipart/form-data`; the whole bundle is uploaded in one request.
    """

    display_title: str
