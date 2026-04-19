"""Resource para operações do Cadastro de Contribuintes (CCC)."""

from __future__ import annotations

from typing import Any

from ..types.ccc import CccCertificateParams, CccDto, CccReadParams
from ._base import AsyncBaseResource, BaseResource


class CccResource(BaseResource):
    """Operações do Cadastro de Contribuintes (síncrono)."""

    def read(
        self,
        params: CccReadParams | dict[str, Any],
    ) -> CccDto:
        """Consulta Inscrições Estaduais.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações das Inscrições Estaduais.

        Example:
            ```python
            ccc = client.ccc.read({"tax_id": "37335118000180"})
            for ie in ccc.registrations:
                print(f"{ie.state}: {ie.number}")
            ```
        """
        if isinstance(params, dict):
            params = CccReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get(
            "/ccc",
            params={"taxId": params.tax_id, **query},
            response_model=CccDto,
        )
        return result

    def certificate(
        self,
        params: CccCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante de Inscrição Estadual (PDF).

        Args:
            params: Parâmetros da emissão (tax_id e state obrigatórios).

        Returns:
            Bytes do arquivo PDF.

        Example:
            ```python
            pdf = client.ccc.certificate({"tax_id": "37335118000180", "state": "SP"})
            with open("ie.pdf", "wb") as f:
                f.write(pdf)
            ```
        """
        if isinstance(params, dict):
            params = CccCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/ccc/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result


class AsyncCccResource(AsyncBaseResource):
    """Operações do Cadastro de Contribuintes (assíncrono)."""

    async def read(
        self,
        params: CccReadParams | dict[str, Any],
    ) -> CccDto:
        """Consulta Inscrições Estaduais."""
        if isinstance(params, dict):
            params = CccReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget(
            "/ccc",
            params={"taxId": params.tax_id, **query},
            response_model=CccDto,
        )
        return result

    async def certificate(
        self,
        params: CccCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante de Inscrição Estadual (PDF)."""
        if isinstance(params, dict):
            params = CccCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/ccc/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result
