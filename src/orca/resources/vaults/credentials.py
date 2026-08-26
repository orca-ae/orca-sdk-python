from __future__ import annotations

from typing import Dict, Optional

import httpx2

from ...types import credential_list_params, credential_create_params, credential_update_params
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
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.vault_credential import VaultCredential, DeletedVaultCredential
from ...types.credential_shared import CredentialCreateAuthParam, CredentialUpdateAuthParam
from ...types.credential_validation import CredentialValidation

__all__ = ["Credentials", "AsyncCredentials"]


class Credentials(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CredentialsWithRawResponse:
        return CredentialsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CredentialsWithStreamingResponse:
        return CredentialsWithStreamingResponse(self)

    def create(
        self,
        vault_id: str,
        *,
        auth: CredentialCreateAuthParam,
        display_name: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Store a credential in a vault.

        Args:
          vault_id: The vault to store the credential in.

          auth: The credential material and how it is presented. Every secret in it is
              write-only: reads return the surrounding configuration without it.

          display_name: Human-readable label for the credential.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._post(
            path_template("/v1/vaults/{vault_id}/credentials", vault_id=vault_id),
            body=maybe_transform(
                {"auth": auth, "display_name": display_name, "metadata": metadata},
                credential_create_params.CredentialCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    def retrieve(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Retrieve a credential.

        The response carries the credential's configuration only; the stored secret is
        write-only and never returned.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._get(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    def update(
        self,
        vault_id: str,
        credential_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        auth: CredentialUpdateAuthParam | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Partially update a credential.

        Uses POST, matching the contract. `auth.type` names the credential shape being
        edited rather than changing it, and omitted fields keep their stored value --
        so rotating a secret means sending just that field.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            body=maybe_transform(
                {"display_name": display_name, "auth": auth, "metadata": metadata},
                credential_update_params.CredentialUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    def list(
        self,
        vault_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[VaultCredential]:
        """
        List the credentials in a vault.

        Args:
          vault_id: The vault whose credentials to list.

          limit: Maximum number of credentials to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived credentials in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._get_api_list(
            path_template("/v1/vaults/{vault_id}/credentials", vault_id=vault_id),
            page=SyncPageCursor[VaultCredential],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    credential_list_params.CredentialListParams,
                ),
            ),
            model=VaultCredential,
        )

    def delete(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedVaultCredential:
        """
        Permanently delete a credential and return its tombstone.

        Use `archive` instead to retire a credential while keeping it retrievable by id.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._delete(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedVaultCredential,
        )

    def archive(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Archive a credential and return it.

        Archiving hides the credential from default listings and stops it being handed
        out, while keeping it retrievable by id. It is not a delete.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}/archive",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    def validate(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CredentialValidation:
        """
        Check a credential's MCP OAuth configuration against the live server.

        The call succeeds whenever the check runs: a credential the server rejects is
        reported as `status="invalid"` on the result, not raised as an error. A
        `status` of `unknown` means the probe was inconclusive.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to validate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialValidation,
        )


class AsyncCredentials(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCredentialsWithRawResponse:
        return AsyncCredentialsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCredentialsWithStreamingResponse:
        return AsyncCredentialsWithStreamingResponse(self)

    async def create(
        self,
        vault_id: str,
        *,
        auth: CredentialCreateAuthParam,
        display_name: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Store a credential in a vault.

        Args:
          vault_id: The vault to store the credential in.

          auth: The credential material and how it is presented. Every secret in it is
              write-only: reads return the surrounding configuration without it.

          display_name: Human-readable label for the credential.

          metadata: Arbitrary string key/value pairs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return await self._post(
            path_template("/v1/vaults/{vault_id}/credentials", vault_id=vault_id),
            body=await async_maybe_transform(
                {"auth": auth, "display_name": display_name, "metadata": metadata},
                credential_create_params.CredentialCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    async def retrieve(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Retrieve a credential.

        The response carries the credential's configuration only; the stored secret is
        write-only and never returned.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._get(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    async def update(
        self,
        vault_id: str,
        credential_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        auth: CredentialUpdateAuthParam | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Partially update a credential.

        Uses POST, matching the contract. `auth.type` names the credential shape being
        edited rather than changing it, and omitted fields keep their stored value --
        so rotating a secret means sending just that field.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to update.

          metadata: A null value removes that individual key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            body=await async_maybe_transform(
                {"display_name": display_name, "auth": auth, "metadata": metadata},
                credential_update_params.CredentialUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    def list(
        self,
        vault_id: str,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        include_archived: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[VaultCredential, AsyncPageCursor[VaultCredential]]:
        """
        List the credentials in a vault.

        Args:
          vault_id: The vault whose credentials to list.

          limit: Maximum number of credentials to return per page.

          page: Opaque page token from a previous response's `next_page`.

          include_archived: Include archived credentials in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        return self._get_api_list(
            path_template("/v1/vaults/{vault_id}/credentials", vault_id=vault_id),
            page=AsyncPageCursor[VaultCredential],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "page": page, "include_archived": include_archived},
                    credential_list_params.CredentialListParams,
                ),
            ),
            model=VaultCredential,
        )

    async def delete(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedVaultCredential:
        """
        Permanently delete a credential and return its tombstone.

        Use `archive` instead to retire a credential while keeping it retrievable by id.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._delete(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedVaultCredential,
        )

    async def archive(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> VaultCredential:
        """
        Archive a credential and return it.

        Archiving hides the credential from default listings and stops it being handed
        out, while keeping it retrievable by id. It is not a delete.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to archive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}/archive",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VaultCredential,
        )

    async def validate(
        self,
        vault_id: str,
        credential_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> CredentialValidation:
        """
        Check a credential's MCP OAuth configuration against the live server.

        The call succeeds whenever the check runs: a credential the server rejects is
        reported as `status="invalid"` on the result, not raised as an error. A
        `status` of `unknown` means the probe was inconclusive.

        Args:
          vault_id: The vault holding the credential.

          credential_id: The credential to validate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vault_id:
            raise ValueError(f"Expected a non-empty value for `vault_id` but received {vault_id!r}")
        if not credential_id:
            raise ValueError(f"Expected a non-empty value for `credential_id` but received {credential_id!r}")
        return await self._post(
            path_template(
                "/v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate",
                vault_id=vault_id,
                credential_id=credential_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CredentialValidation,
        )


class CredentialsWithRawResponse:
    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials

        self.create = to_raw_response_wrapper(credentials.create)
        self.retrieve = to_raw_response_wrapper(credentials.retrieve)
        self.update = to_raw_response_wrapper(credentials.update)
        self.list = to_raw_response_wrapper(credentials.list)
        self.delete = to_raw_response_wrapper(credentials.delete)
        self.archive = to_raw_response_wrapper(credentials.archive)
        self.validate = to_raw_response_wrapper(credentials.validate)


class AsyncCredentialsWithRawResponse:
    def __init__(self, credentials: AsyncCredentials) -> None:
        self._credentials = credentials

        self.create = async_to_raw_response_wrapper(credentials.create)
        self.retrieve = async_to_raw_response_wrapper(credentials.retrieve)
        self.update = async_to_raw_response_wrapper(credentials.update)
        self.list = async_to_raw_response_wrapper(credentials.list)
        self.delete = async_to_raw_response_wrapper(credentials.delete)
        self.archive = async_to_raw_response_wrapper(credentials.archive)
        self.validate = async_to_raw_response_wrapper(credentials.validate)


class CredentialsWithStreamingResponse:
    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials

        self.create = to_streamed_response_wrapper(credentials.create)
        self.retrieve = to_streamed_response_wrapper(credentials.retrieve)
        self.update = to_streamed_response_wrapper(credentials.update)
        self.list = to_streamed_response_wrapper(credentials.list)
        self.delete = to_streamed_response_wrapper(credentials.delete)
        self.archive = to_streamed_response_wrapper(credentials.archive)
        self.validate = to_streamed_response_wrapper(credentials.validate)


class AsyncCredentialsWithStreamingResponse:
    def __init__(self, credentials: AsyncCredentials) -> None:
        self._credentials = credentials

        self.create = async_to_streamed_response_wrapper(credentials.create)
        self.retrieve = async_to_streamed_response_wrapper(credentials.retrieve)
        self.update = async_to_streamed_response_wrapper(credentials.update)
        self.list = async_to_streamed_response_wrapper(credentials.list)
        self.delete = async_to_streamed_response_wrapper(credentials.delete)
        self.archive = async_to_streamed_response_wrapper(credentials.archive)
        self.validate = async_to_streamed_response_wrapper(credentials.validate)
