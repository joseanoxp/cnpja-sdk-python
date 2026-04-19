#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-create}"
LOCAL_BIN="${HOME}/.local/bin"
export PATH="${LOCAL_BIN}:${PATH}"

install_uv() {
    if command -v uv >/dev/null 2>&1; then
        return
    fi

    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="${LOCAL_BIN}:${PATH}"
}

install_task() {
    if command -v task >/dev/null 2>&1; then
        return
    fi

    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b "${LOCAL_BIN}"
    export PATH="${LOCAL_BIN}:${PATH}"
}

install_uv
install_task

uv sync --locked

if [[ "${MODE}" == "create" ]]; then
    uv run pre-commit install --hook-type commit-msg --hook-type pre-push --hook-type pre-commit
fi
