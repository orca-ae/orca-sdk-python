from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .credential_shared import CredentialCreateAuthParam

__all__ = ["CredentialCreateParams"]


class CredentialCreateParams(TypedDict, total=False):
    auth: Required[CredentialCreateAuthParam]
    """Secrets here are write-only; a read never returns them."""

    display_name: Optional[str]

    metadata: Dict[str, str]
    """Arbitrary string key/value pairs."""
