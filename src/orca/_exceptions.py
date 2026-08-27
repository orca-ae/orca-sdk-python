from __future__ import annotations

from typing import Optional, cast
from typing_extensions import Literal

import httpx2

from ._utils import is_dict

__all__ = [
    "OrcaError",
    "ExtensionNotAvailableError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "APIConnectionError",
    "APIConnectionTimeoutError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]

#: The `type` discriminator carried in an API error body, when the server sends one.
ErrorType = str


class OrcaError(Exception):
    """Base class for every error this SDK raises."""


class ExtensionNotAvailableError(OrcaError):
    """A namespace was called against a deployment that does not serve its extension group.

    Deliberately **not** an `APIError`: the SDK resolves extension availability from
    `GET /apis` and refuses the call locally, so no HTTP request is ever made for the
    gated operation and there is no response to attach.
    """

    group: str

    def __init__(self, group: str, message: str) -> None:
        super().__init__(message)
        self.group = group


class APIError(OrcaError):
    message: str
    request: httpx2.Request

    body: object | None
    """The API response body.

    If the API responded with a valid JSON structure then this property will be the
    decoded result.

    If it isn't a valid JSON structure then this will be the raw response.
    """

    def __init__(self, message: str, request: httpx2.Request, *, body: object | None) -> None:
        super().__init__(message)
        self.request = request
        self.message = message
        self.body = body


class APIResponseValidationError(APIError):
    response: httpx2.Response
    status_code: int

    def __init__(self, response: httpx2.Response, body: object | None, *, message: str | None = None) -> None:
        super().__init__(message or "Data returned by API invalid for expected schema.", response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class APIStatusError(APIError):
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx2.Response
    status_code: int
    request_id: str | None
    type: ErrorType | None

    def __init__(self, message: str, *, response: httpx2.Response, body: object | None) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("request-id")
        self.type = None
        if is_dict(body):
            error = body.get("error")
            if is_dict(error):
                self.type = cast(Optional[ErrorType], error.get("type"))

    @property
    def headers(self) -> httpx2.Headers:
        """The response headers, including any `retry-after` the server sent."""
        return self.response.headers

    @property
    def error(self) -> object | None:
        """The decoded `error` object from the response body, when the server sent one."""
        if is_dict(self.body):
            return self.body.get("error")
        return None


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx2.Request) -> None:
        super().__init__(message, request, body=None)


class APIConnectionTimeoutError(APIConnectionError):
    def __init__(self, *, request: httpx2.Request, message: str = "Request timed out.") -> None:
        super().__init__(message=message, request=request)


#: Alias kept so the request pipeline can raise the timeout error by either name.
APITimeoutError = APIConnectionTimeoutError


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400  # pyright: ignore[reportIncompatibleVariableOverride]


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401  # pyright: ignore[reportIncompatibleVariableOverride]


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403  # pyright: ignore[reportIncompatibleVariableOverride]


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404  # pyright: ignore[reportIncompatibleVariableOverride]


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409  # pyright: ignore[reportIncompatibleVariableOverride]


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422  # pyright: ignore[reportIncompatibleVariableOverride]


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429  # pyright: ignore[reportIncompatibleVariableOverride]


class InternalServerError(APIStatusError):
    pass
