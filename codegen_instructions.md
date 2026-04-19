# Codegen Instructions

Este documento descreve como os schemas da API e os tipos Pydantic do SDK são mantidos.

## Fonte de verdade

O contrato oficial da API CNPJá é publicado pela própria CNPJá em:

- **Referência OpenAPI**: https://cnpja.com/api/reference

O snapshot do OpenAPI **não é versionado** neste repositório (está no `.gitignore` como `schemas/`) porque:

1. O artefato pertence à CNPJá — não queremos redistribuir IP sem autorização explícita.
2. A fonte oficial é única (acima) — manter cópia local aumenta risco de drift silencioso.
3. O `sdk-nodejs` segue o mesmo padrão: o schema é obtido via fetch durante o codegen.

## Fluxo de sincronização

Quando a API CNPJá for atualizada (ou ao realinhar os DTOs):

1. Baixar o OpenAPI atual para `schemas/openapi.json` (diretório é gitignored):
   ```bash
   mkdir -p schemas
   curl -sSL <url-do-openapi-fornecida-pela-cnpja> -o schemas/openapi.json
   ```
2. Comparar com `src/cnpja/types/` e atualizar os DTOs manualmente (ou via codegen — ver seção abaixo).
3. Rodar os quality gates:
   ```bash
   task qa
   ```
4. Commitar as mudanças de tipos (sem incluir `schemas/`):
   ```bash
   git commit -m "feat(types): atualiza DTOs para openapi $(date +%Y-%m-%d)"
   ```

## Ferramenta de codegen

> **TODO:** formalizar pipeline automatizado.
>
> Candidatos avaliados para geração automática a partir do OpenAPI:
> - [`datamodel-code-generator`](https://koxudaxi.github.io/datamodel-code-generator/) — gera modelos Pydantic v2 diretamente.
> - [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) — gera client completo (requer mais ajuste no output).
>
> Enquanto o processo não está automatizado, alterações nos tipos devem ser feitas manualmente com revisão contra o schema baixado em `schemas/`.

## Relaxamentos intencionais

Alguns DTOs relaxam nullability em relação ao OpenAPI porque a API em produção retorna `null` onde o schema declara obrigatório. Esses relaxamentos são testes de regressão em `tests/test_types.py`:

- `MemberDto.since: str | None`
- `RfbMemberDto.since: str | None`
- `PersonMemberDto.since: str | None`
- `PersonDto.id: str | None`
- `PersonBaseDto.id: str | None`
- `AddressDto.details: str | None`
- `SimplesSimeiDto.since: str | None`
- `SimplesSimeiHistoryDto.*` (todos opcionais)
- `OfficeDto.alias: str | None`
- `OfficeSuframaDto.since`, `approval_date: str | None`
- `RegistrationDto.status_date: str | None`
- `CccDto.updated: str | None`

Se o OpenAPI for atualizado reforçando esses campos como obrigatórios, **não regredir** — a realidade da API em produção tem prioridade.
