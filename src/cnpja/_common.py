"""BaseModel customizado para DTOs e parâmetros do SDK CNPJá."""

from __future__ import annotations

import pydantic
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class BaseModel(pydantic.BaseModel):
    """Modelo base para DTOs de resposta.

    Converte automaticamente snake_case ↔ camelCase na serialização JSON
    e rejeita campos desconhecidos (contrato estrito com a API).
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
        from_attributes=True,
    )


class BaseParams(BaseModel):
    """Modelo base para parâmetros de requisição.

    Permite campos extras (filtros dinâmicos) e serializa enums pelo seu
    ``.value`` para compatibilidade com query params da API.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
        from_attributes=True,
        use_enum_values=True,
    )
