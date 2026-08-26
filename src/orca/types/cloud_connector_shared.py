from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "CloudProcessingGuarantee",
    "CloudSubscriptionPosition",
    "CloudCompressionType",
    "CloudProducerCryptoFailureAction",
    "CloudConsumerCryptoFailureAction",
    "CloudOpenConfigMap",
    "CloudRuntimeResources",
    "CloudRuntimeResourcesParam",
    "CloudCryptoConfig",
    "CloudCryptoConfigParam",
    "CloudMessagePayloadProcessorConfig",
    "CloudMessagePayloadProcessorConfigParam",
    "CloudConsumerConfig",
    "CloudConsumerConfigParam",
    "CloudBatchingConfig",
    "CloudBatchingConfigParam",
    "CloudProducerConfig",
    "CloudProducerConfigParam",
    "CloudRuntimeUpdateOptionsParam",
    "CloudRuntimeExceptionInformation",
]

# Connector runtime enums. The server fixes these spellings, so they appear once
# here and every config that carries one references the alias.
CloudProcessingGuarantee: TypeAlias = Literal["ATLEAST_ONCE", "ATMOST_ONCE", "EFFECTIVELY_ONCE", "MANUAL"]

CloudSubscriptionPosition: TypeAlias = Literal["Latest", "Earliest"]

CloudCompressionType: TypeAlias = Literal["NONE", "LZ4", "ZLIB", "ZSTD", "SNAPPY"]

CloudProducerCryptoFailureAction: TypeAlias = Literal["FAIL", "SEND"]

CloudConsumerCryptoFailureAction: TypeAlias = Literal["FAIL", "DISCARD", "CONSUME"]

# Connector `configs`, `secrets`, and similar maps are declared open by the
# contract: the server fixes neither the keys nor the value shapes, because each
# connector plugin defines its own. Modelling them as anything narrower would
# reject valid payloads, so they stay open string maps.
CloudOpenConfigMap: TypeAlias = Dict[str, object]


class CloudRuntimeResources(BaseModel):
    """Compute budget for one connector instance.

    Field names are camelCase because the connector runtime serves them that way;
    per `AGENTS.md` section 5 the SDK mirrors the wire shape rather than renaming it.
    """

    cpu: Optional[float] = None

    ram: Optional[int] = None
    """Memory budget in bytes."""

    disk: Optional[int] = None
    """Disk budget in bytes."""


class CloudRuntimeResourcesParam(TypedDict, total=False):
    cpu: float

    ram: int
    """Memory budget in bytes."""

    disk: int
    """Disk budget in bytes."""


class CloudCryptoConfig(BaseModel):
    """End-to-end encryption settings for a connector's messages."""

    cryptoKeyReaderClassName: Optional[str] = None

    cryptoKeyReaderConfig: Optional[CloudOpenConfigMap] = None

    encryptionKeys: Optional[List[str]] = None

    producerCryptoFailureAction: Optional[CloudProducerCryptoFailureAction] = None

    consumerCryptoFailureAction: Optional[CloudConsumerCryptoFailureAction] = None


class CloudCryptoConfigParam(TypedDict, total=False):
    cryptoKeyReaderClassName: str

    cryptoKeyReaderConfig: CloudOpenConfigMap

    encryptionKeys: List[str]

    producerCryptoFailureAction: CloudProducerCryptoFailureAction

    consumerCryptoFailureAction: CloudConsumerCryptoFailureAction


class CloudMessagePayloadProcessorConfig(BaseModel):
    className: Optional[str] = None

    config: Optional[CloudOpenConfigMap] = None


class CloudMessagePayloadProcessorConfigParam(TypedDict, total=False):
    className: str

    config: CloudOpenConfigMap


class CloudConsumerConfig(BaseModel):
    """Per-input consumer settings for a sink connector."""

    schemaType: Optional[str] = None

    serdeClassName: Optional[str] = None

    schemaProperties: Optional[Dict[str, str]] = None

    consumerProperties: Optional[Dict[str, str]] = None

    receiverQueueSize: Optional[int] = None

    cryptoConfig: Optional[CloudCryptoConfig] = None

    messagePayloadProcessorConfig: Optional[CloudMessagePayloadProcessorConfig] = None

    poolMessages: Optional[bool] = None

    regexPattern: Optional[bool] = None
    """Whether the input name is a pattern rather than a literal topic."""


class CloudConsumerConfigParam(TypedDict, total=False):
    schemaType: str

    serdeClassName: str

    schemaProperties: Dict[str, str]

    consumerProperties: Dict[str, str]

    receiverQueueSize: int

    cryptoConfig: CloudCryptoConfigParam

    messagePayloadProcessorConfig: CloudMessagePayloadProcessorConfigParam

    poolMessages: bool

    regexPattern: bool
    """Whether the input name is a pattern rather than a literal topic."""


class CloudBatchingConfig(BaseModel):
    enabled: Optional[bool] = None

    batchingMaxPublishDelayMs: Optional[int] = None

    roundRobinRouterBatchingPartitionSwitchFrequency: Optional[int] = None

    batchingMaxMessages: Optional[int] = None

    batchingMaxBytes: Optional[int] = None

    batchBuilder: Optional[str] = None


class CloudBatchingConfigParam(TypedDict, total=False):
    enabled: bool

    batchingMaxPublishDelayMs: int

    roundRobinRouterBatchingPartitionSwitchFrequency: int

    batchingMaxMessages: int

    batchingMaxBytes: int

    batchBuilder: str


class CloudProducerConfig(BaseModel):
    """Producer settings for a source connector's output."""

    maxPendingMessages: Optional[int] = None

    maxPendingMessagesAcrossPartitions: Optional[int] = None

    useThreadLocalProducers: Optional[bool] = None

    cryptoConfig: Optional[CloudCryptoConfig] = None

    batchBuilder: Optional[str] = None

    compressionType: Optional[CloudCompressionType] = None

    batchingConfig: Optional[CloudBatchingConfig] = None


class CloudProducerConfigParam(TypedDict, total=False):
    maxPendingMessages: int

    maxPendingMessagesAcrossPartitions: int

    useThreadLocalProducers: bool

    cryptoConfig: CloudCryptoConfigParam

    batchBuilder: str

    compressionType: CloudCompressionType

    batchingConfig: CloudBatchingConfigParam


class CloudRuntimeUpdateOptionsParam(TypedDict, total=False):
    """Options that modify how an update is applied, sent alongside the new config."""

    update_auth_data: Annotated[bool, PropertyInfo(alias="update-auth-data")]
    """Whether to replace the connector's stored authentication data.

    The wire name is hyphenated, so it cannot be a Python identifier and is aliased.
    """


class CloudRuntimeExceptionInformation(BaseModel):
    """One exception the runtime recorded, with the time it happened."""

    exceptionString: Optional[str] = None

    timestampMs: Optional[int] = None
