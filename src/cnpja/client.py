"""Cliente principal do SDK CNPJá."""

from __future__ import annotations

from functools import cached_property
from typing import Any, Callable

from ._http_client import HttpClient
from .resources import (
    AsyncCccResource,
    AsyncCompanyResource,
    AsyncCreditResource,
    AsyncListResource,
    AsyncOfficeResource,
    AsyncPersonResource,
    AsyncRfbResource,
    AsyncSimplesResource,
    AsyncSuframaResource,
    AsyncZipResource,
    CccResource,
    CompanyResource,
    CreditResource,
    ListResource,
    OfficeResource,
    PersonResource,
    RfbResource,
    SimplesResource,
    SuframaResource,
    ZipResource,
)


class AsyncClient:
    """Cliente assíncrono para a API CNPJá.

    Acesse via :attr:`Client.aio`.

    Example:
        ```python
        async with client.aio as async_client:
            office = await async_client.office.read({"tax_id": "37335118000180"})
        ```
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client

    @cached_property
    def office(self) -> AsyncOfficeResource:
        """Operações de estabelecimentos (CNPJ)."""
        return AsyncOfficeResource(self._http)

    @cached_property
    def company(self) -> AsyncCompanyResource:
        """Operações de empresas."""
        return AsyncCompanyResource(self._http)

    @cached_property
    def person(self) -> AsyncPersonResource:
        """Operações de pessoas/sócios."""
        return AsyncPersonResource(self._http)

    @cached_property
    def rfb(self) -> AsyncRfbResource:
        """Operações da Receita Federal."""
        return AsyncRfbResource(self._http)

    @cached_property
    def simples(self) -> AsyncSimplesResource:
        """Operações do Simples Nacional."""
        return AsyncSimplesResource(self._http)

    @cached_property
    def ccc(self) -> AsyncCccResource:
        """Operações do Cadastro de Contribuintes."""
        return AsyncCccResource(self._http)

    @cached_property
    def suframa(self) -> AsyncSuframaResource:
        """Operações SUFRAMA."""
        return AsyncSuframaResource(self._http)

    @cached_property
    def zip(self) -> AsyncZipResource:
        """Operações de CEP."""
        return AsyncZipResource(self._http)

    @cached_property
    def list(self) -> AsyncListResource:
        """Operações de listas de CNPJs."""
        return AsyncListResource(self._http)

    @cached_property
    def credit(self) -> AsyncCreditResource:
        """Operações de créditos."""
        return AsyncCreditResource(self._http)

    async def aclose(self) -> None:
        """Fecha o cliente assíncrono."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()


class Client:
    """Cliente principal para a API CNPJá (requer autenticação).

    Example:
        ```python
        from cnpja import Client

        with Client(api_key="sua-api-key") as client:
            office = client.office.read({"tax_id": "37335118000180"})
            print(office.company.name)
        ```
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.cnpja.com",
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        retry_limit: int = 3,
        retry_delay: Callable[[int], float] | None = None,
    ) -> None:
        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            retry_limit=retry_limit,
            retry_delay=retry_delay,
        )

    @cached_property
    def aio(self) -> AsyncClient:
        """Acesso ao cliente assíncrono, compartilhando o mesmo transport."""
        return AsyncClient(self._http)

    @cached_property
    def office(self) -> OfficeResource:
        """Operações de estabelecimentos (CNPJ)."""
        return OfficeResource(self._http)

    @cached_property
    def company(self) -> CompanyResource:
        """Operações de empresas."""
        return CompanyResource(self._http)

    @cached_property
    def person(self) -> PersonResource:
        """Operações de pessoas/sócios."""
        return PersonResource(self._http)

    @cached_property
    def rfb(self) -> RfbResource:
        """Operações da Receita Federal."""
        return RfbResource(self._http)

    @cached_property
    def simples(self) -> SimplesResource:
        """Operações do Simples Nacional."""
        return SimplesResource(self._http)

    @cached_property
    def ccc(self) -> CccResource:
        """Operações do Cadastro de Contribuintes."""
        return CccResource(self._http)

    @cached_property
    def suframa(self) -> SuframaResource:
        """Operações SUFRAMA."""
        return SuframaResource(self._http)

    @cached_property
    def zip(self) -> ZipResource:
        """Operações de CEP."""
        return ZipResource(self._http)

    @cached_property
    def list(self) -> ListResource:
        """Operações de listas de CNPJs."""
        return ListResource(self._http)

    @cached_property
    def credit(self) -> CreditResource:
        """Operações de créditos."""
        return CreditResource(self._http)

    def close(self) -> None:
        """Fecha o cliente e libera recursos."""
        self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
