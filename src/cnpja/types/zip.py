"""DTOs do recurso ZIP (CEP)."""

from __future__ import annotations

from .._common import BaseModel
from ._enums import State


class ZipDto(BaseModel):
    """Informações do CEP."""

    updated: str
    """Data da última atualização."""
    municipality: int
    """Código do município conforme IBGE."""
    code: str
    """Código de Endereçamento Postal."""
    street: str | None = None
    """Logradouro."""
    number: str | None = None
    """Número."""
    district: str | None = None
    """Bairro ou distrito."""
    city: str
    """Município."""
    state: State
    """Sigla da Unidade Federativa."""
