"""DTOs do recurso Office (Estabelecimentos/CNPJ)."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy, EmailOwnership, PhoneType, State
from .common import (
    ActivityDto,
    AddressDto,
    CompanySizeDto,
    EmailDto,
    MemberAgentDto,
    NatureDto,
    OfficeLinkDto,
    OfficeReasonDto,
    OfficeSpecialDto,
    OfficeStatusDto,
    OfficeSuframaDto,
    PersonBaseDto,
    PhoneDto,
    RegistrationDto,
    RoleDto,
    SimplesSimeiDto,
)


class MemberDto(BaseModel):
    """Informações do sócio ou administrador."""

    since: str | None = None
    """Data de entrada na sociedade."""
    person: PersonBaseDto
    """Informações do sócio ou administrador."""
    role: RoleDto
    """Informações da qualificação."""
    agent: MemberAgentDto | None = None
    """Informações do representante legal."""


class OfficeCompanyDto(BaseModel):
    """Informações da empresa do estabelecimento."""

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


class OfficeDto(BaseModel):
    """Informações do estabelecimento (CNPJ)."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
    updated: str
    """Data da última atualização."""
    company: OfficeCompanyDto
    """Informações da empresa."""
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
    registrations: list[RegistrationDto] | None = None
    """Inscrições Estaduais."""
    suframa: list[OfficeSuframaDto] | None = None
    """Lista de inscrições SUFRAMA."""
    links: list[OfficeLinkDto] | None = None
    """Lista de links para arquivos."""


class OfficePageRecordDto(BaseModel):
    """Registro de estabelecimento em página de resultados."""

    tax_id: str
    """Número do CNPJ sem pontuação."""
    updated: str
    """Data da última atualização."""
    company: OfficeCompanyDto
    """Informações da empresa."""
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


class OfficePageDto(BaseModel):
    """Página de resultados de pesquisa de estabelecimentos."""

    next: str | None = None
    """Token da próxima página."""
    limit: int
    """Quantidade de registros lidos."""
    count: int
    """Quantidade de registros disponíveis."""
    records: list[OfficePageRecordDto] = Field(default_factory=list)
    """Lista de estabelecimentos."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class OfficeReadParams(BaseParams):
    """Parâmetros para consulta de estabelecimento."""

    tax_id: str
    """Número do CNPJ."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = None
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = None
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""
    simples: bool | None = None
    """Incluir informações do Simples Nacional."""
    simples_history: bool | None = None
    """Incluir histórico do Simples Nacional."""
    registrations: list[State | Literal["ORIGIN", "ALL"]] | None = None
    """Inscrições Estaduais a consultar."""
    registrations_source: Literal["AUTO", "CCC", "SINTEGRA"] | None = None
    """Fonte das Inscrições Estaduais (AUTO, CCC ou SINTEGRA)."""
    suframa: bool | None = None
    """Incluir informações SUFRAMA."""
    geocoding: bool | None = None
    """Incluir geocodificação."""
    links: list[str] | None = None
    """Links de arquivos a incluir."""
    sync: bool | None = None
    """Aguarda compensação síncrona dos créditos (cabeçalho cnpja-request-cost)."""


class OfficeSearchParams(BaseParams):
    """Parâmetros para pesquisa de estabelecimentos.

    Suporta filtros dinâmicos no formato "campo.operador".
    Exemplo: {"address.state.in": ["SP", "RJ"], "status.id.in": [2]}
    """

    # Filtros de nome
    names_in: list[str] | None = Field(None, alias="names.in")
    names_nin: list[str] | None = Field(None, alias="names.nin")
    company_name_in: list[str] | None = Field(None, alias="company.name.in")
    company_name_nin: list[str] | None = Field(None, alias="company.name.nin")
    alias_in: list[str] | None = Field(None, alias="alias.in")
    alias_nin: list[str] | None = Field(None, alias="alias.nin")

    # Filtros de empresa
    company_equity_gte: float | None = Field(None, alias="company.equity.gte")
    company_equity_lte: float | None = Field(None, alias="company.equity.lte")
    company_nature_id_in: list[int] | None = Field(None, alias="company.nature.id.in")
    company_nature_id_nin: list[int] | None = Field(None, alias="company.nature.id.nin")
    company_size_id_in: list[int] | None = Field(None, alias="company.size.id.in")

    # Filtros de Simples/SIMEI
    company_simples_optant_eq: bool | None = Field(None, alias="company.simples.optant.eq")
    company_simples_since_gte: str | None = Field(None, alias="company.simples.since.gte")
    company_simples_since_lte: str | None = Field(None, alias="company.simples.since.lte")
    company_simei_optant_eq: bool | None = Field(None, alias="company.simei.optant.eq")
    company_simei_since_gte: str | None = Field(None, alias="company.simei.since.gte")
    company_simei_since_lte: str | None = Field(None, alias="company.simei.since.lte")

    # Filtros de estabelecimento
    tax_id_nin: list[str] | None = Field(None, alias="taxId.nin")
    founded_gte: str | None = Field(None, alias="founded.gte")
    founded_lte: str | None = Field(None, alias="founded.lte")
    head_eq: bool | None = Field(None, alias="head.eq")

    # Filtros de situação
    status_date_gte: str | None = Field(None, alias="statusDate.gte")
    status_date_lte: str | None = Field(None, alias="statusDate.lte")
    status_id_in: list[int] | None = Field(None, alias="status.id.in")
    reason_id_in: list[int] | None = Field(None, alias="reason.id.in")
    special_date_gte: str | None = Field(None, alias="specialDate.gte")
    special_date_lte: str | None = Field(None, alias="specialDate.lte")
    special_id_in: list[int] | None = Field(None, alias="special.id.in")

    # Filtros de endereço
    address_municipality_in: list[int] | None = Field(None, alias="address.municipality.in")
    address_municipality_nin: list[int] | None = Field(None, alias="address.municipality.nin")
    address_street_in: list[str] | None = Field(None, alias="address.street.in")
    address_street_nin: list[str] | None = Field(None, alias="address.street.nin")
    address_number_in: list[str] | None = Field(None, alias="address.number.in")
    address_number_nin: list[str] | None = Field(None, alias="address.number.nin")
    address_details_in: list[str] | None = Field(None, alias="address.details.in")
    address_details_nin: list[str] | None = Field(None, alias="address.details.nin")
    address_district_in: list[str] | None = Field(None, alias="address.district.in")
    address_district_nin: list[str] | None = Field(None, alias="address.district.nin")
    address_state_in: list[State] | None = Field(None, alias="address.state.in")
    address_state_nin: list[State] | None = Field(None, alias="address.state.nin")
    address_zip_in: list[str] | None = Field(None, alias="address.zip.in")
    address_zip_gte: str | None = Field(None, alias="address.zip.gte")
    address_zip_lte: str | None = Field(None, alias="address.zip.lte")
    address_country_id_in: list[int] | None = Field(None, alias="address.country.id.in")
    address_country_id_nin: list[int] | None = Field(None, alias="address.country.id.nin")

    # Filtros de atividade
    activities_id_in: list[int] | None = Field(None, alias="activities.id.in")
    activities_id_nin: list[int] | None = Field(None, alias="activities.id.nin")
    main_activity_id_in: list[int] | None = Field(None, alias="mainActivity.id.in")
    main_activity_id_nin: list[int] | None = Field(None, alias="mainActivity.id.nin")
    side_activities_id_in: list[int] | None = Field(None, alias="sideActivities.id.in")
    side_activities_id_nin: list[int] | None = Field(None, alias="sideActivities.id.nin")

    # Filtros de telefone
    phones_ex: bool | None = Field(None, alias="phones.ex")
    phones_type_in: list[PhoneType] | None = Field(None, alias="phones.type.in")
    phones_area_in: list[str] | None = Field(None, alias="phones.area.in")
    phones_area_gte: str | None = Field(None, alias="phones.area.gte")
    phones_area_lte: str | None = Field(None, alias="phones.area.lte")
    phones_number_in: list[str] | None = Field(None, alias="phones.number.in")
    phones_number_nin: list[str] | None = Field(None, alias="phones.number.nin")

    # Filtros de e-mail
    emails_ex: bool | None = Field(None, alias="emails.ex")
    emails_ownership_in: list[EmailOwnership] | None = Field(None, alias="emails.ownership.in")
    emails_address_in: list[str] | None = Field(None, alias="emails.address.in")
    emails_address_nin: list[str] | None = Field(None, alias="emails.address.nin")
    emails_domain_in: list[str] | None = Field(None, alias="emails.domain.in")
    emails_domain_nin: list[str] | None = Field(None, alias="emails.domain.nin")

    # Paginação
    token: str | None = None
    limit: int | None = None


class OfficeMapParams(BaseParams):
    """Parâmetros para geração de mapa aéreo."""

    tax_id: str
    """Número do CNPJ."""
    width: int | None = None
    """Largura da imagem em pixels (80-640)."""
    height: int | None = None
    """Altura da imagem em pixels (80-640)."""
    scale: int | None = None
    """Multiplicador de densidade de pixels (1-2)."""
    zoom: int | None = None
    """Nível de ampliação (1-20, padrão 17)."""
    type: Literal["roadmap", "terrain", "satellite", "hybrid"] | None = None
    """Tipo do mapa (padrão: roadmap)."""


class OfficeStreetParams(BaseParams):
    """Parâmetros para geração de visão de rua."""

    tax_id: str
    """Número do CNPJ."""
    width: int | None = None
    """Largura da imagem em pixels."""
    height: int | None = None
    """Altura da imagem em pixels."""
    fov: int | None = None
    """Campo de visão."""
    pitch: int | None = None
    """Inclinação vertical."""
    heading: int | None = None
    """Direção horizontal."""
