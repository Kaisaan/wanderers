#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

export PATH="$(pwd)/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is not installed or not in PATH"
    echo "Please install uv from https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

if ! command -v dumpsxiso >/dev/null 2>&1; then
    echo "Error: dumpsxiso is not installed or not in PATH"
    exit 1
fi

uv run scripts/extract_iso.py
