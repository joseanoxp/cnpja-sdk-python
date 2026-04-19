"""Testes do SuframaResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client
from cnpja.types import SuframaDto


class TestSuframaRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_suframa: dict[str, Any]
    ) -> None:
        mock_api.get("/suframa").respond(json=sample_suframa)
        suframa = client.suframa.read({"tax_id": "37335118000180"})
        assert isinstance(suframa, SuframaDto)
        assert suframa.number == "200400029"

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_suframa: dict[str, Any]
    ) -> None:
        mock_api.get("/suframa").respond(json=sample_suframa)
        async with client.aio as aio:
            suframa = await aio.suframa.read({"tax_id": "37335118000180"})
        assert isinstance(suframa, SuframaDto)


class TestSuframaCertificate:
    def test_sync_returns_pdf_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/suframa/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        pdf = client.suframa.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)

    @pytest.mark.asyncio
    async def test_async(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/suframa/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        async with client.aio as aio:
            pdf = await aio.suframa.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)
