"""Conventions in `types/` that are easy to get wrong and hard to notice.

The alias check here guards a silent failure: `PropertyInfo(alias=...)` is the
correct mechanism on a request `TypedDict`, but on a response `BaseModel` it does
not raise -- it just yields `None` for that field forever. Prose in the contributor
guide is not enough for a mistake that produces no error, so it fails the build.
"""

from __future__ import annotations

import re
import ast
from typing import Optional
from pathlib import Path
from typing_extensions import Annotated

import pydantic

from orca._utils import PropertyInfo
from orca._models import BaseModel

TYPES_DIR = Path(__file__).parent.parent / "src" / "orca" / "types"


def test_property_info_alias_does_not_work_on_response_models() -> None:
    """Pin the behaviour the lint below exists to prevent.

    If a future runtime change makes `PropertyInfo(alias=...)` work on models, this
    fails and the restriction can be lifted deliberately rather than by accident.
    """

    class ViaPropertyInfo(BaseModel):
        field_name: Annotated[Optional[str], PropertyInfo(alias="fieldName")] = None

    class ViaPydanticField(BaseModel):
        field_name: Optional[str] = pydantic.Field(default=None, alias="fieldName")

    assert ViaPropertyInfo.construct(fieldName="value").field_name is None, (
        "PropertyInfo(alias=) now works on response models -- update AGENTS.md §7 and drop this restriction"
    )
    assert ViaPydanticField.construct(fieldName="value").field_name == "value"


def _model_classes() -> list[tuple[Path, ast.ClassDef]]:
    found: list[tuple[Path, ast.ClassDef]] = []
    for file in sorted(TYPES_DIR.rglob("*.py")):
        tree = ast.parse(file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = {getattr(b, "id", getattr(b, "attr", "")) for b in node.bases}
                if "BaseModel" in bases:
                    found.append((file, node))
    return found


def test_response_models_never_alias_via_property_info() -> None:
    offenders: list[str] = []
    for file, cls in _model_classes():
        for node in ast.walk(cls):
            if isinstance(node, ast.Call):
                name = getattr(node.func, "id", getattr(node.func, "attr", ""))
                if name == "PropertyInfo" and any(kw.arg == "alias" for kw in node.keywords):
                    offenders.append(f"{file.name}:{node.lineno} in {cls.name}")

    assert not offenders, (
        "PropertyInfo(alias=...) on a response model silently yields None for that field. "
        f"Use pydantic.Field(alias=...) instead. Offenders: {offenders}"
    )


def test_models_were_actually_scanned() -> None:
    """Guard the guard: a scanner that finds no models would pass everything."""
    assert len(_model_classes()) >= 50, f"only found {len(_model_classes())} response models to check"


def test_core_response_models_use_wire_casing() -> None:
    """Core response attributes mirror the core wire format, which is snake_case.

    Cloud is deliberately different: its wire format is camelCase, so its models
    mirror that instead. Both follow the same rule -- mirror the wire -- so this
    only pins the core half, where a camelCase field would mean a real mistake.
    """
    offenders: list[str] = []
    for file, cls in _model_classes():
        if file.name.startswith("cloud_"):
            continue
        for node in cls.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if re.search(r"[a-z][A-Z]", node.target.id):
                    offenders.append(f"{file.name}:{node.lineno} {cls.name}.{node.target.id}")

    assert not offenders, f"core response models should mirror the snake_case core wire format: {offenders}"
