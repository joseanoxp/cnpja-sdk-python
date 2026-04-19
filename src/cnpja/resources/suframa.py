"""Resource para operações SUFRAMA."""

from __future__ import annotations

from typing import Any

from ..types.suframa import SuframaCertificateParams, SuframaDto, SuframaReadParams
from ._base import AsyncBaseResource, BaseResource


class SuframaResource(BaseResource):
    """Operações SUFRAMA (síncrono)."""

    def read(
        self,
        params: SuframaReadParams | dict[str, Any],
    ) -> SuframaDto:
        """Consulta informações SUFRAMA.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações SUFRAMA.

        Example:
            ```python
            suframa = client.suframa.read({"tax_id": "37335118000180"})
            print(f"Inscrição: {suframa.number}")
            ```
        """
        if isinstance(params, dict):
            params = SuframaReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get(
            "/suframa",
            params={"taxId": params.tax_id, **query},
            response_model=SuframaDto,
        )
        return result

    def certificate(
        self,
        params: SuframaCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante SUFRAMA (PDF).

        Args:
            params: Parâmetros da emissão (tax_id obrigatório).

        Returns:
            Bytes do arquivo PDF.

        Example:
            ```python
            pdf = client.suframa.certificate({"tax_id": "37335118000180"})
            with open("suframa.pdf", "wb") as f:
                f.write(pdf)
            ```
        """
        if isinstance(params, dict):
            params = SuframaCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/suframa/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result


class AsyncSuframaResource(AsyncBaseResource):
    """Operações SUFRAMA (assíncrono)."""

    async def read(
        self,
        params: SuframaReadParams | dict[str, Any],
    ) -> SuframaDto:
        """Consulta informações SUFRAMA."""
        if isinstance(params, dict):
            params = SuframaReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget(
            "/suframa",
            params={"taxId": params.tax_id, **query},
            response_model=SuframaDto,
        )
        return result

    async def certificate(
        self,
        params: SuframaCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante SUFRAMA (PDF)."""
        if isinstance(params, dict):
            params = SuframaCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/suframa/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result
