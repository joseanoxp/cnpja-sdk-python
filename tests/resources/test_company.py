"""Testes do CompanyResource."""

from __future__ import annotations

from typing import Any

import pytest
import respx

from cnpja import Client, NotFoundError
from cnpja.types import CompanyDto


class TestCompanyRead:
    def test_sync_returns_company_dto(
        self, client: Client, mock_api: respx.MockRouter, sample_company: dict[str, Any]
    ) -> None:
        mock_api.get("/company/37335118").respond(json=sample_company)
        company = client.company.read(37335118)
        assert isinstance(company, CompanyDto)
        assert company.id == 37335118
        assert company.name == "CNPJA TECNOLOGIA LTDA"

    def test_sync_accepts_string_id(
        self, client: Client, mock_api: respx.MockRouter, sample_company: dict[str, Any]
    ) -> None:
        mock_api.get("/company/37335118").respond(json=sample_company)
        company = client.company.read("37335118")
        assert company.id == 37335118

    def test_sync_propagates_404(self, client: Client, mock_api: respx.MockRouter) -> None:
        mock_api.get("/company/99999999").respond(status_code=404, json={"message": "x"})
        with pytest.raises(NotFoundError):
            client.company.read(99999999)

    @pytest.mark.asyncio
    async def test_async_returns_company_dto(
        self, client: Client, mock_api: respx.MockRouter, sample_company: dict[str, Any]
    ) -> None:
        mock_api.get("/company/37335118").respond(json=sample_company)
        async with client.aio as aio:
            company = await aio.company.read(37335118)
        assert isinstance(company, CompanyDto)
        assert company.id == 37335118
