"""Testes do HttpClient (retry, URL build, binary)."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
import respx

from cnpja._http_client import HttpClient, _CallbackWait
from cnpja.errors import BadRequestError
from cnpja.types import ZipDto


class TestUrlBuilder:
    def test_replaces_single_placeholder(self) -> None:
        with HttpClient(api_key="k") as http:
            assert http._build_url("office/:taxId", {"taxId": "123"}) == "office/123"

    def test_replaces_multiple_placeholders(self) -> None:
        with HttpClient(api_key="k") as http:
            url = http._build_url("list/:listId/export/:exportId", {"listId": "A", "exportId": "B"})
            assert url == "list/A/export/B"

    def test_strips_leading_slash(self) -> None:
        with HttpClient(api_key="k") as http:
            assert http._build_url("/office/:id", {"id": "1"}) == "office/1"


class TestCallbackWait:
    """Regression: retry_delay callback era ignorado (chamava wait_fixed(0))."""

    def test_callback_invoked_with_attempt_number(self) -> None:
        cb = MagicMock(return_value=2.5)
        wait = _CallbackWait(cb)
        state = MagicMock(attempt_number=3)
        assert wait(state) == 2.5
        cb.assert_called_once_with(3)


class TestResponseParsing:
    def test_get_returns_parsed_model_when_response_model_given(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/zip/01452922").respond(
                    json={
                        "code": "01452922",
                        "updated": "2024-01-01T00:00:00.000Z",
                        "municipality": 3550308,
                        "street": "Av X",
                        "number": "123",
                        "district": "D",
                        "city": "SP",
                        "state": "SP",
                    },
                )
                result = http.get(
                    "/zip/:code",
                    replacements={"code": "01452922"},
                    response_model=ZipDto,
                )
        assert isinstance(result, ZipDto)
        assert result.code == "01452922"

    def test_get_binary_returns_bytes(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/office/37335118000180/map").respond(
                    content=b"\x89PNG\r\n\x1a\nIHDR",
                    headers={"content-type": "image/png"},
                )
                result = http.get_binary(
                    "/office/:taxId/map",
                    replacements={"taxId": "37335118000180"},
                )
        assert isinstance(result, bytes)
        assert result.startswith(b"\x89PNG")


class TestErrorPropagation:
    def test_http_error_raises_subclass(self) -> None:
        with HttpClient(api_key="k", retry_limit=0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                router.get("/zip/000").respond(
                    status_code=400,
                    json={"message": "cep inválido", "constraints": ["formato"]},
                )
                with pytest.raises(BadRequestError) as exc:
                    http.get("/zip/:code", replacements={"code": "000"})
        assert exc.value.constraints == ["formato"]


class TestRetryOnTransientFailure:
    """Retry automático em códigos 5xx/429 e erros de transporte."""

    def test_retries_on_503_then_succeeds(self) -> None:
        with HttpClient(api_key="k", retry_limit=2, retry_delay=lambda r: 0) as http:
            with respx.mock(base_url="https://api.cnpja.com") as router:
                route = router.get("/zip/01452922").mock(
                    side_effect=[
                        httpx.Response(503, json={"message": "fora"}),
                        httpx.Response(
                            200,
                            json={
                                "code": "01452922",
                                "updated": "2024-01-01T00:00:00.000Z",
                                "municipality": 3550308,
                                "street": "Av X",
                                "number": "1",
                                "district": "D",
                                "city": "SP",
                                "state": "SP",
                            },
                        ),
                    ]
                )
                result = http.get(
                    "/zip/:code", replacements={"code": "01452922"}, response_model=ZipDto
                )
        assert route.call_count == 2
        assert isinstance(result, ZipDto)
