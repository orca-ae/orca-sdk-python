# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Dict, List, Optional

import httpx2

from ...types import guardrail_list_params, guardrail_create_params, guardrail_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._constants import POLICY_EXTENSION_GROUP
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from .._extension_gate import extension_gate, async_extension_gate
from ...types.guardrail import Guardrail, DeletedGuardrail
from ...types.guardrail_type import GuardrailTypeList
from ...types.guardrail_bundle import GuardrailBundle
from ...types.guardrail_shared import GuardrailMode, GuardrailPhase, GuardrailScope, GuardrailRuleParam
from ...types.guardrail_dogwood_schema import GuardrailDogwoodSchema

__all__ = ["Guardrails", "AsyncGuardrails"]


class Guardrails(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GuardrailsWithRawResponse:
        return GuardrailsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GuardrailsWithStreamingResponse:
        return GuardrailsWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        rule: GuardrailRuleParam,
        description: Optional[str] | Omit = omit,
        mode: GuardrailMode | Omit = omit,
        enabled: bool | Omit = omit,
        phases: List[GuardrailPhase] | Omit = omit,
        scope: GuardrailScope | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Create a guardrail on a deployment that serves the policy extension."""
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._post(
            "/apis/policy.runorca.ai/v1/guardrails",
            body=maybe_transform(
                {
                    "name": name,
                    "rule": rule,
                    "description": description,
                    "mode": mode,
                    "enabled": enabled,
                    "phases": phases,
                    "scope": scope,
                    "metadata": metadata,
                },
                guardrail_create_params.GuardrailCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    def retrieve(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Retrieve a guardrail by ID."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._get(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    def update(
        self,
        guardrail_id: str,
        *,
        name: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        mode: GuardrailMode | Omit = omit,
        enabled: bool | Omit = omit,
        phases: List[GuardrailPhase] | Omit = omit,
        scope: GuardrailScope | Omit = omit,
        rule: GuardrailRuleParam | Omit = omit,
        metadata: Dict[str, Optional[str]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Partially update a guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._post(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "mode": mode,
                    "enabled": enabled,
                    "phases": phases,
                    "scope": scope,
                    "rule": rule,
                    "metadata": metadata,
                },
                guardrail_update_params.GuardrailUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
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
    ) -> SyncPageCursor[Guardrail]:
        """List visible guardrails."""
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._get_api_list(
            "/apis/policy.runorca.ai/v1/guardrails",
            page=SyncPageCursor[Guardrail],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    guardrail_list_params.GuardrailListParams,
                ),
            ),
            model=Guardrail,
        )

    def archive(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Archive a guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._post(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}/archive", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    def delete(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedGuardrail:
        """Permanently delete an unreferenced guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._delete(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedGuardrail,
        )

    def list_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> GuardrailTypeList:
        """List builtin guardrail types and their parameter schemas."""
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._get(
            "/apis/policy.runorca.ai/v1/guardrailtypes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GuardrailTypeList,
        )

    def dogwood_schema(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> GuardrailDogwoodSchema:
        """Retrieve the engine Dogwood authoring schema.

        Args:
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        extension_gate(self, POLICY_EXTENSION_GROUP)
        return self._get(
            "/apis/policy.runorca.ai/v1/policyschemas/dogwood",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GuardrailDogwoodSchema,
        )

    def effective(
        self,
        *,
        rule_kinds: str | Omit = omit,
        guardrail_capabilities: str | Omit = omit,
        if_none_match: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Optional[GuardrailBundle]:
        """Retrieve an engine policy bundle, or None for 304; raw responses expose lease headers.

        Args:
          rule_kinds: Comma-separated rule kinds supported by the caller.
          guardrail_capabilities: Comma-separated runtime guardrail capabilities.
          if_none_match: Previously received ETag for a conditional lease exchange.
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        extension_gate(self, POLICY_EXTENSION_GROUP)
        options = make_request_options(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            query={"rule_kinds": rule_kinds, "guardrail_capabilities": guardrail_capabilities},
        )
        if not isinstance(if_none_match, Omit):
            options["headers"] = {"If-None-Match": if_none_match, **(extra_headers or {})}
        options["allowed_status_codes"] = (304,)
        return self._get(
            "/apis/policy.runorca.ai/v1/effectiveguardrails",
            options=options,
            cast_to=GuardrailBundle,
        )


class AsyncGuardrails(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGuardrailsWithRawResponse:
        return AsyncGuardrailsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGuardrailsWithStreamingResponse:
        return AsyncGuardrailsWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        rule: GuardrailRuleParam,
        description: Optional[str] | Omit = omit,
        mode: GuardrailMode | Omit = omit,
        enabled: bool | Omit = omit,
        phases: List[GuardrailPhase] | Omit = omit,
        scope: GuardrailScope | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Create a guardrail on a deployment that serves the policy extension."""
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._post(
            "/apis/policy.runorca.ai/v1/guardrails",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "rule": rule,
                    "description": description,
                    "mode": mode,
                    "enabled": enabled,
                    "phases": phases,
                    "scope": scope,
                    "metadata": metadata,
                },
                guardrail_create_params.GuardrailCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    async def retrieve(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Retrieve a guardrail by ID."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._get(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    async def update(
        self,
        guardrail_id: str,
        *,
        name: str | Omit = omit,
        description: Optional[str] | Omit = omit,
        mode: GuardrailMode | Omit = omit,
        enabled: bool | Omit = omit,
        phases: List[GuardrailPhase] | Omit = omit,
        scope: GuardrailScope | Omit = omit,
        rule: GuardrailRuleParam | Omit = omit,
        metadata: Dict[str, Optional[str]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Partially update a guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._post(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "mode": mode,
                    "enabled": enabled,
                    "phases": phases,
                    "scope": scope,
                    "rule": rule,
                    "metadata": metadata,
                },
                guardrail_update_params.GuardrailUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
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
    ) -> AsyncPaginator[Guardrail, AsyncPageCursor[Guardrail]]:
        """List visible guardrails."""
        return self._get_api_list(
            "/apis/policy.runorca.ai/v1/guardrails",
            page=AsyncPageCursor[Guardrail],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    guardrail_list_params.GuardrailListParams,
                ),
            ),
            model=Guardrail,
            pre_request=lambda: async_extension_gate(self, POLICY_EXTENSION_GROUP),
        )

    async def archive(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Guardrail:
        """Archive a guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._post(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}/archive", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Guardrail,
        )

    async def delete(
        self,
        guardrail_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedGuardrail:
        """Permanently delete an unreferenced guardrail."""
        if not guardrail_id:
            raise ValueError(f"Expected a non-empty value for `guardrail_id` but received {guardrail_id!r}")
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._delete(
            path_template("/apis/policy.runorca.ai/v1/guardrails/{guardrail_id}", guardrail_id=guardrail_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedGuardrail,
        )

    async def list_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> GuardrailTypeList:
        """List builtin guardrail types and their parameter schemas."""
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._get(
            "/apis/policy.runorca.ai/v1/guardrailtypes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GuardrailTypeList,
        )

    async def dogwood_schema(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> GuardrailDogwoodSchema:
        """Retrieve the engine Dogwood authoring schema.

        Args:
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        return await self._get(
            "/apis/policy.runorca.ai/v1/policyschemas/dogwood",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GuardrailDogwoodSchema,
        )

    async def effective(
        self,
        *,
        rule_kinds: str | Omit = omit,
        guardrail_capabilities: str | Omit = omit,
        if_none_match: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Optional[GuardrailBundle]:
        """Retrieve an engine policy bundle, or None for 304; raw responses expose lease headers.

        Args:
          rule_kinds: Comma-separated rule kinds supported by the caller.
          guardrail_capabilities: Comma-separated runtime guardrail capabilities.
          if_none_match: Previously received ETag for a conditional lease exchange.
          extra_headers: Send extra headers
          extra_query: Add additional query parameters to the request
          extra_body: Add additional JSON properties to the request
          timeout: Override the client-level default timeout for this request, in seconds
        """
        await async_extension_gate(self, POLICY_EXTENSION_GROUP)
        options = make_request_options(
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            query={"rule_kinds": rule_kinds, "guardrail_capabilities": guardrail_capabilities},
        )
        if not isinstance(if_none_match, Omit):
            options["headers"] = {"If-None-Match": if_none_match, **(extra_headers or {})}
        options["allowed_status_codes"] = (304,)
        return await self._get(
            "/apis/policy.runorca.ai/v1/effectiveguardrails",
            options=options,
            cast_to=GuardrailBundle,
        )


class GuardrailsWithRawResponse:
    def __init__(self, guardrails: Guardrails) -> None:
        self._guardrails = guardrails
        self.create = to_raw_response_wrapper(guardrails.create)
        self.retrieve = to_raw_response_wrapper(guardrails.retrieve)
        self.update = to_raw_response_wrapper(guardrails.update)
        self.list = to_raw_response_wrapper(guardrails.list)
        self.archive = to_raw_response_wrapper(guardrails.archive)
        self.delete = to_raw_response_wrapper(guardrails.delete)
        self.list_types = to_raw_response_wrapper(guardrails.list_types)
        self.dogwood_schema = to_raw_response_wrapper(guardrails.dogwood_schema)
        self.effective = to_raw_response_wrapper(guardrails.effective)


class AsyncGuardrailsWithRawResponse:
    def __init__(self, guardrails: AsyncGuardrails) -> None:
        self._guardrails = guardrails
        self.create = async_to_raw_response_wrapper(guardrails.create)
        self.retrieve = async_to_raw_response_wrapper(guardrails.retrieve)
        self.update = async_to_raw_response_wrapper(guardrails.update)
        self.list = async_to_raw_response_wrapper(guardrails.list)
        self.archive = async_to_raw_response_wrapper(guardrails.archive)
        self.delete = async_to_raw_response_wrapper(guardrails.delete)
        self.list_types = async_to_raw_response_wrapper(guardrails.list_types)
        self.dogwood_schema = async_to_raw_response_wrapper(guardrails.dogwood_schema)
        self.effective = async_to_raw_response_wrapper(guardrails.effective)


class GuardrailsWithStreamingResponse:
    def __init__(self, guardrails: Guardrails) -> None:
        self._guardrails = guardrails
        self.create = to_streamed_response_wrapper(guardrails.create)
        self.retrieve = to_streamed_response_wrapper(guardrails.retrieve)
        self.update = to_streamed_response_wrapper(guardrails.update)
        self.list = to_streamed_response_wrapper(guardrails.list)
        self.archive = to_streamed_response_wrapper(guardrails.archive)
        self.delete = to_streamed_response_wrapper(guardrails.delete)
        self.list_types = to_streamed_response_wrapper(guardrails.list_types)
        self.dogwood_schema = to_streamed_response_wrapper(guardrails.dogwood_schema)
        self.effective = to_streamed_response_wrapper(guardrails.effective)


class AsyncGuardrailsWithStreamingResponse:
    def __init__(self, guardrails: AsyncGuardrails) -> None:
        self._guardrails = guardrails
        self.create = async_to_streamed_response_wrapper(guardrails.create)
        self.retrieve = async_to_streamed_response_wrapper(guardrails.retrieve)
        self.update = async_to_streamed_response_wrapper(guardrails.update)
        self.list = async_to_streamed_response_wrapper(guardrails.list)
        self.archive = async_to_streamed_response_wrapper(guardrails.archive)
        self.delete = async_to_streamed_response_wrapper(guardrails.delete)
        self.list_types = async_to_streamed_response_wrapper(guardrails.list_types)
        self.dogwood_schema = async_to_streamed_response_wrapper(guardrails.dogwood_schema)
        self.effective = async_to_streamed_response_wrapper(guardrails.effective)
