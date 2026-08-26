from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "CredentialProvider",
    "CredentialProviderScheme",
    "CredentialInjectionLocationParam",
    "CredentialNetworkingParam",
    "CredentialTokenEndpointAuthParam",
    "CredentialOAuthRefreshParam",
    "CredentialCreateAuthParam",
    "CredentialUpdateTokenEndpointAuthParam",
    "CredentialUpdateOAuthRefreshParam",
    "CredentialUpdateAuthParam",
]


# Model-provider discriminator. These are protocol constants: the server defines them
# and the SDK must send them verbatim, so the values are fixed by the contract rather
# than chosen here. Declared once and referenced everywhere the discriminator appears.
CredentialProvider: TypeAlias = Literal[
    "anthropic",  # wire-value
    "openai",
    "openai_compatible",
    "azure_openai",
    "vertex",  # wire-value
    "bedrock",  # wire-value
]

CredentialProviderScheme: TypeAlias = Literal["api_key", "bearer", "gcp-service-account", "aws-sig-v4"]


class CredentialInjectionLocationParam(TypedDict, total=False):
    header: bool

    body: bool


class CredentialLimitedNetworkingParam(TypedDict, total=False):
    type: Required[Literal["limited"]]

    allowed_hosts: Required[SequenceNotStr[str]]


class CredentialUnrestrictedNetworkingParam(TypedDict, total=False):
    type: Required[Literal["unrestricted"]]


CredentialNetworkingParam: TypeAlias = Union[
    CredentialLimitedNetworkingParam,
    CredentialUnrestrictedNetworkingParam,
]


class CredentialNoTokenEndpointAuthParam(TypedDict, total=False):
    type: Required[Literal["none"]]


class CredentialClientSecretBasicAuthParam(TypedDict, total=False):
    type: Required[Literal["client_secret_basic"]]

    client_secret: Required[str]


class CredentialClientSecretPostAuthParam(TypedDict, total=False):
    type: Required[Literal["client_secret_post"]]

    client_secret: Required[str]


CredentialTokenEndpointAuthParam: TypeAlias = Union[
    CredentialNoTokenEndpointAuthParam,
    CredentialClientSecretBasicAuthParam,
    CredentialClientSecretPostAuthParam,
]


class CredentialOAuthRefreshParam(TypedDict, total=False):
    refresh_token: Required[str]

    token_endpoint: Required[str]

    client_id: Required[str]

    token_endpoint_auth: Required[CredentialTokenEndpointAuthParam]

    resource: Optional[str]

    scope: Optional[str]


class CredentialStaticBearerAuthParam(TypedDict, total=False):
    type: Required[Literal["static_bearer"]]

    token: Required[str]
    """Write-only: the stored token is never returned by a read."""

    mcp_server_url: Required[str]


class CredentialMcpOAuthAuthParam(TypedDict, total=False):
    type: Required[Literal["mcp_oauth"]]

    access_token: Required[str]
    """Write-only: the stored token is never returned by a read."""

    mcp_server_url: Required[str]

    expires_at: Optional[str]

    refresh: Optional[CredentialOAuthRefreshParam]
    """Supply refresh material so the server can renew the access token itself."""


class CredentialEnvironmentVariableAuthParam(TypedDict, total=False):
    type: Required[Literal["environment_variable"]]

    secret_name: Required[str]

    secret_value: Required[str]
    """Write-only: the stored value is never returned by a read."""

    networking: Required[CredentialNetworkingParam]
    """Which hosts the secret may be sent to."""

    injection_location: CredentialInjectionLocationParam
    """Where the secret is placed in the outgoing request."""


class CredentialProviderAuthParam(TypedDict, total=False):
    type: Required[Literal["provider"]]

    provider: Required[CredentialProvider]
    """The model provider this credential authenticates against.

    Values are fixed by the API contract.
    """

    scheme: Required[CredentialProviderScheme]

    logical_id: Required[str]

    secret_value: Required[str]
    """Write-only: the stored value is never returned by a read."""


CredentialCreateAuthParam: TypeAlias = Union[
    CredentialStaticBearerAuthParam,
    CredentialMcpOAuthAuthParam,
    CredentialEnvironmentVariableAuthParam,
    CredentialProviderAuthParam,
]


class CredentialUpdateClientSecretBasicAuthParam(TypedDict, total=False):
    type: Required[Literal["client_secret_basic"]]

    client_secret: Optional[str]


class CredentialUpdateClientSecretPostAuthParam(TypedDict, total=False):
    type: Required[Literal["client_secret_post"]]

    client_secret: Optional[str]


CredentialUpdateTokenEndpointAuthParam: TypeAlias = Union[
    CredentialUpdateClientSecretBasicAuthParam,
    CredentialUpdateClientSecretPostAuthParam,
]
"""Narrower than the create-side union: `none` cannot be selected by an update."""


class CredentialUpdateOAuthRefreshParam(TypedDict, total=False):
    refresh_token: Optional[str]

    scope: Optional[str]

    token_endpoint_auth: CredentialUpdateTokenEndpointAuthParam


class CredentialUpdateStaticBearerAuthParam(TypedDict, total=False):
    type: Required[Literal["static_bearer"]]

    token: Optional[str]


class CredentialUpdateMcpOAuthAuthParam(TypedDict, total=False):
    type: Required[Literal["mcp_oauth"]]

    access_token: Optional[str]

    expires_at: Optional[str]

    refresh: Optional[CredentialUpdateOAuthRefreshParam]


class CredentialUpdateEnvironmentVariableAuthParam(TypedDict, total=False):
    type: Required[Literal["environment_variable"]]

    injection_location: CredentialInjectionLocationParam

    networking: Optional[CredentialNetworkingParam]

    secret_value: Optional[str]


class CredentialUpdateProviderAuthParam(TypedDict, total=False):
    type: Required[Literal["provider"]]

    logical_id: str

    secret_value: Optional[str]


CredentialUpdateAuthParam: TypeAlias = Union[
    CredentialUpdateStaticBearerAuthParam,
    CredentialUpdateMcpOAuthAuthParam,
    CredentialUpdateEnvironmentVariableAuthParam,
    CredentialUpdateProviderAuthParam,
]
"""The `type` selects which credential shape is being edited; it is never changed by
an update, and only the fields present in the chosen variant are writable."""
