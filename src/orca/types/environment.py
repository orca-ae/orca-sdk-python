from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "EnvironmentScope",
    "EnvironmentPackages",
    "EnvironmentLimitedNetworking",
    "EnvironmentUnrestrictedNetworking",
    "EnvironmentNetworking",
    "EnvironmentCloudConfig",
    "EnvironmentSelfHostedConfig",
    "EnvironmentConfig",
    "Environment",
    "DeletedEnvironment",
]

EnvironmentScope: TypeAlias = Literal["organization", "account"]


class EnvironmentPackages(BaseModel):
    type: Literal["packages"]

    apt: List[str]

    cargo: List[str]

    gem: List[str]

    go: List[str]

    npm: List[str]

    pip: List[str]


class EnvironmentLimitedNetworking(BaseModel):
    type: Literal["limited"]

    allowed_hosts: Optional[List[str]] = None

    allow_mcp_servers: Optional[bool] = None

    allow_package_managers: Optional[bool] = None


class EnvironmentUnrestrictedNetworking(BaseModel):
    type: Literal["unrestricted"]


EnvironmentNetworking: TypeAlias = Annotated[
    Union[EnvironmentLimitedNetworking, EnvironmentUnrestrictedNetworking], PropertyInfo(discriminator="type")
]


class EnvironmentCloudConfig(BaseModel):
    type: Literal["cloud"]

    packages: EnvironmentPackages

    networking: EnvironmentNetworking


class EnvironmentSelfHostedConfig(BaseModel):
    type: Literal["self_hosted"]
    """A self-hosted environment carries no package or networking config.

    Those knobs belong to the image the operator runs, not to the registry entry.
    """


EnvironmentConfig: TypeAlias = Annotated[
    Union[EnvironmentCloudConfig, EnvironmentSelfHostedConfig], PropertyInfo(discriminator="type")
]


class Environment(BaseModel):
    id: str

    type: Literal["environment"]

    name: str

    description: str

    config: EnvironmentConfig
    """Always carries its `cloud`/`self_hosted` discriminator on the way out, even
    though the discriminator is optional on the way in."""

    metadata: Dict[str, str]

    scope: Optional[EnvironmentScope] = None
    """Omitted entirely by deployments that do not scope environments."""

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
    """Present but null while the environment is active."""


class DeletedEnvironment(BaseModel):
    id: str

    type: Literal["environment_deleted"]
