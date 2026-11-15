# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from .._models import BaseModel

__all__ = ["EnvironmentWorkStats"]


class EnvironmentWorkStats(BaseModel):
    depth: int
    in_flight: int
    worker_connected: bool
