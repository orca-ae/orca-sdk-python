from __future__ import annotations

from typing_extensions import Literal, TypedDict

from .cloud_kafka_connector import CloudKafkaConnectorConfig

__all__ = ["CloudKafkaConnectorCreateParams", "CloudKafkaInitialState"]

CloudKafkaInitialState = Literal["RUNNING", "PAUSED", "STOPPED"]


class CloudKafkaConnectorCreateParams(TypedDict, total=False):
    name: str

    config: CloudKafkaConnectorConfig
    """Plugin settings, including the `connector.class` that selects the plugin."""

    initial_state: CloudKafkaInitialState
    """State to start the connector in. The worker defaults it to running."""
