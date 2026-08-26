from __future__ import annotations

from typing import List, Union
from typing_extensions import TypedDict

from .session_event_stream_params import SessionEventDelta

__all__ = ["SessionThreadEventStreamParams"]


class SessionThreadEventStreamParams(TypedDict, total=False):
    from_cursor: str
    """Resume after this event id instead of starting at the live edge."""

    event_deltas: Union[SessionEventDelta, List[SessionEventDelta]]
    """Event types to receive as incremental deltas rather than only when complete."""
