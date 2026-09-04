"""Policy and pricing operations remain aligned with the vendored extension contract."""

from __future__ import annotations

import re
from pathlib import Path

from orca import Orca, AsyncOrca

SPEC = Path(__file__).parent.parent / "openapi" / "managed-agents-extensions.yaml"

SDK_OPERATIONS: dict[str, str] = {
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
            r"^\s*operationId:\s*((?:guardrails|modelPrices)\.\S+|discovery\.(?:policy|pricing)GroupResources)\s*$",
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
    assert set(SDK_OPERATIONS) == _operation_ids()


def test_sync_and_async_mappings_are_callable() -> None:
    clients: tuple[Orca | AsyncOrca, ...] = (
        Orca(api_key="k", base_url="http://127.0.0.1:4010"),
        AsyncOrca(api_key="k", base_url="http://127.0.0.1:4010"),
    )
    for client in clients:
        for operation_id, dotted in SDK_OPERATIONS.items():
            assert callable(_resolve(client, dotted)), f"{operation_id} -> client.{dotted} is not callable"
