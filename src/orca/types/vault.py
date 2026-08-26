from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Vault", "DeletedVault"]


class Vault(BaseModel):
    id: str

    type: Literal["vault"]

    display_name: str

    metadata: Dict[str, str]

    created_at: str

    updated_at: str

    archived_at: Optional[str] = None
    """Present but null while the vault is active."""


class DeletedVault(BaseModel):
    id: str

    type: Literal["vault_deleted"]
