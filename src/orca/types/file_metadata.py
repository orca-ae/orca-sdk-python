from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "FileSessionScope",
    "SessionScopedFileMetadata",
    "AgentFileMetadata",
    "FileMetadata",
    "DeletedFile",
]


class FileSessionScope(BaseModel):
    type: Literal["session"]

    id: str


class SessionScopedFileMetadata(BaseModel):
    id: str

    created_at: str

    filename: str

    mime_type: str

    size_bytes: int

    type: Literal["file"]

    downloadable: Optional[bool] = None

    scope: Optional[FileSessionScope] = None
    """Null for a file that is not bound to a session."""


class AgentFileMetadata(BaseModel):
    id: str

    filename: str

    mime_type: str

    size_bytes: int

    sha256: str

    metadata: Optional[Dict[str, str]] = None

    purpose: Literal["agent", "agent_output"]

    scope_id: Optional[str] = None
    """Session this file belongs to, or null for an unscoped upload."""

    downloadable: bool

    archived_at: Optional[str] = None
    """Present but null while the file is active."""

    created_at: str

    updated_at: str


FileMetadata: TypeAlias = Union[SessionScopedFileMetadata, AgentFileMetadata]
"""Which variant a deployment returns is a property of that deployment, not of the
call: the two shapes share `id`, `filename`, `mime_type`, and `size_bytes` but
differ everywhere else. There is no shared discriminator to switch on, so callers
that need a variant-only field should check for it rather than assume one."""


class DeletedFile(BaseModel):
    id: str

    type: Literal["file_deleted"]
