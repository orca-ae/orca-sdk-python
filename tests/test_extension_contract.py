# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

"""Every raw engine operation is implemented or explicitly excluded."""

from __future__ import annotations

import re
from pathlib import Path

from orca import Orca, AsyncOrca
from tests.test_contract import NOT_EXPOSED as CORE_EXCLUDED, SDK_OPERATIONS as CORE_OPERATIONS

SPEC = Path(__file__).parent.parent / "openapi" / "managed-agents-engine.yaml"

SDK_OPERATIONS: dict[str, str] = {
    **CORE_OPERATIONS,
    "guardrails.effective": "guardrails.effective",
    "guardrails.dogwoodSchema": "guardrails.dogwood_schema",
    "discovery.pricingV2GroupResources": "discovery.pricing_v2_group_resources",
    "modelPriceRules.list": "model_price_rules.list",
    "discovery.runtimeGroupResources": "discovery.runtime_group_resources",
    "discovery.harnesses": "discovery.harnesses",
    "environments.rotateKey": "environments.rotate_key",
    "environments.revokeKey": "environments.revoke_key",
    "environments.workStats": "environments.work_stats",
    "sessions.interruptThread": "sessions.threads.interrupt",
    "discovery.policyGroupResources": "discovery.policy_group_resources",
    "discovery.pricingGroupResources": "discovery.pricing_group_resources",
    "guardrails.archive": "guardrails.archive",
    "guardrails.create": "guardrails.create",
    "guardrails.delete": "guardrails.delete",
    "guardrails.get": "guardrails.retrieve",
    "guardrails.list": "guardrails.list",
    "guardrails.listTypes": "guardrails.list_types",
    "guardrails.update": "guardrails.update",
    "modelPrices.get": "model_prices.retrieve",
    "modelPrices.list": "model_prices.list",
}


def _operation_ids() -> set[str]:
    return set(
        re.findall(
            r"^\s*operationId:\s*(\S+)\s*$",
            SPEC.read_text(),
            re.M,
        )
    )


def _resolve(client: Orca | AsyncOrca, dotted: str) -> object:
    target: object = client
    for part in dotted.split("."):
        target = getattr(target, part)
    return target


def test_spec_is_vendored() -> None:
    assert SPEC.exists()


def test_every_operation_is_mapped() -> None:
    excluded = {
        **dict.fromkeys(CORE_EXCLUDED, "Excluded by the portable surface; see tests/test_contract.py"),
        "gitProxy.advertise": "Special JWT authentication and binary Git protocol are outside the SDK surface",
        "gitProxy.uploadPack": "Special JWT authentication and binary Git protocol are outside the SDK surface",
    }
    assert not set(SDK_OPERATIONS) & set(excluded)
    assert len(_operation_ids()) == 114
    assert set(SDK_OPERATIONS) | set(excluded) == _operation_ids()


def test_sync_and_async_mappings_are_callable() -> None:
    clients: tuple[Orca | AsyncOrca, ...] = (
        Orca(api_key="k", base_url="http://127.0.0.1:4010"),
        AsyncOrca(api_key="k", base_url="http://127.0.0.1:4010"),
    )
    for client in clients:
        for operation_id, dotted in SDK_OPERATIONS.items():
            assert callable(_resolve(client, dotted)), f"{operation_id} -> client.{dotted} is not callable"
            for wrapper in ("with_raw_response", "with_streaming_response"):
                assert callable(_resolve(getattr(client, wrapper), dotted)), f"{operation_id}: missing {wrapper}"
