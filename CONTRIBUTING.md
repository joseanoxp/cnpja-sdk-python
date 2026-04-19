# Contributing to CNPJá Python SDK

## Prerequisites

- [Python 3.12+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) — Python package and project manager
- [Task](https://taskfile.dev/) — task runner

## Getting Started

```bash
# Clone the repository
git clone https://github.com/joseanoxp/cnpja-sdk-python.git
cd sdk-python

# Install dependencies and git hooks
task setup

# Check your environment
task doctor

# Run the full quality gate
task qa
```

### GitHub Codespaces

If you prefer Codespaces, open the repository in a new Codespace and wait for the devcontainer bootstrap
to finish. The repository now provisions:

- Python 3.12 in the container
- `uv` and `task` in the user environment
- `uv sync --locked`
- pre-commit hooks on first creation

Once the Codespace is ready:

```bash
task doctor
task qa
```

## Available Commands

| Command | Description |
|---|---|
| `task setup` | Install dependencies and git hooks |
| `task doctor` | Check if all required tools are installed |
| `task format` | Format code with Ruff |
| `task format:check` | Verify formatting |
| `task lint` | Run Ruff linter |
| `task lint:fix` | Run linter with auto-fix |
| `task pre-commit` | Run pre-commit hooks for the current tree |
| `task typecheck` | Run mypy (strict mode) |
| `task test` | Run pytest |
| `task qa` | Run the local quality gate (`uv lock --check`, lint, format, typecheck, tests, hooks) |
| `task lock:check` | Verify `uv.lock` is in sync with `pyproject.toml` |

Codespaces users can rely on `.devcontainer/bootstrap.sh`, which keeps the environment aligned with the
locked dependency set used in CI.

## Git Workflow

We follow **GitHub Flow**:

1. Create a branch from `main`
2. Make your changes with small, focused commits
3. Open a Pull Request
4. Address review feedback
5. Squash merge into `main`

### Branch Naming

Branches must follow the pattern `type/short-description`:

```
feat/office-search-filters
fix/pager-empty-page
docs/update-quickstart
refactor/http-client-overloads
test/smoke-regression
chore/bump-mypy
ci/validate-pr-title
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Enforced locally by `scripts/check_branch_name.py` (pre-push hook).

### Commit Messages and PR Titles

We use [Conventional Commits](https://www.conventionalcommits.org/). You can use the interactive helper:

```bash
uv run cz commit
```

Or write manually:

```
type(scope): description

feat(office): add filter by registration source
fix(pager): stop on empty first page
docs: update CONTRIBUTING with new task commands
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

**Since we squash merge, the PR title becomes the single commit on `main`** — it must also follow Conventional Commits. The CI validates this automatically.

### Pull Requests

- Fill out the PR template (Summary, Test Plan, Checklist)
- Ensure `task qa` passes locally before opening the PR
- At least 1 approval required
- All review threads must be resolved
- Only squash merge is allowed

## Code Quality

### Pre-commit Hooks

These run automatically after `task setup` — no manual action needed:

| Stage | Hook | What it checks |
|---|---|---|
| `pre-commit` | ruff-check | Lint + auto-fix |
| `pre-commit` | ruff-format | Code formatting |
| `commit-msg` | commitizen | Commit message format |
| `pre-push` | branch-name-check | Branch naming convention |

To run the same hook suite checked in CI, use:

```bash
task pre-commit
```

### CI Pipeline

Every PR runs the full `Quality Control` workflow:

- `uv lock --check` — lockfile is up to date
- `uv sync --locked` — reproducible install
- `ruff check`, `ruff format --check`, `mypy src/`, `pytest`
- `pre-commit run --all-files` — all hooks
- `cz check --message` — PR title is Conventional
- `cz check --rev-range` — every commit on the branch is Conventional

Locally, `task qa` covers the reproducible checks above except the PR-title and branch commit-message
validation, which only make sense in CI.

## Release

The version is bumped automatically by [release-please](https://github.com/googleapis/release-please-action):

1. Commits in `main` following Conventional Commits trigger the `Release` workflow.
2. `release-please` opens (or updates) a PR titled `chore: release X.Y.Z` containing the version bump in `pyproject.toml` and a new `CHANGELOG.md` entry.
3. Merging that PR creates the `vX.Y.Z` tag and publishes a GitHub Release.

Consumers pin the tag in their projects:

```bash
uv add git+https://github.com/joseanoxp/cnpja-sdk-python --tag vX.Y.Z
```

## Project Structure

```
sdk-python/
├── src/cnpja/             # SDK source
│   ├── client.py          # Authenticated Client + AsyncClient
│   ├── open_client.py     # Public CnpjaOpen + AsyncCnpjaOpen
│   ├── _http_client.py    # Transport layer (retry, overloads)
│   ├── resources/         # Endpoint-to-method (sync + async twins)
│   ├── types/             # Pydantic DTOs and request params
│   ├── errors.py          # Exception hierarchy
│   ├── pagers.py          # Sync/async pagination
│   └── version.py
├── tests/                 # Regression coverage
├── schemas/               # OpenAPI source of truth
│   ├── openapi.json
│   └── schemas-summary.json
├── scripts/               # Utility scripts
├── .github/               # CI, templates, CODEOWNERS
├── Taskfile.yml           # Task runner
├── pyproject.toml
├── .pre-commit-config.yaml
└── codegen_instructions.md
```

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Runtime |
| Pydantic v2 | DTO validation |
| httpx | HTTP transport (sync + async) |
| tenacity | Retry with backoff |
| uv | Package management |
| Ruff | Linter + formatter |
| mypy (strict) | Type checker |
| pytest + respx | Testing |
| pre-commit + commitizen | Git hooks and commit validation |
| Task | Task runner |
| release-please | Automated versioning |
