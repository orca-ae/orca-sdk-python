# End-to-end tests

The `e2e-managed-agents.yml` workflow installs the engine with Helm on a Kind cluster
and runs the Python SDK against it directly with a workspace API key. The deployment
includes the engine's own registry service; no separate proprietary provider is needed.

The workflow resolves the pinned engine images to immutable digests, checks out the engine
source at the revision those images were built from, and builds and installs the SDK wheel
from this checkout. Then it runs `sdk_scenario.py`. It covers:

- extension discovery
- the Guardrail lifecycle, and attaching guardrails to Agents and Sessions
- Model Price reads
- Environment, Trigger, File and Session lifecycle calls
- deterministic execution with SSE replay
- rejection of hosted extension calls when the deployment does not serve that API group

The deployment stores files in RustFS, an S3-compatible object store deployed from
`object-store.yaml`.

Session cleanup uses `POST /v1/sessions/{id}/archive` and verifies the returned Session ID
and `archived_at`. It does not call DELETE.

Hosted extension APIs remain part of the SDK and are covered by mocked tests in
`tests/api_resources/cloud/`; this suite does not deploy a hosted service.

## Who can run it

The suite depends on private sources and credentials, so it only runs where the
repository's secrets are available. That means pushes to `main`, the daily schedule, manual
runs, and pull requests from branches in this repository. Pull requests from forks and from
Dependabot skip it.

## Configuration

The dependency pins live in `dependencies.env`: the engine source repository and the
paired registry and harness images. To move a pin, change it there in a pull request.

Credentials live in repository secrets:

| Secret | Holds |
|---|---|
| `SNBOT_GITHUB_TOKEN` | Token that can read the private sources and pull their images |

## Keeping the logs clean

This repository is public, so its workflow logs are too. The suite follows these rules:

- **Credentials in secrets.** Anything that grants access, or points at an authentication
  service, comes from a secret, so GitHub masks it everywhere.
- **Mask what you derive.** Values read from private sources at run time, such as an image's
  source revision or the gateway image named in the engine chart, are masked as soon as
  they're computed.
- **Keep third-party output off the log.** The output of deployment scripts and builds that
  the suite doesn't own goes to files under `$RUNNER_TEMP`, which are never printed or
  uploaded.
- **No debugging aids that expose the runner.** No step summaries, diagnostics dumps,
  uploaded artifacts or debug shells.

When a run fails, the log shows which step failed and the pod status. To dig deeper,
reproduce the topology locally.
