"""Function status.

Wire names are mirrored verbatim; see `cloud_function_shared` for why.
"""

from __future__ import annotations

from typing import List, Optional

from .._models import BaseModel
from .cloud_function_shared import CloudRuntimeExceptionInformation

__all__ = ["CloudFunctionStatus", "CloudFunctionInstanceStatus"]


class CloudFunctionInstanceStatus(BaseModel):
    """Status of a single function instance."""

    running: Optional[bool] = None

    error: Optional[str] = None

    numRestarts: Optional[int] = None

    numReceived: Optional[int] = None

    numSuccessfullyProcessed: Optional[int] = None

    numUserExceptions: Optional[int] = None

    latestUserExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    numSystemExceptions: Optional[int] = None

    latestSystemExceptions: Optional[List[CloudRuntimeExceptionInformation]] = None

    averageLatency: Optional[float] = None

    lastInvocationTime: Optional[int] = None

    workerId: Optional[str] = None


class CloudFunctionStatusInstance(BaseModel):
    instanceId: Optional[int] = None

    status: Optional[CloudFunctionInstanceStatus] = None


class CloudFunctionStatus(BaseModel):
    """Aggregate status across every instance of a function."""

    numInstances: Optional[int] = None

    numRunning: Optional[int] = None

    instances: Optional[List[CloudFunctionStatusInstance]] = None
