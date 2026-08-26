from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .trigger_shared import TriggerStatus, TriggerSessionMode

__all__ = [
    "TriggerAgent",
    "TriggerSessionConfig",
    "TriggerInputSchemaConfig",
    "TriggerCronSource",
    "TriggerKafkaSource",
    "TriggerPulsarSource",
    "TriggerSource",
    "Trigger",
    "DeletedTrigger",
]


class TriggerAgent(BaseModel):
    type: Literal["agent"]

    id: str

    version: int


class TriggerSessionConfig(BaseModel):
    environment_id: str

    title_template: Optional[str] = None
    """Present but null when the trigger uses the server's default title."""

    metadata: Dict[str, str]

    vault_ids: List[str]


class TriggerInputSchemaConfig(BaseModel):
    subject: Optional[str] = None

    type: Optional[str] = None

    version: Optional[int] = None


class TriggerCronSource(BaseModel):
    type: Literal["cron"]

    schedule: str

    timezone: str

    payload: str


class TriggerKafkaSource(BaseModel):
    type: Literal["kafka"]

    connection: str

    topics: Optional[List[str]] = None

    topic_pattern: Optional[str] = None

    subscription_name: Optional[str] = None

    type_class_name: Optional[str] = None

    type_class_definition: Optional[str] = None

    schema_type: Optional[str] = None

    consumer_additional_config: Optional[Dict[str, object]] = None
    """Connector-specific consumer settings; the contract leaves this object open."""

    input_schema_configs: Optional[Dict[str, TriggerInputSchemaConfig]] = None


class TriggerPulsarSource(BaseModel):
    type: Literal["pulsar"]

    connection: str

    topics: Optional[List[str]] = None

    topic_pattern: Optional[str] = None

    subscription_name: Optional[str] = None

    type_class_name: Optional[str] = None

    type_class_definition: Optional[str] = None

    schema_type: Optional[str] = None


TriggerSource: TypeAlias = Annotated[
    Union[TriggerCronSource, TriggerKafkaSource, TriggerPulsarSource],
    PropertyInfo(discriminator="type"),
]


class Trigger(BaseModel):
    id: str

    type: Literal["trigger"]

    name: str

    agent: TriggerAgent

    session_mode: TriggerSessionMode
    """Only `SESSION_PER_EVENT` and `SHARED` occur alongside a `cron` source."""

    source: TriggerSource

    session: TriggerSessionConfig

    replicas: int

    status: TriggerStatus

    next_fire_at: Optional[str] = None

    last_fired_at: Optional[str] = None

    error: Optional[str] = None
    """The last failure reported for this trigger, if any."""

    archived_at: Optional[str] = None

    created_at: str

    updated_at: str


class DeletedTrigger(BaseModel):
    id: str

    type: Literal["trigger_deleted"]
