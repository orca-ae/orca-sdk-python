from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._models import BaseModel

__all__ = [
    "SessionResourceBranchCheckout",
    "SessionResourceCommitCheckout",
    "SessionResourceCheckoutConfig",
    "SessionFileResource",
    "SessionRepositoryResource",
    "SessionMemoryStoreResource",
    "SessionResource",
    "DeletedSessionResource",
    "SessionResourceBranchCheckoutParam",
    "SessionResourceCommitCheckoutParam",
    "SessionResourceCheckoutConfigParam",
    "FileSessionResourceRequestParam",
    "RepositorySessionResourceRequestParam",
    "MemoryStoreSessionResourceRequestParam",
    "SessionResourceRequestParam",
]

SessionResourceAccess: TypeAlias = Literal["read_only", "read_write"]


# ---- Response models -------------------------------------------------------


class SessionResourceBranchCheckout(BaseModel):
    type: Literal["branch"]

    name: str


class SessionResourceCommitCheckout(BaseModel):
    type: Literal["commit"]

    sha: str


SessionResourceCheckoutConfig: TypeAlias = Union[
    SessionResourceBranchCheckout,
    SessionResourceCommitCheckout,
]


class SessionFileResource(BaseModel):
    id: str

    type: Literal["file"]

    file_id: str

    mount_path: str

    created_at: str

    updated_at: str


class SessionRepositoryResource(BaseModel):
    id: str

    type: Literal["github_repository"]

    mount_path: str

    url: str

    checkout: Optional[SessionResourceCheckoutConfig] = None

    created_at: str

    updated_at: str


class SessionMemoryStoreResource(BaseModel):
    type: Literal["memory_store"]

    memory_store_id: str

    access: Optional[SessionResourceAccess] = None

    description: Optional[str] = None

    instructions: Optional[str] = None

    mount_path: Optional[str] = None

    name: Optional[str] = None


SessionResource: TypeAlias = Union[
    SessionFileResource,
    SessionRepositoryResource,
    SessionMemoryStoreResource,
]


class DeletedSessionResource(BaseModel):
    id: str

    type: Literal["session_resource_deleted"]


# ---- Request parameter types -----------------------------------------------


class SessionResourceBranchCheckoutParam(TypedDict, total=False):
    type: Required[Literal["branch"]]

    name: Required[str]


class SessionResourceCommitCheckoutParam(TypedDict, total=False):
    type: Required[Literal["commit"]]

    sha: Required[str]


SessionResourceCheckoutConfigParam: TypeAlias = Union[
    SessionResourceBranchCheckoutParam,
    SessionResourceCommitCheckoutParam,
]


class FileSessionResourceRequestParam(TypedDict, total=False):
    type: Required[Literal["file"]]

    file_id: Required[str]

    access: Optional[SessionResourceAccess]

    instructions: Optional[str]

    mount_path: Optional[str]

    mount_strategy: Literal["tarball_prefetch"]


class RepositorySessionResourceRequestParam(TypedDict, total=False):
    type: Required[Literal["github_repository"]]

    authorization_token: Required[str]
    """Write-only: the server stores the token and never returns it."""

    url: Required[str]

    access: Optional[SessionResourceAccess]

    checkout: Optional[SessionResourceCheckoutConfigParam]

    instructions: Optional[str]

    mount_path: Optional[str]


class MemoryStoreSessionResourceRequestParam(TypedDict, total=False):
    type: Required[Literal["memory_store"]]

    memory_store_id: Required[str]

    access: Optional[SessionResourceAccess]

    instructions: Optional[str]


SessionResourceRequestParam: TypeAlias = Union[
    FileSessionResourceRequestParam,
    RepositorySessionResourceRequestParam,
    MemoryStoreSessionResourceRequestParam,
]
