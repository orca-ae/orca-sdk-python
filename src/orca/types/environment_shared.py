from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EnvironmentPackagesParam",
    "EnvironmentLimitedNetworkingParam",
    "EnvironmentUnrestrictedNetworkingParam",
    "EnvironmentNetworkingParam",
    "EnvironmentCloudConfigParam",
    "EnvironmentSelfHostedConfigParam",
    "EnvironmentConfigParam",
]


class EnvironmentPackagesParam(TypedDict, total=False):
    type: Literal["packages"]
    """Optional on input; the server infers `"packages"` when omitted."""

    apt: Optional[List[str]]

    cargo: Optional[List[str]]

    gem: Optional[List[str]]

    go: Optional[List[str]]

    npm: Optional[List[str]]

    pip: Optional[List[str]]


class EnvironmentLimitedNetworkingParam(TypedDict, total=False):
    type: Required[Literal["limited"]]

    allowed_hosts: Optional[List[str]]

    allow_mcp_servers: Optional[bool]

    allow_package_managers: Optional[bool]


class EnvironmentUnrestrictedNetworkingParam(TypedDict, total=False):
    type: Required[Literal["unrestricted"]]


EnvironmentNetworkingParam: TypeAlias = Union[EnvironmentLimitedNetworkingParam, EnvironmentUnrestrictedNetworkingParam]


class EnvironmentCloudConfigParam(TypedDict, total=False):
    type: Literal["cloud"]
    """Optional on input; the server infers `"cloud"` when omitted."""

    packages: Optional[EnvironmentPackagesParam]

    networking: Optional[EnvironmentNetworkingParam]


class EnvironmentSelfHostedConfigParam(TypedDict, total=False):
    type: Required[Literal["self_hosted"]]
    """Required, unlike the cloud variant: selecting self-hosted is never inferred."""

    packages: Optional[EnvironmentPackagesParam]

    networking: Optional[EnvironmentNetworkingParam]


EnvironmentConfigParam: TypeAlias = Union[EnvironmentCloudConfigParam, EnvironmentSelfHostedConfigParam]
