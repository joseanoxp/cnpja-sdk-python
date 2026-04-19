"""DTOs do recurso SUFRAMA."""

from __future__ import annotations

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy
from .common import (
    AddressDto,
    EmailDto,
    NatureDto,
    PhoneDto,
    SuframaActivityDto,
    SuframaIncentiveDto,
    SuframaStatusDto,
)


class SuframaDto(BaseModel):
    """Informações da consulta SUFRAMA."""

    tax_id: str
    """Número do CNPJ ou CPF sem pontuação."""
    updated: str
    """Data da última atualização."""
    number: str
    """Número da inscrição SUFRAMA."""
    name: str
    """Razão social."""
    since: str | None = None
    """Data de inscrição na SUFRAMA."""
    head: bool
    """Indica se o estabelecimento é a Matriz."""
    approved: bool
    """Indica se o projeto está aprovado."""
    approval_date: str | None = None
    """Data de aprovação do projeto."""
    status: SuframaStatusDto
    """Informações da situação cadastral."""
    nature: NatureDto
    """Informações da natureza jurídica."""
    address: AddressDto
    """Informações do endereço."""
    phones: list[PhoneDto]
    """Lista de telefones."""
    emails: list[EmailDto]
    """Lista de e-mails."""
    main_activity: SuframaActivityDto
    """Informações da atividade econômica principal."""
    side_activities: list[SuframaActivityDto]
    """Lista de atividades econômicas secundárias."""
    incentives: list[SuframaIncentiveDto]
    """Lista de incentivos fiscais."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class SuframaReadParams(BaseParams):
    """Parâmetros para consulta SUFRAMA."""

    tax_id: str
    """Número do CNPJ ou CPF."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
    sync: bool | None = None
    """Aguarda compensação síncrona dos créditos (cabeçalho cnpja-request-cost)."""


class SuframaCertificateParams(BaseParams):
    """Parâmetros para emissão de comprovante SUFRAMA."""

    tax_id: str
    """Número do CNPJ ou CPF."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
