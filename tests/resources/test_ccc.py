"""Testes do CccResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client
from cnpja.types import CccDto


class TestCccRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_ccc: dict[str, Any]
    ) -> None:
        route = mock_api.get("/ccc").respond(json=sample_ccc)
        ccc = client.ccc.read({"tax_id": "37335118000180", "states": ["SP"]})
        assert isinstance(ccc, CccDto)
        assert ccc.name == "CNPJA TECNOLOGIA LTDA"
        url = str(route.calls[0].request.url)
        assert "taxId=37335118000180" in url
        assert "states=SP" in url

    def test_sync_with_source_and_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_ccc: dict[str, Any]
    ) -> None:
        route = mock_api.get("/ccc").respond(json=sample_ccc)
        client.ccc.read(
            {
                "tax_id": "37335118000180",
                "states": ["ORIGIN"],
                "source": "SINTEGRA",
                "sync": True,
            }
        )
        url = str(route.calls[0].request.url)
        assert "source=SINTEGRA" in url
        assert "sync=true" in url

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_ccc: dict[str, Any]
    ) -> None:
        mock_api.get("/ccc").respond(json=sample_ccc)
        async with client.aio as aio:
            ccc = await aio.ccc.read({"tax_id": "37335118000180", "states": ["SP"]})
        assert isinstance(ccc, CccDto)


class TestCccCertificate:
    def test_sync_returns_pdf_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/ccc/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        pdf = client.ccc.certificate({"tax_id": "37335118000180", "state": "SP"})
        assert isinstance(pdf, bytes)

    @pytest.mark.asyncio
    async def test_async(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/ccc/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        async with client.aio as aio:
            pdf = await aio.ccc.certificate({"tax_id": "37335118000180", "state": "SP"})
        assert isinstance(pdf, bytes)
