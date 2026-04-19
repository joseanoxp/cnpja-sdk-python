#!/usr/bin/env python3
"""Valida o nome da branch atual contra a convenção GitHub Flow.

Formato esperado: ``type/short-description`` (ex: ``feat/office-search-filters``).

Invocado pelo hook ``pre-push`` do pre-commit. Branches ``main`` e detached HEAD
(ex: rebase, checkout de tag) são ignoradas.
"""

import re
import subprocess
import sys

PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)/[a-z0-9]+(-[a-z0-9]+)*$"
)
SKIP_BRANCHES = {"main"}


def current_branch() -> str | None:
    """Retorna o nome da branch atual, ou ``None`` se em detached HEAD."""
    result = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def main() -> int:
    branch = current_branch()

    # detached HEAD (rebase, checkout de tag, etc.) — não bloqueia
    if branch is None:
        return 0

    if branch in SKIP_BRANCHES:
        return 0

    if PATTERN.match(branch):
        return 0

    print(f'\nBranch "{branch}" does not follow the convention.\n')
    print("Expected format: type/short-description")
    print("Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert")
    print("Example: feat/office-search-filters, fix/pager-empty-page\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
