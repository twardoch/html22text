#!/bin/bash
# this_file: scripts/test.sh

set -e  # Exit on error

echo "🧪 Running tests for html22text..."

# Run linting
echo "🔍 Running linting..."
python -m ruff check src/ tests/
python -m ruff format --check src/ tests/

# Run type checking
echo "🔍 Running type checking..."
python -m mypy --package html22text --package tests

# Run tests with coverage
echo "🧪 Running tests with coverage..."
python -m pytest --cov=src/html22text --cov-report=term-missing --cov-report=html --cov-fail-under=80 tests/

echo "✅ All tests passed!"