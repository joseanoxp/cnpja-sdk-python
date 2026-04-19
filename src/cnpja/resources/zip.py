"""Resource para consulta de CEP."""

from __future__ import annotations

from ..types.zip import ZipDto
from ._base import AsyncBaseResource, BaseResource


class ZipResource(BaseResource):
    """Operações de CEP (síncrono)."""

    def read(self, code: str) -> ZipDto:
        """Consulta informações de um CEP.

        Args:
            code: Código do CEP (8 dígitos).

        Returns:
            Informações do CEP.

        Example:
            ```python
            zip_info = client.zip.read("01452922")
            print(f"Cidade: {zip_info.city}")
            ```
        """
        result = self._http.get(
            "/zip/:code",
            replacements={"code": code},
            response_model=ZipDto,
        )
        return result


class AsyncZipResource(AsyncBaseResource):
    """Operações de CEP (assíncrono)."""

    async def read(self, code: str) -> ZipDto:
        """Consulta informações de um CEP.

        Args:
            code: Código do CEP (8 dígitos).

        Returns:
            Informações do CEP.

        Example:
            ```python
            zip_info = await client.aio.zip.read("01452922")
            print(f"Cidade: {zip_info.city}")
            ```
        """
        result = await self._http.aget(
            "/zip/:code",
            replacements={"code": code},
            response_model=ZipDto,
        )
        return result
