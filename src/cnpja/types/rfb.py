"""DTOs do recurso RFB (Receita Federal)."""

from __future__ import annotations

from typing import Literal

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy
from .common import (
    ActivityDto,
    AddressDto,
    CompanySizeDto,
    EmailDto,
    MemberAgentDto,
    NatureDto,
    OfficeReasonDto,
    OfficeSpecialDto,
    OfficeStatusDto,
    PersonBaseDto,
    PhoneDto,
    RoleDto,
)


class RfbMemberDto(BaseModel):
    """Informações do sócio ou administrador da RFB."""

    since: str | None = None
    """Data de entrada na sociedade."""
    role: RoleDto
    """Informações da qualificação."""
    person: PersonBaseDto
    """Informações do sócio ou administrador."""
    agent: MemberAgentDto | None = None
    """Informações do representante legal."""


class RfbDto(BaseModel):
    """Informações da consulta à Receita Federal."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
    updated: str
    """Data da última atualização."""
    name: str
    """Razão social."""
    jurisdiction: str | None = None
    """Ente federativo responsável."""
    equity: float
    """Capital social."""
    nature: NatureDto
    """Informações da natureza jurídica."""
    size: CompanySizeDto
    """Informações do porte."""
    alias: str | None = None
    """Nome fantasia."""
    founded: str
    """Data de abertura."""
    head: bool
    """Indica se o estabelecimento é a Matriz."""
    status_date: str
    """Data da situação cadastral."""
    status: OfficeStatusDto
    """Informações da situação cadastral."""
    reason: OfficeReasonDto | None = None
    """Informações do motivo da situação cadastral."""
    special_date: str | None = None
    """Data da situação especial."""
    special: OfficeSpecialDto | None = None
    """Informações da situação especial."""
    address: AddressDto
    """Informações do endereço."""
    phones: list[PhoneDto]
    """Lista de telefones."""
    emails: list[EmailDto]
    """Lista de e-mails."""
    main_activity: ActivityDto
    """Informações da atividade econômica principal."""
    side_activities: list[ActivityDto]
    """Lista de atividades econômicas secundárias."""
    members: list[RfbMemberDto]
    """Quadro de sócios e administradores."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class RfbReadParams(BaseParams):
    """Parâmetros para consulta RFB."""

    tax_id: str
    """Número do CNPJ."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
    sync: bool | None = None
    """Aguarda compensação síncrona dos créditos (cabeçalho cnpja-request-cost)."""


class RfbCertificateParams(BaseParams):
    """Parâmetros para emissão de comprovante RFB."""

    tax_id: str
    """Número do CNPJ."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
    pages: list[Literal["REGISTRATION", "MEMBERS"]] | None = None
    """Páginas a incluir no comprovante (padrão: ambas)."""
