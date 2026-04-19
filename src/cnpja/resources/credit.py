"""Resource para consulta de créditos."""

from __future__ import annotations

from ..types.credit import CreditDto
from ._base import AsyncBaseResource, BaseResource


class CreditResource(BaseResource):
    """Operações de créditos (síncrono)."""

    def read(self) -> CreditDto:
        """Consulta saldo de créditos.

        Returns:
            Informações de créditos.

        Example:
            ```python
            credits = client.credit.read()
            print(f"Saldo: {credits.balance}")
            ```
        """
        result = self._http.get("/credit", response_model=CreditDto)
        return result


class AsyncCreditResource(AsyncBaseResource):
    """Operações de créditos (assíncrono)."""

    async def read(self) -> CreditDto:
        """Consulta saldo de créditos.

        Returns:
            Informações de créditos.

        Example:
            ```python
            credits = await client.aio.credit.read()
            print(f"Saldo: {credits.balance}")
            ```
        """
        result = await self._http.aget("/credit", response_model=CreditDto)
        return result
