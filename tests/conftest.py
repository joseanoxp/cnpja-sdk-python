"""Fixtures compartilhadas entre os testes."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
import respx

from cnpja import Client, CnpjaOpen


@pytest.fixture
def api_key() -> str:
    return "test-key-0000"


@pytest.fixture
def client(api_key: str) -> Iterator[Client]:
    c = Client(api_key=api_key, retry_limit=0)
    yield c
    c.close()


@pytest.fixture
def open_client() -> Iterator[CnpjaOpen]:
    c = CnpjaOpen(retry_limit=0)
    yield c
    c.close()


@pytest.fixture
def mock_api() -> Iterator[respx.MockRouter]:
    """Router respx para a API autenticada (https://api.cnpja.com)."""
    with respx.mock(base_url="https://api.cnpja.com", assert_all_called=False) as router:
        yield router


@pytest.fixture
def mock_open_api() -> Iterator[respx.MockRouter]:
    """Router respx para a API pública (https://open.cnpja.com)."""
    with respx.mock(base_url="https://open.cnpja.com", assert_all_called=False) as router:
        yield router


# =============================================================================
# Payloads de resposta JSON (válidos para os DTOs)
# =============================================================================


def _address(state: str = "SP", city: str = "São Paulo") -> dict[str, Any]:
    return {
        "municipality": 3550308,
        "street": "Avenida Brigadeiro Faria Lima",
        "number": "2369",
        "district": "Jardim Paulistano",
        "city": city,
        "state": state,
        "zip": "01452922",
        "country": {"id": 76, "name": "Brasil"},
    }


def _office_company(members: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "id": 37335118,
        "name": "CNPJA TECNOLOGIA LTDA",
        "equity": 1000.0,
        "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
        "size": {"id": 1, "acronym": "ME", "text": "Microempresa"},
        "members": members or [],
    }


@pytest.fixture
def sample_office() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "company": _office_company(),
        "alias": "Cnpja",
        "founded": "2020-06-05",
        "head": True,
        "statusDate": "2020-06-05",
        "status": {"id": 2, "text": "Ativa"},
        "address": _address(),
        "phones": [],
        "emails": [],
        "mainActivity": {"id": 6311900, "text": "Tratamento de dados"},
        "sideActivities": [],
    }


@pytest.fixture
def sample_office_page_record() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "company": _office_company(),
        "alias": "Cnpja",
        "founded": "2020-06-05",
        "head": True,
        "statusDate": "2020-06-05",
        "status": {"id": 2, "text": "Ativa"},
        "address": _address(),
        "phones": [],
        "emails": [],
        "mainActivity": {"id": 6311900, "text": "Tratamento de dados"},
        "sideActivities": [],
    }


@pytest.fixture
def sample_company() -> dict[str, Any]:
    return {
        "id": 37335118,
        "name": "CNPJA TECNOLOGIA LTDA",
        "equity": 1000.0,
        "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
        "size": {"id": 1, "acronym": "ME", "text": "Microempresa"},
        "members": [],
        "offices": [
            {
                "taxId": "37335118000180",
                "founded": "2020-06-05",
                "head": True,
                "statusDate": "2020-06-05",
                "status": {"id": 2, "text": "Ativa"},
            }
        ],
    }


@pytest.fixture
def sample_person() -> dict[str, Any]:
    return {
        "id": "1e5ed433-0f39-4309-8e85-8d21a571b212",
        "type": "NATURAL",
        "name": "João Silva",
        "membership": [],
    }


@pytest.fixture
def sample_rfb() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "name": "CNPJA TECNOLOGIA LTDA",
        "equity": 1000.0,
        "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
        "size": {"id": 1, "acronym": "ME", "text": "Microempresa"},
        "alias": "Cnpja",
        "founded": "2020-06-05",
        "head": True,
        "statusDate": "2020-06-05",
        "status": {"id": 2, "text": "Ativa"},
        "address": _address(),
        "phones": [],
        "emails": [],
        "mainActivity": {"id": 6311900, "text": "Tratamento de dados"},
        "sideActivities": [],
        "members": [],
    }


@pytest.fixture
def sample_simples() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "simples": {"optant": True, "since": "2020-06-05"},
        "simei": {"optant": False},
    }


@pytest.fixture
def sample_ccc() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "name": "CNPJA TECNOLOGIA LTDA",
        "originState": "SP",
        "registrations": [],
    }


@pytest.fixture
def sample_suframa() -> dict[str, Any]:
    return {
        "taxId": "37335118000180",
        "updated": "2024-01-01T00:00:00.000Z",
        "number": "200400029",
        "name": "CNPJA TECNOLOGIA LTDA",
        "head": True,
        "approved": True,
        "status": {"id": 1, "text": "Ativa"},
        "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
        "address": _address(),
        "phones": [],
        "emails": [],
        "mainActivity": {"id": 6311900, "text": "Tratamento de dados", "performed": True},
        "sideActivities": [],
        "incentives": [],
    }


@pytest.fixture
def sample_zip() -> dict[str, Any]:
    return {
        "code": "01452922",
        "updated": "2024-01-01T00:00:00.000Z",
        "municipality": 3550308,
        "street": "Avenida Brigadeiro Faria Lima",
        "number": "2369",
        "district": "Jardim Paulistano",
        "city": "São Paulo",
        "state": "SP",
    }


@pytest.fixture
def sample_credit() -> dict[str, Any]:
    return {"perpetual": 1000, "transient": 987}


@pytest.fixture
def sample_list() -> dict[str, Any]:
    return {
        "id": "5680a75e-750e-4c31-a1a1-e61e0e4f5618",
        "created": "2024-03-11T17:30:20.757Z",
        "updated": "2024-03-11T17:30:20.757Z",
        "title": "Minha Lista",
        "description": "Lista de teste",
        "size": 2,
        "items": ["37335118000180", "00000000000191"],
    }


@pytest.fixture
def sample_list_summary() -> dict[str, Any]:
    return {
        "id": "5680a75e-750e-4c31-a1a1-e61e0e4f5618",
        "created": "2024-03-11T17:30:20.757Z",
        "updated": "2024-03-11T17:30:20.757Z",
        "title": "Minha Lista",
        "description": "Lista de teste",
        "size": 2,
    }


@pytest.fixture
def sample_list_export() -> dict[str, Any]:
    return {
        "id": "db344b70-3daf-43f3-b324-0f204ebfbd99",
        "created": "2024-03-11T17:30:20.757Z",
        "updated": "2024-03-11T17:30:20.757Z",
        "status": "COMPLETED",
        "progress": 1.0,
        "options": {"simples": True},
        "links": [{"type": "EXCEL", "url": "https://example.com/export.xlsx"}],
    }


@pytest.fixture
def sample_list_export_id() -> dict[str, Any]:
    return {"id": "db344b70-3daf-43f3-b324-0f204ebfbd99"}
