# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import List, Optional

from .._models import BaseModel
from .session_event import SessionEvent

__all__ = ["SessionEventSendResponse"]


class SessionEventSendResponse(BaseModel):
    data: Optional[List[SessionEvent]] = None
    """The persisted representation of each event that was accepted."""
