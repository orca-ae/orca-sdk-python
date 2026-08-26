"""Runtime shapes the function surface shares with the connector surface.

`Resources`, `ConsumerConfig`, `ProducerConfig`, `UpdateOptions`, and
`ExceptionInformation` are a single set of schemas in the contract: functions,
sinks, and sources all embed the same definitions. They are declared once, in
`cloud_connector_shared`, and re-exported here so the function modules read as
function modules and there is exactly one class per contract schema. If a third
surface picks them up, move the declarations to a neutral module and change
these imports -- nothing else refers to them by module.

Field names throughout the cloud namespace are the wire names verbatim: the
extension serves camelCase JSON and `AGENTS.md` section 5 says we mirror the
wire shape rather than re-spell it. Only names that are not valid Python
identifiers get an alias (`update-auth-data`, `1min`).
"""

from __future__ import annotations

from .cloud_connector_shared import (
    CloudCryptoConfig as CloudCryptoConfig,
    CloudOpenConfigMap as CloudOpenConfigMap,
    CloudBatchingConfig as CloudBatchingConfig,
    CloudConsumerConfig as CloudConsumerConfig,
    CloudProducerConfig as CloudProducerConfig,
    CloudCompressionType as CloudCompressionType,
    CloudRuntimeResources as CloudRuntimeResources,
    CloudCryptoConfigParam as CloudCryptoConfigParam,
    CloudBatchingConfigParam as CloudBatchingConfigParam,
    CloudConsumerConfigParam as CloudConsumerConfigParam,
    CloudProcessingGuarantee as CloudProcessingGuarantee,
    CloudProducerConfigParam as CloudProducerConfigParam,
    CloudSubscriptionPosition as CloudSubscriptionPosition,
    CloudRuntimeResourcesParam as CloudRuntimeResourcesParam,
    CloudRuntimeUpdateOptionsParam as CloudRuntimeUpdateOptionsParam,
    CloudRuntimeExceptionInformation as CloudRuntimeExceptionInformation,
    CloudMessagePayloadProcessorConfig as CloudMessagePayloadProcessorConfig,
    CloudMessagePayloadProcessorConfigParam as CloudMessagePayloadProcessorConfigParam,
)

__all__ = [
    "CloudOpenConfigMap",
    "CloudProcessingGuarantee",
    "CloudSubscriptionPosition",
    "CloudCompressionType",
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
