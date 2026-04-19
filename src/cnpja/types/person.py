"""DTOs do recurso Person (Pessoas/Sócios)."""

from __future__ import annotations

from pydantic import Field

from .._common import BaseModel, BaseParams
from ._enums import AgeRange, PersonType, State
from .common import (
    CompanySizeDto,
    CountryDto,
    MemberAgentDto,
    NatureDto,
    RoleDto,
)


class PersonMemberCompanyDto(BaseModel):
    """Informações da empresa da qual a pessoa é sócia."""

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


class PersonMemberDto(BaseModel):
    """Informações da participação societária."""

    since: str | None = None
    """Data de entrada na sociedade."""
    role: RoleDto
    """Informações da qualificação."""
    agent: MemberAgentDto | None = None
    """Informações do representante legal."""
    company: PersonMemberCompanyDto
    """Informações da empresa."""


class PersonDto(BaseModel):
    """Informações da pessoa."""

    id: str | None = None
    """Código da pessoa (UUID)."""
    type: PersonType
    """Tipo da pessoa."""
    name: str
    """Nome ou razão social."""
    tax_id: str | None = None
    """CPF ou CNPJ."""
    age: AgeRange | None = None
    """Faixa etária."""
    country: CountryDto | None = None
    """País de origem."""
    membership: list[PersonMemberDto]
    """Lista de sociedades participantes."""


class PersonPageDto(BaseModel):
    """Página de resultados de pesquisa de pessoas."""

    next: str | None = None
    """Token da próxima página."""
    limit: int
    """Quantidade de registros lidos."""
    count: int
    """Quantidade de registros disponíveis."""
    records: list[PersonDto] = Field(default_factory=list)
    """Lista de pessoas."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class PersonSearchParams(BaseParams):
    """Parâmetros para pesquisa de pessoas."""

    # Filtros de pessoa
    name_in: list[str] | None = Field(None, alias="name.in")
    name_nin: list[str] | None = Field(None, alias="name.nin")
    type_in: list[PersonType] | None = Field(None, alias="type.in")
    tax_id_in: list[str] | None = Field(None, alias="taxId.in")
    age_in: list[AgeRange] | None = Field(None, alias="age.in")
    country_id_in: list[int] | None = Field(None, alias="country.id.in")
    country_id_nin: list[int] | None = Field(None, alias="country.id.nin")

    # Filtros de sociedade
    role_id_in: list[int] | None = Field(None, alias="role.id.in")
    role_id_nin: list[int] | None = Field(None, alias="role.id.nin")
    since_gte: str | None = Field(None, alias="since.gte")
    since_lte: str | None = Field(None, alias="since.lte")

    # Filtros de empresa
    company_equity_gte: float | None = Field(None, alias="company.equity.gte")
    company_equity_lte: float | None = Field(None, alias="company.equity.lte")
    company_nature_id_in: list[int] | None = Field(None, alias="company.nature.id.in")
    company_nature_id_nin: list[int] | None = Field(None, alias="company.nature.id.nin")
    company_size_id_in: list[int] | None = Field(None, alias="company.size.id.in")

    # Filtros de estabelecimento
    office_head_eq: bool | None = Field(None, alias="office.head.eq")
    office_status_id_in: list[int] | None = Field(None, alias="office.status.id.in")
    office_address_municipality_in: list[int] | None = Field(
        None, alias="office.address.municipality.in"
    )
    office_address_city_in: list[str] | None = Field(None, alias="office.address.city.in")
    office_address_state_in: list[State] | None = Field(None, alias="office.address.state.in")

    # Filtros de atividade
    office_main_activity_id_in: list[int] | None = Field(None, alias="office.mainActivity.id.in")
    office_main_activity_id_nin: list[int] | None = Field(None, alias="office.mainActivity.id.nin")

    # Paginação
    token: str | None = None
    limit: int | None = None
