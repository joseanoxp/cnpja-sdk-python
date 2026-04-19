"""Resource público para consulta de estabelecimentos (CNPJ)."""

from __future__ import annotations

from typing import Any

from ..types.office import OfficeDto, OfficeReadParams
from ._base import AsyncBaseResource, BaseResource


class OpenOfficeResource(BaseResource):
    """Operações públicas de estabelecimentos/CNPJ (síncrono)."""

    def read(
        self,
        params: OfficeReadParams | dict[str, Any],
    ) -> OfficeDto:
        """Consulta informações públicas de um CNPJ."""
        if isinstance(params, dict):
            params = OfficeReadParams.model_validate(params)

        result = self._http.get(
            "/office/:taxId",
            replacements={"taxId": params.tax_id},
            response_model=OfficeDto,
        )
        return result


class AsyncOpenOfficeResource(AsyncBaseResource):
    """Operações públicas de estabelecimentos/CNPJ (assíncrono)."""

    async def read(
        self,
        params: OfficeReadParams | dict[str, Any],
    ) -> OfficeDto:
        """Consulta informações públicas de um CNPJ."""
        if isinstance(params, dict):
            params = OfficeReadParams.model_validate(params)

        result = await self._http.aget(
            "/office/:taxId",
            replacements={"taxId": params.tax_id},
            response_model=OfficeDto,
        )
        return result
