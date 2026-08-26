from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .credential_shared import CredentialUpdateAuthParam

__all__ = ["CredentialUpdateParams"]


class CredentialUpdateParams(TypedDict, total=False):
    display_name: Optional[str]

    auth: CredentialUpdateAuthParam
    """Rotate secrets or edit configuration in place.

    `auth.type` selects which credential shape is being edited rather than changing
    it; omitted fields keep their stored value.
    """

    metadata: Optional[Dict[str, Optional[str]]]
    """A null value removes that individual key."""
