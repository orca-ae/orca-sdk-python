"""Function statistics.

Wire names are mirrored verbatim; see `cloud_function_shared` for why. The
one-minute rollup is served under the key `1min`, which is not a Python
identifier, so it is exposed as `one_min` with an alias.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CloudFunctionStats", "CloudFunctionInstanceStats", "CloudFunctionStatsBase"]


class CloudFunctionStatsBase(BaseModel):
    receivedTotal: Optional[int] = None

    processedSuccessfullyTotal: Optional[int] = None

    systemExceptionsTotal: Optional[int] = None

    userExceptionsTotal: Optional[int] = None

    avgProcessLatency: Optional[float] = None


class CloudFunctionInstanceStats(CloudFunctionStatsBase):
    """Statistics for a single function instance."""

    one_min: Optional[CloudFunctionStatsBase] = FieldInfo(alias="1min", default=None)

    lastInvocation: Optional[int] = None

    userMetrics: Optional[Dict[str, float]] = None


class CloudFunctionInstanceStatsMetrics(CloudFunctionStatsBase):
    """The per-instance rollup carried inside an aggregate stats response.

    It repeats the instance shape but names the one-minute window `oneMin`
    rather than `1min`; the contract spells the two differently and we mirror it.
    """

    lastInvocation: Optional[int] = None

    oneMin: Optional[CloudFunctionStatsBase] = None

    userMetrics: Optional[Dict[str, float]] = None


class CloudFunctionStatsInstance(BaseModel):
    instanceId: Optional[int] = None

    metrics: Optional[CloudFunctionInstanceStatsMetrics] = None


class CloudFunctionStats(CloudFunctionStatsBase):
    """Aggregate statistics across every instance of a function."""

    one_min: Optional[CloudFunctionStatsBase] = FieldInfo(alias="1min", default=None)

    lastInvocation: Optional[int] = None

    instances: Optional[List[CloudFunctionStatsInstance]] = None
