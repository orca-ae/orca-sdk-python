from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._types import FileTypes
from .._utils import PropertyInfo

__all__ = ["CloudFunctionTriggerParams"]


class CloudFunctionTriggerParams(TypedDict, total=False):
    data: str
    """Inline input. Unlike the create/update `data` part this is text, not a file."""

    data_stream: Annotated[FileTypes, PropertyInfo(alias="dataStream")]
    """Input read from a file or stream instead of `data`. Sent as `dataStream`."""

    topic: str
    """The input topic to publish the trigger message to."""
