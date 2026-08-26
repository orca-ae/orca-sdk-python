"""The function configuration document.

Wire names are mirrored verbatim; see `cloud_function_shared` for why.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypedDict

from .._models import BaseModel
from .cloud_function_shared import (
    CloudOpenConfigMap,
    CloudConsumerConfig,
    CloudProducerConfig,
    CloudRuntimeResources,
    CloudConsumerConfigParam,
    CloudProcessingGuarantee,
    CloudProducerConfigParam,
    CloudSubscriptionPosition,
    CloudRuntimeResourcesParam,
)

__all__ = [
    "CloudFunctionConfig",
    "CloudFunctionConfigParam",
    "CloudFunctionWindowConfig",
    "CloudFunctionWindowConfigParam",
]


class CloudFunctionWindowConfig(BaseModel):
    windowLengthCount: Optional[int] = None

    windowLengthDurationMs: Optional[int] = None

    slidingIntervalCount: Optional[int] = None

    slidingIntervalDurationMs: Optional[int] = None

    lateDataTopic: Optional[str] = None

    maxLagMs: Optional[int] = None

    watermarkEmitIntervalMs: Optional[int] = None

    timestampExtractorClassName: Optional[str] = None

    actualWindowFunctionClassName: Optional[str] = None

    processingGuarantees: Optional[Literal["ATLEAST_ONCE", "ATMOST_ONCE"]] = None
    """Windowed processing supports only the two at-least/at-most modes."""


class CloudFunctionWindowConfigParam(TypedDict, total=False):
    windowLengthCount: int

    windowLengthDurationMs: int

    slidingIntervalCount: int

    slidingIntervalDurationMs: int

    lateDataTopic: str

    maxLagMs: int

    watermarkEmitIntervalMs: int

    timestampExtractorClassName: str

    actualWindowFunctionClassName: str

    processingGuarantees: Literal["ATLEAST_ONCE", "ATMOST_ONCE"]


class CloudFunctionConfig(BaseModel):
    runtimeFlags: Optional[str] = None

    tenant: Optional[str] = None

    namespace: Optional[str] = None

    name: Optional[str] = None

    className: Optional[str] = None

    inputs: Optional[List[str]] = None

    customSerdeInputs: Optional[Dict[str, str]] = None

    topicsPattern: Optional[str] = None

    customSchemaInputs: Optional[Dict[str, str]] = None

    customSchemaOutputs: Optional[Dict[str, str]] = None

    inputSpecs: Optional[Dict[str, CloudConsumerConfig]] = None

    inputTypeClassName: Optional[str] = None

    output: Optional[str] = None

    producerConfig: Optional[CloudProducerConfig] = None

    outputSchemaType: Optional[str] = None

    outputTypeClassName: Optional[str] = None

    outputSerdeClassName: Optional[str] = None

    logTopic: Optional[str] = None

    processingGuarantees: Optional[CloudProcessingGuarantee] = None

    retainOrdering: Optional[bool] = None

    retainKeyOrdering: Optional[bool] = None

    batchBuilder: Optional[str] = None

    forwardSourceMessageProperty: Optional[bool] = None

    userConfig: Optional[CloudOpenConfigMap] = None

    secrets: Optional[CloudOpenConfigMap] = None

    runtime: Optional[Literal["JAVA", "PYTHON", "GO"]] = None

    autoAck: Optional[bool] = None

    maxMessageRetries: Optional[int] = None

    deadLetterTopic: Optional[str] = None

    subName: Optional[str] = None

    parallelism: Optional[int] = None

    resources: Optional[CloudRuntimeResources] = None

    fqfn: Optional[str] = None

    windowConfig: Optional[CloudFunctionWindowConfig] = None

    timeoutMs: Optional[int] = None

    jar: Optional[str] = None

    py: Optional[str] = None

    go: Optional[str] = None

    functionType: Optional[str] = None

    cleanupSubscription: Optional[bool] = None

    customRuntimeOptions: Optional[str] = None

    maxPendingAsyncRequests: Optional[int] = None

    exposePulsarAdminClientEnabled: Optional[bool] = None

    skipToLatest: Optional[bool] = None

    subscriptionPosition: Optional[CloudSubscriptionPosition] = None

    connection: Optional[str] = None

    snServiceAccount: Optional[str] = None


class CloudFunctionConfigParam(TypedDict, total=False):
    runtimeFlags: str

    tenant: str

    namespace: str

    name: str

    className: str

    inputs: List[str]

    customSerdeInputs: Dict[str, str]

    topicsPattern: str

    customSchemaInputs: Dict[str, str]

    customSchemaOutputs: Dict[str, str]

    inputSpecs: Dict[str, CloudConsumerConfigParam]

    inputTypeClassName: str

    output: str

    producerConfig: CloudProducerConfigParam

    outputSchemaType: str

    outputTypeClassName: str

    outputSerdeClassName: str

    logTopic: str

    processingGuarantees: CloudProcessingGuarantee

    retainOrdering: bool

    retainKeyOrdering: bool

    batchBuilder: str

    forwardSourceMessageProperty: bool

    userConfig: CloudOpenConfigMap

    secrets: CloudOpenConfigMap

    runtime: Literal["JAVA", "PYTHON", "GO"]

    autoAck: bool

    maxMessageRetries: int

    deadLetterTopic: str

    subName: str

    parallelism: int

    resources: CloudRuntimeResourcesParam

    fqfn: str

    windowConfig: CloudFunctionWindowConfigParam

    timeoutMs: int

    jar: str

    py: str

    go: str

    functionType: str

    cleanupSubscription: bool

    customRuntimeOptions: str

    maxPendingAsyncRequests: int

    exposePulsarAdminClientEnabled: bool

    skipToLatest: bool

    subscriptionPosition: CloudSubscriptionPosition

    connection: str

    snServiceAccount: str
