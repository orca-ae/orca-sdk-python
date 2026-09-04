# End-to-end tests

The two workflows exercise the Python SDK against the same deployment topologies
as the TypeScript SDK:

- `e2e-managed-agents.yml` installs Managed Agents with Helm and connects directly
  with a workspace API key.
- `e2e-registry-provider.yml` deploys the Registry provider topology and connects
  through its OAuth-protected endpoint.

Both workflows pin the paired Registry and Harness images in `dependencies.env`,
resolve their immutable digests, and check out the matching Helm chart revision.
They build and install the current SDK wheel before running the shared Python
scenario, which covers extension discovery, Guardrail lifecycle,
Agent and Session guardrail attachment, Model Price reads, Environment, Trigger,
File, and Session lifecycle calls, deterministic execution with SSE replay, and
cloud discovery where available.

The direct workflow requires `SNBOT_GITHUB_TOKEN`. The Registry/provider workflow
also requires `LICENSE`, `OAUTH_CLIENT_ID`, and `OAUTH_CLIENT_SECRET`. Secret-backed
jobs skip fork pull requests.
