from __future__ import annotations

from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .file_metadata import FileMetadata

__all__ = ["SessionFile", "DeletedSessionFile"]

SessionFile: TypeAlias = FileMetadata
"""Metadata for a file attached to a session.

A session file is an ordinary stored file surfaced through the session that owns
it, so it carries the same shape as `FileMetadata`; the session id stays in the
request path so the server validates ownership on every call.
"""


class DeletedSessionFile(BaseModel):
    id: str

    type: Literal["file_deleted"]
