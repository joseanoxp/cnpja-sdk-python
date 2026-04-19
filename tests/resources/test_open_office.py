"""Testes do OpenOfficeResource (API pública)."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import CnpjaOpen
from cnpja.resources import AsyncOpenOfficeResource, OpenOfficeResource
from cnpja.types import OfficeDto


class TestOpenOfficeSurface:
    def test_sync_read_only_surface(self, open_client: CnpjaOpen) -> None:
        assert isinstance(open_client.office, OpenOfficeResource)
        assert not hasattr(open_client.office, "search")
        assert not hasattr(open_client.office, "map")
        assert not hasattr(open_client.office, "street")

    def test_async_read_only_surface(self, open_client: CnpjaOpen) -> None:
        assert isinstance(open_client.aio.office, AsyncOpenOfficeResource)
        assert not hasattr(open_client.aio.office, "search")
        assert not hasattr(open_client.aio.office, "map")
        assert not hasattr(open_client.aio.office, "street")


class TestOpenOfficeRead:
    def test_sync_hits_open_subdomain(
        self,
        open_client: CnpjaOpen,
        mock_open_api: respx.MockRouter,
        sample_office: dict[str, Any],
    ) -> None:
        route = mock_open_api.get("/office/37335118000180").respond(json=sample_office)
        office = open_client.office.read({"tax_id": "37335118000180"})
        assert route.called
        assert isinstance(office, OfficeDto)
        assert office.tax_id == "37335118000180"

    @pytest.mark.asyncio
    async def test_async_hits_open_subdomain(
        self,
        open_client: CnpjaOpen,
        mock_open_api: respx.MockRouter,
        sample_office: dict[str, Any],
    ) -> None:
        route = mock_open_api.get("/office/37335118000180").respond(json=sample_office)
        async with open_client.aio as aio:
            office = await aio.office.read({"tax_id": "37335118000180"})
        assert route.called
        assert isinstance(office, OfficeDto)
