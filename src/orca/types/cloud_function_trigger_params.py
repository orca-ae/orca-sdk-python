from __future__ import annotations

from typing_extensions import TypedDict

from .._types import FileTypes

__all__ = ["CloudFunctionTriggerParams"]


class CloudFunctionTriggerParams(TypedDict, total=False):
    data: str
    """Inline input. Unlike the create/update `data` part this is text, not a file."""

    dataStream: FileTypes
    """Input read from a file or stream instead of `data`."""

    topic: str
    """The input topic to publish the trigger message to."""
