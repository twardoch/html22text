#!/usr/bin/env bash
# this_file: build.sh
# Test html22text and build the package into dist/.
# Usage: ./build.sh [all|test|package]   (default: all)
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
target="${1:-all}"
case "$target" in
  all|test|package) ;;
  *) echo "usage: $0 [all|test|package]" >&2; exit 2 ;;
esac
if [[ "$target" == all || "$target" == test ]]; then
  uv run --isolated --with pytest --with-editable . python -m pytest -q tests
fi
if [[ "$target" == all || "$target" == package ]]; then
  rm -rf dist
  uv build
  uvx twine check dist/*
fi
