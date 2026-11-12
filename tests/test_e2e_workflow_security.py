# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"


def test_credential_backed_e2e_only_runs_trusted_main_events() -> None:
    workflow = yaml.safe_load((WORKFLOWS / "e2e-managed-agents.yml").read_text())
    # PyYAML's YAML 1.1 loader treats the GitHub Actions key `on` as True.
    events = workflow[True]
    assert set(events) == {"push", "schedule", "workflow_dispatch"}
    assert events["push"]["branches"] == ["main"]
    guard = (
        "github.ref == 'refs/heads/main' && "
        "(github.event_name == 'push' || github.event_name == 'schedule' || "
        "github.event_name == 'workflow_dispatch')"
    )
    for name in ("secret-gate", "e2e"):
        condition = " ".join(workflow["jobs"][name]["if"].split())
        expected = guard if name == "secret-gate" else "needs.secret-gate.outputs.enabled == 'true' && " + guard
        assert condition == expected


def test_sdk_checkout_and_cache_do_not_bridge_pr_state() -> None:
    workflow = yaml.safe_load((WORKFLOWS / "e2e-managed-agents.yml").read_text())
    steps = workflow["jobs"]["e2e"]["steps"]
    checkout = steps[0]
    assert checkout["uses"].startswith("actions/checkout@")
    assert checkout["with"]["ref"] == "${{ github.sha }}"
    assert checkout["with"]["persist-credentials"] is False
    for step in steps:
        if step.get("uses", "").startswith("astral-sh/setup-uv@"):
            assert step["with"]["enable-cache"] is False


def test_pr_ci_remains_available_without_e2e_credentials() -> None:
    text = (WORKFLOWS / "ci.yml").read_text()
    workflow = yaml.safe_load(text)
    assert "pull_request" in workflow[True]
    assert {"lint", "test", "build"} <= set(workflow["jobs"])
    assert "secrets." not in text
