"""Cloud extension namespace.

Only the `Cloud` router is re-exported here. Its eight sub-namespaces are
deliberately not, so that importing `orca.resources.cloud` -- which
`_client.py` does to mount `client.cloud` -- costs one module rather than the
whole extension surface. Reach a sub-namespace through the router
(`client.cloud.catalog`) or import its module directly
(`orca.resources.cloud.catalog`).
"""

from .cloud import (
    Cloud,
    AsyncCloud,
    CloudWithRawResponse,
    AsyncCloudWithRawResponse,
    CloudWithStreamingResponse,
    AsyncCloudWithStreamingResponse,
)

__all__ = [
    "Cloud",
    "AsyncCloud",
    "CloudWithRawResponse",
    "AsyncCloudWithRawResponse",
    "CloudWithStreamingResponse",
    "AsyncCloudWithStreamingResponse",
]
