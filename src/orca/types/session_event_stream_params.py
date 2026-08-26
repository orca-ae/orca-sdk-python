from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = ["SessionEventStreamParams", "SessionEventDelta"]

SessionEventDelta: TypeAlias = Literal["agent.message", "agent.thinking"]


class SessionEventStreamParams(TypedDict, total=False):
    from_cursor: str
    """Resume after this event id instead of starting at the live edge."""

    subpath: str

    event_deltas: Union[SessionEventDelta, List[SessionEventDelta]]
    """Event types to receive as incremental deltas rather than only when complete."""
