from __future__ import annotations

from typing_extensions import Required, TypedDict

from .trigger_shared import (
    TriggerAgentParam,
    TriggerSessionMode,
    TriggerSourceCreateParam,
    TriggerSessionCreateParam,
)

__all__ = ["TriggerCreateParams"]


class TriggerCreateParams(TypedDict, total=False):
    name: Required[str]

    agent: Required[TriggerAgentParam]

    session_mode: Required[TriggerSessionMode]

    source: Required[TriggerSourceCreateParam]

    session: Required[TriggerSessionCreateParam]

    replicas: int
    """Number of concurrent consumers. Positive; the server bounds the maximum."""

    paused: bool
    """Create the trigger already paused instead of active."""
