from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from .session_event import SessionEventInputParam

__all__ = ["SessionEventSendParams"]


class SessionEventSendParams(TypedDict, total=False):
    events: Required[List[SessionEventInputParam]]
