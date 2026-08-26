from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypeAlias, TypedDict

from .._models import BaseModel
from .cloud_connector_shared import (
    CloudOpenConfigMap,
    CloudConsumerConfig,
    CloudRuntimeResources,
    CloudConsumerConfigParam,
    CloudProcessingGuarantee,
    CloudSubscriptionPosition,
    CloudRuntimeResourcesParam,
    CloudRuntimeExceptionInformation,
)

__all__ = [
    "CloudSinkConfig",
    "CloudSinkConfigParam",
    "CloudSinkInstanceStatus",
    "CloudSinkStatusInstance",
    "CloudSinkStatus",
    "CloudSinkNameList",
]


class CloudSinkConfig(BaseModel):
    """A registered sink connector's configuration.

    Field names are camelCase because the connector registry serves them that way;
    per `AGENTS.md` section 5 the SDK mirrors the wire shape rather than renaming it,
    so these read the same here as in the contract and in the JSON.
    """

    tenant: Optional[str] = None

    namespace: Optional[str] = None

    name: Optional[str] = None

    className: Optional[str] = None

    sourceSubscriptionName: Optional[str] = None

    sourceSubscriptionPosition: Optional[CloudSubscriptionPosition] = None

    inputs: Optional[List[str]] = None

    topicToSerdeClassName: Optional[Dict[str, str]] = None

    topicsPattern: Optional[str] = None

    topicToSchemaType: Optional[Dict[str, str]] = None

    topicToSchemaProperties: Optional[Dict[str, str]] = None

    inputSpecs: Optional[Dict[str, CloudConsumerConfig]] = None
    """Per-input consumer settings, keyed by input name."""

    maxMessageRetries: Optional[int] = None

    deadLetterTopic: Optional[str] = None

    configs: Optional[CloudOpenConfigMap] = None
    """Plugin-defined settings. The contract leaves the keys and values open."""

    secrets: Optional[CloudOpenConfigMap] = None
    """Plugin-defined secret references. Write-only on the server: reads redact values."""

    parallelism: Optional[int] = None

    processingGuarantees: Optional[CloudProcessingGuarantee] = None

    retainOrdering: Optional[bool] = None

    retainKeyOrdering: Optional[bool] = None

    resources: Optional[CloudRuntimeResources] = None

    autoAck: Optional[bool] = None

    timeoutMs: Optional[int] = None

    negativeAckRedeliveryDelayMs: Optional[int] = None

    sinkType: Optional[str] = None

    archive: Optional[str] = None
    """Package the sink runs from, e.g. a registry reference or a built-in name."""

    cleanupSubscription: Optional[bool] = None

    runtimeFlags: Optional[str] = None

    customRuntimeOptions: Optional[str] = None

    transformFunction: Optional[str] = None

    transformFunctionClassName: Optional[str] = None

    transformFunctionConfig: Optional[str] = None

    logTopic: Optional[str] = None

    connection: Optional[str] = None
    """Named connection this sink writes through."""

    snServiceAccount: Optional[str] = None


class CloudSinkConfigParam(TypedDict, total=False):
    tenant: str

    namespace: str

    name: str

    className: str

    sourceSubscriptionName: str

    sourceSubscriptionPosition: CloudSubscriptionPosition

    inputs: List[str]

    topicToSerdeClassName: Dict[str, str]

    topicsPattern: str

    topicToSchemaType: Dict[str, str]

    topicToSchemaProperties: Dict[str, str]

    inputSpecs: Dict[str, CloudConsumerConfigParam]
    """Per-input consumer settings, keyed by input name."""

    maxMessageRetries: int

    deadLetterTopic: str

    configs: CloudOpenConfigMap
    """Plugin-defined settings. The contract leaves the keys and values open."""

    secrets: CloudOpenConfigMap
    """Plugin-defined secret references. Write-only on the server: reads redact values."""

    parallelism: int

    processingGuarantees: CloudProcessingGuarantee

    retainOrdering: bool

    retainKeyOrdering: bool

    resources: CloudRuntimeResourcesParam

    autoAck: bool

    timeoutMs: int

    negativeAckRedeliveryDelayMs: int

    sinkType: str

    archive: str
    """Package the sink runs from, e.g. a registry reference or a built-in name."""

    cleanupSubscription: bool

    runtimeFlags: str

    customRuntimeOptions: str

    transformFunction: str

    transformFunctionClassName: str

    transformFunctionConfig: str

    logTopic: str

    connection: str
    """Named connection this sink writes through."""

    snServiceAccount: str


class CloudSinkInstanceStatus(BaseModel):
    """Runtime counters for one sink connector instance."""

    running: Optional[bool] = None

    error: Optional[str] = None

    numRestarts: Optional[int] = None

    numReadFromPulsar: Optional[int] = None

    numSystemExceptions: Optional[int] = None

    latestSystemExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    numSinkExceptions: Optional[int] = None

    latestSinkExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    numWrittenToSink: Optional[int] = None

    lastReceivedTime: Optional[int] = None

    workerId: Optional[str] = None


class CloudSinkStatusInstance(BaseModel):
    """One entry of the aggregate status: an instance id and that instance's counters."""

    instanceId: Optional[int] = None

    status: Optional[CloudSinkInstanceStatus] = None


class CloudSinkStatus(BaseModel):
    """Aggregate status across every instance of a sink connector."""

    numInstances: Optional[int] = None

    numRunning: Optional[int] = None

    instances: Optional[List[CloudSinkStatusInstance]] = None


CloudSinkNameList: TypeAlias = List[str]
