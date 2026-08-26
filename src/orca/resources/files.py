from __future__ import annotations

from typing import Any, Mapping, cast

import httpx2

from ..types import file_list_params, file_upload_params
from .._files import deepcopy_with_paths
from .._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPage, AsyncPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.file_metadata import DeletedFile, FileMetadata

__all__ = ["Files", "AsyncFiles"]


class Files(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesWithRawResponse:
        return FilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesWithStreamingResponse:
        return FilesWithStreamingResponse(self)

    def upload(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> FileMetadata:
        """
        Upload a file as `multipart/form-data`.

        `file` is the only part the contract accepts. The server records the MIME type
        the part declares, so pass a `(filename, content, content_type)` tuple when
        the content type matters and you cannot rely on it being inferred.

        Args:
          file: The file bytes to upload.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, paths=[["file"]])
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return cast(
            FileMetadata,
            self._post(
                "/v1/files",
                body=maybe_transform(body, file_upload_params.FileUploadParams),
                files=extracted_files,
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                # Union types cannot be passed in as arguments in the type system.
                cast_to=cast(Any, FileMetadata),
            ),
        )

    def retrieve(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> FileMetadata:
        """
        Retrieve metadata for a stored file.

        This returns metadata only; the bytes come from `download`.

        Args:
          file_id: The file to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return cast(
            FileMetadata,
            self._get(
                path_template("/v1/files/{file_id}", file_id=file_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                # Union types cannot be passed in as arguments in the type system.
                cast_to=cast(Any, FileMetadata),
            ),
        )

    def download(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the raw contents of a stored file.

        The endpoint serves `application/octet-stream`, so this returns the underlying
        HTTP response rather than a parsed model: read `.content`, `.text`, or stream
        it yourself. A file whose metadata reports `downloadable` as false is refused
        here by the server.

        Args:
          file_id: The file to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return self._get(
            path_template("/v1/files/{file_id}/content", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[FileMetadata]:
        """
        List uploaded files.

        Files paginate by id cursor rather than by opaque page token. Send one
        direction only: auto-iteration follows `last_id` for an `after_id` query and
        `first_id` for a `before_id` query, and mixing both in one request has no
        coherent meaning.

        Args:
          limit: Maximum number of files to return per page.

          after_id: Return files after this id. Never combine with `before_id`.

          before_id: Return files before this id. Never combine with `after_id`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/files",
            page=SyncPage[FileMetadata],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "after_id": after_id, "before_id": before_id},
                    file_list_params.FileListParams,
                ),
            ),
            # Union types cannot be passed in as arguments in the type system.
            model=cast(Any, FileMetadata),
        )

    def delete(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedFile:
        """
        Permanently delete a stored file and return its tombstone.

        There is no archive for files: this is irreversible, and sessions still
        referencing the file lose access to its bytes.

        Args:
          file_id: The file to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._delete(
            path_template("/v1/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedFile,
        )


class AsyncFiles(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesWithRawResponse:
        return AsyncFilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesWithStreamingResponse:
        return AsyncFilesWithStreamingResponse(self)

    async def upload(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> FileMetadata:
        """
        Upload a file as `multipart/form-data`.

        `file` is the only part the contract accepts. The server records the MIME type
        the part declares, so pass a `(filename, content, content_type)` tuple when
        the content type matters and you cannot rely on it being inferred.

        Args:
          file: The file bytes to upload.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, paths=[["file"]])
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # The Content-Type actually sent carries a `boundary` parameter that httpx
        # fills in, e.g. `multipart/form-data; boundary=---abc--`.
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return cast(
            FileMetadata,
            await self._post(
                "/v1/files",
                body=await async_maybe_transform(body, file_upload_params.FileUploadParams),
                files=extracted_files,
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                # Union types cannot be passed in as arguments in the type system.
                cast_to=cast(Any, FileMetadata),
            ),
        )

    async def retrieve(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> FileMetadata:
        """
        Retrieve metadata for a stored file.

        This returns metadata only; the bytes come from `download`.

        Args:
          file_id: The file to describe.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return cast(
            FileMetadata,
            await self._get(
                path_template("/v1/files/{file_id}", file_id=file_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                # Union types cannot be passed in as arguments in the type system.
                cast_to=cast(Any, FileMetadata),
            ),
        )

    async def download(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> httpx2.Response:
        """
        Download the raw contents of a stored file.

        The endpoint serves `application/octet-stream`, so this returns the underlying
        HTTP response rather than a parsed model: read `.content`, `.text`, or stream
        it yourself. A file whose metadata reports `downloadable` as false is refused
        here by the server.

        Args:
          file_id: The file to download.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        extra_headers = {"Accept": "application/octet-stream", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/files/{file_id}/content", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx2.Response,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[FileMetadata, AsyncPage[FileMetadata]]:
        """
        List uploaded files.

        Files paginate by id cursor rather than by opaque page token. Send one
        direction only: auto-iteration follows `last_id` for an `after_id` query and
        `first_id` for a `before_id` query, and mixing both in one request has no
        coherent meaning.

        Args:
          limit: Maximum number of files to return per page.

          after_id: Return files after this id. Never combine with `before_id`.

          before_id: Return files before this id. Never combine with `after_id`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/files",
            page=AsyncPage[FileMetadata],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"limit": limit, "after_id": after_id, "before_id": before_id},
                    file_list_params.FileListParams,
                ),
            ),
            # Union types cannot be passed in as arguments in the type system.
            model=cast(Any, FileMetadata),
        )

    async def delete(
        self,
        file_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedFile:
        """
        Permanently delete a stored file and return its tombstone.

        There is no archive for files: this is irreversible, and sessions still
        referencing the file lose access to its bytes.

        Args:
          file_id: The file to delete.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._delete(
            path_template("/v1/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeletedFile,
        )


class FilesWithRawResponse:
    def __init__(self, files: Files) -> None:
        self._files = files

        self.upload = to_raw_response_wrapper(files.upload)
        self.retrieve = to_raw_response_wrapper(files.retrieve)
        self.download = to_raw_response_wrapper(files.download)
        self.list = to_raw_response_wrapper(files.list)
        self.delete = to_raw_response_wrapper(files.delete)


class AsyncFilesWithRawResponse:
    def __init__(self, files: AsyncFiles) -> None:
        self._files = files

        self.upload = async_to_raw_response_wrapper(files.upload)
        self.retrieve = async_to_raw_response_wrapper(files.retrieve)
        self.download = async_to_raw_response_wrapper(files.download)
        self.list = async_to_raw_response_wrapper(files.list)
        self.delete = async_to_raw_response_wrapper(files.delete)


class FilesWithStreamingResponse:
    def __init__(self, files: Files) -> None:
        self._files = files

        self.upload = to_streamed_response_wrapper(files.upload)
        self.retrieve = to_streamed_response_wrapper(files.retrieve)
        self.download = to_streamed_response_wrapper(files.download)
        self.list = to_streamed_response_wrapper(files.list)
        self.delete = to_streamed_response_wrapper(files.delete)


class AsyncFilesWithStreamingResponse:
    def __init__(self, files: AsyncFiles) -> None:
        self._files = files

        self.upload = async_to_streamed_response_wrapper(files.upload)
        self.retrieve = async_to_streamed_response_wrapper(files.retrieve)
        self.download = async_to_streamed_response_wrapper(files.download)
        self.list = async_to_streamed_response_wrapper(files.list)
        self.delete = async_to_streamed_response_wrapper(files.delete)
