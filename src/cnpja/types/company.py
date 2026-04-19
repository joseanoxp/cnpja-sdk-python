"""DTOs do recurso Company (Empresas)."""

from __future__ import annotations

from .._common import BaseModel
from .common import (
    ActivityDto,
    AddressDto,
    CompanySizeDto,
    EmailDto,
    NatureDto,
    OfficeStatusDto,
    PhoneDto,
    SimplesSimeiDto,
)
from .office import MemberDto


class CompanyOfficeDto(BaseModel):
    """Informações do estabelecimento da empresa."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
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
    address: AddressDto | None = None
    """Informações do endereço."""
    phones: list[PhoneDto] | None = None
    """Lista de telefones."""
    emails: list[EmailDto] | None = None
    """Lista de e-mails."""
    main_activity: ActivityDto | None = None
    """Atividade econômica principal."""


class CompanyDto(BaseModel):
    """Informações da empresa."""

    id: int
    """Código da empresa (8 primeiros dígitos do CNPJ)."""
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
    simples: SimplesSimeiDto | None = None
    """Informações da opção pelo Simples Nacional."""
    simei: SimplesSimeiDto | None = None
    """Informações do enquadramento no MEI."""
    members: list[MemberDto]
    """Quadro de sócios e administradores."""
    offices: list[CompanyOfficeDto]
    """Lista de estabelecimentos."""
