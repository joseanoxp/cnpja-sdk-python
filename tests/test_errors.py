"""Testes da hierarquia de exceções e parsing de respostas HTTP."""

from __future__ import annotations

import httpx
import pytest

from cnpja.errors import (
    APIError,
    BadRequestError,
    ClientError,
    NotFoundError,
    ServerError,
    TooManyRequestsError,
    UnauthorizedError,
)


def _response(
    status: int,
    json: dict[str, object] | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    return httpx.Response(
        status_code=status,
        json=json if json is not None else {"message": "erro"},
        headers=headers or {},
    )


class TestErrorHierarchy:
    def test_400_maps_to_bad_request(self) -> None:
        err = APIError.from_response(
            _response(400, {"message": "inválido", "constraints": ["campo X"]})
        )
        assert isinstance(err, BadRequestError)
        assert err.code == 400
        assert err.message == "inválido"
        assert err.constraints == ["campo X"]

    def test_401_maps_to_unauthorized(self) -> None:
        err = APIError.from_response(_response(401, {"message": "sem auth"}))
        assert isinstance(err, UnauthorizedError)
        assert err.code == 401

    def test_404_maps_to_not_found(self) -> None:
        err = APIError.from_response(_response(404, {"message": "não encontrado"}))
        assert isinstance(err, NotFoundError)
        assert err.code == 404

    def test_other_4xx_maps_to_client_error(self) -> None:
        err = APIError.from_response(_response(403, {"message": "proibido"}))
        assert isinstance(err, ClientError)
        assert not isinstance(err, (BadRequestError, UnauthorizedError, NotFoundError))

    def test_5xx_maps_to_server_error(self) -> None:
        err = APIError.from_response(_response(503, {"message": "serviço fora"}))
        assert isinstance(err, ServerError)
        assert err.code == 503


class TestTooManyRequestsCreditHeaders:
    """Regression: créditos extraídos dos headers x-credit-required/remaining."""

    def test_parses_credit_headers(self) -> None:
        err = APIError.from_response(
            _response(
                429,
                {"message": "sem créditos"},
                {"x-credit-required": "5", "x-credit-remaining": "2"},
            )
        )
        assert isinstance(err, TooManyRequestsError)
        assert err.required == 5
        assert err.remaining == 2

    def test_missing_credit_headers_is_safe(self) -> None:
        err = APIError.from_response(_response(429, {"message": "rate limit"}))
        assert isinstance(err, TooManyRequestsError)
        assert err.required is None
        assert err.remaining is None

    def test_invalid_credit_header_values_dont_crash(self) -> None:
        err = APIError.from_response(
            _response(
                429,
                {"message": "limit"},
                {"x-credit-required": "not-a-number"},
            )
        )
        assert isinstance(err, TooManyRequestsError)
        assert err.required is None


class TestTraceIdCapture:
    def test_trace_id_from_header(self) -> None:
        err = APIError.from_response(_response(400, headers={"x-trace-id": "abc-123"}))
        assert err.trace_id == "abc-123"

    def test_trace_id_absent(self) -> None:
        err = APIError.from_response(_response(400))
        assert err.trace_id is None


class TestNonJsonFallback:
    def test_html_response_falls_back_to_text(self) -> None:
        resp = httpx.Response(status_code=502, text="<html>Bad Gateway</html>")
        err = APIError.from_response(resp)
        assert err.message == "<html>Bad Gateway</html>"
        assert err.constraints == []


class TestRaiseForResponse:
    def test_success_is_silent(self) -> None:
        APIError.raise_for_response(_response(200, {"ok": True}))

    def test_failure_raises_subclass(self) -> None:
        with pytest.raises(NotFoundError):
            APIError.raise_for_response(_response(404))

    def test_429_raises_with_credits(self) -> None:
        with pytest.raises(TooManyRequestsError) as exc:
            APIError.raise_for_response(
                _response(429, headers={"x-credit-required": "3", "x-credit-remaining": "0"})
            )
        assert exc.value.required == 3
        assert exc.value.remaining == 0
