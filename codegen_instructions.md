# Codegen Instructions

Este documento descreve como os schemas da API e os tipos Pydantic do SDK são mantidos.

## Arquivos de origem

Os schemas da API CNPJá ficam em `schemas/`:

- `schemas/openapi.json` — especificação OpenAPI completa da API.
- `schemas/schemas-summary.json` — sumário dos schemas (referência auxiliar).

## Artefatos derivados

Os modelos Pydantic em `src/cnpja/types/` representam o contrato da API e são mantidos em sincronia com `schemas/openapi.json`.

Quando a API for atualizada:

1. Substituir `schemas/openapi.json` (e opcionalmente `schemas-summary.json`) pela versão nova.
2. Regerar ou atualizar `src/cnpja/types/` conforme diff do OpenAPI.
3. Rodar os quality gates:
   ```bash
   uv run ruff check src/
   uv run ruff format --check src/
   uv run mypy src/
   uv run pytest
   ```
4. Commitar as mudanças separadamente:
   ```bash
   git commit -m "feat(types): atualiza DTOs para openapi $(date +%Y-%m-%d)"
   ```

## Ferramenta de codegen

> **TODO:** formalizar o pipeline automatizado.
>
> Candidatos avaliados para geração automática a partir do OpenAPI:
> - [`datamodel-code-generator`](https://koxudaxi.github.io/datamodel-code-generator/) — gera modelos Pydantic v2 diretamente.
> - [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) — gera client completo (requer mais ajuste no output).
>
> Enquanto o processo não está automatizado, alterações nos tipos devem ser feitas manualmente com revisão contra o schema.
