# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from .._models import BaseModel

__all__ = ["EnvironmentKey"]


class EnvironmentKey(BaseModel):
    env_key: str
    env_key_expires_at: str
