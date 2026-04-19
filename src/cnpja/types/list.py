"""DTOs do recurso List (Listas de CNPJs)."""

from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field

from .._common import BaseModel, BaseParams
from ._enums import CacheStrategy, State


class ListQueryDto(BaseModel):
    """Query de filtros da lista.

    Aceita o conjunto completo de filtros do endpoint `/list` (mesmos filtros
    de `OfficeSearchParams`). `extra="allow"` permite usar qualquer alias
    documentado da API sem precisar atualizar este DTO.
    """

    model_config = ConfigDict(extra="allow")


class ListLinkDto(BaseModel):
    """Link de arquivo da lista."""

    type: Literal["EXCEL", "JSON_ZIP"]
    """Tipo do link."""
    url: str
    """URL do arquivo."""


class ListJobOptionsDto(BaseModel):
    """Opções do job de exportação."""

    simples: bool | None = None
    """Incluir informações do Simples Nacional."""
    simples_history: bool | None = Field(None, alias="simplesHistory")
    """Incluir histórico do Simples Nacional."""
    registrations: list[State] | None = None
    """Inscrições Estaduais a consultar."""
    registrations_source: Literal["AUTO", "CCC", "SINTEGRA"] | None = Field(
        None, alias="registrationsSource"
    )
    """Fonte das Inscrições Estaduais."""
    suframa: bool | None = None
    """Incluir informações SUFRAMA."""
    geocoding: bool | None = None
    """Incluir geocodificação."""
    strategy: CacheStrategy | None = None
    """Estratégia de cache."""
    max_age: int | None = Field(None, alias="maxAge")
    """Idade máxima do cache em dias (1-3650)."""
    max_stale: int | None = Field(None, alias="maxStale")
    """Idade máxima aceita em caso de erro, em dias (1-3650)."""


class ListDto(BaseModel):
    """Informações da lista de CNPJs."""

    id: str
    """Identificador da lista (UUID)."""
    created: str
    """Data de criação."""
    updated: str
    """Data da última atualização."""
    title: str
    """Título da lista."""
    description: str
    """Descrição da lista."""
    size: int
    """Quantidade de estabelecimentos na lista."""
    items: list[str]
    """Lista de CNPJs."""
    query: ListQueryDto | None = None
    """Query de filtros usada para criar a lista."""
    limit: int | None = None
    """Limite de estabelecimentos."""


class ListSummaryDto(BaseModel):
    """Resumo da lista (usado em páginas de listagem)."""

    id: str
    """Identificador da lista (UUID)."""
    created: str
    """Data de criação."""
    updated: str
    """Data da última atualização."""
    title: str
    """Título da lista."""
    description: str
    """Descrição da lista."""
    size: int
    """Quantidade de estabelecimentos na lista."""
    query: ListQueryDto | None = None
    """Query de filtros usada para criar a lista."""
    limit: int | None = None
    """Limite de estabelecimentos."""


class ListExportIdDto(BaseModel):
    """Identificador da exportação."""

    id: str
    """Identificador da exportação (UUID)."""


class ListExportDto(BaseModel):
    """Informações da exportação da lista."""

    id: str
    """Identificador da exportação (UUID)."""
    created: str
    """Data de criação."""
    updated: str
    """Data da última atualização."""
    status: Literal["PENDING", "PROCESSING", "PROCESSED", "EXPORTING", "COMPLETED", "FAILED"]
    """Status da exportação."""
    status_reason: str | None = Field(None, alias="statusReason")
    """Motivo do status."""
    progress: float
    """Progresso da exportação (0-100)."""
    options: ListJobOptionsDto
    """Opções de exportação."""
    links: list[ListLinkDto]
    """Links para download."""


class ListPageDto(BaseModel):
    """Página de resultados de pesquisa de listas."""

    next: str | None = None
    """Token da próxima página."""
    limit: int
    """Quantidade de registros lidos."""
    count: int
    """Quantidade de registros disponíveis."""
    records: list[ListSummaryDto]
    """Lista de resumos de listas."""


class ListExportPageDto(BaseModel):
    """Página de resultados de exportações."""

    next: str | None = None
    """Token da próxima página."""
    limit: int
    """Quantidade de registros lidos."""
    count: int
    """Quantidade de registros disponíveis."""
    records: list[ListExportDto]
    """Lista de exportações."""


# ============================================================================
# Parâmetros de Requisição
# ============================================================================


class ListCreateParams(BaseParams):
    """Parâmetros para criação de lista."""

    title: str
    """Título da lista."""
    description: str | None = None
    """Descrição da lista."""
    limit: int | None = None
    """Limite de estabelecimentos."""
    items: list[str] | None = None
    """Lista de CNPJs a incluir."""
    query: ListQueryDto | None = None
    """Query de filtros para pesquisa."""


class ListUpdateParams(BaseParams):
    """Parâmetros para atualização de lista."""

    title: str | None = None
    """Novo título da lista."""
    description: str | None = None
    """Nova descrição da lista."""
    items: list[str] | None = None
    """Nova lista de CNPJs (substitui a lista atual)."""


class ListSearchParams(BaseParams):
    """Parâmetros para pesquisa de listas."""

    token: str | None = None
    """Token da página."""
    limit: int | None = None
    """Limite de resultados."""
    search: str | None = None
    """Termo a ser pesquisado no título ou descrição."""


class ListExportCreateParams(BaseParams):
    """Parâmetros para criação de exportação."""

    options: ListJobOptionsDto | None = None
    """Opções de exportação."""


class ListExportSearchParams(BaseParams):
    """Parâmetros para pesquisa de exportações."""

    token: str | None = None
    """Token da página."""
    limit: int | None = None
    """Limite de resultados."""
