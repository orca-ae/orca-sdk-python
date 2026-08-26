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
from orca.types.vault import Vault, DeletedVault
from orca.types.vault_credential import VaultCredential, DeletedVaultCredential
from orca.types.credential_validation import CredentialValidation

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

VAULT: dict[str, Any] = {
    "id": "vlt_123",
    "type": "vault",
    "display_name": "My vault",
    "metadata": {},
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
    "archived_at": None,
}

DELETED_VAULT: dict[str, Any] = {"id": "vlt_123", "type": "vault_deleted"}

CREDENTIAL: dict[str, Any] = {
    "id": "vcrd_123",
    "type": "vault_credential",
    "vault_id": "vlt_123",
    "display_name": "My credential",
    "auth": {"type": "static_bearer", "mcp_server_url": "https://mcp.test"},
    "metadata": {},
    "archived_at": None,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

ENV_VAR_CREDENTIAL: dict[str, Any] = {
    **CREDENTIAL,
    "auth": {
        "type": "environment_variable",
        "secret_name": "API_TOKEN",
        "networking": {"type": "limited", "allowed_hosts": ["api.test"]},
        "injection_location": {"header": True, "body": False},
    },
}

DELETED_CREDENTIAL: dict[str, Any] = {"id": "vcrd_123", "type": "vault_credential_deleted"}

VALIDATION: dict[str, Any] = {
    "type": "vault_credential_validation",
    "credential_id": "vcrd_123",
    "vault_id": "vlt_123",
    "validated_at": "2026-01-01T00:00:00Z",
    "has_refresh_token": True,
    "status": "valid",
    "mcp_probe": {
        "method": "initialize",
        "http_response": {
            "status_code": 200,
            "content_type": "application/json",
            "body": "{}",
            "body_truncated": False,
        },
    },
    "refresh": {"status": "succeeded", "http_response": None},
}


def _req(route: Any, index: int = 0) -> httpx2.Request:
    """Typed accessor for a recorded request.

    respx exposes `.calls` untyped, which strict type-checking rejects; this keeps
    the assertions below readable without scattering casts through them.
    """
    return cast("httpx2.Request", route.calls[index].request)


def _page(*items: dict[str, Any], next_page: str | None = None) -> dict[str, Any]:
    return {"data": list(items), "next_page": next_page}


class TestVaults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        vault = client.vaults.create(display_name="My vault")
        assert_matches_type(Vault, vault, path=["response"])
        assert json.loads(_req(route).content) == {"display_name": "My vault"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        client.vaults.create(display_name="My vault", metadata={"team": "core"})
        assert json.loads(_req(route).content)["metadata"] == {"team": "core"}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        response = client.vaults.with_raw_response.create(display_name="My vault")
        assert response.is_closed is True
        assert_matches_type(Vault, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        with client.vaults.with_streaming_response.create(display_name="My vault") as response:
            assert not response.is_closed
            assert_matches_type(Vault, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=VAULT))
        assert_matches_type(Vault, client.vaults.retrieve("vlt_123"), path=["response"])
        assert _req(route).method == "GET"

    @parametrize
    def test_path_params_retrieve(self, client: Orca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            client.vaults.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_is_escaped(self, client: Orca, respx_mock: MockRouter) -> None:
        """A path segment must not be able to smuggle in extra path structure."""
        route = respx_mock.get(url__regex=r".*").mock(return_value=httpx2.Response(200, json=VAULT))
        client.vaults.retrieve("a b/c")
        assert "/v1/vaults/a%20b%2Fc" in str(_req(route).url)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_uses_post(self, client: Orca, respx_mock: MockRouter) -> None:
        """Update is a POST, matching the contract -- not PATCH or PUT."""
        route = respx_mock.post("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=VAULT))
        client.vaults.update("vlt_123", display_name="Renamed", metadata={"drop": None})
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {"display_name": "Renamed", "metadata": {"drop": None}}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults").mock(return_value=httpx2.Response(200, json=_page(VAULT)))
        assert_matches_type(SyncPageCursor[Vault], client.vaults.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/vaults").mock(return_value=httpx2.Response(200, json=_page(VAULT)))
        client.vaults.list(limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates(self, client: Orca, respx_mock: MockRouter) -> None:
        second = {**VAULT, "id": "vlt_456"}
        respx_mock.get("/v1/vaults").mock(
            side_effect=[
                httpx2.Response(200, json=_page(VAULT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [v.id for v in client.vaults.list()] == ["vlt_123", "vlt_456"]
        assert _req(respx_mock, 1).url.params["page"] == "cursor-2"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=DELETED_VAULT))
        assert_matches_type(DeletedVault, client.vaults.delete("vlt_123"), path=["response"])
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/archive").mock(return_value=httpx2.Response(200, json=VAULT))
        assert_matches_type(Vault, client.vaults.archive("vlt_123"), path=["response"])
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_request_options_pass_through(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/vaults").mock(return_value=httpx2.Response(200, json=_page()))
        client.vaults.list(extra_headers={"X-Test-Header": "propagated"})
        assert _req(route).headers["x-test-header"] == "propagated"


class TestCredentials:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        credential = client.vaults.credentials.create(
            "vlt_123",
            auth={"type": "static_bearer", "token": "secret", "mcp_server_url": "https://mcp.test"},
            display_name="My credential",
        )
        assert_matches_type(VaultCredential, credential, path=["response"])
        body = json.loads(_req(route).content)
        assert body["auth"] == {"type": "static_bearer", "token": "secret", "mcp_server_url": "https://mcp.test"}
        assert body["display_name"] == "My credential"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_environment_variable_auth(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials").mock(
            return_value=httpx2.Response(200, json=ENV_VAR_CREDENTIAL)
        )
        credential = client.vaults.credentials.create(
            "vlt_123",
            auth={
                "type": "environment_variable",
                "secret_name": "API_TOKEN",
                "secret_value": "secret",
                "networking": {"type": "limited", "allowed_hosts": ["api.test"]},
                "injection_location": {"header": True},
            },
            metadata={"team": "core"},
        )
        assert_matches_type(VaultCredential, credential, path=["response"])
        body = json.loads(_req(route).content)
        assert body["auth"]["networking"] == {"type": "limited", "allowed_hosts": ["api.test"]}
        assert body["auth"]["injection_location"] == {"header": True}

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults/vlt_123/credentials").mock(return_value=httpx2.Response(200, json=CREDENTIAL))
        response = client.vaults.credentials.with_raw_response.create(
            "vlt_123", auth={"type": "static_bearer", "token": "s", "mcp_server_url": "https://mcp.test"}
        )
        assert response.is_closed is True
        assert_matches_type(VaultCredential, response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults/vlt_123/credentials").mock(return_value=httpx2.Response(200, json=CREDENTIAL))
        with client.vaults.credentials.with_streaming_response.create(
            "vlt_123", auth={"type": "static_bearer", "token": "s", "mcp_server_url": "https://mcp.test"}
        ) as response:
            assert not response.is_closed
            assert_matches_type(VaultCredential, response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_retrieve(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        assert_matches_type(
            VaultCredential, client.vaults.credentials.retrieve("vlt_123", "vcrd_123"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update_uses_post(self, client: Orca, respx_mock: MockRouter) -> None:
        """Update is a POST, matching the contract -- not PATCH or PUT."""
        route = respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        client.vaults.credentials.update(
            "vlt_123",
            "vcrd_123",
            display_name="Renamed",
            auth={"type": "static_bearer", "token": "rotated"},
            metadata={"drop": None},
        )
        request = _req(route)
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "display_name": "Renamed",
            "auth": {"type": "static_bearer", "token": "rotated"},
            "metadata": {"drop": None},
        }

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: Orca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults/vlt_123/credentials").mock(return_value=httpx2.Response(200, json=_page(CREDENTIAL)))
        assert_matches_type(
            SyncPageCursor[VaultCredential], client.vaults.credentials.list("vlt_123"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.get("/v1/vaults/vlt_123/credentials").mock(
            return_value=httpx2.Response(200, json=_page(CREDENTIAL))
        )
        client.vaults.credentials.list("vlt_123", limit=20, page="tok", include_archived=True)
        params = _req(route).url.params
        assert params["limit"] == "20"
        assert params["page"] == "tok"
        assert params["include_archived"] == "true"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.delete("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=DELETED_CREDENTIAL)
        )
        assert_matches_type(
            DeletedVaultCredential, client.vaults.credentials.delete("vlt_123", "vcrd_123"), path=["response"]
        )
        assert _req(route).method == "DELETE"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_archive(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123/archive").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        assert_matches_type(
            VaultCredential, client.vaults.credentials.archive("vlt_123", "vcrd_123"), path=["response"]
        )
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_validate(self, client: Orca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123/mcp_oauth_validate").mock(
            return_value=httpx2.Response(200, json=VALIDATION)
        )
        result = client.vaults.credentials.validate("vlt_123", "vcrd_123")
        assert_matches_type(CredentialValidation, result, path=["response"])
        request = _req(route)
        assert request.method == "POST"
        assert request.url.path == "/v1/vaults/vlt_123/credentials/vcrd_123/mcp_oauth_validate"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_validate_reports_invalid_without_raising(self, client: Orca, respx_mock: MockRouter) -> None:
        """A rejected credential is a result, not an error."""
        respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123/mcp_oauth_validate").mock(
            return_value=httpx2.Response(
                200,
                json={
                    **VALIDATION,
                    "status": "invalid",
                    "has_refresh_token": False,
                    "mcp_probe": {"method": "initialize", "http_response": None},
                    "refresh": {"status": "no_refresh_token", "http_response": None},
                },
            )
        )
        result = client.vaults.credentials.validate("vlt_123", "vcrd_123")
        assert result.status == "invalid"
        assert result.mcp_probe.http_response is None

    @parametrize
    def test_path_params(self, client: Orca) -> None:
        raw = client.vaults.credentials.with_raw_response
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            raw.list("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            raw.create("", auth={"type": "static_bearer", "token": "s", "mcp_server_url": "https://mcp.test"})
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            raw.retrieve("vlt_123", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            raw.update("vlt_123", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            raw.delete("vlt_123", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            raw.archive("vlt_123", "")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `credential_id` but received ''"):
            raw.validate("vlt_123", "")


class TestAsyncVaults:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        vault = await async_client.vaults.create(display_name="My vault")
        assert_matches_type(Vault, vault, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        response = await async_client.vaults.with_raw_response.create(display_name="My vault")
        assert response.is_closed is True
        assert_matches_type(Vault, await response.parse(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults").mock(return_value=httpx2.Response(200, json=VAULT))
        async with async_client.vaults.with_streaming_response.create(display_name="My vault") as response:
            assert not response.is_closed
            assert_matches_type(Vault, await response.parse(), path=["response"])
        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=VAULT))
        assert_matches_type(Vault, await async_client.vaults.retrieve("vlt_123"), path=["response"])

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOrca) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `vault_id` but received ''"):
            await async_client.vaults.with_raw_response.retrieve("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update_uses_post(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=VAULT))
        await async_client.vaults.update("vlt_123", display_name="Renamed")
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults").mock(return_value=httpx2.Response(200, json=_page(VAULT)))
        assert_matches_type(AsyncPageCursor[Vault], await async_client.vaults.list(), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        second = {**VAULT, "id": "vlt_456"}
        respx_mock.get("/v1/vaults").mock(
            side_effect=[
                httpx2.Response(200, json=_page(VAULT, next_page="cursor-2")),
                httpx2.Response(200, json=_page(second)),
            ]
        )
        assert [v.id async for v in async_client.vaults.list()] == ["vlt_123", "vlt_456"]

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/vaults/vlt_123").mock(return_value=httpx2.Response(200, json=DELETED_VAULT))
        assert_matches_type(DeletedVault, await async_client.vaults.delete("vlt_123"), path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults/vlt_123/archive").mock(return_value=httpx2.Response(200, json=VAULT))
        assert_matches_type(Vault, await async_client.vaults.archive("vlt_123"), path=["response"])


class TestAsyncCredentials:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults/vlt_123/credentials").mock(return_value=httpx2.Response(200, json=CREDENTIAL))
        credential = await async_client.vaults.credentials.create(
            "vlt_123", auth={"type": "static_bearer", "token": "s", "mcp_server_url": "https://mcp.test"}
        )
        assert_matches_type(VaultCredential, credential, path=["response"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_retrieve(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=ENV_VAR_CREDENTIAL)
        )
        assert_matches_type(
            VaultCredential, await async_client.vaults.credentials.retrieve("vlt_123", "vcrd_123"), path=["response"]
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update_uses_post(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        await async_client.vaults.credentials.update("vlt_123", "vcrd_123", display_name="Renamed")
        assert _req(route).method == "POST"

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/vaults/vlt_123/credentials").mock(return_value=httpx2.Response(200, json=_page(CREDENTIAL)))
        assert_matches_type(
            AsyncPageCursor[VaultCredential],
            await async_client.vaults.credentials.list("vlt_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/vaults/vlt_123/credentials/vcrd_123").mock(
            return_value=httpx2.Response(200, json=DELETED_CREDENTIAL)
        )
        assert_matches_type(
            DeletedVaultCredential,
            await async_client.vaults.credentials.delete("vlt_123", "vcrd_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_archive(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123/archive").mock(
            return_value=httpx2.Response(200, json=CREDENTIAL)
        )
        assert_matches_type(
            VaultCredential,
            await async_client.vaults.credentials.archive("vlt_123", "vcrd_123"),
            path=["response"],
        )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_validate(self, async_client: AsyncOrca, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/vaults/vlt_123/credentials/vcrd_123/mcp_oauth_validate").mock(
            return_value=httpx2.Response(200, json=VALIDATION)
        )
        result = await async_client.vaults.credentials.validate("vlt_123", "vcrd_123")
        assert_matches_type(CredentialValidation, result, path=["response"])
        assert _req(route).url.path == "/v1/vaults/vlt_123/credentials/vcrd_123/mcp_oauth_validate"
