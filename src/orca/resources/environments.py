from __future__ import annotations

from typing import Dict, Optional

import httpx2

from ..types import environment_list_params, environment_create_params, environment_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPageCursor, AsyncPageCursor
from .._base_client import AsyncPaginator, make_request_options
from ..types.environment import Environment, EnvironmentScope, DeletedEnvironment
from ..types.environment_shared import EnvironmentConfigParam

__all__ = ["Environments", "AsyncEnvironments"]


class Environments(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnvironmentsWithRawResponse:
        return EnvironmentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnvironmentsWithStreamingResponse:
        return EnvironmentsWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        config: Optional[EnvironmentConfigParam] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        scope: Optional[EnvironmentScope] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Create an environment in the registry.

        Args:
          name: Human-readable name for the environment.

          description: Free-text description.

          config: Package, networking, and target selection. The discriminator is optional here
              and defaults to `cloud`; responses always carry it. The contract's flat
              `packages`, `networking`, `image`, and `target` fields are not portable across
              backends and are deliberately not exposed — use `config` instead.

          metadata: Arbitrary string key/value pairs.

          scope: Visibility of the environment. Omit to accept the deployment's default.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/environments",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "scope": scope,
                },
                environment_create_params.EnvironmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    def retrieve(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Retrieve an environment.

        Args:
          environment_id: The environment to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return self._get(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    def update(
        self,
        environment_id: str,
        *,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        config: Optional[EnvironmentConfigParam] | Omit = omit,
        metadata: Dict[str, Optional[str]] | Omit = omit,
        scope: Optional[EnvironmentScope] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Partially update an environment.

        Uses POST, matching the contract. Environments carry no version field, so
        there is no optimistic-concurrency check here: last write wins.

        Args:
          environment_id: The environment to update.

          config: Replaces the stored config wholesale rather than merging into it.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return self._post(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "scope": scope,
                },
                environment_update_params.EnvironmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[Environment]:
        """
        List environments.

        Args:
          limit: Maximum number of environments to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived environments in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/environments",
            page=SyncPageCursor[Environment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    environment_list_params.EnvironmentListParams,
                ),
            ),
            model=Environment,
        )

    def delete(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedEnvironment:
        """
        Permanently delete an environment and return its tombstone.

        Unlike `archive`, this is irreversible and the environment stops being
        retrievable by id. Prefer `archive` when you only want it out of listings.

        Args:
          environment_id: The environment to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return self._delete(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedEnvironment,
        )

    def archive(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Archive an environment and return it.

        Archiving hides the environment from default listings while keeping it
        retrievable by id and usable by sessions that already reference it. It is
        reversible in a way `delete` is not.

        Args:
          environment_id: The environment to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return self._post(
            path_template("/v1/environments/{environment_id}/archive", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )


class AsyncEnvironments(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnvironmentsWithRawResponse:
        return AsyncEnvironmentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnvironmentsWithStreamingResponse:
        return AsyncEnvironmentsWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        config: Optional[EnvironmentConfigParam] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        scope: Optional[EnvironmentScope] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Create an environment in the registry.

        Args:
          name: Human-readable name for the environment.

          description: Free-text description.

          config: Package, networking, and target selection. The discriminator is optional here
              and defaults to `cloud`; responses always carry it. The contract's flat
              `packages`, `networking`, `image`, and `target` fields are not portable across
              backends and are deliberately not exposed — use `config` instead.

          metadata: Arbitrary string key/value pairs.

          scope: Visibility of the environment. Omit to accept the deployment's default.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/environments",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "scope": scope,
                },
                environment_create_params.EnvironmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    async def retrieve(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Retrieve an environment.

        Args:
          environment_id: The environment to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return await self._get(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    async def update(
        self,
        environment_id: str,
        *,
        name: Optional[str] | Omit = omit,
        description: Optional[str] | Omit = omit,
        config: Optional[EnvironmentConfigParam] | Omit = omit,
        metadata: Dict[str, Optional[str]] | Omit = omit,
        scope: Optional[EnvironmentScope] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Partially update an environment.

        Uses POST, matching the contract. Environments carry no version field, so
        there is no optimistic-concurrency check here: last write wins.

        Args:
          environment_id: The environment to update.

          config: Replaces the stored config wholesale rather than merging into it.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return await self._post(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "config": config,
                    "metadata": metadata,
                    "scope": scope,
                },
                environment_update_params.EnvironmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Environment, AsyncPageCursor[Environment]]:
        """
        List environments.

        Args:
          limit: Maximum number of environments to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived environments in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/environments",
            page=AsyncPageCursor[Environment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    environment_list_params.EnvironmentListParams,
                ),
            ),
            model=Environment,
        )

    async def delete(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedEnvironment:
        """
        Permanently delete an environment and return its tombstone.

        Unlike `archive`, this is irreversible and the environment stops being
        retrievable by id. Prefer `archive` when you only want it out of listings.

        Args:
          environment_id: The environment to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return await self._delete(
            path_template("/v1/environments/{environment_id}", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedEnvironment,
        )

    async def archive(
        self,
        environment_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Environment:
        """
        Archive an environment and return it.

        Archiving hides the environment from default listings while keeping it
        retrievable by id and usable by sessions that already reference it. It is
        reversible in a way `delete` is not.

        Args:
          environment_id: The environment to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        return await self._post(
            path_template("/v1/environments/{environment_id}/archive", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Environment,
        )


class EnvironmentsWithRawResponse:
    def __init__(self, environments: Environments) -> None:
        self._environments = environments

        self.create = to_raw_response_wrapper(environments.create)
        self.retrieve = to_raw_response_wrapper(environments.retrieve)
        self.update = to_raw_response_wrapper(environments.update)
        self.list = to_raw_response_wrapper(environments.list)
        self.delete = to_raw_response_wrapper(environments.delete)
        self.archive = to_raw_response_wrapper(environments.archive)


class AsyncEnvironmentsWithRawResponse:
    def __init__(self, environments: AsyncEnvironments) -> None:
        self._environments = environments

        self.create = async_to_raw_response_wrapper(environments.create)
        self.retrieve = async_to_raw_response_wrapper(environments.retrieve)
        self.update = async_to_raw_response_wrapper(environments.update)
        self.list = async_to_raw_response_wrapper(environments.list)
        self.delete = async_to_raw_response_wrapper(environments.delete)
        self.archive = async_to_raw_response_wrapper(environments.archive)


class EnvironmentsWithStreamingResponse:
    def __init__(self, environments: Environments) -> None:
        self._environments = environments

        self.create = to_streamed_response_wrapper(environments.create)
        self.retrieve = to_streamed_response_wrapper(environments.retrieve)
        self.update = to_streamed_response_wrapper(environments.update)
        self.list = to_streamed_response_wrapper(environments.list)
        self.delete = to_streamed_response_wrapper(environments.delete)
        self.archive = to_streamed_response_wrapper(environments.archive)


class AsyncEnvironmentsWithStreamingResponse:
    def __init__(self, environments: AsyncEnvironments) -> None:
        self._environments = environments

        self.create = async_to_streamed_response_wrapper(environments.create)
        self.retrieve = async_to_streamed_response_wrapper(environments.retrieve)
        self.update = async_to_streamed_response_wrapper(environments.update)
        self.list = async_to_streamed_response_wrapper(environments.list)
        self.delete = async_to_streamed_response_wrapper(environments.delete)
        self.archive = async_to_streamed_response_wrapper(environments.archive)
