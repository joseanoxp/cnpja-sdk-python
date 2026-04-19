"""DTOs do recurso CCC (Cadastro de Contribuintes)."""

from __future__ import annotations

from typing import Literal

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy, State
from .common import RegistrationDto

# Tipo para estados CCC (inclui valores especiais ORIGIN e ALL)
CccState = Literal[
    "ORIGIN",
    "ALL",
    "AC",
    "AL",
    "AM",
    "AP",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MG",
    "MS",
    "MT",
    "PA",
    "PB",
    "PE",
    "PI",
    "PR",
    "RJ",
    "RN",
    "RO",
    "RR",
    "RS",
    "SC",
    "SP",
    "SE",
    "TO",
]

# Fonte de dados CCC
CccSource = Literal["AUTO", "CCC", "SINTEGRA"]


class CccDto(BaseModel):
    """Informações do Cadastro de Contribuintes."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
    updated: str | None = None
    """Data da última atualização."""
    name: str
    """Razão social."""
    origin_state: State
    """Estado de origem (sede)."""
    registrations: list[RegistrationDto]
    """Lista de Inscrições Estaduais."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class CccReadParams(BaseParams):
    """Parâmetros para consulta CCC."""

    tax_id: str
    """Número do CNPJ ou CPF de produtor rural."""
    states: list[CccState]
    """Estados a consultar. Use 'ORIGIN' para o estado sede ou 'ALL' para todos."""
    source: CccSource | None = None
    """Fonte de dados (AUTO, CCC, SINTEGRA)."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias."""
    max_stale: int | None = None
    """Idade máxima do cache em caso de erro, em dias."""
    sync: bool | None = None
    """Aguarda compensação síncrona dos créditos (cabeçalho cnpja-request-cost)."""


class CccCertificateParams(BaseParams):
    """Parâmetros para emissão de comprovante CCC."""

    tax_id: str
    """Número do CNPJ."""
    state: CccState
    """Estado da Inscrição Estadual."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias."""
    max_stale: int | None = None
    """Idade máxima do cache em caso de erro, em dias."""
