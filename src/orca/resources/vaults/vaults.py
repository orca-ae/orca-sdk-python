from __future__ import annotations

from typing import Dict, Optional

import httpx2

from ...types import vault_list_params, vault_create_params, vault_update_params
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
from .credentials import (
    Credentials,
    AsyncCredentials,
    CredentialsWithRawResponse,
    AsyncCredentialsWithRawResponse,
    CredentialsWithStreamingResponse,
    AsyncCredentialsWithStreamingResponse,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.vault import Vault, DeletedVault
from ..._base_client import AsyncPaginator, make_request_options

__all__ = ["Vaults", "AsyncVaults"]


class Vaults(SyncAPIResource):
    @cached_property
    def credentials(self) -> Credentials:
        return Credentials(self._client)

    @cached_property
    def with_raw_response(self) -> VaultsWithRawResponse:
        return VaultsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VaultsWithStreamingResponse:
        return VaultsWithStreamingResponse(self)

    def create(
        self,
        *,
        display_name: str,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Create a vault.

        Args:
          display_name: Human-readable name for the vault.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/vaults",
            body=maybe_transform(
                {"display_name": display_name, "metadata": metadata},
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )

    def retrieve(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Retrieve a vault.

        Args:
          vault_id: The vault to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._get(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )

    def update(
        self,
        vault_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Partially update a vault.

        Uses POST, matching the contract. Omitted fields keep their stored value.

        Args:
          vault_id: The vault to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._post(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            body=maybe_transform(
                {"display_name": display_name, "metadata": metadata},
                vault_update_params.VaultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
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
    ) -> SyncPageCursor[Vault]:
        """
        List vaults.

        Args:
          limit: Maximum number of vaults to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived vaults in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/vaults",
            page=SyncPageCursor[Vault],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    vault_list_params.VaultListParams,
                ),
            ),
            model=Vault,
        )

    def delete(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedVault:
        """
        Permanently delete a vault and return its tombstone.

        Use `archive` instead to retire a vault while keeping it retrievable by id.

        Args:
          vault_id: The vault to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._delete(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedVault,
        )

    def archive(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Archive a vault and return it.

        Archiving hides the vault from default listings while keeping it retrievable by
        id. It is not a delete: `delete` removes the vault permanently.

        Args:
          vault_id: The vault to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._post(
            path_template("/v1/vaults/{vault_id}/archive", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )


class AsyncVaults(AsyncAPIResource):
    @cached_property
    def credentials(self) -> AsyncCredentials:
        return AsyncCredentials(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVaultsWithRawResponse:
        return AsyncVaultsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVaultsWithStreamingResponse:
        return AsyncVaultsWithStreamingResponse(self)

    async def create(
        self,
        *,
        display_name: str,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Create a vault.

        Args:
          display_name: Human-readable name for the vault.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/vaults",
            body=await async_maybe_transform(
                {"display_name": display_name, "metadata": metadata},
                vault_create_params.VaultCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )

    async def retrieve(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Retrieve a vault.

        Args:
          vault_id: The vault to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return await self._get(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )

    async def update(
        self,
        vault_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Partially update a vault.

        Uses POST, matching the contract. Omitted fields keep their stored value.

        Args:
          vault_id: The vault to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return await self._post(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            body=await async_maybe_transform(
                {"display_name": display_name, "metadata": metadata},
                vault_update_params.VaultUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
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
    ) -> AsyncPaginator[Vault, AsyncPageCursor[Vault]]:
        """
        List vaults.

        Args:
          limit: Maximum number of vaults to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived vaults in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/vaults",
            page=AsyncPageCursor[Vault],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    vault_list_params.VaultListParams,
                ),
            ),
            model=Vault,
        )

    async def delete(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedVault:
        """
        Permanently delete a vault and return its tombstone.

        Use `archive` instead to retire a vault while keeping it retrievable by id.

        Args:
          vault_id: The vault to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return await self._delete(
            path_template("/v1/vaults/{vault_id}", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedVault,
        )

    async def archive(
        self,
        vault_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> Vault:
        """
        Archive a vault and return it.

        Archiving hides the vault from default listings while keeping it retrievable by
        id. It is not a delete: `delete` removes the vault permanently.

        Args:
          vault_id: The vault to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return await self._post(
            path_template("/v1/vaults/{vault_id}/archive", vault_id=vault_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Vault,
        )


class VaultsWithRawResponse:
    def __init__(self, vaults: Vaults) -> None:
        self._vaults = vaults

        self.create = to_raw_response_wrapper(vaults.create)
        self.retrieve = to_raw_response_wrapper(vaults.retrieve)
        self.update = to_raw_response_wrapper(vaults.update)
        self.list = to_raw_response_wrapper(vaults.list)
        self.delete = to_raw_response_wrapper(vaults.delete)
        self.archive = to_raw_response_wrapper(vaults.archive)

    @cached_property
    def credentials(self) -> CredentialsWithRawResponse:
        return CredentialsWithRawResponse(self._vaults.credentials)


class AsyncVaultsWithRawResponse:
    def __init__(self, vaults: AsyncVaults) -> None:
        self._vaults = vaults

        self.create = async_to_raw_response_wrapper(vaults.create)
        self.retrieve = async_to_raw_response_wrapper(vaults.retrieve)
        self.update = async_to_raw_response_wrapper(vaults.update)
        self.list = async_to_raw_response_wrapper(vaults.list)
        self.delete = async_to_raw_response_wrapper(vaults.delete)
        self.archive = async_to_raw_response_wrapper(vaults.archive)

    @cached_property
    def credentials(self) -> AsyncCredentialsWithRawResponse:
        return AsyncCredentialsWithRawResponse(self._vaults.credentials)


class VaultsWithStreamingResponse:
    def __init__(self, vaults: Vaults) -> None:
        self._vaults = vaults

        self.create = to_streamed_response_wrapper(vaults.create)
        self.retrieve = to_streamed_response_wrapper(vaults.retrieve)
        self.update = to_streamed_response_wrapper(vaults.update)
        self.list = to_streamed_response_wrapper(vaults.list)
        self.delete = to_streamed_response_wrapper(vaults.delete)
        self.archive = to_streamed_response_wrapper(vaults.archive)

    @cached_property
    def credentials(self) -> CredentialsWithStreamingResponse:
        return CredentialsWithStreamingResponse(self._vaults.credentials)


class AsyncVaultsWithStreamingResponse:
    def __init__(self, vaults: AsyncVaults) -> None:
        self._vaults = vaults

        self.create = async_to_streamed_response_wrapper(vaults.create)
        self.retrieve = async_to_streamed_response_wrapper(vaults.retrieve)
        self.update = async_to_streamed_response_wrapper(vaults.update)
        self.list = async_to_streamed_response_wrapper(vaults.list)
        self.delete = async_to_streamed_response_wrapper(vaults.delete)
        self.archive = async_to_streamed_response_wrapper(vaults.archive)

    @cached_property
    def credentials(self) -> AsyncCredentialsWithStreamingResponse:
        return AsyncCredentialsWithStreamingResponse(self._vaults.credentials)
