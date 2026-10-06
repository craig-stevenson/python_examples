#!/usr/bin/env bash
# Run on a machine WITH internet access to (re)populate ./wheels.
# uv has no `pip download` command, so this borrows pip through uvx.
#
# Usage: ./refresh-wheels.sh [package ...]
# With no arguments it downloads the packages this example depends on.
set -euo pipefail

cd "$(dirname "$0")"

packages=("$@")
if [ ${#packages[@]} -eq 0 ]; then
    packages=(python-dateutil)
fi

# --only-binary=:all: refuses sdists, so nothing needs building offline.
# pip also downloads every transitive dependency (here: six).
uvx pip download --only-binary=:all: --dest wheels "${packages[@]}"
