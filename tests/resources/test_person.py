"""Testes do PersonResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client, NotFoundError
from cnpja.types import PersonDto

PERSON_ID = "1e5ed433-0f39-4309-8e85-8d21a571b212"


class TestPersonRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_person: dict[str, Any]
    ) -> None:
        mock_api.get(f"/person/{PERSON_ID}").respond(json=sample_person)
        person = client.person.read(PERSON_ID)
        assert isinstance(person, PersonDto)
        assert person.id == PERSON_ID

    def test_sync_propagates_404(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get(f"/person/{PERSON_ID}").respond(status_code=404, json={"message": "x"})
        with pytest.raises(NotFoundError):
            client.person.read(PERSON_ID)

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_person: dict[str, Any]
    ) -> None:
        mock_api.get(f"/person/{PERSON_ID}").respond(json=sample_person)
        async with client.aio as aio:
            person = await aio.person.read(PERSON_ID)
        assert isinstance(person, PersonDto)


class TestPersonSearch:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_person: dict[str, Any]
    ) -> None:
        mock_api.get("/person").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_person]}
        )
        items = list(client.person.search({"name.in": ["João Silva"]}))
        assert len(items) == 1
        assert items[0].name == "João Silva"

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_person: dict[str, Any]
    ) -> None:
        mock_api.get("/person").respond(
            json={"next": None, "limit": 1, "count": 1, "records": [sample_person]}
        )
        async with client.aio as aio:
            items = [p async for p in aio.person.search({"name.in": ["João Silva"]})]
        assert len(items) == 1
