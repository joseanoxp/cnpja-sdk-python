---
applyTo: "Taskfile.yml,pyproject.toml,.pre-commit-config.yaml,README.md,CONTRIBUTING.md,SECURITY.md,CLAUDE.md,.github/**/*.yml,.github/**/*.yaml,.github/**/*.md"
---

# Repository configuration and workflow instructions

Treat the toolchain as a connected system. If you change a command, validation step, or workflow expectation, update every affected source of truth: `Taskfile.yml`, `.github/workflows/quality_control.yml`, `.github/workflows/release.yml`, `.pre-commit-config.yaml`, `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, and `.github/PULL_REQUEST_TEMPLATE.md`.

CI is the baseline validation contract. It installs dependencies with `uv sync --locked`, verifies `uv lock --check`, lints with `uv run ruff check .`, checks formatting with `uv run ruff format --check .`, type-checks with `uv run mypy src/`, runs tests with `uv run pytest`, runs every pre-commit hook via `uv run pre-commit run --all-files`, and validates the PR title and branch commits with Commitizen. Keep local task aliases consistent with those commands.

Do not weaken repository policy accidentally. Branch naming is enforced by `scripts/check_branch_name.py`, commit messages and PR title are validated by Commitizen, Dependabot uses conventional prefixes (`chore(deps)` / `ci(deps)`) and labels, and release automation runs via `googleapis/release-please-action@v4` (squash merge into `main` triggers it).

The SDK is a library consumed via `uv add git+https://github.com/joseanoxp/cnpja-sdk-python --tag vX.Y.Z`. Preserve this contract:

- `pyproject.toml` stays publishable but **not** published to PyPI — `Repository = "https://github.com/joseanoxp/cnpja-sdk-python"`.
- Version is bumped exclusively by `release-please` (never manually in `pyproject.toml`).
- `schemas/openapi.json` and `schemas/schemas-summary.json` are the source of truth for DTOs; changes in `src/cnpja/types/` must follow `codegen_instructions.md`.
- Quality gate must remain strict: `mypy strict = true`, `ruff target-version` aligned with `requires-python`, and every relaxation must be documented (see `MemberDto.since`, `PersonDto.id`, etc.).

When documenting setup, prefer `task setup`, `task doctor`, and the existing task commands over bespoke shell sequences unless the task specifically concerns the underlying tools.
