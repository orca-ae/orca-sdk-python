from __future__ import annotations

from typing_extensions import TypeAlias

from .session_resource import SessionResourceRequestParam

__all__ = ["SessionResourceAddParams"]

#: The request body is the resource itself, discriminated on `type` -- there is no
#: enclosing object, so this is an alias rather than its own `TypedDict`.
SessionResourceAddParams: TypeAlias = SessionResourceRequestParam
