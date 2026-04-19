"""Hierarquia de exceções do SDK CNPJá."""

from __future__ import annotations

from typing import Any

import httpx


class CnpjaError(Exception):
    """Erro base do SDK CNPJá."""


class APIError(CnpjaError):
    """Erro retornado pela API CNPJá.

    Attributes:
        code: Código de status HTTP.
        message: Mensagem de erro.
        trace_id: ID de rastreamento da requisição.
        constraints: Lista de erros de validação.
        response: Resposta HTTP original.
    """

    def __init__(
        self,
        code: int,
        message: str,
        *,
        trace_id: str | None = None,
        constraints: list[str] | None = None,
        response: httpx.Response | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.trace_id = trace_id
        self.constraints = constraints or []
        self.response = response
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Formata a mensagem de erro."""
        parts = [f"[{self.code}] {self.message}"]
        if self.constraints:
            parts.append(f"Constraints: {', '.join(self.constraints)}")
        if self.trace_id:
            parts.append(f"Trace ID: {self.trace_id}")
        return " | ".join(parts)

    @classmethod
    def from_response(cls, response: httpx.Response) -> APIError:
        """Cria uma exceção a partir de uma resposta HTTP.

        Args:
            response: Resposta HTTP com erro.

        Returns:
            Instância apropriada de APIError ou subclasse.
        """
        code = response.status_code
        trace_id: str | None = response.headers.get("x-trace-id")

        try:
            data = response.json()
            message = data.get("message", response.reason_phrase or "Unknown error")
            constraints = data.get("constraints", [])
        except Exception:
            message = response.text or response.reason_phrase or "Unknown error"
            constraints = []

        error_class = cls._get_error_class(code)
        return error_class(
            code=code,
            message=message,
            trace_id=trace_id,
            constraints=constraints,
            response=response,
        )

    @classmethod
    def _get_error_class(cls, code: int) -> type[APIError]:
        """Retorna a classe de erro apropriada para o código HTTP."""
        if code == 400:
            return BadRequestError
        elif code == 401:
            return UnauthorizedError
        elif code == 404:
            return NotFoundError
        elif code == 429:
            return TooManyRequestsError
        elif 400 <= code < 500:
            return ClientError
        elif code >= 500:
            return ServerError
        return APIError

    @classmethod
    def raise_for_response(cls, response: httpx.Response) -> None:
        """Levanta exceção se a resposta contém erro.

        Args:
            response: Resposta HTTP para verificar.

        Raises:
            APIError: Se a resposta contém código de erro (>= 400).
        """
        if response.status_code >= 400:
            raise cls.from_response(response)

    def to_dict(self) -> dict[str, Any]:
        """Converte o erro para dicionário."""
        return {
            "code": self.code,
            "message": self.message,
            "trace_id": self.trace_id,
            "constraints": self.constraints,
        }


class ClientError(APIError):
    """Erro do cliente (4xx)."""


class ServerError(APIError):
    """Erro do servidor (5xx)."""


class BadRequestError(ClientError):
    """Erro 400 - Requisição inválida ou validação falhou."""


class UnauthorizedError(ClientError):
    """Erro 401 - Autenticação inválida ou ausente."""


class NotFoundError(ClientError):
    """Erro 404 - Recurso não encontrado."""


class TooManyRequestsError(ClientError):
    """Erro 429 - Créditos insuficientes ou rate limit excedido.

    Attributes:
        required: Quantidade de créditos necessários.
        remaining: Quantidade de créditos restantes.
    """

    def __init__(
        self,
        code: int,
        message: str,
        *,
        trace_id: str | None = None,
        constraints: list[str] | None = None,
        response: httpx.Response | None = None,
    ) -> None:
        super().__init__(
            code=code,
            message=message,
            trace_id=trace_id,
            constraints=constraints,
            response=response,
        )
        self.required: int | None = None
        self.remaining: int | None = None

        if response is not None:
            self._parse_credit_headers(response)

    def _parse_credit_headers(self, response: httpx.Response) -> None:
        """Extrai informações de crédito dos headers."""
        try:
            required = response.headers.get("x-credit-required")
            remaining = response.headers.get("x-credit-remaining")
            if required:
                self.required = int(required)
            if remaining:
                self.remaining = int(remaining)
        except (ValueError, TypeError):
            pass
