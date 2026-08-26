from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["CloudKafkaOpenResponse", "CloudKafkaWorkerStatus", "CloudKafkaServerInfo", "CloudKafkaMessage"]

# Several Kafka Connect responses are declared as bare JSON objects: the contract
# names no properties, so the SDK hands back the decoded object rather than
# inventing a shape the server has not committed to.
CloudKafkaOpenResponse: TypeAlias = Dict[str, object]


class CloudKafkaWorkerStatus(BaseModel):
    """Health of the Kafka Connect worker itself, not of any one connector."""

    status: Optional[str] = None

    message: Optional[str] = None


class CloudKafkaServerInfo(BaseModel):
    """Identity of the Kafka Connect worker and the cluster it is attached to."""

    version: Optional[str] = None

    commit: Optional[str] = None

    kafka_cluster_id: Optional[str] = None


class CloudKafkaMessage(BaseModel):
    """A bare acknowledgement the worker returns for some mutating operations."""

    message: Optional[str] = None
