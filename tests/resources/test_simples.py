"""Testes do SimplesResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client
from cnpja.types import SimplesDto


class TestSimplesRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_simples: dict[str, Any]
    ) -> None:
        mock_api.get("/simples").respond(json=sample_simples)
        simples = client.simples.read({"tax_id": "37335118000180"})
        assert isinstance(simples, SimplesDto)
        assert simples.simples.optant is True
        assert simples.simei.optant is False

    def test_sync_with_history(
        self, client: Client, mock_api: respx.MockRouter, sample_simples: dict[str, Any]
    ) -> None:
        route = mock_api.get("/simples").respond(json=sample_simples)
        client.simples.read({"tax_id": "37335118000180", "history": True})
        assert "history=true" in str(route.calls[0].request.url)

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_simples: dict[str, Any]
    ) -> None:
        mock_api.get("/simples").respond(json=sample_simples)
        async with client.aio as aio:
            simples = await aio.simples.read({"tax_id": "37335118000180"})
        assert isinstance(simples, SimplesDto)


class TestSimplesCertificate:
    def test_sync_returns_pdf_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/simples/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        pdf = client.simples.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)

    @pytest.mark.asyncio
    async def test_async(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/simples/certificate").respond(
            content=b"%PDF-1.4\n", headers={"content-type": "application/pdf"}
        )
        async with client.aio as aio:
            pdf = await aio.simples.certificate({"tax_id": "37335118000180"})
        assert isinstance(pdf, bytes)
