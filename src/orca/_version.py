from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as _metadata_version

__title__ = "orca-sdk"

try:
    # Single source of truth: the version declared in `pyproject.toml` and recorded
    # in the installed distribution's metadata. Nothing here is hand-maintained, so
    # the packaged version and the version the client reports cannot drift apart.
    __version__ = _metadata_version(__title__)
except PackageNotFoundError:  # pragma: no cover - running from a source tree
    __version__ = "0.0.0.dev0"
