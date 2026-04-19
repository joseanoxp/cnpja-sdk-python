# Changelog

## 1.0.0 (2026-04-19)


### Features

* Implementação inicial do SDK Python para a API CNPJá, com paridade funcional completa ao `sdk-nodejs` oficial
* Client síncrono (`Client`) e assíncrono (`AsyncClient`, acessível via `.aio`)
* Client público `CnpjaOpen` (sem autenticação) apontando para `https://open.cnpja.com`
* 10 resources (`office`, `company`, `person`, `rfb`, `simples`, `ccc`, `suframa`, `zip`, `list`, `credit`) com pares sync/async
* Recurso dedicado `OpenOfficeResource` com superfície reduzida (apenas `read`) para a API pública
* Paginação automática via `Pager` e `AsyncPager` — `pager.page` (sync property) / `await pager.page()` (async method)
* Retry automático com backoff exponencial + jitter (códigos 429/5xx e erros de transporte)
* Endpoints binários (PDF, imagens) via `get_binary` / `aget_binary` com tipagem correta `-> bytes`
* Overloads em `HttpClient` para distinção `response_model: type[T] -> T` vs. `None -> bytes | dict[str, Any]`
* Hierarquia de erros (`APIError`, `ClientError`, `ServerError`, `BadRequestError`, `UnauthorizedError`, `NotFoundError`, `TooManyRequestsError`)
* Parsing automático de créditos restantes (`required`, `remaining`) a partir dos headers `x-credit-required` / `x-credit-remaining`
* Captura do `trace_id` a partir do header `x-trace-id`
* Tipos Pydantic v2 em modo strict com campos nullable realistas (`MemberDto.since`, `PersonDto.id`, `OfficeDto.alias`, etc.)
* Serialização correta de enums em query params (`State.SP -> "SP"`) via `use_enum_values=True` no `BaseParams`


### Documentation

* `README.md` com exemplos de uso sync, async, paginação e API pública
* `CONTRIBUTING.md` com fluxo GitHub Flow, convenções de branch/commit e tabela de comandos
* `CLAUDE.md` e `.github/copilot-instructions.md` para agentes de IA
* `SECURITY.md` com política de vulnerabilidades
* `codegen_instructions.md` com o pipeline de sincronização DTOs ↔ OpenAPI


### Quality & Tooling

* Cobertura de testes: **131 testes, 96% branch+line** (respx como mock transport)
* `mypy --strict` sem erros em 34 arquivos; `ruff check` + `ruff format` limpo
* Quality gate local via `task qa` (lockfile, lint, format, typecheck, tests, pre-commit)
* CI `Quality Control` em cada PR: lint, format, typecheck, tests, pre-commit, upload de `coverage.xml`, validação de Conventional Commits no título e nos commits da branch
* Release automatizado via `release-please-action@v4` (bump de versão + CHANGELOG + tag)
* Dependabot configurado para `uv` e `github-actions` com grupos separados e prefixos convencionais
* Pre-commit com ruff + commitizen + validação de nome de branch (`scripts/check_branch_name.py`)
* `Taskfile.yml`, `.editorconfig`, `.vscode/settings.json`, `.devcontainer/` e `.gitattributes` para padronização
