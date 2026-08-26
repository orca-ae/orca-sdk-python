from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypeAlias, TypedDict

from .._models import BaseModel
from .cloud_connector_shared import (
    CloudOpenConfigMap,
    CloudProducerConfig,
    CloudRuntimeResources,
    CloudProcessingGuarantee,
    CloudProducerConfigParam,
    CloudRuntimeResourcesParam,
    CloudRuntimeExceptionInformation,
)

__all__ = [
    "CloudBatchSourceConfig",
    "CloudBatchSourceConfigParam",
    "CloudSourceConfig",
    "CloudSourceConfigParam",
    "CloudSourceInstanceStatus",
    "CloudSourceStatusInstance",
    "CloudSourceStatus",
    "CloudSourceNameList",
]


class CloudBatchSourceConfig(BaseModel):
    """Discovery settings for a source that runs in batches rather than continuously."""

    discoveryTriggererClassName: Optional[str] = None

    discoveryTriggererConfig: Optional[CloudOpenConfigMap] = None


class CloudBatchSourceConfigParam(TypedDict, total=False):
    discoveryTriggererClassName: str

    discoveryTriggererConfig: CloudOpenConfigMap


class CloudSourceConfig(BaseModel):
    """A registered source connector's configuration.

    Field names are camelCase because the connector registry serves them that way;
    per `AGENTS.md` section 5 the SDK mirrors the wire shape rather than renaming it,
    so these read the same here as in the contract and in the JSON.
    """

    tenant: Optional[str] = None

    namespace: Optional[str] = None

    name: Optional[str] = None

    className: Optional[str] = None

    topicName: Optional[str] = None
    """Topic the source publishes to."""

    producerConfig: Optional[CloudProducerConfig] = None

    serdeClassName: Optional[str] = None

    schemaType: Optional[str] = None

    configs: Optional[CloudOpenConfigMap] = None
    """Plugin-defined settings. The contract leaves the keys and values open."""

    secrets: Optional[CloudOpenConfigMap] = None
    """Plugin-defined secret references. Write-only on the server: reads redact values."""

    parallelism: Optional[int] = None

    processingGuarantees: Optional[CloudProcessingGuarantee] = None

    resources: Optional[CloudRuntimeResources] = None

    sourceType: Optional[str] = None

    archive: Optional[str] = None
    """Package the source runs from, e.g. a registry reference or a built-in name."""

    runtimeFlags: Optional[str] = None

    customRuntimeOptions: Optional[str] = None

    batchSourceConfig: Optional[CloudBatchSourceConfig] = None

    batchBuilder: Optional[str] = None

    logTopic: Optional[str] = None

    connection: Optional[str] = None
    """Named connection this source reads through."""

    snServiceAccount: Optional[str] = None


class CloudSourceConfigParam(TypedDict, total=False):
    tenant: str

    namespace: str

    name: str

    className: str

    topicName: str
    """Topic the source publishes to."""

    producerConfig: CloudProducerConfigParam

    serdeClassName: str

    schemaType: str

    configs: CloudOpenConfigMap
    """Plugin-defined settings. The contract leaves the keys and values open."""

    secrets: CloudOpenConfigMap
    """Plugin-defined secret references. Write-only on the server: reads redact values."""

    parallelism: int

    processingGuarantees: CloudProcessingGuarantee

    resources: CloudRuntimeResourcesParam

    sourceType: str

    archive: str
    """Package the source runs from, e.g. a registry reference or a built-in name."""

    runtimeFlags: str

    customRuntimeOptions: str

    batchSourceConfig: CloudBatchSourceConfigParam

    batchBuilder: str

    logTopic: str

    connection: str
    """Named connection this source reads through."""

    snServiceAccount: str


class CloudSourceInstanceStatus(BaseModel):
    """Runtime counters for one source connector instance."""

    running: Optional[bool] = None

    error: Optional[str] = None

    numRestarts: Optional[int] = None

    numReceivedFromSource: Optional[int] = None

    numSystemExceptions: Optional[int] = None

    latestSystemExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    numSourceExceptions: Optional[int] = None

    latestSourceExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    numWritten: Optional[int] = None

    lastReceivedTime: Optional[int] = None

    workerId: Optional[str] = None


class CloudSourceStatusInstance(BaseModel):
    """One entry of the aggregate status: an instance id and that instance's counters."""

    instanceId: Optional[int] = None

    status: Optional[CloudSourceInstanceStatus] = None


class CloudSourceStatus(BaseModel):
    """Aggregate status across every instance of a source connector."""

    numInstances: Optional[int] = None

    numRunning: Optional[int] = None

    instances: Optional[List[CloudSourceStatusInstance]] = None


CloudSourceNameList: TypeAlias = List[str]
