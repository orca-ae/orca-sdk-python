# Copyright The Orca Authors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import io
import sys
import runpy
import tarfile
import zipfile
import subprocess
from pathlib import Path
from unittest.mock import patch
from importlib.metadata import PackageNotFoundError

import yaml
import pytest

ROOT = Path(__file__).resolve().parents[1]


def make_artifact(directory: Path, *, wheel: bool, name: str = "runorca", version: str = "0.3.0") -> Path:
    metadata = f"Metadata-Version: 2.4\nName: {name}\nVersion: {version}\n".encode()
    if wheel:
        path = directory / f"{name}-{version}-py3-none-any.whl"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(f"{name}-{version}.dist-info/METADATA", metadata)
    else:
        path = directory / f"{name}-{version}.tar.gz"
        with tarfile.open(path, "w:gz") as archive:
            info = tarfile.TarInfo(f"{name}-{version}/PKG-INFO")
            info.size = len(metadata)
            archive.addfile(info, io.BytesIO(metadata))
    return path


def check_artifacts(*paths: Path, tag: str = "v0.3.0") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/check-release-artifacts"), tag, *map(str, paths)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_valid_release_artifacts(tmp_path: Path) -> None:
    result = check_artifacts(make_artifact(tmp_path, wheel=True), make_artifact(tmp_path, wheel=False))
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("wheel", [True, False])
@pytest.mark.parametrize("change", [{"name": "orca-sdk"}, {"version": "0.2.1"}])
def test_wrong_distribution_or_version_is_rejected(tmp_path: Path, wheel: bool, change: dict[str, str]) -> None:
    result = check_artifacts(make_artifact(tmp_path, wheel=wheel, **change), make_artifact(tmp_path, wheel=not wheel))
    assert result.returncode == 1
    assert "expected runorca 0.3.0" in result.stderr


@pytest.mark.parametrize("wheel", [True, False])
def test_incomplete_release_is_rejected(tmp_path: Path, wheel: bool) -> None:
    result = check_artifacts(make_artifact(tmp_path, wheel=wheel))
    assert result.returncode != 0
    assert "one wheel and one source distribution" in result.stderr


def test_duplicate_wheels_are_rejected(tmp_path: Path) -> None:
    wheel = make_artifact(tmp_path, wheel=True)
    result = check_artifacts(wheel, wheel, make_artifact(tmp_path, wheel=False))
    assert result.returncode != 0


def test_tag_must_have_version_prefix(tmp_path: Path) -> None:
    result = check_artifacts(make_artifact(tmp_path, wheel=True), make_artifact(tmp_path, wheel=False), tag="main")
    assert result.returncode != 0


@pytest.mark.parametrize("wheel", [True, False])
def test_corrupt_artifact_is_rejected(tmp_path: Path, wheel: bool) -> None:
    bad = make_artifact(tmp_path, wheel=wheel)
    bad.write_bytes(b"not an archive")
    result = check_artifacts(bad, make_artifact(tmp_path, wheel=not wheel))
    assert result.returncode == 1
    assert "verification failed" in result.stderr


def test_sdk_version_uses_runorca_distribution() -> None:
    with patch("importlib.metadata.version", return_value="0.3.0") as version:
        values = runpy.run_path(str(ROOT / "src/orca/_version.py"))
    version.assert_called_once_with("runorca")
    assert values["__title__"] == "runorca"
    assert values["__version__"] == "0.3.0"


def test_source_tree_version_fallback() -> None:
    with patch("importlib.metadata.version", side_effect=PackageNotFoundError):
        values = runpy.run_path(str(ROOT / "src/orca/_version.py"))
    assert values["__version__"] == "0.0.0.dev0"


@pytest.mark.parametrize("wheel", [True, False])
def test_filename_must_match_metadata(tmp_path: Path, wheel: bool) -> None:
    artifact = make_artifact(tmp_path, wheel=wheel)
    renamed = artifact.rename(artifact.with_name(artifact.name.replace("0.3.0", "9.9.9")))
    result = check_artifacts(renamed, make_artifact(tmp_path, wheel=not wheel))
    assert result.returncode == 1
    assert "filename does not match" in result.stderr


def test_release_workflow_limits_oidc_to_upload_job() -> None:
    workflow = yaml.load((ROOT / ".github/workflows/release.yml").read_text(), Loader=yaml.BaseLoader)
    assert workflow["permissions"] == {"contents": "read"}
    jobs = workflow["jobs"]
    assert jobs["pypi"]["permissions"] == {"id-token": "write"}
    assert "environment" not in jobs["pypi"]  # Matches the configured pending publisher.
    for name, job in jobs.items():
        if name != "pypi":
            assert "id-token" not in job.get("permissions", {})
    assert jobs["build"]["permissions"] == {"contents": "read"}
    assert jobs["pypi"]["needs"] == "build"
    steps = jobs["pypi"]["steps"]
    assert not any(step.get("uses", "").startswith("actions/checkout") for step in steps)
    commands = [step["run"] for step in steps if "run" in step]
    assert len(commands) == 1
    assert "uv publish --trusted-publishing always --check-url https://pypi.org/simple" in commands[0]
    assert jobs["github-release"]["needs"] == ["prepare", "pypi"]


def test_release_workflow_requires_main_and_exact_tags() -> None:
    workflow = yaml.load((ROOT / ".github/workflows/release.yml").read_text(), Loader=yaml.BaseLoader)
    assert set(workflow["on"]) == {"push", "schedule", "workflow_dispatch"}
    assert workflow["on"]["push"]["branches"] == ["main"]
    assert workflow["on"]["workflow_dispatch"]["inputs"]["tag"]["required"] == "false"
    assert workflow["concurrency"]["cancel-in-progress"] == "false"
    prepare = workflow["jobs"]["prepare"]
    assert "github.repository == 'orca-ae/orca-sdk-python'" in prepare["if"]
    assert "github.ref == 'refs/heads/main'" in prepare["if"]
    assert "inputs.tag" in prepare["outputs"]["tag"]
    build = workflow["jobs"]["build"]
    assert build["needs"] == "prepare"
    assert "needs.prepare.outputs.tag != ''" in build["if"]
    checkout = next(step for step in build["steps"] if step.get("uses", "").startswith("actions/checkout"))
    assert checkout["with"]["ref"] == "refs/tags/${{ needs.prepare.outputs.tag }}"
    assert checkout["with"]["persist-credentials"] == "false"
    assert not (ROOT / ".github/workflows/create-releases.yml").exists()
    assert not (ROOT / ".github/workflows/publish-release.yml").exists()
