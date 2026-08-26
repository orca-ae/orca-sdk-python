from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "CredentialValidation",
    "CredentialValidationMcpProbe",
    "CredentialValidationRefresh",
    "CredentialValidationHTTPResponse",
]


class CredentialValidationHTTPResponse(BaseModel):
    status_code: int

    content_type: str

    body: str

    body_truncated: bool
    """True when the body was cut short; it is captured for diagnosis, not replay."""


class CredentialValidationMcpProbe(BaseModel):
    method: Literal["initialize"]

    http_response: Optional[CredentialValidationHTTPResponse] = None
    """Null when the probe never got a response, e.g. the connection failed."""


class CredentialValidationRefresh(BaseModel):
    status: Literal["succeeded", "connect_error", "failed", "no_refresh_token"]

    http_response: Optional[CredentialValidationHTTPResponse] = None
    """Null when no refresh was attempted or the request never completed."""


class CredentialValidation(BaseModel):
    type: Literal["vault_credential_validation"]

    credential_id: str

    vault_id: str

    validated_at: str

    has_refresh_token: bool

    status: Literal["valid", "invalid", "unknown"]
    """`unknown` means the probe was inconclusive, not that the credential is bad."""

    mcp_probe: CredentialValidationMcpProbe

    refresh: CredentialValidationRefresh
