from __future__ import annotations

from typing import Iterable

import httpx2

from ..._gate import cloud_gate, async_cloud_gate
from .....types import (
    cloud_kafka_connector_create_params,
    cloud_kafka_connector_restart_params,
    cloud_kafka_connector_update_offsets_params,
)
from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template, maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.cloud_kafka_shared import CloudKafkaMessage, CloudKafkaOpenResponse
from .....types.cloud_kafka_connector import (
    CloudKafkaTaskState,
    CloudKafkaTaskInfoList,
    CloudKafkaConnectorInfo,
    CloudKafkaConnectorConfig,
    CloudKafkaConnectorOffsets,
    CloudKafkaConnectorStateInfo,
    CloudKafkaConnectorOffsetParam,
)
from .....types.cloud_kafka_connector_create_params import CloudKafkaInitialState

__all__ = ["KafkaConnectors", "AsyncKafkaConnectors"]

_CONNECTORS = "/apis/cloud.sn.io/v1/connectors/kafka/connectors"


class KafkaConnectors(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KafkaConnectorsWithRawResponse:
        return KafkaConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KafkaConnectorsWithStreamingResponse:
        return KafkaConnectorsWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        List the active connectors.

        The worker answers with a bare JSON object rather than a modelled listing, so
        the decoded object is handed back as-is.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._get(
            _CONNECTORS,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    def create(
        self,
        *,
        name: str | Omit = omit,
        config: CloudKafkaConnectorConfig | Omit = omit,
        initial_state: CloudKafkaInitialState | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Create a connector.

        Args:
          name: Name to create the connector under.

          config: Plugin settings, including the `connector.class` that selects the plugin.

          initial_state: State to start the connector in. The worker defaults it to running.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        return self._post(
            _CONNECTORS,
            body=maybe_transform(
                {"name": name, "config": config, "initial_state": initial_state},
                cloud_kafka_connector_create_params.CloudKafkaConnectorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Retrieve a connector's name, configuration, and task list.

        Args:
          name: The connector to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    def delete(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete a connector and stop its tasks.

        The success response carries no body.

        Args:
          name: The connector to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template(_CONNECTORS + "/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def retrieve_config(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve a connector's configuration.

        The worker returns the configuration as a bare JSON object, so it is handed
        back undecoded rather than as a modelled shape.

        Args:
          name: The connector whose configuration to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/config", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    def update_config(
        self,
        name: str,
        *,
        config: CloudKafkaConnectorConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Replace a connector's configuration.

        The request body is the configuration map itself, not a wrapper around it.

        Args:
          name: The connector to reconfigure. The worker creates it if it does not exist yet.

          config: The complete replacement configuration. This is a `PUT`: keys you leave out are
              dropped, not preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._put(
            path_template(_CONNECTORS + "/{name}/config", name=name),
            body=config,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    def retrieve_status(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorStateInfo:
        """
        Retrieve the state of a connector and each of its tasks.

        Args:
          name: The connector to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/status", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorStateInfo,
        )

    def retrieve_offsets(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorOffsets:
        """
        Retrieve the offsets the worker holds for a connector.

        Args:
          name: The connector whose offsets to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorOffsets,
        )

    def reset_offsets(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaMessage:
        """
        Reset a connector's offsets.

        `DELETE` on the offsets sub-resource, per the contract -- resetting offsets is
        modelled as deleting them, not as an action endpoint. The connector must be
        stopped first.

        Args:
          name: The connector whose offsets to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._delete(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaMessage,
        )

    def update_offsets(
        self,
        name: str,
        *,
        offsets: Iterable[CloudKafkaConnectorOffsetParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaMessage:
        """
        Alter a connector's offsets.

        `PATCH`, not `PUT`: only the partitions named in `offsets` are touched.

        Args:
          name: The connector whose offsets to alter.

          offsets: The offsets to write. The connector must be stopped for the worker to accept
              them.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._patch(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            body=maybe_transform(
                {"offsets": offsets},
                cloud_kafka_connector_update_offsets_params.CloudKafkaConnectorUpdateOffsetsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaMessage,
        )

    def retrieve_active_topics(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve the topics a connector is actively using.

        Args:
          name: The connector to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/topics", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    def reset_active_topics(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Reset the record of which topics a connector is actively using.

        The action lives in the path as a `:reset` suffix, which the contract spells
        literally. The success response carries no body.

        Args:
          name: The connector whose active-topic record to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template(_CONNECTORS + "/{name}/topics", name=name) + ":reset",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def list_tasks(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaTaskInfoList:
        """
        List a connector's tasks and the configuration each was given.

        Args:
          name: The connector whose tasks to list.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/tasks", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaTaskInfoList,
        )

    def retrieve_task_status(
        self,
        name: str,
        task: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaTaskState:
        """
        Retrieve the state of one task.

        Args:
          name: The connector the task belongs to.

          task: Zero-based task index. Zero is a valid index, so it is not rejected as empty.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/tasks/{task}/status", name=name, task=task),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaTaskState,
        )

    def retrieve_tasks_config(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve the worker's task-configuration object for a connector.

        This is the worker's own view of every task's configuration, keyed by task id,
        as opposed to `list_tasks()` which returns them as a list.

        Args:
          name: The connector whose task configuration to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._get(
            path_template(_CONNECTORS + "/{name}/tasks-config", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    def pause(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Pause a connector.

        `PUT` with a `:pause` suffix, spelled literally by the contract. Idempotent:
        pausing an already-paused connector changes nothing. The success response
        carries no body.

        Args:
          name: The connector to pause.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":pause",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def restart(
        self,
        name: str,
        *,
        include_tasks: bool | Omit = omit,
        only_failed: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart a connector, optionally including its tasks.

        `POST` with a `:restart` suffix, spelled literally by the contract. The return
        type is open because the worker answers either with a status object (HTTP 202)
        or with nothing at all (HTTP 204), depending on whether tasks were involved.

        Args:
          name: The connector to restart.

          include_tasks: Whether to restart the connector's tasks as well as the connector itself.

          only_failed: Whether to restart only the failed connector and tasks.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            path_template(_CONNECTORS + "/{name}", name=name) + ":restart",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"includeTasks": include_tasks, "onlyFailed": only_failed},
                    cloud_kafka_connector_restart_params.CloudKafkaConnectorRestartParams,
                ),
            ),
            cast_to=object,
        )

    def restart_task(
        self,
        name: str,
        task: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one task.

        A plain path segment, not a `:restart` suffix -- the contract spells the task
        variant differently from the connector one. The success response carries no
        body.

        Args:
          name: The connector the task belongs to.

          task: Zero-based task index. Zero is a valid index, so it is not rejected as empty.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            path_template(_CONNECTORS + "/{name}/tasks/{task}/restart", name=name, task=task),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def resume(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Resume a connector.

        `PUT` with a `:resume` suffix, spelled literally by the contract. Idempotent:
        resuming an already-running connector changes nothing. The success response
        carries no body.

        Args:
          name: The connector to resume.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":resume",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def stop(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop a connector while keeping it registered.

        `PUT` with a `:stop` suffix, spelled literally by the contract. Stopping keeps
        the connector and its configuration; `delete()` removes them. The success
        response carries no body.

        Args:
          name: The connector to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncKafkaConnectors(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKafkaConnectorsWithRawResponse:
        return AsyncKafkaConnectorsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKafkaConnectorsWithStreamingResponse:
        return AsyncKafkaConnectorsWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        List the active connectors.

        The worker answers with a bare JSON object rather than a modelled listing, so
        the decoded object is handed back as-is.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._get(
            _CONNECTORS,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    async def create(
        self,
        *,
        name: str | Omit = omit,
        config: CloudKafkaConnectorConfig | Omit = omit,
        initial_state: CloudKafkaInitialState | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Create a connector.

        Args:
          name: Name to create the connector under.

          config: Plugin settings, including the `connector.class` that selects the plugin.

          initial_state: State to start the connector in. The worker defaults it to running.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        return await self._post(
            _CONNECTORS,
            body=await async_maybe_transform(
                {"name": name, "config": config, "initial_state": initial_state},
                cloud_kafka_connector_create_params.CloudKafkaConnectorCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    async def retrieve(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Retrieve a connector's name, configuration, and task list.

        Args:
          name: The connector to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    async def delete(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete a connector and stop its tasks.

        The success response carries no body.

        Args:
          name: The connector to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template(_CONNECTORS + "/{name}", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def retrieve_config(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve a connector's configuration.

        The worker returns the configuration as a bare JSON object, so it is handed
        back undecoded rather than as a modelled shape.

        Args:
          name: The connector whose configuration to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/config", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    async def update_config(
        self,
        name: str,
        *,
        config: CloudKafkaConnectorConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorInfo:
        """
        Replace a connector's configuration.

        The request body is the configuration map itself, not a wrapper around it.

        Args:
          name: The connector to reconfigure. The worker creates it if it does not exist yet.

          config: The complete replacement configuration. This is a `PUT`: keys you leave out are
              dropped, not preserved.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._put(
            path_template(_CONNECTORS + "/{name}/config", name=name),
            body=config,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorInfo,
        )

    async def retrieve_status(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorStateInfo:
        """
        Retrieve the state of a connector and each of its tasks.

        Args:
          name: The connector to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/status", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorStateInfo,
        )

    async def retrieve_offsets(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaConnectorOffsets:
        """
        Retrieve the offsets the worker holds for a connector.

        Args:
          name: The connector whose offsets to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaConnectorOffsets,
        )

    async def reset_offsets(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaMessage:
        """
        Reset a connector's offsets.

        `DELETE` on the offsets sub-resource, per the contract -- resetting offsets is
        modelled as deleting them, not as an action endpoint. The connector must be
        stopped first.

        Args:
          name: The connector whose offsets to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._delete(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaMessage,
        )

    async def update_offsets(
        self,
        name: str,
        *,
        offsets: Iterable[CloudKafkaConnectorOffsetParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaMessage:
        """
        Alter a connector's offsets.

        `PATCH`, not `PUT`: only the partitions named in `offsets` are touched.

        Args:
          name: The connector whose offsets to alter.

          offsets: The offsets to write. The connector must be stopped for the worker to accept
              them.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._patch(
            path_template(_CONNECTORS + "/{name}/offsets", name=name),
            body=await async_maybe_transform(
                {"offsets": offsets},
                cloud_kafka_connector_update_offsets_params.CloudKafkaConnectorUpdateOffsetsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaMessage,
        )

    async def retrieve_active_topics(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve the topics a connector is actively using.

        Args:
          name: The connector to report on.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/topics", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    async def reset_active_topics(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Reset the record of which topics a connector is actively using.

        The action lives in the path as a `:reset` suffix, which the contract spells
        literally. The success response carries no body.

        Args:
          name: The connector whose active-topic record to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template(_CONNECTORS + "/{name}/topics", name=name) + ":reset",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def list_tasks(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaTaskInfoList:
        """
        List a connector's tasks and the configuration each was given.

        Args:
          name: The connector whose tasks to list.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/tasks", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaTaskInfoList,
        )

    async def retrieve_task_status(
        self,
        name: str,
        task: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaTaskState:
        """
        Retrieve the state of one task.

        Args:
          name: The connector the task belongs to.

          task: Zero-based task index. Zero is a valid index, so it is not rejected as empty.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/tasks/{task}/status", name=name, task=task),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaTaskState,
        )

    async def retrieve_tasks_config(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CloudKafkaOpenResponse:
        """
        Retrieve the worker's task-configuration object for a connector.

        This is the worker's own view of every task's configuration, keyed by task id,
        as opposed to `list_tasks()` which returns them as a list.

        Args:
          name: The connector whose task configuration to read.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._get(
            path_template(_CONNECTORS + "/{name}/tasks-config", name=name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudKafkaOpenResponse,
        )

    async def pause(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Pause a connector.

        `PUT` with a `:pause` suffix, spelled literally by the contract. Idempotent:
        pausing an already-paused connector changes nothing. The success response
        carries no body.

        Args:
          name: The connector to pause.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":pause",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def restart(
        self,
        name: str,
        *,
        include_tasks: bool | Omit = omit,
        only_failed: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart a connector, optionally including its tasks.

        `POST` with a `:restart` suffix, spelled literally by the contract. The return
        type is open because the worker answers either with a status object (HTTP 202)
        or with nothing at all (HTTP 204), depending on whether tasks were involved.

        Args:
          name: The connector to restart.

          include_tasks: Whether to restart the connector's tasks as well as the connector itself.

          only_failed: Whether to restart only the failed connector and tasks.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            path_template(_CONNECTORS + "/{name}", name=name) + ":restart",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"includeTasks": include_tasks, "onlyFailed": only_failed},
                    cloud_kafka_connector_restart_params.CloudKafkaConnectorRestartParams,
                ),
            ),
            cast_to=object,
        )

    async def restart_task(
        self,
        name: str,
        task: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Restart one task.

        A plain path segment, not a `:restart` suffix -- the contract spells the task
        variant differently from the connector one. The success response carries no
        body.

        Args:
          name: The connector the task belongs to.

          task: Zero-based task index. Zero is a valid index, so it is not rejected as empty.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            path_template(_CONNECTORS + "/{name}/tasks/{task}/restart", name=name, task=task),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def resume(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Resume a connector.

        `PUT` with a `:resume` suffix, spelled literally by the contract. Idempotent:
        resuming an already-running connector changes nothing. The success response
        carries no body.

        Args:
          name: The connector to resume.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":resume",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def stop(
        self,
        name: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Stop a connector while keeping it registered.

        `PUT` with a `:stop` suffix, spelled literally by the contract. Stopping keeps
        the connector and its configuration; `delete()` removes them. The success
        response carries no body.

        Args:
          name: The connector to stop.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_cloud_gate(self)
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            path_template(_CONNECTORS + "/{name}", name=name) + ":stop",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class KafkaConnectorsWithRawResponse:
    def __init__(self, connectors: KafkaConnectors) -> None:
        self._connectors = connectors

        self.list = to_raw_response_wrapper(connectors.list)
        self.create = to_raw_response_wrapper(connectors.create)
        self.retrieve = to_raw_response_wrapper(connectors.retrieve)
        self.delete = to_raw_response_wrapper(connectors.delete)
        self.retrieve_config = to_raw_response_wrapper(connectors.retrieve_config)
        self.update_config = to_raw_response_wrapper(connectors.update_config)
        self.retrieve_status = to_raw_response_wrapper(connectors.retrieve_status)
        self.retrieve_offsets = to_raw_response_wrapper(connectors.retrieve_offsets)
        self.reset_offsets = to_raw_response_wrapper(connectors.reset_offsets)
        self.update_offsets = to_raw_response_wrapper(connectors.update_offsets)
        self.retrieve_active_topics = to_raw_response_wrapper(connectors.retrieve_active_topics)
        self.reset_active_topics = to_raw_response_wrapper(connectors.reset_active_topics)
        self.list_tasks = to_raw_response_wrapper(connectors.list_tasks)
        self.retrieve_task_status = to_raw_response_wrapper(connectors.retrieve_task_status)
        self.retrieve_tasks_config = to_raw_response_wrapper(connectors.retrieve_tasks_config)
        self.pause = to_raw_response_wrapper(connectors.pause)
        self.restart = to_raw_response_wrapper(connectors.restart)
        self.restart_task = to_raw_response_wrapper(connectors.restart_task)
        self.resume = to_raw_response_wrapper(connectors.resume)
        self.stop = to_raw_response_wrapper(connectors.stop)


class AsyncKafkaConnectorsWithRawResponse:
    def __init__(self, connectors: AsyncKafkaConnectors) -> None:
        self._connectors = connectors

        self.list = async_to_raw_response_wrapper(connectors.list)
        self.create = async_to_raw_response_wrapper(connectors.create)
        self.retrieve = async_to_raw_response_wrapper(connectors.retrieve)
        self.delete = async_to_raw_response_wrapper(connectors.delete)
        self.retrieve_config = async_to_raw_response_wrapper(connectors.retrieve_config)
        self.update_config = async_to_raw_response_wrapper(connectors.update_config)
        self.retrieve_status = async_to_raw_response_wrapper(connectors.retrieve_status)
        self.retrieve_offsets = async_to_raw_response_wrapper(connectors.retrieve_offsets)
        self.reset_offsets = async_to_raw_response_wrapper(connectors.reset_offsets)
        self.update_offsets = async_to_raw_response_wrapper(connectors.update_offsets)
        self.retrieve_active_topics = async_to_raw_response_wrapper(connectors.retrieve_active_topics)
        self.reset_active_topics = async_to_raw_response_wrapper(connectors.reset_active_topics)
        self.list_tasks = async_to_raw_response_wrapper(connectors.list_tasks)
        self.retrieve_task_status = async_to_raw_response_wrapper(connectors.retrieve_task_status)
        self.retrieve_tasks_config = async_to_raw_response_wrapper(connectors.retrieve_tasks_config)
        self.pause = async_to_raw_response_wrapper(connectors.pause)
        self.restart = async_to_raw_response_wrapper(connectors.restart)
        self.restart_task = async_to_raw_response_wrapper(connectors.restart_task)
        self.resume = async_to_raw_response_wrapper(connectors.resume)
        self.stop = async_to_raw_response_wrapper(connectors.stop)


class KafkaConnectorsWithStreamingResponse:
    def __init__(self, connectors: KafkaConnectors) -> None:
        self._connectors = connectors

        self.list = to_streamed_response_wrapper(connectors.list)
        self.create = to_streamed_response_wrapper(connectors.create)
        self.retrieve = to_streamed_response_wrapper(connectors.retrieve)
        self.delete = to_streamed_response_wrapper(connectors.delete)
        self.retrieve_config = to_streamed_response_wrapper(connectors.retrieve_config)
        self.update_config = to_streamed_response_wrapper(connectors.update_config)
        self.retrieve_status = to_streamed_response_wrapper(connectors.retrieve_status)
        self.retrieve_offsets = to_streamed_response_wrapper(connectors.retrieve_offsets)
        self.reset_offsets = to_streamed_response_wrapper(connectors.reset_offsets)
        self.update_offsets = to_streamed_response_wrapper(connectors.update_offsets)
        self.retrieve_active_topics = to_streamed_response_wrapper(connectors.retrieve_active_topics)
        self.reset_active_topics = to_streamed_response_wrapper(connectors.reset_active_topics)
        self.list_tasks = to_streamed_response_wrapper(connectors.list_tasks)
        self.retrieve_task_status = to_streamed_response_wrapper(connectors.retrieve_task_status)
        self.retrieve_tasks_config = to_streamed_response_wrapper(connectors.retrieve_tasks_config)
        self.pause = to_streamed_response_wrapper(connectors.pause)
        self.restart = to_streamed_response_wrapper(connectors.restart)
        self.restart_task = to_streamed_response_wrapper(connectors.restart_task)
        self.resume = to_streamed_response_wrapper(connectors.resume)
        self.stop = to_streamed_response_wrapper(connectors.stop)


class AsyncKafkaConnectorsWithStreamingResponse:
    def __init__(self, connectors: AsyncKafkaConnectors) -> None:
        self._connectors = connectors

        self.list = async_to_streamed_response_wrapper(connectors.list)
        self.create = async_to_streamed_response_wrapper(connectors.create)
        self.retrieve = async_to_streamed_response_wrapper(connectors.retrieve)
        self.delete = async_to_streamed_response_wrapper(connectors.delete)
        self.retrieve_config = async_to_streamed_response_wrapper(connectors.retrieve_config)
        self.update_config = async_to_streamed_response_wrapper(connectors.update_config)
        self.retrieve_status = async_to_streamed_response_wrapper(connectors.retrieve_status)
        self.retrieve_offsets = async_to_streamed_response_wrapper(connectors.retrieve_offsets)
        self.reset_offsets = async_to_streamed_response_wrapper(connectors.reset_offsets)
        self.update_offsets = async_to_streamed_response_wrapper(connectors.update_offsets)
        self.retrieve_active_topics = async_to_streamed_response_wrapper(connectors.retrieve_active_topics)
        self.reset_active_topics = async_to_streamed_response_wrapper(connectors.reset_active_topics)
        self.list_tasks = async_to_streamed_response_wrapper(connectors.list_tasks)
        self.retrieve_task_status = async_to_streamed_response_wrapper(connectors.retrieve_task_status)
        self.retrieve_tasks_config = async_to_streamed_response_wrapper(connectors.retrieve_tasks_config)
        self.pause = async_to_streamed_response_wrapper(connectors.pause)
        self.restart = async_to_streamed_response_wrapper(connectors.restart)
        self.restart_task = async_to_streamed_response_wrapper(connectors.restart_task)
        self.resume = async_to_streamed_response_wrapper(connectors.resume)
        self.stop = async_to_streamed_response_wrapper(connectors.stop)
