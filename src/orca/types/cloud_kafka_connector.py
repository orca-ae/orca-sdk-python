from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from .._models import BaseModel
from .cloud_kafka_shared import CloudKafkaOpenResponse

__all__ = [
    "CloudKafkaConnectorType",
    "CloudKafkaConnectorTaskID",
    "CloudKafkaConnectorInfo",
    "CloudKafkaConnectorState",
    "CloudKafkaTaskState",
    "CloudKafkaConnectorStateInfo",
    "CloudKafkaTaskInfo",
    "CloudKafkaTaskInfoList",
    "CloudKafkaConnectorOffset",
    "CloudKafkaConnectorOffsetParam",
    "CloudKafkaConnectorOffsets",
    "CloudKafkaConnectorConfig",
]

# Kafka Connect field names are snake_case on the wire, so the models below mirror
# that rather than the camelCase used by the connector registry.
CloudKafkaConnectorType: TypeAlias = Literal["source", "sink", "unknown"]

# A connector's configuration is a flat string map: Kafka Connect stores every
# value as a string, whatever the plugin later parses it into.
CloudKafkaConnectorConfig: TypeAlias = Dict[str, str]


class CloudKafkaConnectorTaskID(BaseModel):
    """Identifies one task by its connector and index."""

    connector: Optional[str] = None

    task: Optional[int] = None


class CloudKafkaConnectorInfo(BaseModel):
    """A connector's name, configuration, and the tasks it has been split into."""

    name: Optional[str] = None

    config: Optional[CloudKafkaConnectorConfig] = None

    tasks: Optional[List[CloudKafkaConnectorTaskID]] = None

    type: Optional[CloudKafkaConnectorType] = None


class CloudKafkaConnectorState(BaseModel):
    """Where the connector itself is running and what state it reports."""

    state: Optional[str] = None

    worker_id: Optional[str] = None

    msg: Optional[str] = None

    trace: Optional[str] = None
    """Stack trace, present when the connector failed."""


class CloudKafkaTaskState(BaseModel):
    """Where one task is running and what state it reports."""

    id: Optional[int] = None

    state: Optional[str] = None

    worker_id: Optional[str] = None

    msg: Optional[str] = None

    trace: Optional[str] = None
    """Stack trace, present when the task failed."""


class CloudKafkaConnectorStateInfo(BaseModel):
    """Status of a connector and each of its tasks."""

    name: Optional[str] = None

    connector: Optional[CloudKafkaConnectorState] = None

    tasks: Optional[List[CloudKafkaTaskState]] = None

    type: Optional[CloudKafkaConnectorType] = None


class CloudKafkaTaskInfo(BaseModel):
    """One task's identity paired with the configuration the worker gave it."""

    id: Optional[CloudKafkaConnectorTaskID] = None

    config: Optional[CloudKafkaConnectorConfig] = None


class CloudKafkaConnectorOffset(BaseModel):
    """One source partition and the offset recorded for it.

    Both halves are plugin-defined -- the contract fixes neither their keys nor
    their value types -- so they stay open objects.
    """

    partition: Optional[CloudKafkaOpenResponse] = None

    offset: Optional[CloudKafkaOpenResponse] = None


class CloudKafkaConnectorOffsetParam(TypedDict, total=False):
    partition: Dict[str, object]

    offset: Dict[str, object]


class CloudKafkaConnectorOffsets(BaseModel):
    """Every offset the worker holds for a connector."""

    offsets: Optional[List[CloudKafkaConnectorOffset]] = None


CloudKafkaTaskInfoList: TypeAlias = List[CloudKafkaTaskInfo]
