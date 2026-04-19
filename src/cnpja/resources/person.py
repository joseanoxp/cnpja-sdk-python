"""Resource para operações de pessoas/sócios."""

from __future__ import annotations

from typing import Any

from ..pagers import AsyncPager, Pager
from ..types.person import PersonDto, PersonSearchParams
from ._base import AsyncBaseResource, BaseResource


class PersonResource(BaseResource):
    """Operações de pessoas/sócios (síncrono)."""

    def read(self, person_id: str) -> PersonDto:
        """Consulta informações de uma pessoa.

        Args:
            person_id: Código da pessoa (UUID).

        Returns:
            Informações da pessoa.

        Example:
            ```python
            person = client.person.read("1e5ed433-0f39-4309-8e85-8d21a571b212")
            print(f"Nome: {person.name}")
            ```
        """
        result = self._http.get(
            "/person/:personId",
            replacements={"personId": person_id},
            response_model=PersonDto,
        )
        return result

    def search(
        self,
        params: PersonSearchParams | dict[str, Any] | None = None,
    ) -> Pager[PersonDto]:
        """Pesquisa pessoas/sócios com filtros.

        Args:
            params: Parâmetros de pesquisa e filtros.

        Returns:
            Paginador para iterar sobre os resultados.

        Example:
            ```python
            for person in client.person.search({"name.in": ["João"]}):
                print(f"{person.name}: {len(person.membership)} empresas")
            ```
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = PersonSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return Pager(
            http_client=self._http,
            path="/person",
            params=query,
            response_model=PersonDto,
        )


class AsyncPersonResource(AsyncBaseResource):
    """Operações de pessoas/sócios (assíncrono)."""

    async def read(self, person_id: str) -> PersonDto:
        """Consulta informações de uma pessoa.

        Args:
            person_id: Código da pessoa (UUID).

        Returns:
            Informações da pessoa.
        """
        result = await self._http.aget(
            "/person/:personId",
            replacements={"personId": person_id},
            response_model=PersonDto,
        )
        return result

    def search(
        self,
        params: PersonSearchParams | dict[str, Any] | None = None,
    ) -> AsyncPager[PersonDto]:
        """Pesquisa pessoas/sócios com filtros.

        Args:
            params: Parâmetros de pesquisa e filtros.

        Returns:
            Paginador assíncrono para iterar sobre os resultados.
        """
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = PersonSearchParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude_none=True)

        return AsyncPager(
            http_client=self._http,
            path="/person",
            params=query,
            response_model=PersonDto,
        )
