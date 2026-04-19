"""Testes do RfbResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client, NotFoundError
from cnpja.types import RfbDto


class TestRfbRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_rfb: dict[str, Any]
    ) -> None:
        route = mock_api.get("/rfb").respond(json=sample_rfb)
        rfb = client.rfb.read({"tax_id": "37335118000180"})
        assert route.called
        assert isinstance(rfb, RfbDto)
        assert rfb.name == "CNPJA TECNOLOGIA LTDA"
        assert "taxId=37335118000180" in str(route.calls[0].request.url)

    def test_sync_propagates_404(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/rfb").respond(status_code=404, json={"message": "x"})
        with pytest.raises(NotFoundError):
            client.rfb.read({"tax_id": "00000000000000"})

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_rfb: dict[str, Any]
    ) -> None:
        mock_api.get("/rfb").respond(json=sample_rfb)
        async with client.aio as aio:
            rfb = await aio.rfb.read({"tax_id": "37335118000180"})
        assert isinstance(rfb, RfbDto)


class TestRfbCertificate:
    def test_sync_returns_pdf_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/rfb/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        pdf = client.rfb.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)
        assert pdf.startswith(b"%PDF")

    def test_sync_with_pages_param(self, client: Client, mock_api: respx.MockRouter) -> None:
        route = mock_api.get("/rfb/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        client.rfb.certificate({"tax_id": "37335118000180", "pages": ["REGISTRATION", "MEMBERS"]})
        url = str(route.calls[0].request.url)
        assert "pages=" in url

    @pytest.mark.asyncio
    async def test_async(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/rfb/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        async with client.aio as aio:
            pdf = await aio.rfb.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)
