from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .environment import EnvironmentScope
from .environment_shared import EnvironmentConfigParam

__all__ = ["EnvironmentCreateParams"]


class EnvironmentCreateParams(TypedDict, total=False):
    name: Required[str]

    description: Optional[str]

    config: Optional[EnvironmentConfigParam]
    """Portable package, networking, and target selection.

    The flat `packages`, `networking`, `image`, and `target` fields the contract also
    accepts are deliberately not exposed: they are not portable across backends.
    """

    metadata: Dict[str, str]

    scope: Optional[EnvironmentScope]
