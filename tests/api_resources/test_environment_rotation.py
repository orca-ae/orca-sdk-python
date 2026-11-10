# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from orca import Orca, APIError, AsyncOrca
from tests.api_resources.test_environments import ENVIRONMENT, base_url


@pytest.mark.parametrize("failure", ["status", "connection", "timeout"])
@pytest.mark.parametrize("global_retries", [2, 4])
@pytest.mark.respx(base_url=base_url)
def test_rotation_does_not_retry(client: Orca, respx_mock: MockRouter, failure: str, global_retries: int) -> None:
    attempts = 0

    def respond(request: httpx2.Request) -> httpx2.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            if failure == "connection":
                raise httpx2.ConnectError("fixture connection lost", request=request)
            if failure == "timeout":
                raise httpx2.ReadTimeout("fixture timeout", request=request)
            return httpx2.Response(504, headers={"retry-after-ms": "1"})
        return httpx2.Response(200, json={"env_key": "fixture", "env_key_expires_at": "2026-11-10T00:00:00Z"})

    route = respx_mock.post("/v1/environments/env_123/rotate-key").mock(side_effect=respond)
    with pytest.raises(APIError):
        client.with_options(max_retries=global_retries).environments.rotate_key(
            "env_123", extra_headers={"X-Test": "rotation", "Idempotency-Key": "explicit"}, timeout=1
        )
    assert route.call_count == 1
    request = cast(Any, route.calls[0]).request
    assert request.headers["X-Test"] == "rotation"
    assert request.headers["Idempotency-Key"] == "explicit"
    assert json.loads(request.content) == {}


@pytest.mark.parametrize("failure", ["status", "connection", "timeout"])
@pytest.mark.parametrize("global_retries", [2, 4])
@pytest.mark.respx(base_url=base_url)
async def test_async_rotation_does_not_retry(
    async_client: AsyncOrca, respx_mock: MockRouter, failure: str, global_retries: int
) -> None:
    attempts = 0

    def respond(request: httpx2.Request) -> httpx2.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            if failure == "connection":
                raise httpx2.ConnectError("fixture connection lost", request=request)
            if failure == "timeout":
                raise httpx2.ReadTimeout("fixture timeout", request=request)
            return httpx2.Response(504, headers={"retry-after-ms": "1"})
        return httpx2.Response(200, json={"env_key": "fixture", "env_key_expires_at": "2026-11-10T00:00:00Z"})

    route = respx_mock.post("/v1/environments/env_123/rotate-key").mock(side_effect=respond)
    with pytest.raises(APIError):
        await async_client.with_options(max_retries=global_retries).environments.rotate_key(
            "env_123", extra_headers={"X-Test": "rotation", "Idempotency-Key": "explicit"}, timeout=1
        )
    assert route.call_count == 1
    request = cast(Any, route.calls[0]).request
    assert request.headers["X-Test"] == "rotation"
    assert request.headers["Idempotency-Key"] == "explicit"
    assert json.loads(request.content) == {}


@pytest.mark.respx(base_url=base_url)
def test_rotation_succeeds_and_reads_keep_retries(client: Orca, respx_mock: MockRouter) -> None:
    rotation = respx_mock.post("/v1/environments/env_123/rotate-key").respond(
        200, json={"env_key": "fixture", "env_key_expires_at": "2026-11-10T00:00:00Z"}
    )
    assert client.environments.rotate_key("env_123").env_key == "fixture"
    assert rotation.call_count == 1
    read = respx_mock.get("/v1/environments/env_123").mock(
        side_effect=[httpx2.Response(504, headers={"retry-after-ms": "1"}), httpx2.Response(200, json=ENVIRONMENT)]
    )
    assert client.environments.retrieve("env_123").id == "env_123"
    assert read.call_count == 2


@pytest.mark.respx(base_url=base_url)
async def test_async_rotation_succeeds_and_reads_keep_retries(async_client: AsyncOrca, respx_mock: MockRouter) -> None:
    rotation = respx_mock.post("/v1/environments/env_123/rotate-key").respond(
        200, json={"env_key": "fixture", "env_key_expires_at": "2026-11-10T00:00:00Z"}
    )
    assert (await async_client.environments.rotate_key("env_123")).env_key == "fixture"
    assert rotation.call_count == 1
    read = respx_mock.get("/v1/environments/env_123").mock(
        side_effect=[httpx2.Response(504, headers={"retry-after-ms": "1"}), httpx2.Response(200, json=ENVIRONMENT)]
    )
    assert (await async_client.environments.retrieve("env_123")).id == "env_123"
    assert read.call_count == 2
