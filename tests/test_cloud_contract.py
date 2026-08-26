"""Every cloud-extension operation is reachable, with the right verb and path.

Matching by operationId would not work here -- the contract's cloud names do not
correspond to SDK method names -- so this checks the thing that actually matters:
for each `(verb, path)` the contract declares, the SDK issues a request with that
same verb and path. That also catches a wrong HTTP verb, which is the most likely
way this group drifts, since Kafka Connect mixes PUT, POST, PATCH and DELETE for
operations that read like the same kind of action.
"""

from __future__ import annotations

import re
import ast
from pathlib import Path

import pytest

SPEC = Path(__file__).parent.parent / "openapi" / "cloud-extensions.yaml"
CLOUD_SRC = Path(__file__).parent.parent / "src" / "orca" / "resources" / "cloud"

# The contract declares these paths relative to the extension group's server URL.
PREFIX = "/apis/cloud.sn.io/v1"

VERBS = ("get", "post", "put", "patch", "delete")

# Deliberately not exposed: its only declared response is HTTP 400 stating that
# validation is unsupported, so there is nothing to call successfully.
NOT_EXPOSED = {("PUT", f"{PREFIX}/connectors/kafka/connector-plugins/{{}}/config/validate")}


def _placeholders(path: str) -> str:
    """Normalise `{name}` / `{plugin_name}` so spec and SDK parameter names can differ."""
    return re.sub(r"\{[^}]*\}", "{}", path)


def _spec_operations() -> set[tuple[str, str]]:
    path = verb = None
    found: set[tuple[str, str]] = set()
    for line in SPEC.read_text().split("\n"):
        m = re.match(r"^  (/\S*):\s*$", line)
        if m:
            path, verb = m.group(1), None
            continue
        m = re.match(rf"^    ({'|'.join(VERBS)}):\s*$", line)
        if m:
            verb = m.group(1)
            continue
        if re.match(r"^\s+operationId:\s*\S+\s*$", line) and path and verb:
            full = PREFIX + ("/" if path == "/" else path)
            found.add((verb.upper(), _placeholders(full)))
    return found


def _sdk_operations() -> set[tuple[str, str]]:
    """Extract the (verb, path) pairs the cloud resources issue.

    Paths are assembled from string literals, module-level constants, and
    `path_template(...)` calls, sometimes with a trailing `":action"` suffix. This
    resolves all of those so the check sees the real request path.
    """
    found: set[tuple[str, str]] = set()

    for file in sorted(CLOUD_SRC.rglob("*.py")):
        tree = ast.parse(file.read_text())

        # module-level `NAME = "literal"` path constants
        consts: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                if isinstance(node.value.value, str):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            consts[target.id] = node.value.value

        def resolve(node: ast.AST, consts: dict[str, str] = consts) -> str | None:
            """Fold a path expression down to a literal, or give up."""
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return node.value
            if isinstance(node, ast.Name):
                return consts.get(node.id)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left, right = resolve(node.left), resolve(node.right)
                return None if left is None or right is None else left + right
            if isinstance(node, ast.Call):
                func = node.func
                name = getattr(func, "id", None) or getattr(func, "attr", None)
                if name == "path_template" and node.args:
                    return resolve(node.args[0])
            return None

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not isinstance(func, ast.Attribute) or not node.args:
                continue
            attr = func.attr
            if not attr.startswith("_"):
                continue
            verb = attr[1:].removesuffix("_api_list")
            if verb not in VERBS:
                continue
            path = resolve(node.args[0])
            if path and path.startswith(PREFIX):
                found.add((verb.upper(), _placeholders(path)))

    return found


@pytest.fixture(scope="module")
def spec_ops() -> set[tuple[str, str]]:
    return _spec_operations()


@pytest.fixture(scope="module")
def sdk_ops() -> set[tuple[str, str]]:
    return _sdk_operations()


def test_spec_is_vendored() -> None:
    assert SPEC.exists(), f"vendored contract missing at {SPEC}"


def test_extractor_found_operations(spec_ops: set[tuple[str, str]], sdk_ops: set[tuple[str, str]]) -> None:
    """Guard the guard: an extractor that silently finds nothing would pass everything."""
    assert len(spec_ops) >= 90, f"only parsed {len(spec_ops)} operations from the contract"
    assert len(sdk_ops) >= 90, f"only found {len(sdk_ops)} request paths in the cloud resources"


def test_every_operation_is_reachable(spec_ops: set[tuple[str, str]], sdk_ops: set[tuple[str, str]]) -> None:
    missing = spec_ops - sdk_ops - NOT_EXPOSED
    assert not missing, (
        "cloud operations in the contract that the SDK never requests: "
        f"{sorted(missing)}. Check both the path and the HTTP verb."
    )


def test_unsupported_operation_stays_unexposed(sdk_ops: set[tuple[str, str]]) -> None:
    for verb, path in NOT_EXPOSED:
        assert (verb, path) not in sdk_ops, f"{verb} {path} declares only an error response and must not be called"


def test_no_paths_outside_the_contract(spec_ops: set[tuple[str, str]], sdk_ops: set[tuple[str, str]]) -> None:
    invented = sdk_ops - spec_ops
    assert not invented, f"SDK requests cloud paths the contract does not declare: {sorted(invented)}"
