"""Testes do CreditResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client
from cnpja.types import CreditDto


class TestCreditRead:
    def test_sync(
        self, client: Client, mock_api: respx.MockRouter, sample_credit: dict[str, Any]
    ) -> None:
        mock_api.get("/credit").respond(json=sample_credit)
        credit = client.credit.read()
        assert isinstance(credit, CreditDto)
        assert credit.perpetual == 1000
        assert credit.transient == 987

    @pytest.mark.asyncio
    async def test_async(
        self, client: Client, mock_api: respx.MockRouter, sample_credit: dict[str, Any]
    ) -> None:
        mock_api.get("/credit").respond(json=sample_credit)
        async with client.aio as aio:
            credit = await aio.credit.read()
        assert isinstance(credit, CreditDto)
