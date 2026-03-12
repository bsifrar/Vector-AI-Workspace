#!/bin/bash

set -euo pipefail

vector_root_dir() {
    cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd
}

load_vector_env() {
    local root_dir
    root_dir="$(vector_root_dir)"
    if [[ -f "$root_dir/.env" ]]; then
        set -a
        source "$root_dir/.env"
        set +a
    fi
}
