"""Resource para operações da Receita Federal."""

from __future__ import annotations

from typing import Any

from ..types.rfb import RfbCertificateParams, RfbDto, RfbReadParams
from ._base import AsyncBaseResource, BaseResource


class RfbResource(BaseResource):
    """Operações da Receita Federal (síncrono)."""

    def read(
        self,
        params: RfbReadParams | dict[str, Any],
    ) -> RfbDto:
        """Consulta informações da Receita Federal.

        Args:
            params: Parâmetros da consulta (tax_id obrigatório).

        Returns:
            Informações da RFB.

        Example:
            ```python
            rfb = client.rfb.read({"tax_id": "37335118000180"})
            print(f"QSA: {len(rfb.members)} sócios")
            ```
        """
        if isinstance(params, dict):
            params = RfbReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get(
            "/rfb",
            params={"taxId": params.tax_id, **query},
            response_model=RfbDto,
        )
        return result

    def certificate(
        self,
        params: RfbCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante de inscrição e situação cadastral (PDF).

        Args:
            params: Parâmetros da emissão (tax_id obrigatório).

        Returns:
            Bytes do arquivo PDF.

        Example:
            ```python
            pdf = client.rfb.certificate({"tax_id": "37335118000180"})
            with open("comprovante.pdf", "wb") as f:
                f.write(pdf)
            ```
        """
        if isinstance(params, dict):
            params = RfbCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = self._http.get_binary(
            "/rfb/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result


class AsyncRfbResource(AsyncBaseResource):
    """Operações da Receita Federal (assíncrono)."""

    async def read(
        self,
        params: RfbReadParams | dict[str, Any],
    ) -> RfbDto:
        """Consulta informações da Receita Federal."""
        if isinstance(params, dict):
            params = RfbReadParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget(
            "/rfb",
            params={"taxId": params.tax_id, **query},
            response_model=RfbDto,
        )
        return result

    async def certificate(
        self,
        params: RfbCertificateParams | dict[str, Any],
    ) -> bytes:
        """Emite comprovante de inscrição e situação cadastral (PDF)."""
        if isinstance(params, dict):
            params = RfbCertificateParams.model_validate(params)

        query = params.model_dump(by_alias=True, exclude={"tax_id"}, exclude_none=True)

        result = await self._http.aget_binary(
            "/rfb/certificate",
            params={"taxId": params.tax_id, **query},
        )
        return result
