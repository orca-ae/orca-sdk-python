from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["CloudAgentProvider", "CloudAgentProviderList"]


class CloudAgentProvider(BaseModel):
    """A model provider registered with the cloud extension service.

    Every field is optional: the contract declares no required properties, so a
    deployment may report as little as a name.
    """

    name: Optional[str] = None

    type: Optional[str] = None
    """Provider family the registry resolved this entry to."""

    api_url: Optional[str] = None

    api_version: Optional[str] = None

    beta_version: Optional[str] = None
    """Beta opt-in the server has configured for this provider, if any.

    Read-only and server-reported. This is not the request-side beta opt-in: SDK
    callers select a beta with the `orca-beta` header via `extra_headers`, and no
    request type carries a `beta_version` field.
    """

    api_key_env: Optional[str] = None
    """Name of the environment variable the server reads the API key from."""

    api_key_configured: Optional[bool] = None
    """Whether a key is already configured server-side.

    The key itself is never returned, so this is the only way to tell a configured
    provider from an unconfigured one.
    """


CloudAgentProviderList: TypeAlias = List[CloudAgentProvider]
