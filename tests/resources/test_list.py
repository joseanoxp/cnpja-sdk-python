"""Testes do ListResource (maior superfície de mutações)."""

from __future__ import annotations

import json
from typing import Any

import pytest
import respx

from cnpja import Client
from cnpja.types import ListDto, ListExportDto, ListExportIdDto, ListSummaryDto

LIST_ID = "5680a75e-750e-4c31-a1a1-e61e0e4f5618"
EXPORT_ID = "db344b70-3daf-43f3-b324-0f204ebfbd99"


class TestListCreate:
    def test_sync_serializes_body(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        route = mock_api.post("/list").respond(json=sample_list)
        result = client.list.create({"title": "Minha Lista", "items": ["37335118000180"]})
        assert isinstance(result, ListDto)
        body = json.loads(route.calls[0].request.content)
        assert body == {"title": "Minha Lista", "items": ["37335118000180"]}

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        mock_api.post("/list").respond(json=sample_list)
        async with client.aio as aio:
            result = await aio.list.create({"title": "X", "items": ["1"]})
        assert isinstance(result, ListDto)


class TestListRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        mock_api.get(f"/list/{LIST_ID}").respond(json=sample_list)
        result = client.list.read(LIST_ID)
        assert isinstance(result, ListDto)
        assert result.id == LIST_ID

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        mock_api.get(f"/list/{LIST_ID}").respond(json=sample_list)
        async with client.aio as aio:
            result = await aio.list.read(LIST_ID)
        assert isinstance(result, ListDto)


class TestListSearch:
    def test_sync(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_summary: dict[str, Any],
    ) -> None:
        mock_api.get("/list").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_list_summary]}
        )
        items = list(client.list.search({"search": "Minha"}))
        assert len(items) == 1
        assert isinstance(items[0], ListSummaryDto)

    @pytest.mark.asyncio
    async def test_async(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_summary: dict[str, Any],
    ) -> None:
        mock_api.get("/list").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_list_summary]}
        )
        async with client.aio as aio:
            items = [x async for x in aio.list.search({"search": "Minha"})]
        assert len(items) == 1


class TestListUpdate:
    def test_sync_serializes_body(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        route = mock_api.patch(f"/list/{LIST_ID}").respond(json=sample_list)
        client.list.update(LIST_ID, {"title": "Novo Título"})
        body = json.loads(route.calls[0].request.content)
        assert body == {"title": "Novo Título"}

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_list: dict[str, Any]
    ) -> None:
        mock_api.patch(f"/list/{LIST_ID}").respond(json=sample_list)
        async with client.aio as aio:
            await aio.list.update(LIST_ID, {"title": "X"})


class TestListDelete:
    def test_sync(self, client: Client, mock_api: respx.MockRouter) -> None:
        route = mock_api.delete(f"/list/{LIST_ID}").respond(status_code=204)
        client.list.delete(LIST_ID)
        assert route.called

    @pytest.mark.asyncio
    async def test_async(self, client: Client, mock_api: respx.MockRouter) -> None:
        route = mock_api.delete(f"/list/{LIST_ID}").respond(status_code=204)
        async with client.aio as aio:
            await aio.list.delete(LIST_ID)
        assert route.called


class TestListExportCreate:
    def test_sync_serializes_body(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export_id: dict[str, Any],
    ) -> None:
        route = mock_api.post(f"/list/{LIST_ID}/export").respond(json=sample_list_export_id)
        result = client.list.create_export(LIST_ID, {"options": {"simples": True}})
        assert isinstance(result, ListExportIdDto)
        body = json.loads(route.calls[0].request.content)
        assert body == {"options": {"simples": True}}

    @pytest.mark.asyncio
    async def test_async(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export_id: dict[str, Any],
    ) -> None:
        mock_api.post(f"/list/{LIST_ID}/export").respond(json=sample_list_export_id)
        async with client.aio as aio:
            result = await aio.list.create_export(LIST_ID, {"options": {"simples": True}})
        assert isinstance(result, ListExportIdDto)


class TestListExportSearch:
    def test_sync(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export: dict[str, Any],
    ) -> None:
        mock_api.get(f"/list/{LIST_ID}/export").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_list_export]}
        )
        items = list(client.list.search_export(LIST_ID))
        assert len(items) == 1
        assert isinstance(items[0], ListExportDto)

    @pytest.mark.asyncio
    async def test_async(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export: dict[str, Any],
    ) -> None:
        mock_api.get(f"/list/{LIST_ID}/export").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_list_export]}
        )
        async with client.aio as aio:
            items = [x async for x in aio.list.search_export(LIST_ID)]
        assert len(items) == 1


class TestListExportRead:
    def test_sync(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export: dict[str, Any],
    ) -> None:
        mock_api.post(f"/list/{LIST_ID}/export/{EXPORT_ID}").respond(json=sample_list_export)
        result = client.list.read_export(LIST_ID, EXPORT_ID)
        assert isinstance(result, ListExportDto)

    @pytest.mark.asyncio
    async def test_async(
        self,
        client: Client,
        mock_api: respx.MockRouter,
        sample_list_export: dict[str, Any],
    ) -> None:
        mock_api.post(f"/list/{LIST_ID}/export/{EXPORT_ID}").respond(json=sample_list_export)
        async with client.aio as aio:
            result = await aio.list.read_export(LIST_ID, EXPORT_ID)
        assert isinstance(result, ListExportDto)
