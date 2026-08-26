from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = [
    "CloudCatalogConnectorDefinition",
    "CloudCatalogConfigFieldDefinition",
    "CloudCatalogConnectorList",
    "CloudCatalogConfigFieldList",
]


class CloudCatalogConnectorDefinition(BaseModel):
    """One connector the catalog offers.

    Field names are camelCase because the catalog serves them that way; per
    `AGENTS.md` section 5 the SDK mirrors the wire shape rather than renaming it,
    so these read the same here as in the contract and in the JSON.
    """

    name: Optional[str] = None

    description: Optional[str] = None

    sourceClass: Optional[str] = None
    """Implementation class used when the connector runs as a source."""

    sinkClass: Optional[str] = None
    """Implementation class used when the connector runs as a sink."""

    sourceConfigClass: Optional[str] = None

    sinkConfigClass: Optional[str] = None


class CloudCatalogConfigFieldDefinition(BaseModel):
    """One configuration field a connector accepts.

    camelCase for the same reason as `CloudCatalogConnectorDefinition`.
    """

    fieldName: Optional[str] = None

    typeName: Optional[str] = None
    """Declared type of the field, as the connector's own runtime names it."""

    attributes: Optional[Dict[str, str]] = None
    """Free-form per-field metadata.

    The contract fixes neither the keys nor their meaning, so this stays an open
    string map rather than a modelled shape.
    """


CloudCatalogConnectorList: TypeAlias = List[CloudCatalogConnectorDefinition]

CloudCatalogConfigFieldList: TypeAlias = List[CloudCatalogConfigFieldDefinition]
