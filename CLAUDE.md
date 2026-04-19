# CNPJá Python SDK

Python SDK for the CNPJá API (CNPJ, CPF, and Brazilian business data). Distributed as a private Git dependency — consumers install with `uv add git+https://github.com/joseanoxp/cnpja-sdk-python --tag vX.Y.Z`.

## Build and Test

- Install: `task setup`
- Quality gate (all checks): `task qa`
- Pre-commit sanity: `task pre-commit`
- Format: `task format`
- Lint: `task lint`
- Type check: `task typecheck`
- Tests: `task test`
- Environment check: `task doctor`

## Tech Stack

- Python 3.12+, Pydantic v2 (strict), httpx, tenacity
- uv (package manager), Taskfile (task runner)
- Ruff (lint + format), mypy strict (type check), pytest + respx (tests)
- pre-commit + commitizen (git hooks)
- release-please (automated versioning and CHANGELOG)

## Code Style

- Line length: 100
- Ruff rules: E, F, I, W
- `mypy strict = true`, `target-version = "py312"`
- Type hints required on all new code
- `from __future__ import annotations` at top of every `.py` file
- Use `uv run` for all Python commands, never `pip` or `python` directly
- `AsyncPager.page()` is a **method**, not a property — call `await pager.page()` with parentheses. Never decorate an `async def` with `@property` (anti-pattern in Python).
- `BaseModel` uses `extra="forbid"` (strict DTOs). `BaseParams` uses `extra="allow"` and `use_enum_values=True` (serializes enums by value in query params).

## Git Conventions

- Branch naming: `type/short-description` (e.g. `feat/office-search`, `fix/pager-null-page`)
- Commit messages and PR titles: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- Merge strategy: **squash merge only** (the PR title becomes the commit in `main`)
- All PRs require 1 approval and passing CI

## Project Structure

- `src/cnpja/` — library source
  - `client.py`, `open_client.py` — public clients (`Client`, `AsyncClient`, `CnpjaOpen`, `AsyncCnpjaOpen`)
  - `_http_client.py` — transport layer (retry, overloads, binary)
  - `resources/` — endpoint-to-method mapping (sync + async twins, plus `open_office.py` for public-only)
  - `types/` — Pydantic DTOs and request params
  - `pagers.py` — `Pager` / `AsyncPager`
  - `errors.py` — exception hierarchy
  - `version.py` — reads from package metadata
- `tests/` — 131 tests, 96% coverage
  - `tests/resources/` — one file per resource
  - `tests/test_{errors,http_client,pager,lifecycle,edge_cases,types}.py` — cross-cutting concerns
  - `tests/conftest.py` — shared fixtures (clients, mock routers, sample payloads)
- `schemas/` — OpenAPI source of truth for DTOs (`openapi.json`, `schemas-summary.json`)
- `scripts/` — utility scripts (e.g. `check_branch_name.py`)
- `.github/` — CI workflows, PR/issue templates, CODEOWNERS, Dependabot, `instructions/`, `copilot-instructions.md`
- `.devcontainer/` — Codespaces bootstrap (`devcontainer.json`, `bootstrap.sh`)
- `Taskfile.yml` — task runner
- `pyproject.toml` — project config (`[tool.uv]`, `[tool.mypy]`, `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.coverage.*]`, `[tool.commitizen]`)

## Important

- Never commit API keys or any `.env*` file
- Run `task qa` before pushing
- Release automation: commits with Conventional Commits → release-please opens a "chore: release X.Y.Z" PR → merge it → tag is pushed automatically
- `src/cnpja/types/` must stay in sync with `schemas/openapi.json` (see `codegen_instructions.md`)
