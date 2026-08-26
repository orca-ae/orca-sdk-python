from __future__ import annotations

from typing_extensions import TypedDict

from .cloud_function_state import CloudFunctionStateParam

__all__ = ["CloudFunctionUpdateStateParams"]


class CloudFunctionUpdateStateParams(TypedDict, total=False):
    state: CloudFunctionStateParam
