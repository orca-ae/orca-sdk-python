from __future__ import annotations

import os
import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, AsyncOrca
from tests.utils import assert_matches_type
from orca.pagination import SyncPageCursor, AsyncPageCursor
from orca.types.environment import (
    Environment,
    DeletedEnvironment,
    EnvironmentCloudConfig,
    EnvironmentSelfHostedConfig,
    EnvironmentUnrestrictedNetworking,
)
from orca.resources.environments import Environments, AsyncEnvironments

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

ENVIRONMENT: dict[str, Any] = {
    "id": "env_123",
    "type": "environment",
    "name": "production",
    "description": "prod sandbox",
    "config": {
        "type": "cloud",
        "packages": {"type": "packages", "apt": [], "cargo": [], "gem": [], "go": [], "npm": ["typescript"], "pip": []},
        "networking": {"type": "unrestricted"},
    },
    "metadata": {},
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "archived_at": None,
}

SELF_HOSTED_ENVIRONMENT: dict[str, Any] = {
    **ENVIRONMENT,
    "id": "env_456",
    "config": {"type": "self_hosted"},
    "scope": "organization",
}

DELETED_ENVIRONMENT: dict[str, Any] = {"id": "env_123", "type": "environment_deleted"}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*environments: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(environments), "next_page": next_page}


def _sync(client: Orca) -> Environments:
    """`Orca.environments` is mounted in `_client.py`, which this change does not
    own; constructing the resource directly keeps these tests independent of that
    wiring while exercising exactly the same code path."""
    return Environments(client)


def _async(client: AsyncOrca) -> AsyncEnvironments:
    return AsyncEnvironments(client)


class TestEnvironments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        environment = _sync(client).create(name="production")
        assert_matches_type(Environment, environment, path=["response"])
        assert _req(route).method == "POST"
        assert json.loads(_req(route).content) == {"name": "production"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        environment = _sync(client).create(
            name="production",
            description="prod sandbox",
            config={
                "type": "cloud",
                "packages": {"npm": ["typescript"], "pip": None},
                "networking": {"type": "limited", "allowed_hosts": ["example.test"], "allow_mcp_servers": True},
            },
            metadata={"team": "core"},
            scope="organization",
        )
        assert_matches_type(Environment, environment, path=["response"])
        body = json.loads(_req(route).content)
        assert body["config"] == {
            "type": "cloud",
            "packages": {"npm": ["typescript"], "pip": None},
            "networking": {"type": "limited", "allowed_hosts": ["example.test"], "allow_mcp_servers": True},
        }
        assert body["metadata"] == {"team": "core"}
        assert body["scope"] == "organization"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_create_omits_non_portable_flat_fields(self, client: Orca, respx_mock: MockRouter) -> None:
        """`packages`, `networking`, `image`, and `target` are not portable across
        backends, so `config` is the only way to express them here."""
        route = respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        _sync(client).create(name="production", config={"type": "self_hosted"})
        body = json.loads(_req(route).content)
        assert set(body) == {"name", "config"}
        assert body["config"] == {"type": "self_hosted"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        response = _sync(client).with_raw_response.create(name="production")
        assert response.is_closed is True
        assert_matches_type(Environment, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        with _sync(client).with_streaming_response.create(name="production") as response:
            assert not response.is_closed
            assert_matches_type(Environment, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        assert_matches_type(Environment, _sync(client).retrieve("env_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_config_discriminates_cloud_from_self_hosted(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        respx_mock.get("/v1/environments/env_456").mock(return_value=httpx2.Response(200, json=SELF_HOSTED_ENVIRONMENT))

        cloud = _sync(client).retrieve("env_123")
        assert isinstance(cloud.config, EnvironmentCloudConfig)
        assert cloud.config.packages.npm == ["typescript"]
        assert isinstance(cloud.config.networking, EnvironmentUnrestrictedNetworking)
        assert cloud.scope is None

        self_hosted = _sync(client).retrieve("env_456")
        assert isinstance(self_hosted.config, EnvironmentSelfHostedConfig)
        assert self_hosted.scope == "organization"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            _sync(client).with_raw_response.retrieve("")

    @parametrize
    def test_path_params_update(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            _sync(client).with_raw_response.update("")

    @parametrize
    def test_path_params_delete(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            _sync(client).with_raw_response.delete("")

    @parametrize
    def test_path_params_archive(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            _sync(client).with_raw_response.archive("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        _sync(client).retrieve("a b/c")
        assert "/v1/environments/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        environment = _sync(client).update("env_123", name="staging", metadata={"drop": None})
        assert_matches_type(Environment, environment, path=["response"])
        assert _req(route).method == "POST"
        assert json.loads(_req(route).content) == {"name": "staging", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        _sync(client).update(
            "env_123",
            name=None,
            description=None,
            config={"type": "self_hosted"},
            metadata={"team": "core"},
            scope=None,
        )
        assert json.loads(_req(route).content) == {
            "name": None,
            "description": None,
            "config": {"type": "self_hosted"},
            "metadata": {"team": "core"},
            "scope": None,
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/environments").mock(return_value=httpx2.Response(200, json=_page(ENVIRONMENT)))
        assert_matches_type(SyncPageCursor[Environment], _sync(client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/environments").mock(return_value=httpx2.Response(200, json=_page(ENVIRONMENT)))
        _sync(client).list(limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**ENVIRONMENT, "id": "env_456"}
        respx_mock.get("/v1/environments").mock(
            side_effect=[
                httpx2.Response(200, json=_page(ENVIRONMENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [e.id for e in _sync(client).list()]
        assert ids == ["env_123", "env_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/environments/env_123").mock(
            return_value=httpx2.Response(200, json=DELETED_ENVIRONMENT)
        )
        deleted = _sync(client).delete("env_123")
        assert_matches_type(DeletedEnvironment, deleted, path=["response"])
        assert deleted.type == "environment_deleted"
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments/env_123/archive").mock(
            return_value=httpx2.Response(200, json=ENVIRONMENT)
        )
        assert_matches_type(Environment, _sync(client).archive("env_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/environments").mock(return_value=httpx2.Response(200, json=_page()))
        _sync(client).list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"


class TestAsyncEnvironments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        environment = await _async(async_client).create(name="production")
        assert_matches_type(Environment, environment, path=["response"])
        assert json.loads(_req(route).content) == {"name": "production"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        response = await _async(async_client).with_raw_response.create(name="production")
        assert response.is_closed is True
        assert_matches_type(Environment, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/environments").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        async with _async(async_client).with_streaming_response.create(name="production") as response:
            assert not response.is_closed
            assert_matches_type(Environment, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        assert_matches_type(Environment, await _async(async_client).retrieve("env_123"), path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await _async(async_client).with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        await _async(async_client).update("env_123", name="staging", metadata={"drop": None})
        assert json.loads(_req(route).content) == {"name": "staging", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/environments").mock(return_value=httpx2.Response(200, json=_page(ENVIRONMENT)))
        assert_matches_type(AsyncPageCursor[Environment], await _async(async_client).list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**ENVIRONMENT, "id": "env_456"}
        respx_mock.get("/v1/environments").mock(
            side_effect=[
                httpx2.Response(200, json=_page(ENVIRONMENT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        ids = [e.id async for e in _async(async_client).list()]
        assert ids == ["env_123", "env_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/environments/env_123").mock(return_value=httpx2.Response(200, json=DELETED_ENVIRONMENT))
        deleted = await _async(async_client).delete("env_123")
        assert_matches_type(DeletedEnvironment, deleted, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/environments/env_123/archive").mock(return_value=httpx2.Response(200, json=ENVIRONMENT))
        assert_matches_type(Environment, await _async(async_client).archive("env_123"), path=["response"])
