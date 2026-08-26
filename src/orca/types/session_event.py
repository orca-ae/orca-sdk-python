from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._models import BaseModel

__all__ = [
    "SessionEvent",
    "TextContentBlockParam",
    "Base64ContentSourceParam",
    "URLContentSourceParam",
    "FileContentSourceParam",
    "BinaryContentSourceParam",
    "TextDocumentSourceParam",
    "ImageContentBlockParam",
    "DocumentContentBlockParam",
    "SearchResultContentBlockParam",
    "MessageContentBlockParam",
    "ToolResultContentBlockParam",
    "OutcomeRubricParam",
    "SessionUserMessageEventInputParam",
    "SessionInterruptEventInputParam",
    "SessionToolConfirmationEventInputParam",
    "SessionCustomToolResultEventInputParam",
    "SessionDefineOutcomeEventInputParam",
    "SessionToolResultEventInputParam",
    "SessionSystemMessageEventInputParam",
    "SessionEventInputParam",
]


class SessionEvent(BaseModel):
    """One persisted event on a session's timeline.

    Only `id`, `type`, and `processed_at` are fixed by the contract; the rest of an
    event's payload is specific to its `type`. `BaseModel` keeps those extra fields,
    so callers discriminate on `type` and read the payload from the instance rather
    than from a closed union that would drop server-added event kinds.
    """

    id: str

    type: str

    processed_at: Optional[str] = None


# ---- Content blocks --------------------------------------------------------


class TextContentBlockParam(TypedDict, total=False):
    type: Required[Literal["text"]]

    text: Required[str]


class Base64ContentSourceParam(TypedDict, total=False):
    type: Required[Literal["base64"]]

    media_type: Required[str]

    data: Required[str]


class URLContentSourceParam(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class FileContentSourceParam(TypedDict, total=False):
    type: Required[Literal["file"]]

    file_id: Required[str]


BinaryContentSourceParam: TypeAlias = Union[
    Base64ContentSourceParam,
    URLContentSourceParam,
    FileContentSourceParam,
]


class TextDocumentSourceParam(TypedDict, total=False):
    """An inline text document source.

    The contract leaves this shape open; unlisted keys are forwarded untouched.
    """

    type: Required[Literal["text"]]

    data: Required[str]

    media_type: str


class ImageContentBlockParam(TypedDict, total=False):
    """An image block.

    The contract leaves this shape open; unlisted keys are forwarded untouched.
    """

    type: Required[Literal["image"]]

    source: Required[BinaryContentSourceParam]


class DocumentContentBlockParam(TypedDict, total=False):
    type: Required[Literal["document"]]

    source: Required[Union[BinaryContentSourceParam, TextDocumentSourceParam]]

    context: Optional[str]

    title: Optional[str]


class SearchResultContentBlockParam(TypedDict, total=False):
    """A search-result block.

    Only the discriminator is fixed by the contract; the payload varies by search
    provider, so unlisted keys are forwarded untouched.
    """

    type: Required[Literal["search_result"]]


MessageContentBlockParam: TypeAlias = Union[
    TextContentBlockParam,
    ImageContentBlockParam,
    DocumentContentBlockParam,
]

ToolResultContentBlockParam: TypeAlias = Union[
    MessageContentBlockParam,
    SearchResultContentBlockParam,
]


# ---- Outcome rubric --------------------------------------------------------


class OutcomeRubricTextParam(TypedDict, total=False):
    type: Required[Literal["text"]]

    content: Required[str]


class OutcomeRubricFileParam(TypedDict, total=False):
    type: Required[Literal["file"]]

    file_id: Required[str]


OutcomeRubricParam: TypeAlias = Union[OutcomeRubricTextParam, OutcomeRubricFileParam]


# ---- Event inputs ----------------------------------------------------------


class SessionUserMessageEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.message"]]

    content: Required[List[MessageContentBlockParam]]
    """Must hold at least one block; the server rejects an empty list."""


class SessionInterruptEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.interrupt"]]

    session_thread_id: Optional[str]
    """Interrupt one thread. Omit to interrupt the session's primary thread."""


class SessionToolConfirmationEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.tool_confirmation"]]

    tool_use_id: Required[str]

    result: Required[Literal["allow", "deny"]]

    deny_message: Optional[str]


class SessionCustomToolResultEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.custom_tool_result"]]

    custom_tool_use_id: Required[str]

    content: List[ToolResultContentBlockParam]

    is_error: Optional[bool]


class SessionDefineOutcomeEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.define_outcome"]]

    description: Required[str]

    rubric: Required[OutcomeRubricParam]

    max_iterations: Optional[int]


class SessionToolResultEventInputParam(TypedDict, total=False):
    type: Required[Literal["user.tool_result"]]

    tool_use_id: Required[str]

    content: List[ToolResultContentBlockParam]

    is_error: Optional[bool]


class SessionSystemMessageEventInputParam(TypedDict, total=False):
    type: Required[Literal["system.message"]]

    content: Required[List[TextContentBlockParam]]
    """Must hold at least one block; the server rejects an empty list."""


SessionEventInputParam: TypeAlias = Union[
    SessionUserMessageEventInputParam,
    SessionInterruptEventInputParam,
    SessionToolConfirmationEventInputParam,
    SessionCustomToolResultEventInputParam,
    SessionDefineOutcomeEventInputParam,
    SessionToolResultEventInputParam,
    SessionSystemMessageEventInputParam,
]
