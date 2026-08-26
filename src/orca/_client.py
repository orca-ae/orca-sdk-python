from __future__ import annotations

import os
import re
import asyncio
import inspect
import logging
import threading
from typing import TYPE_CHECKING, Any, Union, Mapping, Callable, Awaitable, cast
from typing_extensions import Self, TypeAlias, override

import httpx2

from . import _exceptions
from ._qs import Querystring

if TYPE_CHECKING:
    from .lib.session import SessionHandle, AsyncSessionHandle
    from .resources.files import (
        Files,
        AsyncFiles,
        FilesWithRawResponse,
        AsyncFilesWithRawResponse,
        FilesWithStreamingResponse,
        AsyncFilesWithStreamingResponse,
    )
    from .resources.agents import (
        Agents,
        AsyncAgents,
        AgentsWithRawResponse,
        AsyncAgentsWithRawResponse,
        AgentsWithStreamingResponse,
        AsyncAgentsWithStreamingResponse,
    )
    from .resources.skills import (
        Skills,
        AsyncSkills,
        SkillsWithRawResponse,
        AsyncSkillsWithRawResponse,
        SkillsWithStreamingResponse,
        AsyncSkillsWithStreamingResponse,
    )
    from .resources.vaults import (
        Vaults,
        AsyncVaults,
        VaultsWithRawResponse,
        AsyncVaultsWithRawResponse,
        VaultsWithStreamingResponse,
        AsyncVaultsWithStreamingResponse,
    )
    from .resources.sessions import (
        Sessions,
        AsyncSessions,
        SessionsWithRawResponse,
        AsyncSessionsWithRawResponse,
        SessionsWithStreamingResponse,
        AsyncSessionsWithStreamingResponse,
    )
    from .resources.triggers import (
        Triggers,
        AsyncTriggers,
        TriggersWithRawResponse,
        AsyncTriggersWithRawResponse,
        TriggersWithStreamingResponse,
        AsyncTriggersWithStreamingResponse,
    )
    from .resources.discovery import (
        Discovery,
        AsyncDiscovery,
        DiscoveryWithRawResponse,
        AsyncDiscoveryWithRawResponse,
        DiscoveryWithStreamingResponse,
        AsyncDiscoveryWithStreamingResponse,
    )
    from .resources.environments import (
        Environments,
        AsyncEnvironments,
        EnvironmentsWithRawResponse,
        AsyncEnvironmentsWithRawResponse,
        EnvironmentsWithStreamingResponse,
        AsyncEnvironmentsWithStreamingResponse,
    )
    from .resources.memory_stores import (
        MemoryStores,
        AsyncMemoryStores,
        MemoryStoresWithRawResponse,
        AsyncMemoryStoresWithRawResponse,
        MemoryStoresWithStreamingResponse,
        AsyncMemoryStoresWithStreamingResponse,
    )
from ._types import Omit, Timeout, NotGiven, RequestOptions, not_given
from ._utils import is_given
from ._compat import cached_property
from ._models import FinalRequestOptions
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import (
    OrcaError,
    NotFoundError,
    APIStatusError,
    ExtensionNotAvailableError,
)
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    merge_headers,
)

log: logging.Logger = logging.getLogger(__name__)

#: An `api_key` may be a literal token or a callable resolved on every request,
#: which is how callers plug in short-lived or rotating credentials.
ApiKeyProvider: TypeAlias = Union[str, Callable[[], str], None]
AsyncApiKeyProvider: TypeAlias = Union[str, Callable[[], Union[str, Awaitable[str]]], None]

# Deployments used to require one of these suffixes on the base URL. They are no
# longer part of it -- core is served at the host root -- so strip and warn.
_LEGACY_BASE_URL_SUFFIX = re.compile(r"(/api/v1|/v1/registry|/v1)$")

#: Extension group serving the `cloud.*` namespace. Single-sourced so the gate
#: never re-derives the group name from a request path.
CLOUD_EXTENSION_GROUP = "cloud.sn.io"

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

    A legacy `/v1`, `/v1/registry`, or `/api/v1` suffix is stripped with a warning.
    `/api/v1` is stripped **whole** rather than having only its trailing `/v1`
    removed: leaving `/api` would still resolve core paths through the `/api/v1/*`
    alias while silently breaking every `/apis/...` extension call -- half the
    surface broken with nothing to notice.
    """
    if base_url is None:
        base_url = os.environ.get("ORCA_BASE_URL")
    if not base_url:
        raise OrcaError("base_url is required: pass `base_url` to the Orca constructor or set ORCA_BASE_URL")

    original = str(base_url)
    url = httpx2.URL(original.rstrip("/"))
    path = url.path.rstrip("/")

    match = _LEGACY_BASE_URL_SUFFIX.search(path)
    if match is None:
        return url

    stripped = url.copy_with(raw_path=path[: -len(match.group(0))].encode())
    log.warning(
        'base_url %r ends with "%s", which is no longer part of the base URL -- every '
        "deployment now serves core at the host root (e.g. GET {base}/v1/agents). "
        "Using %r instead. Update ORCA_BASE_URL or the `base_url` option to the host "
        "root; this compatibility shim may be removed in a future major version.",
        original,
        match.group(0),
        str(stripped),
    )
    return stripped


class Orca(SyncAPIClient):
    api_key: ApiKeyProvider
    _extension_lock: threading.Lock

    def __init__(
        self,
        *,
        api_key: ApiKeyProvider | NotGiven = not_given,
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

        `api_key` may also be a callable, which is invoked once per request. That is
        the hook for short-lived or rotating credentials: return the current token and
        the SDK will pick it up without the client being rebuilt.

        `base_url` defaults to the `ORCA_BASE_URL` environment variable and is required.
        It is the **host root** — the SDK writes the `/v1/...` and `/apis/...` prefixes
        itself.
        """
        if not is_given(api_key):
            api_key = os.environ.get("ORCA_API_KEY") or None
        self.api_key = api_key
        self._extension_groups: dict[str, frozenset[str]] = {}
        self._extension_lock = threading.Lock()

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
    def agents(self) -> Agents:
        from .resources.agents import Agents

        return Agents(self)

    @cached_property
    def sessions(self) -> Sessions:
        from .resources.sessions import Sessions

        return Sessions(self)

    @cached_property
    def environments(self) -> Environments:
        from .resources.environments import Environments

        return Environments(self)

    @cached_property
    def files(self) -> Files:
        from .resources.files import Files

        return Files(self)

    @cached_property
    def skills(self) -> Skills:
        from .resources.skills import Skills

        return Skills(self)

    @cached_property
    def vaults(self) -> Vaults:
        from .resources.vaults import Vaults

        return Vaults(self)

    @cached_property
    def memory_stores(self) -> MemoryStores:
        from .resources.memory_stores import MemoryStores

        return MemoryStores(self)

    @cached_property
    def triggers(self) -> Triggers:
        from .resources.triggers import Triggers

        return Triggers(self)

    @cached_property
    def discovery(self) -> Discovery:
        from .resources.discovery import Discovery

        return Discovery(self)

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
        api_key = _resolve_api_key(self.api_key)
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
        api_key: ApiKeyProvider | NotGiven = not_given,
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

    def session(self, session_id: str) -> SessionHandle:
        """A handle whose sub-resources carry `session_id` for you.

        Equivalent to calling `client.sessions.*` with the id repeated on every call;
        it holds no state and performs no I/O when constructed.
        """
        from .lib.session import SessionHandle

        return SessionHandle(self, session_id)

    def _ensure_extension_available(self, group: str) -> None:
        """Raise unless this deployment advertises `group` via `GET /apis`.

        Namespaces served by an extension are gated here rather than being allowed
        to fail as a 404, so calling one against a deployment that does not serve it
        produces `ExtensionNotAvailableError` and makes no HTTP request at all.

        The discovery result is cached per base URL, and the lock collapses a burst
        of concurrent first-calls into a single probe.
        """
        base = str(self.base_url)
        groups = self._extension_groups.get(base)
        if groups is None:
            with self._extension_lock:
                groups = self._extension_groups.get(base)
                if groups is None:
                    groups = self._fetch_extension_groups()
                    self._extension_groups[base] = groups

        if group not in groups:
            raise ExtensionNotAvailableError(
                group,
                f'This deployment does not advertise the "{group}" extension group '
                f"(GET /apis groups: [{', '.join(sorted(groups))}]). Methods under this "
                "namespace require a deployment that serves this extension group.",
            )

    def _fetch_extension_groups(self) -> frozenset[str]:
        try:
            response = self.get("/apis", cast_to=httpx2.Response)
        except NotFoundError:
            # A deployment predating the discovery route serves no extensions.
            log.warning("GET /apis is not served by this deployment; treating it as serving no extension groups")
            return frozenset()
        return _parse_extension_groups(cast("object", response.json()))

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
    api_key: AsyncApiKeyProvider
    _extension_lock: asyncio.Lock | None

    def __init__(
        self,
        *,
        api_key: AsyncApiKeyProvider | NotGiven = not_given,
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
        self._extension_groups: dict[str, frozenset[str]] = {}
        self._extension_lock = None

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
    def agents(self) -> AsyncAgents:
        from .resources.agents import AsyncAgents

        return AsyncAgents(self)

    @cached_property
    def sessions(self) -> AsyncSessions:
        from .resources.sessions import AsyncSessions

        return AsyncSessions(self)

    @cached_property
    def environments(self) -> AsyncEnvironments:
        from .resources.environments import AsyncEnvironments

        return AsyncEnvironments(self)

    @cached_property
    def files(self) -> AsyncFiles:
        from .resources.files import AsyncFiles

        return AsyncFiles(self)

    @cached_property
    def skills(self) -> AsyncSkills:
        from .resources.skills import AsyncSkills

        return AsyncSkills(self)

    @cached_property
    def vaults(self) -> AsyncVaults:
        from .resources.vaults import AsyncVaults

        return AsyncVaults(self)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStores:
        from .resources.memory_stores import AsyncMemoryStores

        return AsyncMemoryStores(self)

    @cached_property
    def triggers(self) -> AsyncTriggers:
        from .resources.triggers import AsyncTriggers

        return AsyncTriggers(self)

    @cached_property
    def discovery(self) -> AsyncDiscovery:
        from .resources.discovery import AsyncDiscovery

        return AsyncDiscovery(self)

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
        # A callable `api_key` may return an awaitable, which this synchronous
        # property cannot resolve. Literals are handled here; callables are
        # resolved in `_prepare_options` below, which runs in async context
        # before the request headers are built.
        api_key = self.api_key
        if api_key is None or callable(api_key):
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        api_key = self.api_key
        if callable(api_key):
            resolved = api_key()
            if inspect.isawaitable(resolved):
                resolved = await resolved
            if not resolved or not isinstance(cast("object", resolved), str):
                raise OrcaError("the `api_key` callable must return a non-empty string")
            headers = dict(options.headers) if is_given(options.headers) else {}
            headers.setdefault("Authorization", f"Bearer {resolved}")
            options.headers = headers
        return options

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
        api_key: AsyncApiKeyProvider | NotGiven = not_given,
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

    def session(self, session_id: str) -> AsyncSessionHandle:
        """A handle whose sub-resources carry `session_id` for you.

        Equivalent to calling `client.sessions.*` with the id repeated on every call;
        it holds no state and performs no I/O when constructed.
        """
        from .lib.session import AsyncSessionHandle

        return AsyncSessionHandle(self, session_id)

    async def _ensure_extension_available(self, group: str) -> None:
        """Async counterpart to `Orca._ensure_extension_available`.

        The lock is created lazily because a client may be constructed outside a
        running event loop, and binding an asyncio primitive at that point would
        tie it to the wrong loop.
        """
        base = str(self.base_url)
        groups = self._extension_groups.get(base)
        if groups is None:
            if self._extension_lock is None:
                self._extension_lock = asyncio.Lock()
            async with self._extension_lock:
                groups = self._extension_groups.get(base)
                if groups is None:
                    groups = await self._fetch_extension_groups()
                    self._extension_groups[base] = groups

        if group not in groups:
            raise ExtensionNotAvailableError(
                group,
                f'This deployment does not advertise the "{group}" extension group '
                f"(GET /apis groups: [{', '.join(sorted(groups))}]). Methods under this "
                "namespace require a deployment that serves this extension group.",
            )

    async def _fetch_extension_groups(self) -> frozenset[str]:
        try:
            response = await self.get("/apis", cast_to=httpx2.Response)
        except NotFoundError:
            log.warning("GET /apis is not served by this deployment; treating it as serving no extension groups")
            return frozenset()
        return _parse_extension_groups(cast("object", response.json()))

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx2.Response,
    ) -> APIStatusError:
        return _make_status_error(err_msg, body=body, response=response)


def _parse_extension_groups(payload: object) -> frozenset[str]:
    """Extract the advertised group names from a `GET /apis` body.

    An empty or unrecognised body yields an empty set: "no extensions installed" is a
    valid deployment state, not an error.
    """
    if not isinstance(payload, dict):
        return frozenset()
    groups = cast("Mapping[str, object]", payload).get("groups")
    if not isinstance(groups, list):
        return frozenset()

    names: set[str] = set()
    for entry in cast("list[object]", groups):
        if not isinstance(entry, dict):
            continue
        name = cast("Mapping[str, object]", entry).get("name")
        if isinstance(name, str) and name:
            names.add(name)
    return frozenset(names)


def _resolve_api_key(api_key: object) -> str | None:
    """Resolve a literal or callable `api_key` down to the token for this request.

    A callable is invoked per request, which is the hook for short-lived or rotating
    credentials. Returning an empty string is treated as a configuration error rather
    than silently sending an unauthenticated request.
    """
    if api_key is None:
        return None
    if callable(api_key):
        resolved = api_key()
        if not isinstance(resolved, str) or not resolved:
            raise OrcaError("the `api_key` callable must return a non-empty string")
        return resolved
    return cast("str", api_key)


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

    @cached_property
    def agents(self) -> AgentsWithRawResponse:
        from .resources.agents import AgentsWithRawResponse

        return AgentsWithRawResponse(self._client.agents)

    @cached_property
    def sessions(self) -> SessionsWithRawResponse:
        from .resources.sessions import SessionsWithRawResponse

        return SessionsWithRawResponse(self._client.sessions)

    @cached_property
    def environments(self) -> EnvironmentsWithRawResponse:
        from .resources.environments import EnvironmentsWithRawResponse

        return EnvironmentsWithRawResponse(self._client.environments)

    @cached_property
    def files(self) -> FilesWithRawResponse:
        from .resources.files import FilesWithRawResponse

        return FilesWithRawResponse(self._client.files)

    @cached_property
    def skills(self) -> SkillsWithRawResponse:
        from .resources.skills import SkillsWithRawResponse

        return SkillsWithRawResponse(self._client.skills)

    @cached_property
    def vaults(self) -> VaultsWithRawResponse:
        from .resources.vaults import VaultsWithRawResponse

        return VaultsWithRawResponse(self._client.vaults)

    @cached_property
    def memory_stores(self) -> MemoryStoresWithRawResponse:
        from .resources.memory_stores import MemoryStoresWithRawResponse

        return MemoryStoresWithRawResponse(self._client.memory_stores)

    @cached_property
    def triggers(self) -> TriggersWithRawResponse:
        from .resources.triggers import TriggersWithRawResponse

        return TriggersWithRawResponse(self._client.triggers)

    @cached_property
    def discovery(self) -> DiscoveryWithRawResponse:
        from .resources.discovery import DiscoveryWithRawResponse

        return DiscoveryWithRawResponse(self._client.discovery)


class AsyncOrcaWithRawResponse:
    _client: AsyncOrca

    def __init__(self, client: AsyncOrca) -> None:
        self._client = client

    @cached_property
    def agents(self) -> AsyncAgentsWithRawResponse:
        from .resources.agents import AsyncAgentsWithRawResponse

        return AsyncAgentsWithRawResponse(self._client.agents)

    @cached_property
    def sessions(self) -> AsyncSessionsWithRawResponse:
        from .resources.sessions import AsyncSessionsWithRawResponse

        return AsyncSessionsWithRawResponse(self._client.sessions)

    @cached_property
    def environments(self) -> AsyncEnvironmentsWithRawResponse:
        from .resources.environments import AsyncEnvironmentsWithRawResponse

        return AsyncEnvironmentsWithRawResponse(self._client.environments)

    @cached_property
    def files(self) -> AsyncFilesWithRawResponse:
        from .resources.files import AsyncFilesWithRawResponse

        return AsyncFilesWithRawResponse(self._client.files)

    @cached_property
    def skills(self) -> AsyncSkillsWithRawResponse:
        from .resources.skills import AsyncSkillsWithRawResponse

        return AsyncSkillsWithRawResponse(self._client.skills)

    @cached_property
    def vaults(self) -> AsyncVaultsWithRawResponse:
        from .resources.vaults import AsyncVaultsWithRawResponse

        return AsyncVaultsWithRawResponse(self._client.vaults)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStoresWithRawResponse:
        from .resources.memory_stores import AsyncMemoryStoresWithRawResponse

        return AsyncMemoryStoresWithRawResponse(self._client.memory_stores)

    @cached_property
    def triggers(self) -> AsyncTriggersWithRawResponse:
        from .resources.triggers import AsyncTriggersWithRawResponse

        return AsyncTriggersWithRawResponse(self._client.triggers)

    @cached_property
    def discovery(self) -> AsyncDiscoveryWithRawResponse:
        from .resources.discovery import AsyncDiscoveryWithRawResponse

        return AsyncDiscoveryWithRawResponse(self._client.discovery)


class OrcaWithStreamedResponse:
    _client: Orca

    def __init__(self, client: Orca) -> None:
        self._client = client

    @cached_property
    def agents(self) -> AgentsWithStreamingResponse:
        from .resources.agents import AgentsWithStreamingResponse

        return AgentsWithStreamingResponse(self._client.agents)

    @cached_property
    def sessions(self) -> SessionsWithStreamingResponse:
        from .resources.sessions import SessionsWithStreamingResponse

        return SessionsWithStreamingResponse(self._client.sessions)

    @cached_property
    def environments(self) -> EnvironmentsWithStreamingResponse:
        from .resources.environments import EnvironmentsWithStreamingResponse

        return EnvironmentsWithStreamingResponse(self._client.environments)

    @cached_property
    def files(self) -> FilesWithStreamingResponse:
        from .resources.files import FilesWithStreamingResponse

        return FilesWithStreamingResponse(self._client.files)

    @cached_property
    def skills(self) -> SkillsWithStreamingResponse:
        from .resources.skills import SkillsWithStreamingResponse

        return SkillsWithStreamingResponse(self._client.skills)

    @cached_property
    def vaults(self) -> VaultsWithStreamingResponse:
        from .resources.vaults import VaultsWithStreamingResponse

        return VaultsWithStreamingResponse(self._client.vaults)

    @cached_property
    def memory_stores(self) -> MemoryStoresWithStreamingResponse:
        from .resources.memory_stores import MemoryStoresWithStreamingResponse

        return MemoryStoresWithStreamingResponse(self._client.memory_stores)

    @cached_property
    def triggers(self) -> TriggersWithStreamingResponse:
        from .resources.triggers import TriggersWithStreamingResponse

        return TriggersWithStreamingResponse(self._client.triggers)

    @cached_property
    def discovery(self) -> DiscoveryWithStreamingResponse:
        from .resources.discovery import DiscoveryWithStreamingResponse

        return DiscoveryWithStreamingResponse(self._client.discovery)


class AsyncOrcaWithStreamedResponse:
    _client: AsyncOrca

    def __init__(self, client: AsyncOrca) -> None:
        self._client = client

    @cached_property
    def agents(self) -> AsyncAgentsWithStreamingResponse:
        from .resources.agents import AsyncAgentsWithStreamingResponse

        return AsyncAgentsWithStreamingResponse(self._client.agents)

    @cached_property
    def sessions(self) -> AsyncSessionsWithStreamingResponse:
        from .resources.sessions import AsyncSessionsWithStreamingResponse

        return AsyncSessionsWithStreamingResponse(self._client.sessions)

    @cached_property
    def environments(self) -> AsyncEnvironmentsWithStreamingResponse:
        from .resources.environments import AsyncEnvironmentsWithStreamingResponse

        return AsyncEnvironmentsWithStreamingResponse(self._client.environments)

    @cached_property
    def files(self) -> AsyncFilesWithStreamingResponse:
        from .resources.files import AsyncFilesWithStreamingResponse

        return AsyncFilesWithStreamingResponse(self._client.files)

    @cached_property
    def skills(self) -> AsyncSkillsWithStreamingResponse:
        from .resources.skills import AsyncSkillsWithStreamingResponse

        return AsyncSkillsWithStreamingResponse(self._client.skills)

    @cached_property
    def vaults(self) -> AsyncVaultsWithStreamingResponse:
        from .resources.vaults import AsyncVaultsWithStreamingResponse

        return AsyncVaultsWithStreamingResponse(self._client.vaults)

    @cached_property
    def memory_stores(self) -> AsyncMemoryStoresWithStreamingResponse:
        from .resources.memory_stores import AsyncMemoryStoresWithStreamingResponse

        return AsyncMemoryStoresWithStreamingResponse(self._client.memory_stores)

    @cached_property
    def triggers(self) -> AsyncTriggersWithStreamingResponse:
        from .resources.triggers import AsyncTriggersWithStreamingResponse

        return AsyncTriggersWithStreamingResponse(self._client.triggers)

    @cached_property
    def discovery(self) -> AsyncDiscoveryWithStreamingResponse:
        from .resources.discovery import AsyncDiscoveryWithStreamingResponse

        return AsyncDiscoveryWithStreamingResponse(self._client.discovery)


Client = Orca
AsyncClient = AsyncOrca
