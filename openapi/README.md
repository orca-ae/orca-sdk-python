# Contract provenance

These files are the API contracts this SDK is built against. The servers that implement
them generate them, and they are vendored here; AGENTS.md §1 describes what each one
governs.

## `managed-agents.yaml`

Refreshed on 2026-09-09 from the published SDK core contract, without editing or
reserializing its bytes. It is identical to the copy the public Go SDK carries at
`orca-ae/orca-sdk-go`, `openapi/managed-agents.yaml`
(SHA-256 `5320b32f415cb7e73383323dcdcdc3a5d36c418dfc73cca590a5e520ab3ce984`). All nine
`guardrail_ids` property definitions agree with the engine's server contract.

The published SDK core contract is **not** a byte-for-byte copy of the engine's current
combined server contract. The server also includes the policy and pricing operations,
which the SDKs take from `managed-agents-extensions.yaml`, plus additional environment and
session operations and other shared-path differences. This refresh keeps the published SDK
contract boundary rather than silently importing those changes. A fully server-identical
refresh needs coordinated contract publishing across the SDKs; until then this file
records the exception to the contributor guide's byte-for-byte provenance rule.

## Local edits

Three lines differ from the server output, so that the public repository names neither
internal systems nor the company that runs the hosted service:

- `managed-agents-deployment.overlay.yaml`: `info.title`, and the value of
  `x-deployment-deviations-source`.
- `cloud-extensions.yaml`: `info.title`.

No operation, path, parameter or schema changed. Once the owning services emit the neutral
text themselves, the next refresh returns these files to byte-for-byte copies.
