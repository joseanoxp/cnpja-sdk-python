"""Resource para operações do Simples Nacional."""

from __future__ import annotations

from typing import Any

from ..types.simples import SimplesCertificateParams, SimplesDto, SimplesReadParams
from ._base import AsyncBaseResource, BaseResource


class SimplesResource(BaseResource):
    """Operações do Simples Nacional (síncrono)."""

    def read(
        self,
        params: SimplesReadParams | dict[str, Any],
    ) -> SimplesDto:
        """Consulta informações do Simples Nacional e MEI.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações do Simples Nacional.

        Example:
            ```python
            simples = client.simples.read({"tax_id": "37335118000180"})
            print(f"Optante: {simples.simples.optant}")
            ```
        """
        if isinstance(params, dict):
            params = SimplesReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get(
            "/simples",
            params={"taxId": params.tax_id, **query},
            response_model=SimplesDto,
        )
        return result

    def certificate(
        self,
        params: SimplesCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante do Simples Nacional (PDF).

        Args:
            params: Parâmetros da emissão (tax_id obrigatório).

        Returns:
            Bytes do arquivo PDF.

        Example:
            ```python
            pdf = client.simples.certificate({"tax_id": "37335118000180"})
            with open("simples.pdf", "wb") as f:
                f.write(pdf)
            ```
        """
        if isinstance(params, dict):
            params = SimplesCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/simples/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result


class AsyncSimplesResource(AsyncBaseResource):
    """Operações do Simples Nacional (assíncrono)."""

    async def read(
        self,
        params: SimplesReadParams | dict[str, Any],
    ) -> SimplesDto:
        """Consulta informações do Simples Nacional e MEI."""
        if isinstance(params, dict):
            params = SimplesReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget(
            "/simples",
            params={"taxId": params.tax_id, **query},
            response_model=SimplesDto,
        )
        return result

    async def certificate(
        self,
        params: SimplesCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante do Simples Nacional (PDF)."""
        if isinstance(params, dict):
            params = SimplesCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/simples/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result
