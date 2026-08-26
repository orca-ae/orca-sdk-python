from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CloudKafkaConnectorRestartParams"]


class CloudKafkaConnectorRestartParams(TypedDict, total=False):
    includeTasks: bool
    """Whether to restart the connector's tasks as well as the connector itself."""

    onlyFailed: bool
    """Whether to restart only the failed connector and tasks."""
