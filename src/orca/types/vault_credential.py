from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .credential_shared import CredentialProvider, CredentialProviderScheme

__all__ = [
    "VaultCredential",
    "VaultCredentialAuth",
    "VaultCredentialOAuthRefresh",
    "VaultCredentialTokenEndpointAuth",
    "CredentialNetworking",
    "CredentialInjectionLocation",
    "DeletedVaultCredential",
]


class CredentialInjectionLocation(BaseModel):
    header: bool

    body: bool


class CredentialLimitedNetworking(BaseModel):
    type: Literal["limited"]

    allowed_hosts: List[str]


class CredentialUnrestrictedNetworking(BaseModel):
    type: Literal["unrestricted"]


CredentialNetworking: TypeAlias = Annotated[
    Union[CredentialLimitedNetworking, CredentialUnrestrictedNetworking],
    PropertyInfo(discriminator="type"),
]


class VaultCredentialTokenEndpointAuth(BaseModel):
    type: Literal["none", "client_secret_basic", "client_secret_post"]
    """Read shape: the client secret itself is write-only and never returned."""


class VaultCredentialOAuthRefresh(BaseModel):
    token_endpoint: str

    client_id: str

    token_endpoint_auth: VaultCredentialTokenEndpointAuth

    resource: Optional[str] = None

    scope: Optional[str] = None


class VaultCredentialStaticBearerAuth(BaseModel):
    type: Literal["static_bearer"]

    mcp_server_url: str


class VaultCredentialMcpOAuthAuth(BaseModel):
    type: Literal["mcp_oauth"]

    mcp_server_url: str

    expires_at: Optional[str] = None

    refresh: Optional[VaultCredentialOAuthRefresh] = None


class VaultCredentialEnvironmentVariableAuth(BaseModel):
    type: Literal["environment_variable"]

    secret_name: str

    networking: CredentialNetworking

    injection_location: CredentialInjectionLocation


class VaultCredentialProviderAuth(BaseModel):
    type: Literal["provider"]

    provider: CredentialProvider
    """The model provider this credential authenticates against.

    Values are fixed by the API contract.
    """

    scheme: CredentialProviderScheme

    logical_id: str

    version: str


VaultCredentialAuth: TypeAlias = Annotated[
    Union[
        VaultCredentialStaticBearerAuth,
        VaultCredentialMcpOAuthAuth,
        VaultCredentialEnvironmentVariableAuth,
        VaultCredentialProviderAuth,
    ],
    PropertyInfo(discriminator="type"),
]


class VaultCredential(BaseModel):
    id: str

    type: Literal["vault_credential"]

    vault_id: str

    display_name: Optional[str] = None

    auth: VaultCredentialAuth
    """Read shape of the credential.

    Every secret supplied on write -- token, access token, secret value, client
    secret -- is omitted here; only the non-secret configuration comes back.
    """

    metadata: Dict[str, str]

    archived_at: Optional[str] = None
    """Present but null while the credential is active."""

    created_at: str

    updated_at: str


class DeletedVaultCredential(BaseModel):
    id: str

    type: Literal["vault_credential_deleted"]
