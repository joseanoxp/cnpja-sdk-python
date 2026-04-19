"""Resource para operações de listas de CNPJs."""

from __future__ import annotations

from typing import Any

from ..pagers import AsyncPager, Pager
from ..types.list import (
    ListCreateParams,
    ListDto,
    ListExportCreateParams,
    ListExportDto,
    ListExportIdDto,
    ListExportSearchParams,
    ListSearchParams,
    ListSummaryDto,
    ListUpdateParams,
)
from ._base import AsyncBaseResource, BaseResource


class ListResource(BaseResource):
    """Operações de listas de CNPJs (síncrono)."""

    def create(
        self,
        params: ListCreateParams | dict[str, Any],
    ) -> ListDto:
        """Cria uma nova lista de CNPJs.

        Args:
            params: Parâmetros da lista (title obrigatório).

        Returns:
            Informações da lista criada.

        Example:
            ```python
            lista = client.list.create({
                "title": "Minha Lista",
                "items": ["37335118000180"]
            })
            print(f"ID: {lista.id}")
            ```
        """
        if isinstance(params, dict):
            params = ListCreateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = self._http.post("/list", json=body, response_model=ListDto)
        return result

    def search(
        self,
        params: ListSearchParams | dict[str, Any] | None = None,
    ) -> Pager[ListSummaryDto]:
        """Pesquisa listas de CNPJs.

        Args:
            params: Parâmetros de pesquisa.

        Returns:
            Paginador para iterar sobre os resultados.

        Example:
            ```python
            for lista in client.list.search():
                print(f"{lista.title}: {lista.size} CNPJs")
            ```
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = ListSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return Pager(
            http_client=self._http,
            path="/list",
            params=query,
            response_model=ListSummaryDto,
        )

    def read(self, list_id: str) -> ListDto:
        """Consulta informações de uma lista.

        Args:
            list_id: Identificador da lista (UUID).

        Returns:
            Informações da lista.

        Example:
            ```python
            lista = client.list.read("37505509-b2a5-42c2-94f4-aa99d2033bf5")
            print(f"Total: {lista.size}")
            ```
        """
        result = self._http.get(
            "/list/:listId",
            replacements={"listId": list_id},
            response_model=ListDto,
        )
        return result

    def update(
        self,
        list_id: str,
        params: ListUpdateParams | dict[str, Any],
    ) -> ListDto:
        """Atualiza uma lista de CNPJs.

        Args:
            list_id: Identificador da lista (UUID).
            params: Parâmetros de atualização.

        Returns:
            Informações da lista atualizada.

        Example:
            ```python
            lista = client.list.update(
                "37505509-b2a5-42c2-94f4-aa99d2033bf5",
                {"title": "Novo Título"}
            )
            ```
        """
        if isinstance(params, dict):
            params = ListUpdateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = self._http.patch(
            "/list/:listId",
            replacements={"listId": list_id},
            json=body,
            response_model=ListDto,
        )
        return result

    def delete(self, list_id: str) -> None:
        """Remove uma lista de CNPJs.

        Args:
            list_id: Identificador da lista (UUID).

        Example:
            ```python
            client.list.delete("37505509-b2a5-42c2-94f4-aa99d2033bf5")
            ```
        """
        self._http.delete("/list/:listId", replacements={"listId": list_id})

    def create_export(
        self,
        list_id: str,
        params: ListExportCreateParams | dict[str, Any] | None = None,
    ) -> ListExportIdDto:
        """Cria uma exportação da lista.

        Args:
            list_id: Identificador da lista (UUID).
            params: Parâmetros da exportação.

        Returns:
            Identificador da exportação.

        Example:
            ```python
            export = client.list.create_export(
                "37505509-b2a5-42c2-94f4-aa99d2033bf5",
                {"options": {"simples": True, "registrations": ["ORIGIN"]}},
            )
            print(f"Export ID: {export.id}")
            ```
        """
        if params is None:
            params = ListExportCreateParams()
        if isinstance(params, dict):
            params = ListExportCreateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = self._http.post(
            "/list/:listId/export",
            replacements={"listId": list_id},
            json=body,
            response_model=ListExportIdDto,
        )
        return result

    def search_export(
        self,
        list_id: str,
        params: ListExportSearchParams | dict[str, Any] | None = None,
    ) -> Pager[ListExportDto]:
        """Pesquisa exportações de uma lista.

        Args:
            list_id: Identificador da lista (UUID).
            params: Parâmetros de pesquisa.

        Returns:
            Paginador para iterar sobre os resultados.
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = ListExportSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return Pager(
            http_client=self._http,
            path=f"/list/{list_id}/export",
            params=query,
            response_model=ListExportDto,
        )

    def read_export(self, list_id: str, export_id: str) -> ListExportDto:
        """Consulta informações de uma exportação.

        Args:
            list_id: Identificador da lista (UUID).
            export_id: Identificador da exportação (UUID).

        Returns:
            Informações da exportação.

        Example:
            ```python
            export = client.list.read_export(
                "37505509-b2a5-42c2-94f4-aa99d2033bf5",
                "abc123",
            )
            if export.links:
                print(f"Download: {export.links[0].url}")
            ```
        """
        result = self._http.post(
            "/list/:listId/export/:exportId",
            replacements={"listId": list_id, "exportId": export_id},
            response_model=ListExportDto,
        )
        return result


class AsyncListResource(AsyncBaseResource):
    """Operações de listas de CNPJs (assíncrono)."""

    async def create(
        self,
        params: ListCreateParams | dict[str, Any],
    ) -> ListDto:
        """Cria uma nova lista de CNPJs."""
        if isinstance(params, dict):
            params = ListCreateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.apost("/list", json=body, response_model=ListDto)
        return result

    def search(
        self,
        params: ListSearchParams | dict[str, Any] | None = None,
    ) -> AsyncPager[ListSummaryDto]:
        """Pesquisa listas de CNPJs."""
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = ListSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return AsyncPager(
            http_client=self._http,
            path="/list",
            params=query,
            response_model=ListSummaryDto,
        )

    async def read(self, list_id: str) -> ListDto:
        """Consulta informações de uma lista."""
        result = await self._http.aget(
            "/list/:listId",
            replacements={"listId": list_id},
            response_model=ListDto,
        )
        return result

    async def update(
        self,
        list_id: str,
        params: ListUpdateParams | dict[str, Any],
    ) -> ListDto:
        """Atualiza uma lista de CNPJs."""
        if isinstance(params, dict):
            params = ListUpdateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.apatch(
            "/list/:listId",
            replacements={"listId": list_id},
            json=body,
            response_model=ListDto,
        )
        return result

    async def delete(self, list_id: str) -> None:
        """Remove uma lista de CNPJs."""
        await self._http.adelete("/list/:listId", replacements={"listId": list_id})

    async def create_export(
        self,
        list_id: str,
        params: ListExportCreateParams | dict[str, Any] | None = None,
    ) -> ListExportIdDto:
        """Cria uma exportação da lista."""
        if params is None:
            params = ListExportCreateParams()
        if isinstance(params, dict):
            params = ListExportCreateParams.model_validate(params)

        body = params.model_dump(by_alias=True, exclude_none=True)

        result = await self._http.apost(
            "/list/:listId/export",
            replacements={"listId": list_id},
            json=body,
            response_model=ListExportIdDto,
        )
        return result

    def search_export(
        self,
        list_id: str,
        params: ListExportSearchParams | dict[str, Any] | None = None,
    ) -> AsyncPager[ListExportDto]:
        """Pesquisa exportações de uma lista."""
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = ListExportSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return AsyncPager(
            http_client=self._http,
            path=f"/list/{list_id}/export",
            params=query,
            response_model=ListExportDto,
        )

    async def read_export(self, list_id: str, export_id: str) -> ListExportDto:
        """Consulta informações de uma exportação."""
        result = await self._http.apost(
            "/list/:listId/export/:exportId",
            replacements={"listId": list_id, "exportId": export_id},
            response_model=ListExportDto,
        )
        return result
