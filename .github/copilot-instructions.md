# GitHub Copilot instructions for CNPJá Python SDK

This repository is the **Python SDK for the CNPJá API**, consumed by internal projects via `uv add git+...`. It mirrors the feature surface of [`sdk-nodejs`](https://github.com/cnpja/sdk-nodejs) while offering:

- Native sync + async clients (`Client` / `AsyncClient` via `.aio`)
- Strict Pydantic v2 validation (`mypy strict`)
- Typed HTTP overloads for JSON vs. binary responses

Trust this file before re-exploring the repository. The main places to work are:

- `src/cnpja/client.py` and `src/cnpja/open_client.py` for entry points
- `src/cnpja/_http_client.py` for transport, retry, and overloads
- `src/cnpja/resources/*.py` for endpoint-to-method mapping
- `src/cnpja/types/*.py` for Pydantic DTOs and request params
- `src/cnpja/errors.py` for the exception hierarchy
- `src/cnpja/pagers.py` for sync/async pagination
- `tests/` for regression coverage of historical bugs
- `schemas/openapi.json` + `schemas/schemas-summary.json` for the API contract source of truth
- `Taskfile.yml`, `pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/` for toolchain

Use Python `3.12` with `uv` and `task`. Prefer the existing task aliases: `task setup`, `task doctor`, `task format`, `task format:check`, `task lint`, `task lint:fix`, `task typecheck`, `task test`, `task qa`, `task lock:check`. For one-off commands, use `uv run ...`; never invoke `pip` or `python` directly.

Follow the current Python conventions: add type hints to every new function/method, keep line length at `100`, use `from __future__ import annotations`, prefer explicit `Literal` for constrained string unions, and avoid broad `try/except` blocks. DTOs inherit from `BaseModel` (`src/cnpja/_common.py`) with `extra="forbid"`; request params inherit from `BaseParams` with `extra="allow"` and `use_enum_values=True`.

Keep consistency with the Node.js SDK when the CNPJá API evolves. If a new DTO or parameter lands in `sdk-nodejs/source/cnpja/cnpja.dto.ts`, reflect it here. However, **do not regress the Python-specific relaxations** (e.g. `MemberDto.since: str | None`, `PersonDto.id: str | None`) — those exist because the real API returns `null` where the OpenAPI schema is overly strict.

HTTP layer rules:

- `HttpClient.get`/`post`/`patch`/`aget`/`apost`/`apatch` have `@overload` for `response_model=type[T] -> T` vs. no model -> `bytes | dict[str, Any]`.
- Binary endpoints (PDFs, images) use `HttpClient.get_binary` / `aget_binary` — never call `get()` without `response_model` for binary responses, it would widen the type.
- Retry is handled by `tenacity` with the `_CallbackWait` adapter; respect `retry_delay: Callable[[int], float]` when the user customizes it.

Pagination rules:

- `Pager.page` is a property — read with `pager.page` (no call).
- `AsyncPager.page()` is a **method** — call `await pager.page()` with parentheses. Never decorate an `async def` with `@property` (anti-pattern in Python that returns a coroutine instead of the value).

Error handling:

- `APIError.from_response(httpx.Response)` is the single factory for exceptions.
- `TooManyRequestsError` parses credit headers (`x-credit-required`, `x-credit-remaining`).
- `trace_id` is extracted from the `x-trace-id` header.

Git workflow is enforced by automation: branches must match `type/short-description`, commits and PR titles use Conventional Commits, pre-commit hooks run Ruff and Commitizen, pull requests are squash-merged with passing CI and at least one approval. Prefer small, surgical changes that fit the existing structure, and only search deeper when these instructions do not cover the part of the repository you need.
