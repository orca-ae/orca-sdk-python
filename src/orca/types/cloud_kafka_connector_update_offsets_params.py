from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .cloud_kafka_connector import CloudKafkaConnectorOffsetParam

__all__ = ["CloudKafkaConnectorUpdateOffsetsParams"]


class CloudKafkaConnectorUpdateOffsetsParams(TypedDict, total=False):
    offsets: List[CloudKafkaConnectorOffsetParam]
    """The offsets to write. The connector must be stopped for the worker to accept them."""
