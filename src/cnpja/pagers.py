"""Paginação sync e async para resultados da API CNPJá."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Generic, Iterator, TypeVar

import pydantic

if TYPE_CHECKING:
    from ._http_client import HttpClient

T = TypeVar("T", bound=pydantic.BaseModel)


class Pager(Generic[T]):
    """Iterador síncrono para resultados paginados.

    Example:
        ```python
        for office in client.office.search({"address.state.in": ["SP"]}):
            print(office.company.name)
        ```
    """

    def __init__(
        self,
        http_client: HttpClient,
        path: str,
        params: dict[str, Any],
        response_model: type[T],
        items_key: str = "records",
        token_key: str = "next",
    ) -> None:
        self._http = http_client
        self._path = path
        self._params = params.copy()
        self._response_model = response_model
        self._items_key = items_key
        self._token_key = token_key

        self._current_page: list[T] = []
        self._current_index = 0
        self._next_token: str | None = None
        self._exhausted = False
        self._initialized = False

    def _fetch_page(self) -> None:
        if self._next_token:
            self._params["token"] = self._next_token

        response = self._http.get(self._path, params=self._params)

        if isinstance(response, dict):
            items_data = response.get(self._items_key, [])
            self._next_token = response.get(self._token_key)
        else:
            items_data = []
            self._next_token = None

        self._current_page = [self._response_model.model_validate(item) for item in items_data]
        self._current_index = 0

        if not self._current_page or not self._next_token:
            self._exhausted = True

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            self._initialized = True
            self._fetch_page()

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        self._ensure_initialized()

        if self._current_index < len(self._current_page):
            item = self._current_page[self._current_index]
            self._current_index += 1
            return item

        if self._exhausted:
            raise StopIteration

        self._fetch_page()

        if not self._current_page:
            raise StopIteration

        item = self._current_page[self._current_index]
        self._current_index += 1
        return item

    @property
    def page(self) -> list[T]:
        """Retorna a página atual, carregando a primeira se ainda não foi."""
        self._ensure_initialized()
        return self._current_page

    def next_page(self) -> list[T]:
        """Avança para a próxima página e retorna os itens (vazio se esgotada)."""
        if self._exhausted:
            return []
        self._fetch_page()
        return self._current_page

    def collect(self, limit: int | None = None) -> list[T]:
        """Coleta todos os itens em uma lista, opcionalmente limitada."""
        items: list[T] = []
        for item in self:
            items.append(item)
            if limit is not None and len(items) >= limit:
                break
        return items


class AsyncPager(Generic[T]):
    """Iterador assíncrono para resultados paginados.

    Example:
        ```python
        async for office in client.aio.office.search({"address.state.in": ["SP"]}):
            print(office.company.name)
        ```
    """

    def __init__(
        self,
        http_client: HttpClient,
        path: str,
        params: dict[str, Any],
        response_model: type[T],
        items_key: str = "records",
        token_key: str = "next",
    ) -> None:
        self._http = http_client
        self._path = path
        self._params = params.copy()
        self._response_model = response_model
        self._items_key = items_key
        self._token_key = token_key

        self._current_page: list[T] = []
        self._current_index = 0
        self._next_token: str | None = None
        self._exhausted = False
        self._initialized = False

    async def _fetch_page(self) -> None:
        if self._next_token:
            self._params["token"] = self._next_token

        response = await self._http.aget(self._path, params=self._params)

        if isinstance(response, dict):
            items_data = response.get(self._items_key, [])
            self._next_token = response.get(self._token_key)
        else:
            items_data = []
            self._next_token = None

        self._current_page = [self._response_model.model_validate(item) for item in items_data]
        self._current_index = 0

        if not self._current_page or not self._next_token:
            self._exhausted = True

    async def _ensure_initialized(self) -> None:
        if not self._initialized:
            self._initialized = True
            await self._fetch_page()

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        await self._ensure_initialized()

        if self._current_index < len(self._current_page):
            item = self._current_page[self._current_index]
            self._current_index += 1
            return item

        if self._exhausted:
            raise StopAsyncIteration

        await self._fetch_page()

        if not self._current_page:
            raise StopAsyncIteration

        item = self._current_page[self._current_index]
        self._current_index += 1
        return item

    async def page(self) -> list[T]:
        """Retorna a página atual, carregando a primeira se ainda não foi."""
        await self._ensure_initialized()
        return self._current_page

    async def next_page(self) -> list[T]:
        """Avança para a próxima página e retorna os itens (vazio se esgotada)."""
        if self._exhausted:
            return []
        await self._fetch_page()
        return self._current_page

    async def collect(self, limit: int | None = None) -> list[T]:
        """Coleta todos os itens em uma lista, opcionalmente limitada."""
        items: list[T] = []
        async for item in self:
            items.append(item)
            if limit is not None and len(items) >= limit:
                break
        return items
