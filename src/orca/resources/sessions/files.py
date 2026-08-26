from __future__ import annotations

from typing import Any, cast

import httpx2

from ...types import session_file_list_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPage, AsyncPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.session_file import SessionFile, DeletedSessionFile

__all__ = ["SessionFiles", "AsyncSessionFiles"]


class SessionFiles(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionFilesWithRawResponse:
        return SessionFilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionFilesWithStreamingResponse:
        return SessionFilesWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[SessionFile]:
        """
        List the files attached to a session.

        This list uses id cursors rather than opaque page tokens. Auto-iteration
        preserves the requested direction: a `before_id` query follows `first_id`,
        otherwise it follows `last_id`. Never send both in one request.

        Args:
          session_id: The session whose files to list.

          limit: Maximum number of files to return per page.

          after_id: Page forward from this file id.

          before_id: Page backward from this file id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/files", session_id=session_id),
            page=SyncPage[SessionFile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "after_id": after_id, "before_id": before_id},
                    session_file_list_params.SessionFileListParams,
                ),
            ),
            model=cast(Any, SessionFile),  # Union types cannot be passed in as arguments in the type system
        )

    def retrieve(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionFile:
        """
        Retrieve the metadata for one session file.

        Args:
          session_id: The session that owns the file.

          file_id: The file to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return cast(
            SessionFile,
            self._get(
                path_template("/v1/sessions/{session_id}/files/{file_id}", session_id=session_id, file_id=file_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionFile),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def download(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the raw bytes of a session file.

        Returns the underlying HTTP response rather than a parsed model: the body is
        the file itself, of whatever content type it was stored with.

        Args:
          session_id: The session that owns the file.

          file_id: The file to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return self._get(
            path_template("/v1/sessions/{session_id}/files/{file_id}/content", session_id=session_id, file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    def delete(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSessionFile:
        """
        Permanently delete a session file and return its tombstone.

        Args:
          session_id: The session that owns the file.

          file_id: The file to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._delete(
            path_template("/v1/sessions/{session_id}/files/{file_id}", session_id=session_id, file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSessionFile,
        )


class AsyncSessionFiles(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionFilesWithRawResponse:
        return AsyncSessionFilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionFilesWithStreamingResponse:
        return AsyncSessionFilesWithStreamingResponse(self)

    def list(
        self,
        session_id: str,
        *,
        limit: int | Omit = omit,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SessionFile, AsyncPage[SessionFile]]:
        """
        List the files attached to a session.

        This list uses id cursors rather than opaque page tokens. Auto-iteration
        preserves the requested direction: a `before_id` query follows `first_id`,
        otherwise it follows `last_id`. Never send both in one request.

        Args:
          session_id: The session whose files to list.

          limit: Maximum number of files to return per page.

          after_id: Page forward from this file id.

          before_id: Page backward from this file id.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        return self._get_api_list(
            path_template("/v1/sessions/{session_id}/files", session_id=session_id),
            page=AsyncPage[SessionFile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "after_id": after_id, "before_id": before_id},
                    session_file_list_params.SessionFileListParams,
                ),
            ),
            model=cast(Any, SessionFile),  # Union types cannot be passed in as arguments in the type system
        )

    async def retrieve(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SessionFile:
        """
        Retrieve the metadata for one session file.

        Args:
          session_id: The session that owns the file.

          file_id: The file to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return cast(
            SessionFile,
            await self._get(
                path_template("/v1/sessions/{session_id}/files/{file_id}", session_id=session_id, file_id=file_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, SessionFile),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def download(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the raw bytes of a session file.

        Returns the underlying HTTP response rather than a parsed model: the body is
        the file itself, of whatever content type it was stored with.

        Args:
          session_id: The session that owns the file.

          file_id: The file to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/sessions/{session_id}/files/{file_id}/content", session_id=session_id, file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    async def delete(
        self,
        session_id: str,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedSessionFile:
        """
        Permanently delete a session file and return its tombstone.

        Args:
          session_id: The session that owns the file.

          file_id: The file to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._delete(
            path_template("/v1/sessions/{session_id}/files/{file_id}", session_id=session_id, file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedSessionFile,
        )


class SessionFilesWithRawResponse:
    def __init__(self, files: SessionFiles) -> None:
        self._files = files

        self.list = to_raw_response_wrapper(files.list)
        self.retrieve = to_raw_response_wrapper(files.retrieve)
        self.download = to_raw_response_wrapper(files.download)
        self.delete = to_raw_response_wrapper(files.delete)


class AsyncSessionFilesWithRawResponse:
    def __init__(self, files: AsyncSessionFiles) -> None:
        self._files = files

        self.list = async_to_raw_response_wrapper(files.list)
        self.retrieve = async_to_raw_response_wrapper(files.retrieve)
        self.download = async_to_raw_response_wrapper(files.download)
        self.delete = async_to_raw_response_wrapper(files.delete)


class SessionFilesWithStreamingResponse:
    def __init__(self, files: SessionFiles) -> None:
        self._files = files

        self.list = to_streamed_response_wrapper(files.list)
        self.retrieve = to_streamed_response_wrapper(files.retrieve)
        self.download = to_streamed_response_wrapper(files.download)
        self.delete = to_streamed_response_wrapper(files.delete)


class AsyncSessionFilesWithStreamingResponse:
    def __init__(self, files: AsyncSessionFiles) -> None:
        self._files = files

        self.list = async_to_streamed_response_wrapper(files.list)
        self.retrieve = async_to_streamed_response_wrapper(files.retrieve)
        self.download = async_to_streamed_response_wrapper(files.download)
        self.delete = async_to_streamed_response_wrapper(files.delete)
