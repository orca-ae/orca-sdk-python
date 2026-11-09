# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from typing import Dict

from .._models import BaseModel

__all__ = ["GuardrailDogwoodSchema", "GuardrailDogwoodEventSchemas"]


class GuardrailDogwoodEventSchemas(BaseModel):
    session: str
    principal: str


class GuardrailDogwoodSchema(BaseModel):
    base_schema: str
    event_schemas: GuardrailDogwoodEventSchemas
    language_version: str
    core_version: str
    limits: Dict[str, object]
