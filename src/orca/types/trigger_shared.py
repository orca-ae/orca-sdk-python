from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "TriggerSessionMode",
    "TriggerCronSessionMode",
    "TriggerSourceType",
    "TriggerStatus",
    "TriggerAgentReferenceParam",
    "TriggerAgentParam",
    "TriggerSessionCreateParam",
    "TriggerSessionUpdateParam",
    "TriggerInputSchemaConfigParam",
    "TriggerCronSourceCreateParam",
    "TriggerKafkaSourceParam",
    "TriggerPulsarSourceParam",
    "TriggerSourceCreateParam",
    "TriggerCronSourceUpdateParam",
    "TriggerKafkaSourceUpdateParam",
    "TriggerPulsarSourceUpdateParam",
    "TriggerSourceUpdateParam",
]

TriggerSessionMode: TypeAlias = Literal["SESSION_PER_EVENT", "SESSION_PER_TOPIC", "SESSION_PER_KEY", "SHARED"]
"""How a trigger maps incoming events onto sessions.

Deliberately wide: a `cron` source accepts only `SESSION_PER_EVENT` and `SHARED`
(see `TriggerCronSessionMode`), and a deployment that implements a narrower subset
returns its own API error. The SDK does no client-side gating.
"""

TriggerCronSessionMode: TypeAlias = Literal["SESSION_PER_EVENT", "SHARED"]
"""The session modes a `cron` source supports."""

TriggerSourceType: TypeAlias = Literal["cron", "kafka", "pulsar"]

TriggerStatus: TypeAlias = Literal["active", "paused", "archived"]


class TriggerAgentReferenceParam(TypedDict, total=False):
    type: Required[Literal["agent"]]

    id: Required[str]

    version: int
    """Pin the trigger to a historical agent version instead of the current one."""


TriggerAgentParam: TypeAlias = Union[str, TriggerAgentReferenceParam]
"""A plain string is shorthand for `{"type": "agent", "id": <string>}`."""


class TriggerSessionCreateParam(TypedDict, total=False):
    environment_id: Required[str]

    title_template: Optional[str]

    metadata: Dict[str, str]

    vault_ids: List[str]


class TriggerSessionUpdateParam(TypedDict, total=False):
    environment_id: str

    title_template: Optional[str]

    metadata: Dict[str, Optional[str]]
    """A null value removes that individual key."""

    vault_ids: List[str]


class TriggerInputSchemaConfigParam(TypedDict, total=False):
    subject: Optional[str]

    type: Optional[str]

    version: Optional[int]


class TriggerCronSourceCreateParam(TypedDict, total=False):
    type: Required[Literal["cron"]]

    schedule: Required[str]

    payload: Required[str]

    timezone: str


class TriggerKafkaSourceParam(TypedDict, total=False):
    """Set exactly one of `topics` or `topic_pattern`."""

    type: Required[Literal["kafka"]]

    connection: Required[str]

    topics: List[str]

    topic_pattern: str

    subscription_name: str

    type_class_name: str

    type_class_definition: str

    schema_type: str

    consumer_additional_config: Dict[str, object]
    """Connector-specific consumer settings; the contract leaves this object open."""

    input_schema_configs: Dict[str, TriggerInputSchemaConfigParam]


class TriggerPulsarSourceParam(TypedDict, total=False):
    """Set exactly one of `topics` or `topic_pattern`."""

    type: Required[Literal["pulsar"]]

    connection: Required[str]

    topics: List[str]

    topic_pattern: str

    subscription_name: str

    type_class_name: str

    type_class_definition: str

    schema_type: str


TriggerSourceCreateParam: TypeAlias = Union[
    TriggerCronSourceCreateParam,
    TriggerKafkaSourceParam,
    TriggerPulsarSourceParam,
]


class TriggerCronSourceUpdateParam(TypedDict, total=False):
    type: Required[Literal["cron"]]

    schedule: str

    timezone: str

    payload: str


class TriggerKafkaSourceUpdateParam(TypedDict, total=False):
    """Every field but the discriminator is optional; unset fields are preserved."""

    type: Required[Literal["kafka"]]

    connection: str

    topics: List[str]

    topic_pattern: str

    subscription_name: str

    type_class_name: str

    type_class_definition: str

    schema_type: str

    consumer_additional_config: Dict[str, object]
    """Connector-specific consumer settings; the contract leaves this object open."""

    input_schema_configs: Dict[str, TriggerInputSchemaConfigParam]


class TriggerPulsarSourceUpdateParam(TypedDict, total=False):
    """Every field but the discriminator is optional; unset fields are preserved."""

    type: Required[Literal["pulsar"]]

    connection: str

    topics: List[str]

    topic_pattern: str

    subscription_name: str

    type_class_name: str

    type_class_definition: str

    schema_type: str


TriggerSourceUpdateParam: TypeAlias = Union[
    TriggerCronSourceUpdateParam,
    TriggerKafkaSourceUpdateParam,
    TriggerPulsarSourceUpdateParam,
]
