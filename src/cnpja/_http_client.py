"""Cliente HTTP interno com retry e suporte sync+async."""

from __future__ import annotations

import logging
import re
from typing import Any, Callable, TypeVar, cast, overload

import httpx
import pydantic
import tenacity
from tenacity.wait import wait_base

from .errors import APIError
from .version import __version__

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=pydantic.BaseModel)

DEFAULT_RETRY_LIMIT = 3
DEFAULT_RETRY_INITIAL_DELAY = 1.0
DEFAULT_RETRY_MAX_DELAY = 30.0
DEFAULT_RETRY_EXP_BASE = 2.0
DEFAULT_RETRY_JITTER = 0.5
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def _should_retry(exception: BaseException) -> bool:
    if isinstance(exception, APIError):
        return exception.code in RETRYABLE_STATUS_CODES
    if isinstance(exception, httpx.TransportError):
        return True
    return False


class _CallbackWait(wait_base):
    """Estratégia de espera que delega o cálculo do atraso a um callback.

    O callback recebe o número da tentativa atual (1-indexed) e retorna
    o atraso em segundos antes da próxima tentativa.
    """

    def __init__(self, fn: Callable[[int], float]) -> None:
        self._fn = fn

    def __call__(self, retry_state: tenacity.RetryCallState) -> float:
        return self._fn(retry_state.attempt_number)


def _create_retry_decorator(
    retry_limit: int,
    retry_delay: Callable[[int], float] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    if retry_limit <= 0:
        return lambda fn: fn

    wait: wait_base
    if retry_delay is not None:
        wait = _CallbackWait(retry_delay)
    else:
        wait = tenacity.wait_exponential_jitter(
            initial=DEFAULT_RETRY_INITIAL_DELAY,
            max=DEFAULT_RETRY_MAX_DELAY,
            exp_base=DEFAULT_RETRY_EXP_BASE,
            jitter=DEFAULT_RETRY_JITTER,
        )

    return tenacity.retry(
        stop=tenacity.stop_after_attempt(retry_limit + 1),
        wait=wait,
        retry=tenacity.retry_if_exception(_should_retry),
        reraise=True,
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
    )


class HttpClient:
    """Cliente HTTP interno para a API CNPJá (sync + async com retry automático)."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = "https://api.cnpja.com",
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        retry_limit: int = DEFAULT_RETRY_LIMIT,
        retry_delay: Callable[[int], float] | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._retry_limit = retry_limit
        self._retry_delay = retry_delay

        self._headers = {
            "User-Agent": f"cnpja-python/{__version__}",
            "Accept": "application/json",
        }
        if api_key:
            self._headers["Authorization"] = api_key
        if headers:
            self._headers.update(headers)

        self._sync_client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    @property
    def sync_client(self) -> httpx.Client:
        if self._sync_client is None:
            self._sync_client = httpx.Client(
                base_url=self._base_url,
                headers=self._headers,
                timeout=self._timeout,
                follow_redirects=True,
            )
        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                headers=self._headers,
                timeout=self._timeout,
                follow_redirects=True,
            )
        return self._async_client

    def _build_url(self, path: str, replacements: dict[str, str] | None = None) -> str:
        url = path.lstrip("/")
        if replacements:
            for key, value in replacements.items():
                url = re.sub(rf":{key}\b", str(value), url)
        return url

    @overload
    def _process_response(
        self,
        response: httpx.Response,
        response_model: type[T],
    ) -> T: ...
    @overload
    def _process_response(
        self,
        response: httpx.Response,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    def _process_response(
        self,
        response: httpx.Response,
        response_model: type[T] | None = None,
    ) -> Any:
        APIError.raise_for_response(response)

        if "application/json" not in response.headers.get("content-type", ""):
            return response.content

        data = response.json()
        if response_model is not None:
            return response_model.model_validate(data)
        return data

    @overload
    def get(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    def get(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    def get(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """GET síncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        def _request() -> Any:
            url = self._build_url(path, replacements)
            response = self.sync_client.get(url, params=params)
            return self._process_response(response, response_model)

        return _request()

    @overload
    def post(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    def post(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    def post(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """POST síncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        def _request() -> Any:
            url = self._build_url(path, replacements)
            response = self.sync_client.post(url, params=params, json=json)
            return self._process_response(response, response_model)

        return _request()

    @overload
    def patch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    def patch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    def patch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """PATCH síncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        def _request() -> Any:
            url = self._build_url(path, replacements)
            response = self.sync_client.patch(url, params=params, json=json)
            return self._process_response(response, response_model)

        return _request()

    def delete(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """DELETE síncrono."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        def _request() -> None:
            url = self._build_url(path, replacements)
            response = self.sync_client.delete(url, params=params)
            APIError.raise_for_response(response)

        _request()

    def get_binary(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """GET síncrono para endpoints binários (PDF, imagens)."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        def _request() -> bytes:
            url = self._build_url(path, replacements)
            response = self.sync_client.get(url, params=params)
            APIError.raise_for_response(response)
            return response.content

        return cast(bytes, _request())

    @overload
    async def aget(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    async def aget(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    async def aget(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """GET assíncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        async def _request() -> Any:
            url = self._build_url(path, replacements)
            response = await self.async_client.get(url, params=params)
            return self._process_response(response, response_model)

        return await _request()

    @overload
    async def apost(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    async def apost(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    async def apost(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """POST assíncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        async def _request() -> Any:
            url = self._build_url(path, replacements)
            response = await self.async_client.post(url, params=params, json=json)
            return self._process_response(response, response_model)

        return await _request()

    @overload
    async def apatch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: type[T],
    ) -> T: ...
    @overload
    async def apatch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = ...,
        params: dict[str, Any] | None = ...,
        json: dict[str, Any] | None = ...,
        response_model: None = None,
    ) -> bytes | dict[str, Any]: ...

    async def apatch(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> Any:
        """PATCH assíncrono. Use ``response_model`` para parse automático em Pydantic."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        async def _request() -> Any:
            url = self._build_url(path, replacements)
            response = await self.async_client.patch(url, params=params, json=json)
            return self._process_response(response, response_model)

        return await _request()

    async def adelete(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """DELETE assíncrono."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        async def _request() -> None:
            url = self._build_url(path, replacements)
            response = await self.async_client.delete(url, params=params)
            APIError.raise_for_response(response)

        await _request()

    async def aget_binary(
        self,
        path: str,
        *,
        replacements: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """GET assíncrono para endpoints binários (PDF, imagens)."""

        @_create_retry_decorator(self._retry_limit, self._retry_delay)
        async def _request() -> bytes:
            url = self._build_url(path, replacements)
            response = await self.async_client.get(url, params=params)
            APIError.raise_for_response(response)
            return response.content

        return cast(bytes, await _request())

    def close(self) -> None:
        """Fecha o cliente HTTP síncrono."""
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def aclose(self) -> None:
        """Fecha o cliente HTTP assíncrono."""
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> HttpClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
