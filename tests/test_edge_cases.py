"""Casos limite: transport errors, retry, URL edge cases."""

from __future__ import annotations

import httpx
import pytest
import respx

from cnpja._http_client import HttpClient
from cnpja.errors import BadRequestError, ServerError, TooManyRequestsError


class TestTransportErrorRetry:
    def test_retries_on_transport_error_then_succeeds(self) -> None:
        with HttpClient(api_key="k", retry_limit=2, retry_delay=lambda _: 0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                route = router.get("/credit").mock(
                    side_effect=[
                        httpx.ConnectError("network unreachable"),
                        httpx.Response(200, json={"perpetual": 1, "transient": 1}),
                    ]
                )
                result = http.get("/credit")
        assert route.call_count == 2
        assert isinstance(result, dict)

    def test_gives_up_after_retry_limit(self) -> None:
        with HttpClient(api_key="k", retry_limit=2, retry_delay=lambda _: 0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/credit").respond(status_code=503, json={"message": "down"})
                with pytest.raises(ServerError):
                    http.get("/credit")

    def test_does_not_retry_on_4xx(self) -> None:
        with HttpClient(api_key="k", retry_limit=3, retry_delay=lambda _: 0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                route = router.get("/credit").respond(
                    status_code=400, json={"message": "invalid", "constraints": ["foo"]}
                )
                with pytest.raises(BadRequestError):
                    http.get("/credit")
        assert route.call_count == 1

    def test_retries_on_429(self) -> None:
        with HttpClient(api_key="k", retry_limit=2, retry_delay=lambda _: 0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                route = router.get("/credit").respond(
                    status_code=429,
                    json={"message": "rate"},
                    headers={"x-credit-required": "3", "x-credit-remaining": "0"},
                )
                with pytest.raises(TooManyRequestsError):
                    http.get("/credit")
        assert route.call_count == 3


class TestPaginationTokenPropagation:
    def test_second_request_sends_token(self) -> None:
        from cnpja.pagers import Pager
        from cnpja.types import OfficePageRecordDto

        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                route = router.get("/office").mock(
                    side_effect=[
                        httpx.Response(
                            200,
                            json={
                                "next": "TOK123",
                                "limit": 1,
                                "count": 2,
                                "records": [_minimal_record("11111111000191")],
                            },
                        ),
                        httpx.Response(
                            200,
                            json={
                                "next": None,
                                "limit": 1,
                                "count": 2,
                                "records": [_minimal_record("22222222000192")],
                            },
                        ),
                    ]
                )
                pager: Pager[OfficePageRecordDto] = Pager(
                    http_client=http, path="/office", params={}, response_model=OfficePageRecordDto
                )
                list(pager)
        assert route.calls[1].request.url.params["token"] == "TOK123"


def _minimal_record(tax_id: str) -> dict[str, object]:
    return {
        "taxId": tax_id,
        "updated": "2024-01-01",
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
