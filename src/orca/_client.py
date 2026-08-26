from __future__ import annotations

import os
from typing import Any, Mapping
from typing_extensions import Self, override

import httpx2

from . import _exceptions
from ._qs import Querystring
from ._types import Omit, Timeout, NotGiven, RequestOptions, not_given
from ._utils import is_given
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import OrcaError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    merge_headers,
)

__all__ = [
    "Timeout",
    "Stream",
    "AsyncStream",
    "RequestOptions",
    "Orca",
    "AsyncOrca",
    "Client",
    "AsyncClient",
]


def _resolve_base_url(base_url: str | httpx2.URL | None) -> str | httpx2.URL:
    """Resolve the deployment root, falling back to `ORCA_BASE_URL`.

    There is no default host: this API is self-hosted, so a missing base URL is a
    configuration error rather than something the SDK can guess at.
    """
    if base_url is None:
        base_url = os.environ.get("ORCA_BASE_URL")
    if not base_url:
        raise OrcaError("base_url is required: pass `base_url` to the Orca constructor or set ORCA_BASE_URL")
    return base_url


class Orca(SyncAPIClient):
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None | NotGiven = not_given,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Pass a `DefaultHttpxClient` to retain the default `limits`, `timeout`
        # and `follow_redirects` values while customising the transport.
        http_client: httpx2.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Orca client instance.

        `api_key` defaults to the `ORCA_API_KEY` environment variable. Passing an
        explicit `None` disables the `Authorization` header entirely, which is useful
        when the deployment sits behind a separately authenticated proxy.

        `base_url` defaults to the `ORCA_BASE_URL` environment variable and is required.
        It is the **host root** — the SDK writes the `/v1/...` and `/apis/...` prefixes
        itself.
        """
        if not is_given(api_key):
            api_key = os.environ.get("ORCA_API_KEY") or None
        self.api_key = api_key

        super().__init__(
            version=__version__,
            base_url=_resolve_base_url(base_url),
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def with_raw_response(self) -> OrcaWithRawResponse:
        return OrcaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrcaWithStreamedResponse:
        return OrcaWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        # List values repeat the key (`tags=a&tags=b`) rather than using bracket
        # or index notation.
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None | NotGiven = not_given,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client re-using this client's options, with optional overrides."""
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key if is_given(api_key) else self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).agents.list(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx2.Response,
    ) -> APIStatusError:
        return _make_status_error(err_msg, body=body, response=response)


class AsyncOrca(AsyncAPIClient):
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None | NotGiven = not_given,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Pass a `DefaultAsyncHttpxClient` to retain the default `limits`, `timeout`
        # and `follow_redirects` values while customising the transport.
        http_client: httpx2.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new asynchronous Orca client instance.

        See `Orca.__init__` for the option semantics; they are identical.
        """
        if not is_given(api_key):
            api_key = os.environ.get("ORCA_API_KEY") or None
        self.api_key = api_key

        super().__init__(
            version=__version__,
            base_url=_resolve_base_url(base_url),
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def with_raw_response(self) -> AsyncOrcaWithRawResponse:
        return AsyncOrcaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrcaWithStreamedResponse:
        return AsyncOrcaWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None | NotGiven = not_given,
        base_url: str | httpx2.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx2.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """Create a new client re-using this client's options, with optional overrides."""
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = merge_headers(headers, default_headers)
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key if is_given(api_key) else self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx2.Response,
    ) -> APIStatusError:
        return _make_status_error(err_msg, body=body, response=response)


def _make_status_error(err_msg: str, *, body: object, response: httpx2.Response) -> APIStatusError:
    """Map an HTTP status onto this SDK's error lineup.

    Shared by both clients so the sync and async trees can never disagree about
    which exception a given status produces.
    """
    if response.status_code == 400:
        return _exceptions.BadRequestError(err_msg, response=response, body=body)
    if response.status_code == 401:
        return _exceptions.AuthenticationError(err_msg, response=response, body=body)
    if response.status_code == 403:
        return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)
    if response.status_code == 404:
        return _exceptions.NotFoundError(err_msg, response=response, body=body)
    if response.status_code == 409:
        return _exceptions.ConflictError(err_msg, response=response, body=body)
    if response.status_code == 422:
        return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)
    if response.status_code == 429:
        return _exceptions.RateLimitError(err_msg, response=response, body=body)
    if response.status_code >= 500:
        return _exceptions.InternalServerError(err_msg, response=response, body=body)
    return APIStatusError(err_msg, response=response, body=body)


class OrcaWithRawResponse:
    _client: Orca

    def __init__(self, client: Orca) -> None:
        self._client = client


class AsyncOrcaWithRawResponse:
    _client: AsyncOrca

    def __init__(self, client: AsyncOrca) -> None:
        self._client = client


class OrcaWithStreamedResponse:
    _client: Orca

    def __init__(self, client: Orca) -> None:
        self._client = client


class AsyncOrcaWithStreamedResponse:
    _client: AsyncOrca

    def __init__(self, client: AsyncOrca) -> None:
        self._client = client


Client = Orca
AsyncClient = AsyncOrca
