"""Cliente público do SDK CNPJá (sem autenticação)."""

from __future__ import annotations

from functools import cached_property
from typing import Any, Callable

from ._http_client import HttpClient
from .resources import (
    AsyncOpenOfficeResource,
    AsyncZipResource,
    OpenOfficeResource,
    ZipResource,
)


class AsyncCnpjaOpen:
    """Cliente assíncrono para a API pública CNPJá (sem autenticação).

    Acesse via :attr:`CnpjaOpen.aio`.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client

    @cached_property
    def office(self) -> AsyncOpenOfficeResource:
        """Operações de estabelecimentos (CNPJ) — apenas leitura."""
        return AsyncOpenOfficeResource(self._http)

    @cached_property
    def zip(self) -> AsyncZipResource:
        """Operações de CEP."""
        return AsyncZipResource(self._http)

    async def aclose(self) -> None:
        """Fecha o cliente assíncrono."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncCnpjaOpen:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()


class CnpjaOpen:
    """Cliente para a API pública CNPJá (sem autenticação).

    Apenas ``office.read()`` e ``zip.read()`` estão disponíveis (limites de 5
    requisições por minuto por IP).

    Example:
        ```python
        from cnpja import CnpjaOpen

        with CnpjaOpen() as client:
            zip_info = client.zip.read("01452922")
            print(zip_info.city)
        ```
    """

    def __init__(
        self,
        *,
        base_url: str = "https://open.cnpja.com",
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        retry_limit: int = 3,
        retry_delay: Callable[[int], float] | None = None,
    ) -> None:
        self._http = HttpClient(
            api_key=None,
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            retry_limit=retry_limit,
            retry_delay=retry_delay,
        )

    @cached_property
    def aio(self) -> AsyncCnpjaOpen:
        """Acesso ao cliente assíncrono, compartilhando o mesmo transport."""
        return AsyncCnpjaOpen(self._http)

    @cached_property
    def office(self) -> OpenOfficeResource:
        """Operações de estabelecimentos (CNPJ) — apenas leitura."""
        return OpenOfficeResource(self._http)

    @cached_property
    def zip(self) -> ZipResource:
        """Operações de CEP."""
        return ZipResource(self._http)

    def close(self) -> None:
        """Fecha o cliente e libera recursos."""
        self._http.close()

    def __enter__(self) -> CnpjaOpen:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
