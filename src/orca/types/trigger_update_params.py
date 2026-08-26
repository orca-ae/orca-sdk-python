from __future__ import annotations

from typing_extensions import TypedDict

from .trigger_shared import TriggerSessionMode, TriggerSourceUpdateParam, TriggerSessionUpdateParam

__all__ = ["TriggerUpdateParams"]


class TriggerUpdateParams(TypedDict, total=False):
    name: str

    session_mode: TriggerSessionMode

    source: TriggerSourceUpdateParam
    """Must carry its `type` discriminator, which cannot be changed."""

    session: TriggerSessionUpdateParam

    replicas: int
