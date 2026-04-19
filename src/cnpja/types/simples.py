"""DTOs do recurso Simples (Simples Nacional e MEI)."""

from __future__ import annotations

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy
from .common import SimplesSimeiDto


class SimplesDto(BaseModel):
    """Informações do Simples Nacional e MEI."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
    updated: str
    """Data da última atualização."""
    simples: SimplesSimeiDto
    """Informações da opção pelo Simples Nacional."""
    simei: SimplesSimeiDto
    """Informações do enquadramento no MEI."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class SimplesReadParams(BaseParams):
    """Parâmetros para consulta Simples Nacional."""

    tax_id: str
    """Número do CNPJ."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
    history: bool | None = None
    """Incluir histórico de períodos anteriores."""
    sync: bool | None = None
    """Aguarda compensação síncrona dos créditos (cabeçalho cnpja-request-cost)."""


class SimplesCertificateParams(BaseParams):
    """Parâmetros para emissão de comprovante Simples Nacional."""

    tax_id: str
    """Número do CNPJ."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
