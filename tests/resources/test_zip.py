"""Testes do ZipResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client, NotFoundError
from cnpja.types import ZipDto


class TestZipRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_zip: dict[str, Any]
    ) -> None:
        mock_api.get("/zip/01452922").respond(json=sample_zip)
        zip_info = client.zip.read("01452922")
        assert isinstance(zip_info, ZipDto)
        assert zip_info.code == "01452922"
        assert zip_info.city == "São Paulo"

    def test_sync_propagates_404(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/zip/00000000").respond(status_code=404, json={"message": "x"})
        with pytest.raises(NotFoundError):
            client.zip.read("00000000")

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_zip: dict[str, Any]
    ) -> None:
        mock_api.get("/zip/01452922").respond(json=sample_zip)
        async with client.aio as aio:
            zip_info = await aio.zip.read("01452922")
        assert isinstance(zip_info, ZipDto)
