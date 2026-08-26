"""Functions served by the `cloud.sn.io` extension.

Wire field names are mirrored verbatim throughout the cloud namespace; see
`orca.types.cloud_function_shared` for why.

Several actions here are spelled as a colon suffix on the resource path --
`/functions/{name}:restart`, `/functions/{name}/{instanceId}:stop`. That is the
contract's spelling, not a convenience of this SDK, and the colon reaches the
server unescaped.
"""

from __future__ import annotations

from typing import Any, List, cast

import httpx2

from ._gate import cloud_gate, async_cloud_gate
from ...types import (
    cloud_function_create_params,
    cloud_function_update_params,
    cloud_function_trigger_params,
    cloud_function_update_state_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ..._utils import transform, path_template, async_transform
from ..._compat import cached_property
from ._multipart import encode_cloud_multipart
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.cloud_function_state import CloudFunctionState, CloudFunctionStateParam
from ...types.cloud_function_stats import CloudFunctionStats, CloudFunctionInstanceStats
from ...types.cloud_function_config import CloudFunctionConfig, CloudFunctionConfigParam
from ...types.cloud_function_shared import CloudRuntimeUpdateOptionsParam
from ...types.cloud_function_status import CloudFunctionStatus, CloudFunctionInstanceStatus

__all__ = ["Functions", "AsyncFunctions"]


class Functions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FunctionsWithRawResponse:
        return FunctionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FunctionsWithStreamingResponse:
        return FunctionsWithStreamingResponse(self)

    def create(
        self,
        function_name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        function_config: CloudFunctionConfigParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Register a function.

        The body is `multipart/form-data`. `functionConfig` is a structured
        value, so it travels as its own JSON part rather than as a form scalar;
        `_multipart.py` explains the encoding. The contract declares no response
        schema, so the parsed body is returned as-is.

        Args:
          function_name: The name to register the function under.

          data: The function archive to upload. Use this or `url`, not both.

          url: A location the server fetches the archive from instead of `data`.

          function_config: The function's configuration document. Sent as `functionConfig`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            transform(
                {"data": data, "url": url, "function_config": function_config},
                cloud_function_create_params.CloudFunctionCreateParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionConfig:
        """
        Retrieve a function's configuration, with server defaults filled in.

        Args:
          function_name: The function to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionConfig,
        )

    def update(
        self,
        function_name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        function_config: CloudFunctionConfigParam | Omit = omit,
        update_options: CloudRuntimeUpdateOptionsParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Update a registered function.

        A `PUT` carrying `multipart/form-data`: the structured parts
        (`functionConfig`, `updateOptions`) travel as their own JSON parts. The
        contract declares no response schema, so the parsed body is returned as-is.

        Args:
          function_name: The function to update.

          data: A replacement archive to upload. Use this or `url`, not both.

          url: A location the server fetches the replacement archive from instead of `data`.

          function_config: The configuration to apply. Sent as `functionConfig`.

          update_options: Controls applied to the update itself, such as whether stored auth data is
              refreshed. Sent as `updateOptions`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            transform(
                {"data": data, "url": url, "function_config": function_config, "update_options": update_options},
                cloud_function_update_params.CloudFunctionUpdateParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._put(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def delete(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deregister a function.

        Args:
          function_name: The function to deregister.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve_instance_stats(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionInstanceStats:
        """
        Retrieve statistics for one function instance.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to report on, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}/stats",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionInstanceStats,
        )

    def retrieve_instance_status(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionInstanceStatus:
        """
        Retrieve status for one function instance.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to report on, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}/status",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionInstanceStatus,
        )

    def retrieve_state(
        self,
        function_name: str,
        key: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionState:
        """
        Read one entry from a function's state store.

        Args:
          function_name: The function whose state is read.

          key: The state key to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/state/{key}", function_name=function_name, key=key
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionState,
        )

    def update_state(
        self,
        function_name: str,
        key: str,
        *,
        state: CloudFunctionStateParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Write one entry to a function's state store.

        The body is `multipart/form-data` with a single structured part, so
        `state` is sent as a JSON document rather than as form scalars. The
        contract declares no response schema, so the parsed body is returned as-is.

        Args:
          function_name: The function whose state is written.

          key: The state key to write.

          state: The value to store. Set exactly one of `stringValue`, `byteValue`, or `numberValue`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            transform({"state": state}, cloud_function_update_state_params.CloudFunctionUpdateStateParams)
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/state/{key}", function_name=function_name, key=key
            ),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve_stats(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionStats:
        """
        Retrieve statistics aggregated across every instance of a function.

        Args:
          function_name: The function to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}/stats", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionStats,
        )

    def retrieve_status(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionStatus:
        """
        Retrieve status aggregated across every instance of a function.

        Args:
          function_name: The function to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}/status", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionStatus,
        )

    def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> List[str]:
        """
        List the names of every registered function.

        The contract returns names only, and returns all of them; there is no cursor.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            "/apis/cloud.sn.io/v1/functions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, List[str]),  # List types cannot be passed as arguments in the type system
        )

    def restart(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart every instance of a function.

        Args:
          function_name: The function to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:restart", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def restart_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to restart, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:restart",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def start(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start every instance of a function.

        Args:
          function_name: The function to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:start", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def start_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to start, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:start",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def stop(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop every instance of a function.

        Args:
          function_name: The function to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:stop", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def stop_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to stop, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:stop",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def trigger(
        self,
        function_name: str,
        *,
        data: str | Omit = omit,
        data_stream: FileTypes | Omit = omit,
        topic: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Trigger a function with one input message and return its output.

        The body is `multipart/form-data`. The response body is handed back as
        raw text rather than JSON-decoded, so a contract that quotes the output
        leaves the quotes in place -- the same convention `health` uses for its
        scalar responses.

        Args:
          function_name: The function to trigger.

          data: Inline input. Unlike the create/update `data` part, this one is text.

          data_stream: Input read from a file or stream instead of `data`. Sent as `dataStream`.

          topic: The input topic to publish the trigger message to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            transform(
                {"data": data, "data_stream": data_stream, "topic": topic},
                cloud_function_trigger_params.CloudFunctionTriggerParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:trigger", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncFunctions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFunctionsWithRawResponse:
        return AsyncFunctionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFunctionsWithStreamingResponse:
        return AsyncFunctionsWithStreamingResponse(self)

    async def create(
        self,
        function_name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        function_config: CloudFunctionConfigParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Register a function.

        The body is `multipart/form-data`. `functionConfig` is a structured
        value, so it travels as its own JSON part rather than as a form scalar;
        `_multipart.py` explains the encoding. The contract declares no response
        schema, so the parsed body is returned as-is.

        Args:
          function_name: The name to register the function under.

          data: The function archive to upload. Use this or `url`, not both.

          url: A location the server fetches the archive from instead of `data`.

          function_config: The function's configuration document. Sent as `functionConfig`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            await async_transform(
                {"data": data, "url": url, "function_config": function_config},
                cloud_function_create_params.CloudFunctionCreateParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionConfig:
        """
        Retrieve a function's configuration, with server defaults filled in.

        Args:
          function_name: The function to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionConfig,
        )

    async def update(
        self,
        function_name: str,
        *,
        data: FileTypes | Omit = omit,
        url: str | Omit = omit,
        function_config: CloudFunctionConfigParam | Omit = omit,
        update_options: CloudRuntimeUpdateOptionsParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Update a registered function.

        A `PUT` carrying `multipart/form-data`: the structured parts
        (`functionConfig`, `updateOptions`) travel as their own JSON parts. The
        contract declares no response schema, so the parsed body is returned as-is.

        Args:
          function_name: The function to update.

          data: A replacement archive to upload. Use this or `url`, not both.

          url: A location the server fetches the replacement archive from instead of `data`.

          function_config: The configuration to apply. Sent as `functionConfig`.

          update_options: Controls applied to the update itself, such as whether stored auth data is
              refreshed. Sent as `updateOptions`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            await async_transform(
                {"data": data, "url": url, "function_config": function_config, "update_options": update_options},
                cloud_function_update_params.CloudFunctionUpdateParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._put(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def delete(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Deregister a function.

        Args:
          function_name: The function to deregister.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve_instance_stats(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionInstanceStats:
        """
        Retrieve statistics for one function instance.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to report on, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}/stats",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionInstanceStats,
        )

    async def retrieve_instance_status(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionInstanceStatus:
        """
        Retrieve status for one function instance.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to report on, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}/status",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionInstanceStatus,
        )

    async def retrieve_state(
        self,
        function_name: str,
        key: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionState:
        """
        Read one entry from a function's state store.

        Args:
          function_name: The function whose state is read.

          key: The state key to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return await self._get(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/state/{key}", function_name=function_name, key=key
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionState,
        )

    async def update_state(
        self,
        function_name: str,
        key: str,
        *,
        state: CloudFunctionStateParam | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Write one entry to a function's state store.

        The body is `multipart/form-data` with a single structured part, so
        `state` is sent as a JSON document rather than as form scalars. The
        contract declares no response schema, so the parsed body is returned as-is.

        Args:
          function_name: The function whose state is written.

          key: The state key to write.

          state: The value to store. Set exactly one of `stringValue`, `byteValue`, or `numberValue`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            await async_transform({"state": state}, cloud_function_update_state_params.CloudFunctionUpdateStateParams)
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/state/{key}", function_name=function_name, key=key
            ),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve_stats(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionStats:
        """
        Retrieve statistics aggregated across every instance of a function.

        Args:
          function_name: The function to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}/stats", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionStats,
        )

    async def retrieve_status(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudFunctionStatus:
        """
        Retrieve status aggregated across every instance of a function.

        Args:
          function_name: The function to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        return await self._get(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}/status", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudFunctionStatus,
        )

    async def list(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> List[str]:
        """
        List the names of every registered function.

        The contract returns names only, and returns all of them; there is no cursor.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            "/apis/cloud.sn.io/v1/functions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, List[str]),  # List types cannot be passed as arguments in the type system
        )

    async def restart(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart every instance of a function.

        Args:
          function_name: The function to restart.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:restart", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def restart_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to restart, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:restart",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def start(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start every instance of a function.

        Args:
          function_name: The function to start.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:start", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def start_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Start one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to start, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:start",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def stop(
        self,
        function_name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop every instance of a function.

        Args:
          function_name: The function to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:stop", function_name=function_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def stop_instance(
        self,
        function_name: str,
        instance_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop one instance of a function.

        Args:
          function_name: The function the instance belongs to.

          instance_id: The instance to stop, as a string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        if not instance_id:
            raise ValueError(f"Expected a non-empty value for `instance_id` but received {instance_id!r}")
        # The success response carries no declared content, so no JSON media type is
        # requested for it.
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/apis/cloud.sn.io/v1/functions/{function_name}/{instance_id}:stop",
                function_name=function_name,
                instance_id=instance_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def trigger(
        self,
        function_name: str,
        *,
        data: str | Omit = omit,
        data_stream: FileTypes | Omit = omit,
        topic: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Trigger a function with one input message and return its output.

        The body is `multipart/form-data`. The response body is handed back as
        raw text rather than JSON-decoded, so a contract that quotes the output
        leaves the quotes in place -- the same convention `health` uses for its
        scalar responses.

        Args:
          function_name: The function to trigger.

          data: Inline input. Unlike the create/update `data` part, this one is text.

          data_stream: Input read from a file or stream instead of `data`. Sent as `dataStream`.

          topic: The input topic to publish the trigger message to.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not function_name:
            raise ValueError(f"Expected a non-empty value for `function_name` but received {function_name!r}")
        # `transform` is load-bearing, not cosmetic: it rewrites these snake_case
        # argument keys into their wire spellings, and the encoder names each part
        # after the key it receives.
        fields, parts = encode_cloud_multipart(
            await async_transform(
                {"data": data, "data_stream": data_stream, "topic": topic},
                cloud_function_trigger_params.CloudFunctionTriggerParams,
            )
        )
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            path_template("/apis/cloud.sn.io/v1/functions/{function_name}:trigger", function_name=function_name),
            body=fields,
            files=parts,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class FunctionsWithRawResponse:
    def __init__(self, functions: Functions) -> None:
        self._functions = functions

        self.create = to_raw_response_wrapper(functions.create)
        self.retrieve = to_raw_response_wrapper(functions.retrieve)
        self.update = to_raw_response_wrapper(functions.update)
        self.delete = to_raw_response_wrapper(functions.delete)
        self.retrieve_instance_stats = to_raw_response_wrapper(functions.retrieve_instance_stats)
        self.retrieve_instance_status = to_raw_response_wrapper(functions.retrieve_instance_status)
        self.retrieve_state = to_raw_response_wrapper(functions.retrieve_state)
        self.update_state = to_raw_response_wrapper(functions.update_state)
        self.retrieve_stats = to_raw_response_wrapper(functions.retrieve_stats)
        self.retrieve_status = to_raw_response_wrapper(functions.retrieve_status)
        self.list = to_raw_response_wrapper(functions.list)
        self.restart = to_raw_response_wrapper(functions.restart)
        self.restart_instance = to_raw_response_wrapper(functions.restart_instance)
        self.start = to_raw_response_wrapper(functions.start)
        self.start_instance = to_raw_response_wrapper(functions.start_instance)
        self.stop = to_raw_response_wrapper(functions.stop)
        self.stop_instance = to_raw_response_wrapper(functions.stop_instance)
        self.trigger = to_raw_response_wrapper(functions.trigger)


class AsyncFunctionsWithRawResponse:
    def __init__(self, functions: AsyncFunctions) -> None:
        self._functions = functions

        self.create = async_to_raw_response_wrapper(functions.create)
        self.retrieve = async_to_raw_response_wrapper(functions.retrieve)
        self.update = async_to_raw_response_wrapper(functions.update)
        self.delete = async_to_raw_response_wrapper(functions.delete)
        self.retrieve_instance_stats = async_to_raw_response_wrapper(functions.retrieve_instance_stats)
        self.retrieve_instance_status = async_to_raw_response_wrapper(functions.retrieve_instance_status)
        self.retrieve_state = async_to_raw_response_wrapper(functions.retrieve_state)
        self.update_state = async_to_raw_response_wrapper(functions.update_state)
        self.retrieve_stats = async_to_raw_response_wrapper(functions.retrieve_stats)
        self.retrieve_status = async_to_raw_response_wrapper(functions.retrieve_status)
        self.list = async_to_raw_response_wrapper(functions.list)
        self.restart = async_to_raw_response_wrapper(functions.restart)
        self.restart_instance = async_to_raw_response_wrapper(functions.restart_instance)
        self.start = async_to_raw_response_wrapper(functions.start)
        self.start_instance = async_to_raw_response_wrapper(functions.start_instance)
        self.stop = async_to_raw_response_wrapper(functions.stop)
        self.stop_instance = async_to_raw_response_wrapper(functions.stop_instance)
        self.trigger = async_to_raw_response_wrapper(functions.trigger)


class FunctionsWithStreamingResponse:
    def __init__(self, functions: Functions) -> None:
        self._functions = functions

        self.create = to_streamed_response_wrapper(functions.create)
        self.retrieve = to_streamed_response_wrapper(functions.retrieve)
        self.update = to_streamed_response_wrapper(functions.update)
        self.delete = to_streamed_response_wrapper(functions.delete)
        self.retrieve_instance_stats = to_streamed_response_wrapper(functions.retrieve_instance_stats)
        self.retrieve_instance_status = to_streamed_response_wrapper(functions.retrieve_instance_status)
        self.retrieve_state = to_streamed_response_wrapper(functions.retrieve_state)
        self.update_state = to_streamed_response_wrapper(functions.update_state)
        self.retrieve_stats = to_streamed_response_wrapper(functions.retrieve_stats)
        self.retrieve_status = to_streamed_response_wrapper(functions.retrieve_status)
        self.list = to_streamed_response_wrapper(functions.list)
        self.restart = to_streamed_response_wrapper(functions.restart)
        self.restart_instance = to_streamed_response_wrapper(functions.restart_instance)
        self.start = to_streamed_response_wrapper(functions.start)
        self.start_instance = to_streamed_response_wrapper(functions.start_instance)
        self.stop = to_streamed_response_wrapper(functions.stop)
        self.stop_instance = to_streamed_response_wrapper(functions.stop_instance)
        self.trigger = to_streamed_response_wrapper(functions.trigger)


class AsyncFunctionsWithStreamingResponse:
    def __init__(self, functions: AsyncFunctions) -> None:
        self._functions = functions

        self.create = async_to_streamed_response_wrapper(functions.create)
        self.retrieve = async_to_streamed_response_wrapper(functions.retrieve)
        self.update = async_to_streamed_response_wrapper(functions.update)
        self.delete = async_to_streamed_response_wrapper(functions.delete)
        self.retrieve_instance_stats = async_to_streamed_response_wrapper(functions.retrieve_instance_stats)
        self.retrieve_instance_status = async_to_streamed_response_wrapper(functions.retrieve_instance_status)
        self.retrieve_state = async_to_streamed_response_wrapper(functions.retrieve_state)
        self.update_state = async_to_streamed_response_wrapper(functions.update_state)
        self.retrieve_stats = async_to_streamed_response_wrapper(functions.retrieve_stats)
        self.retrieve_status = async_to_streamed_response_wrapper(functions.retrieve_status)
        self.list = async_to_streamed_response_wrapper(functions.list)
        self.restart = async_to_streamed_response_wrapper(functions.restart)
        self.restart_instance = async_to_streamed_response_wrapper(functions.restart_instance)
        self.start = async_to_streamed_response_wrapper(functions.start)
        self.start_instance = async_to_streamed_response_wrapper(functions.start_instance)
        self.stop = async_to_streamed_response_wrapper(functions.stop)
        self.stop_instance = async_to_streamed_response_wrapper(functions.stop_instance)
        self.trigger = async_to_streamed_response_wrapper(functions.trigger)
