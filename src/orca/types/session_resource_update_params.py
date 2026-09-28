# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SessionResourceUpdateParams"]


class SessionResourceUpdateParams(TypedDict, total=False):
    authorization_token: Required[str]
    """Replacement token for a repository resource. Write-only; never returned."""
