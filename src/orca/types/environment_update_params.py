from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .environment import EnvironmentScope
from .environment_shared import EnvironmentConfigParam

__all__ = ["EnvironmentUpdateParams"]


class EnvironmentUpdateParams(TypedDict, total=False):
    name: Optional[str]

    description: Optional[str]

    config: Optional[EnvironmentConfigParam]
    """Portable package, networking, and target selection.

    The flat `packages`, `networking`, `image`, and `target` fields the contract also
    accepts are deliberately not exposed: they are not portable across backends.
    """

    metadata: Dict[str, Optional[str]]
    """A null value removes that individual key."""

    scope: Optional[EnvironmentScope]
