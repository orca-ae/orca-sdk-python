# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from typing_extensions import TypedDict

__all__ = ["ModelPriceRuleListParams"]


class ModelPriceRuleListParams(TypedDict, total=False):
    limit: int
    page: str
