# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from typing import List

from .._models import BaseModel

__all__ = ["Harness", "HarnessCapabilities", "HarnessModel", "HarnessList"]


class HarnessCapabilities(BaseModel):
    managed_skills: bool
    multiagent: bool
    native_resume: bool


class HarnessModel(BaseModel):
    provider: str
    id: str
    efforts: List[str]


class Harness(BaseModel):
    id: str
    provider: str
    modes: List[str]
    capabilities: HarnessCapabilities
    models: List[HarnessModel]


class HarnessList(BaseModel):
    data: List[Harness]
