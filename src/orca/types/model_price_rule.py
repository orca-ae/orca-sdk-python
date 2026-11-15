# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "ModelPriceRule",
    "ModelPriceRuleConditions",
    "ModelPriceRuleTokenRange",
    "ModelPriceRuleRates",
    "ModelPriceRuleProvenance",
    "ConditionalModel",
]


class ModelPriceRuleTokenRange(BaseModel):
    min: int
    max: Optional[int]


class ModelPriceRuleConditions(BaseModel):
    service_tier: str
    request_input_tokens: ModelPriceRuleTokenRange


class ModelPriceRuleRates(BaseModel):
    input_per_million_tokens: float
    output_per_million_tokens: float
    cache_read_per_million_tokens: Optional[float]
    cache_write_per_million_tokens: Optional[float]
    cache_write_1h_per_million_tokens: Optional[float]


class ModelPriceRuleProvenance(BaseModel):
    source_id: str
    document_sha256: str
    adapter_version: str
    observed_at: str


class ConditionalModel(BaseModel):
    provider: str
    model_id: str


class ModelPriceRule(BaseModel):
    conditions: ModelPriceRuleConditions
    rates: ModelPriceRuleRates
    rule_set_id: str
    rule_id: str
    revision: int
    provider: str
    model_id: str
    source: Literal["operator", "upstream", "seed"]
    organization_id: Optional[str] = None
    usage_profile: Literal["exclusive-v1", "anthropic-cache-v1"]  # wire-value
    profile_version: str
    provenance: ModelPriceRuleProvenance
    provider_effective_at: Optional[str]
    active_from: str
    retired_at: Optional[str]
    valid_until: Optional[str]
