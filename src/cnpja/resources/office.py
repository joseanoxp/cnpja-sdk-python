"""Resource para operações de estabelecimentos (CNPJ)."""

from __future__ import annotations

from typing import Any

from ..pagers import AsyncPager, Pager
from ..types.office import (
    OfficeDto,
    OfficeMapParams,
    OfficePageRecordDto,
    OfficeReadParams,
    OfficeSearchParams,
    OfficeStreetParams,
)
from ._base import AsyncBaseResource, BaseResource


class OfficeResource(BaseResource):
    """Operações de estabelecimentos/CNPJ (síncrono)."""

    def read(
        self,
        params: OfficeReadParams | dict[str, Any],
    ) -> OfficeDto:
        """Consulta informações de um CNPJ.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações do estabelecimento.

        Example:
            ```python
            office = client.office.read({"tax_id": "37335118000180"})
            print(f"Empresa: {office.company.name}")
            ```
        """
        if isinstance(params, dict):
            params = OfficeReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get(
            "/office/:taxId",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
            response_model=OfficeDto,
        )
        return result

    def search(
        self,
        params: OfficeSearchParams | dict[str, Any] | None = None,
    ) -> Pager[OfficePageRecordDto]:
        """Pesquisa estabelecimentos com filtros.

        Args:
            params: Parâmetros de pesquisa e filtros.

        Returns:
            Paginador para iterar sobre os resultados.

        Example:
            ```python
            for office in client.office.search({"address.state.in": ["SP"]}):
                print(f"{office.tax_id}: {office.company.name}")
            ```
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = OfficeSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return Pager(
            http_client=self._http,
            path="/office",
            params=query,
            response_model=OfficePageRecordDto,
        )

    def map(
        self,
        params: OfficeMapParams | dict[str, Any],
    ) -> bytes:
        """Gera imagem de mapa aéreo do endereço.

        Args:
            params: Parâmetros da imagem (tax_id obrigatório).

        Returns:
            Bytes da imagem PNG.

        Example:
            ```python
            image = client.office.map({"tax_id": "37335118000180"})
            with open("mapa.png", "wb") as f:
                f.write(image)
            ```
        """
        if isinstance(params, dict):
            params = OfficeMapParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/office/:taxId/map",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
        )
        return result

    def street(
        self,
        params: OfficeStreetParams | dict[str, Any],
    ) -> bytes:
        """Gera imagem de visão de rua do endereço.

        Args:
            params: Parâmetros da imagem (tax_id obrigatório).

        Returns:
            Bytes da imagem PNG.

        Example:
            ```python
            image = client.office.street({"tax_id": "37335118000180"})
            with open("rua.png", "wb") as f:
                f.write(image)
            ```
        """
        if isinstance(params, dict):
            params = OfficeStreetParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/office/:taxId/street",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
        )
        return result


class AsyncOfficeResource(AsyncBaseResource):
    """Operações de estabelecimentos/CNPJ (assíncrono)."""

    async def read(
        self,
        params: OfficeReadParams | dict[str, Any],
    ) -> OfficeDto:
        """Consulta informações de um CNPJ.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações do estabelecimento.
        """
        if isinstance(params, dict):
            params = OfficeReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget(
            "/office/:taxId",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
            response_model=OfficeDto,
        )
        return result

    def search(
        self,
        params: OfficeSearchParams | dict[str, Any] | None = None,
    ) -> AsyncPager[OfficePageRecordDto]:
        """Pesquisa estabelecimentos com filtros.

        Args:
            params: Parâmetros de pesquisa e filtros.

        Returns:
            Paginador assíncrono para iterar sobre os resultados.
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = OfficeSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return AsyncPager(
            http_client=self._http,
            path="/office",
            params=query,
            response_model=OfficePageRecordDto,
        )

    async def map(
        self,
        params: OfficeMapParams | dict[str, Any],
    ) -> bytes:
        """Gera imagem de mapa aéreo do endereço."""
        if isinstance(params, dict):
            params = OfficeMapParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/office/:taxId/map",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
        )
        return result

    async def street(
        self,
        params: OfficeStreetParams | dict[str, Any],
    ) -> bytes:
        """Gera imagem de visão de rua do endereço."""
        if isinstance(params, dict):
            params = OfficeStreetParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/office/:taxId/street",
            replacements={"taxId": params.tax_id},
            params=query if query else None,
        )
        return result
