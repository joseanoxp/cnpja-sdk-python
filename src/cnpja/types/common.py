"""DTOs comuns compartilhados entre recursos."""

from __future__ import annotations

from pydantic import Field

from .._common import BaseModel
from ._enums import (
    AgeRange,
    EmailOwnership,
    OfficeLinkType,
    PersonType,
    PhoneType,
    State,
    SuframaTribute,
)


class CountryDto(BaseModel):
    """Informações do país."""

    id: int
    """Código do país conforme M49."""
    name: str
    """Nome do país."""


class AddressDto(BaseModel):
    """Informações do endereço."""

    municipality: int
    """Código do município conforme IBGE."""
    street: str
    """Logradouro."""
    number: str
    """Número."""
    district: str
    """Bairro ou distrito."""
    city: str
    """Município."""
    state: State
    """Sigla da Unidade Federativa."""
    details: str | None = None
    """Complemento."""
    zip: str
    """Código de Endereçamento Postal."""
    latitude: float | None = None
    """Latitude."""
    longitude: float | None = None
    """Longitude."""
    country: CountryDto
    """Informações do país."""


class PhoneDto(BaseModel):
    """Informações do telefone."""

    type: PhoneType
    """Tipo do telefone."""
    area: str
    """Código de DDD."""
    number: str
    """Número."""


class EmailDto(BaseModel):
    """Informações do e-mail."""

    ownership: EmailOwnership
    """Tipo de propriedade do e-mail."""
    address: str
    """Endereço de e-mail."""
    domain: str
    """Domínio de registro."""


class NatureDto(BaseModel):
    """Informações da natureza jurídica."""

    id: int
    """Código da natureza jurídica conforme IBGE."""
    text: str
    """Descrição da natureza jurídica."""


class ActivityDto(BaseModel):
    """Informações da atividade econômica (CNAE)."""

    id: int
    """Código da atividade econômica conforme IBGE."""
    text: str
    """Descrição da atividade econômica."""


class RoleDto(BaseModel):
    """Informações da qualificação do sócio."""

    id: int
    """Código da qualificação conforme Receita Federal."""
    text: str
    """Descrição da qualificação."""


class CompanySizeDto(BaseModel):
    """Informações do porte da empresa."""

    id: int
    """Código do porte."""
    acronym: str
    """Sigla do porte."""
    text: str
    """Descrição do porte."""


class OfficeStatusDto(BaseModel):
    """Informações da situação cadastral do estabelecimento."""

    id: int
    """Código da situação cadastral."""
    text: str
    """Descrição da situação cadastral."""


class OfficeReasonDto(BaseModel):
    """Informações do motivo da situação cadastral."""

    id: int
    """Código do motivo da situação cadastral."""
    text: str
    """Descrição do motivo da situação cadastral."""


class OfficeSpecialDto(BaseModel):
    """Informações da situação especial."""

    id: int
    """Código da situação especial."""
    text: str
    """Descrição da situação especial."""


class PersonBaseDto(BaseModel):
    """Informações básicas da pessoa."""

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


class MemberAgentDto(BaseModel):
    """Informações do representante legal."""

    person: PersonBaseDto
    """Informações da pessoa representante legal."""
    role: RoleDto
    """Informações da qualificação do representante legal."""


class SimplesSimeiHistoryDto(BaseModel):
    """Histórico de períodos anteriores Simples/SIMEI."""

    from_: str | None = Field(None, alias="from")
    """Data de início do período."""
    until: str | None = None
    """Data de término do período."""
    text: str | None = None
    """Motivo de encerramento."""


class SimplesSimeiDto(BaseModel):
    """Informações da opção pelo Simples Nacional ou enquadramento no MEI."""

    optant: bool
    """Indica se optante ou enquadrado."""
    since: str | None = None
    """Data de inclusão no período vigente."""
    history: list[SimplesSimeiHistoryDto] | None = None
    """Histórico de períodos anteriores."""


class RegistrationStatusDto(BaseModel):
    """Situação cadastral da Inscrição Estadual."""

    id: int
    """Código da situação cadastral."""
    text: str
    """Descrição da situação cadastral."""


class RegistrationTypeDto(BaseModel):
    """Tipo da Inscrição Estadual."""

    id: int
    """Código do tipo."""
    text: str
    """Descrição do tipo."""


class RegistrationDto(BaseModel):
    """Informações da Inscrição Estadual."""

    number: str
    """Número da Inscrição Estadual."""
    state: State
    """Unidade Federativa de registro."""
    enabled: bool
    """Indica se habilitada como contribuinte."""
    status_date: str | None = None
    """Data da situação cadastral."""
    status: RegistrationStatusDto
    """Situação cadastral da inscrição."""
    type: RegistrationTypeDto
    """Tipo da inscrição."""


class SuframaStatusDto(BaseModel):
    """Informações da situação cadastral SUFRAMA."""

    id: int
    """Código da situação cadastral."""
    text: str
    """Descrição da situação cadastral."""


class SuframaActivityDto(BaseModel):
    """Atividade econômica SUFRAMA."""

    id: int
    """Código da atividade econômica."""
    text: str
    """Descrição da atividade econômica."""
    performed: bool
    """Indica se a atividade é exercida."""


class SuframaIncentiveDto(BaseModel):
    """Incentivo fiscal SUFRAMA."""

    tribute: SuframaTribute
    """Nome do tributo incentivado."""
    benefit: str
    """Benefício aplicado ao incentivo."""
    purpose: str
    """Finalidade do incentivo."""
    basis: str
    """Base legal do incentivo."""


class OfficeSuframaDto(BaseModel):
    """Informações da inscrição SUFRAMA do estabelecimento."""

    number: str
    """Número da inscrição SUFRAMA."""
    since: str | None = None
    """Data de inscrição na SUFRAMA."""
    approved: bool
    """Indica se o projeto está aprovado."""
    approval_date: str | None = None
    """Data de aprovação do projeto."""
    status: SuframaStatusDto
    """Informações da situação cadastral."""
    incentives: list[SuframaIncentiveDto]
    """Lista de incentivos fiscais."""


class OfficeLinkDto(BaseModel):
    """Link para arquivo."""

    type: OfficeLinkType
    """Tipo de arquivo a qual o link se refere."""
    url: str
    """URL pública de acesso ao arquivo."""
