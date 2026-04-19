"""Testes do OfficeResource (autenticado)."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client, NotFoundError
from cnpja.types import CacheStrategy, OfficeDto, OfficeReadParams


class TestOfficeRead:
    def test_returns_office_dto(
        self, client: Client, mock_api: respx.MockRouter, sample_office: dict[str, Any]
    ) -> None:
        mock_api.get("/office/37335118000180").respond(json=sample_office)
        office = client.office.read({"tax_id": "37335118000180"})
        assert isinstance(office, OfficeDto)
        assert office.tax_id == "37335118000180"
        assert office.company.name == "CNPJA TECNOLOGIA LTDA"

    def test_accepts_pydantic_params(
        self, client: Client, mock_api: respx.MockRouter, sample_office: dict[str, Any]
    ) -> None:
        route = mock_api.get("/office/37335118000180").respond(json=sample_office)
        params = OfficeReadParams(
            tax_id="37335118000180", strategy=CacheStrategy.CACHE_IF_FRESH, sync=True
        )
        client.office.read(params)
        assert route.called
        assert "strategy=CACHE_IF_FRESH" in str(route.calls[0].request.url)
        assert "sync=true" in str(route.calls[0].request.url)

    def test_propagates_404(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/office/00000000000000").respond(status_code=404, json={"message": "x"})
        with pytest.raises(NotFoundError):
            client.office.read({"tax_id": "00000000000000"})


class TestOfficeSearch:
    def test_single_page(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_office_page_record: dict[str, Any],
    ) -> None:
        mock_api.get("/office").respond(
            json={
                "next": None,
                "limit": 2,
                "count": 1,
                "records": [sample_office_page_record],
            }
        )
        items = list(client.office.search({"address.state.in": ["SP"]}))
        assert len(items) == 1
        assert items[0].tax_id == "37335118000180"


class TestOfficeBinary:
    def test_map_returns_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/office/37335118000180/map").respond(
            content=b"\x89PNG\r\n\x1a\nMAP", headers={"content-type": "image/png"}
        )
        result = client.office.map({"tax_id": "37335118000180"})
        assert isinstance(result, bytes)
        assert result.startswith(b"\x89PNG")

    def test_street_returns_bytes(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/office/37335118000180/street").respond(
            content=b"\x89PNG\r\n\x1a\nSTREET", headers={"content-type": "image/png"}
        )
        result = client.office.street({"tax_id": "37335118000180"})
        assert isinstance(result, bytes)
        assert result.startswith(b"\x89PNG")


@pytest.mark.asyncio
class TestOfficeAsync:
    async def test_read(
        self, client: Client, mock_api: respx.MockRouter, sample_office: dict[str, Any]
    ) -> None:
        mock_api.get("/office/37335118000180").respond(json=sample_office)
        async with client.aio as aio:
            office = await aio.office.read({"tax_id": "37335118000180"})
        assert isinstance(office, OfficeDto)

    async def test_map(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/office/37335118000180/map").respond(
            content=b"\x89PNG\r\n\x1a\nMAP", headers={"content-type": "image/png"}
        )
        async with client.aio as aio:
            result = await aio.office.map({"tax_id": "37335118000180"})
        assert isinstance(result, bytes)

    async def test_street(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/office/37335118000180/street").respond(
            content=b"\x89PNG", headers={"content-type": "image/png"}
        )
        async with client.aio as aio:
            result = await aio.office.street({"tax_id": "37335118000180"})
        assert isinstance(result, bytes)

    async def test_search(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_office_page_record: dict[str, Any],
    ) -> None:
        mock_api.get("/office").respond(
            json={
                "next": None,
                "limit": 1,
                "count": 1,
                "records": [sample_office_page_record],
            }
        )
        async with client.aio as aio:
            items = [item async for item in aio.office.search({"address.state.in": ["SP"]})]
        assert len(items) == 1
