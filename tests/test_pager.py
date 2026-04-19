"""Testes dos paginadores Pager e AsyncPager."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx

from cnpja._http_client import HttpClient
from cnpja.pagers import AsyncPager, Pager
from cnpja.types import OfficePageRecordDto


def _office_record(tax_id: str) -> dict[str, Any]:
    return {
        "taxId": tax_id,
        "updated": "2024-01-01T00:00:00.000Z",
        "company": {
            "id": int(tax_id[:8]),
            "name": "X",
            "equity": 0.0,
            "nature": {"id": 2062, "text": "LTDA"},
            "size": {"id": 1, "acronym": "ME", "text": "ME"},
            "members": [],
        },
        "alias": None,
        "founded": "2020-01-01",
        "head": True,
        "statusDate": "2020-01-01",
        "status": {"id": 2, "text": "Ativa"},
        "address": {
            "municipality": 3550308,
            "street": "X",
            "number": "1",
            "district": "D",
            "city": "SP",
            "state": "SP",
            "zip": "01000000",
            "country": {"id": 76, "name": "Brasil"},
        },
        "phones": [],
        "emails": [],
        "mainActivity": {"id": 6311900, "text": "TI"},
        "sideActivities": [],
    }


class TestPager:
    def test_iterates_multiple_pages(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").mock(
                    side_effect=[
                        httpx.Response(
                            200,
                            json={
                                "next": "t2",
                                "limit": 2,
                                "count": 3,
                                "records": [
                                    _office_record("11111111000191"),
                                    _office_record("22222222000192"),
                                ],
                            },
                        ),
                        httpx.Response(
                            200,
                            json={
                                "next": None,
                                "limit": 2,
                                "count": 3,
                                "records": [_office_record("33333333000193")],
                            },
                        ),
                    ]
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = list(pager)
        assert [i.tax_id for i in items] == [
            "11111111000191",
            "22222222000192",
            "33333333000193",
        ]

    def test_page_returns_first_page_without_consuming_iteration(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={
                        "next": "t2",
                        "limit": 2,
                        "count": 3,
                        "records": [
                            _office_record("11111111000191"),
                            _office_record("22222222000192"),
                        ],
                    }
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = pager.page
        assert [item.tax_id for item in items] == ["11111111000191", "22222222000192"]

    def test_next_page_advances_after_page_property(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").mock(
                    side_effect=[
                        httpx.Response(
                            200,
                            json={
                                "next": "t2",
                                "limit": 2,
                                "count": 3,
                                "records": [
                                    _office_record("11111111000191"),
                                    _office_record("22222222000192"),
                                ],
                            },
                        ),
                        httpx.Response(
                            200,
                            json={
                                "next": None,
                                "limit": 1,
                                "count": 3,
                                "records": [_office_record("33333333000193")],
                            },
                        ),
                    ]
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                _ = pager.page
                next_items = pager.next_page()
        assert [item.tax_id for item in next_items] == ["33333333000193"]

    def test_empty_first_page_stops(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={"next": None, "limit": 0, "count": 0, "records": []}
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                assert list(pager) == []

    def test_collect_respects_limit(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={
                        "next": None,
                        "limit": 3,
                        "count": 3,
                        "records": [
                            _office_record("11111111000191"),
                            _office_record("22222222000192"),
                            _office_record("33333333000193"),
                        ],
                    }
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = pager.collect(limit=2)
        assert len(items) == 2


@pytest.mark.asyncio
class TestAsyncPager:
    async def test_iterates_multiple_pages(self) -> None:
        async with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").mock(
                    side_effect=[
                        httpx.Response(
                            200,
                            json={
                                "next": "t2",
                                "limit": 2,
                                "count": 3,
                                "records": [
                                    _office_record("11111111000191"),
                                    _office_record("22222222000192"),
                                ],
                            },
                        ),
                        httpx.Response(
                            200,
                            json={
                                "next": None,
                                "limit": 2,
                                "count": 3,
                                "records": [_office_record("33333333000193")],
                            },
                        ),
                    ]
                )
                pager: AsyncPager[OfficePageRecordDto] = AsyncPager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = [item async for item in pager]
        assert len(items) == 3

    async def test_page_returns_first_page_via_async_method(self) -> None:
        async with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={
                        "next": "t2",
                        "limit": 2,
                        "count": 3,
                        "records": [
                            _office_record("11111111000191"),
                            _office_record("22222222000192"),
                        ],
                    }
                )
                pager: AsyncPager[OfficePageRecordDto] = AsyncPager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = await pager.page()
        assert [item.tax_id for item in items] == ["11111111000191", "22222222000192"]

    async def test_next_page_advances_after_page_method(self) -> None:
        async with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").mock(
                    side_effect=[
                        httpx.Response(
                            200,
                            json={
                                "next": "t2",
                                "limit": 2,
                                "count": 3,
                                "records": [
                                    _office_record("11111111000191"),
                                    _office_record("22222222000192"),
                                ],
                            },
                        ),
                        httpx.Response(
                            200,
                            json={
                                "next": None,
                                "limit": 1,
                                "count": 3,
                                "records": [_office_record("33333333000193")],
                            },
                        ),
                    ]
                )
                pager: AsyncPager[OfficePageRecordDto] = AsyncPager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                _ = await pager.page()
                next_items = await pager.next_page()
        assert [item.tax_id for item in next_items] == ["33333333000193"]

    async def test_empty_first_page_stops(self) -> None:
        async with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={"next": None, "limit": 0, "count": 0, "records": []}
                )
                pager: AsyncPager[OfficePageRecordDto] = AsyncPager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = [item async for item in pager]
        assert items == []

    async def test_collect_respects_limit(self) -> None:
        async with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office").respond(
                    json={
                        "next": None,
                        "limit": 3,
                        "count": 3,
                        "records": [
                            _office_record("11111111000191"),
                            _office_record("22222222000192"),
                            _office_record("33333333000193"),
                        ],
                    }
                )
                pager: AsyncPager[OfficePageRecordDto] = AsyncPager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                items = await pager.collect(limit=2)
        assert len(items) == 2
