from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca, ExtensionNotAvailableError
from tests.utils import assert_matches_type
from orca.resources.cloud import Cloud, AsyncCloud

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

# method name -> path it probes
PROBES = pytest.mark.parametrize(
    ("method", "path"),
    [
        ("check", "/apis/cloud.sn.io/v1/health"),
        ("ready", "/apis/cloud.sn.io/v1/health/ready"),
        ("live", "/apis/cloud.sn.io/v1/health/live"),
    ],
)


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _gate(respx_mock: MockRouter, client: Orca | AsyncOrca, *, available: bool = True) -> Any:
    """Stub `GET /apis` and drop any discovery result the client already cached.

    Discovery is cached per base URL and the client fixture is session-scoped, so
    without the reset whichever cloud test ran first would decide the answer for
    every test after it.
    """
    client._extension_groups.clear()
    groups = [{"name": "cloud.sn.io"}] if available else []
    return respx_mock.get("/apis").mock(
        return_value=httpx2.Response(200, json={"kind": "APIGroupList", "groups": groups})
    )


class TestHealth:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @PROBES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method(self, client: Orca, respx_mock: MockRouter, method: str, path: str) -> None:
        _gate(respx_mock, client)
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json=True))
        probe = getattr(Cloud(client).health, method)
        result = probe()
        assert_matches_type(bool, result, path=["response"])
        assert result is True
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_check_false(self, client: Orca, respx_mock: MockRouter) -> None:
        """An unhealthy service answers 200 with `false`, not an error status."""
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/health").mock(return_value=httpx2.Response(200, json=False))
        assert Cloud(client).health.check() is False

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_check(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/health").mock(return_value=httpx2.Response(200, json=True))
        response = Cloud(client).health.with_raw_response.check()
        assert response.is_closed is True
        assert_matches_type(bool, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_live(self, client: Orca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, client)
        respx_mock.get("/apis/cloud.sn.io/v1/health/live").mock(return_value=httpx2.Response(200, json=True))
        with Cloud(client).health.with_streaming_response.live() as response:
            assert not response.is_closed
            assert_matches_type(bool, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @PROBES
    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_gate_blocks_when_extension_absent(
        self, client: Orca, respx_mock: MockRouter, method: str, path: str
    ) -> None:
        """No cloud group advertised means no request is made at all."""
        _gate(respx_mock, client, available=False)
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json=True))
        probe = getattr(Cloud(client).health, method)
        with pytest.raises(ExtensionNotAvailableError):
            probe()
        assert route.called is False


class TestAsyncHealth:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @PROBES
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method(self, async_client: AsyncOrca, respx_mock: MockRouter, method: str, path: str) -> None:
        _gate(respx_mock, async_client)
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json=True))
        probe = getattr(AsyncCloud(async_client).health, method)
        result = await probe()
        assert_matches_type(bool, result, path=["response"])
        assert result is True
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_ready(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/health/ready").mock(return_value=httpx2.Response(200, json=True))
        response = await AsyncCloud(async_client).health.with_raw_response.ready()
        assert response.is_closed is True
        assert_matches_type(bool, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_live(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        _gate(respx_mock, async_client)
        respx_mock.get("/apis/cloud.sn.io/v1/health/live").mock(return_value=httpx2.Response(200, json=True))
        async with AsyncCloud(async_client).health.with_streaming_response.live() as response:
            assert not response.is_closed
            assert_matches_type(bool, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @PROBES
    @parametrize
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_gate_blocks_when_extension_absent(
        self, async_client: AsyncOrca, respx_mock: MockRouter, method: str, path: str
    ) -> None:
        _gate(respx_mock, async_client, available=False)
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json=True))
        probe = getattr(AsyncCloud(async_client).health, method)
        with pytest.raises(ExtensionNotAvailableError):
            await probe()
        assert route.called is False
