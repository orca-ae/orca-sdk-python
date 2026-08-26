from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .cloud_catalog import CloudCatalogConfigFieldDefinition

__all__ = [
    "CloudKafkaConfigKeyInfo",
    "CloudKafkaConfigKeyInfoList",
    "CloudKafkaPluginInfo",
    "CloudKafkaPluginInfoList",
    "CloudKafkaPluginCatalogEntry",
    "CloudKafkaPluginCatalogEntryList",
]


class CloudKafkaConfigKeyInfo(BaseModel):
    """One configuration key a connector plugin accepts.

    Field names are snake_case here because Kafka Connect serves them that way --
    unlike the connector registry, which is camelCase. Both mirror their own wire
    shape rather than being normalised to a single house style.
    """

    name: Optional[str] = None

    type: Optional[str] = None

    required: Optional[bool] = None

    default_value: Optional[str] = None

    importance: Optional[str] = None

    documentation: Optional[str] = None

    group: Optional[str] = None

    order_in_group: Optional[int] = None

    width: Optional[str] = None

    display_name: Optional[str] = None

    dependents: Optional[List[str]] = None
    """Other keys whose meaning depends on this one."""

    order: Optional[int] = None


class CloudKafkaPluginInfo(BaseModel):
    """One connector plugin installed on the worker."""

    class_: Optional[str] = FieldInfo(alias="class", default=None)
    """Implementation class.

    The wire name is `class`, a Python keyword, so the field is aliased rather than
    renamed on the wire.
    """

    type: Optional[str] = None

    version: Optional[str] = None


class CloudKafkaPluginCatalogEntry(BaseModel):
    """One connector the plugin catalog offers, with its packaging and field metadata.

    Field names are camelCase because the catalog serves them that way; per
    `AGENTS.md` section 5 the SDK mirrors the wire shape rather than renaming it.
    """

    name: Optional[str] = None

    description: Optional[str] = None

    sourceClass: Optional[str] = None

    sinkClass: Optional[str] = None

    sourceConfigClass: Optional[str] = None

    sinkConfigClass: Optional[str] = None

    id: Optional[str] = None

    version: Optional[str] = None

    imageRegistry: Optional[str] = None

    imageRepository: Optional[str] = None

    imageTag: Optional[str] = None

    typeClassName: Optional[str] = None

    sourceTypeClassName: Optional[str] = None

    sinkTypeClassName: Optional[str] = None

    jarFullName: Optional[str] = None

    defaultSchemaType: Optional[str] = None

    defaultSerdeClassName: Optional[str] = None

    iconLink: Optional[str] = None

    sinkDocLink: Optional[str] = None

    sourceDocLink: Optional[str] = None

    sinkConfigFieldDefinitions: Optional[List[CloudCatalogConfigFieldDefinition]] = None

    sourceConfigFieldDefinitions: Optional[List[CloudCatalogConfigFieldDefinition]] = None

    jar: Optional[str] = None


CloudKafkaConfigKeyInfoList: TypeAlias = List[CloudKafkaConfigKeyInfo]

CloudKafkaPluginInfoList: TypeAlias = List[CloudKafkaPluginInfo]

CloudKafkaPluginCatalogEntryList: TypeAlias = List[CloudKafkaPluginCatalogEntry]
