from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypeAlias

from .session import SessionAgentMember, SessionCacheCreationUsage
from .._models import BaseModel

__all__ = [
    "SessionThreadStatus",
    "SessionThreadStats",
    "SessionThreadUsage",
    "SessionThread",
]

SessionThreadStatus: TypeAlias = Literal["running", "idle", "rescheduling", "terminated"]


class SessionThreadStats(BaseModel):
    active_seconds: Optional[int] = None

    duration_seconds: Optional[int] = None

    startup_seconds: Optional[int] = None


class SessionThreadUsage(BaseModel):
    input_tokens: Optional[int] = None

    output_tokens: Optional[int] = None

    cache_read_input_tokens: Optional[int] = None

    cache_creation: Optional[SessionCacheCreationUsage] = None


class SessionThread(BaseModel):
    """One execution thread within a session.

    A session has one primary thread plus zero or more child threads spawned by a
    coordinator agent. Threads are never created through the SDK.
    """

    id: str

    type: Literal["session_thread"]

    session_id: str

    agent: SessionAgentMember
    """Agent snapshot taken when the thread was created."""

    parent_thread_id: Optional[str] = None
    """Null for the session's primary thread."""

    status: SessionThreadStatus

    stats: Optional[SessionThreadStats] = None

    usage: Optional[SessionThreadUsage] = None

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
