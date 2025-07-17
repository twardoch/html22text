#!/bin/bash
# this_file: scripts/dev-setup.sh

set -e  # Exit on error

echo "🔧 Setting up development environment for html22text..."

# Check if Python 3.10+ is available
python_version=$(python --version 2>&1 | cut -d' ' -f2)
echo "🐍 Python version: $python_version"

# Install/upgrade pip and build tools
echo "📦 Installing/upgrading build tools..."
python -m pip install --upgrade pip setuptools wheel

# Install build dependencies
echo "📦 Installing build dependencies..."
python -m pip install build twine

# Install development dependencies
echo "📦 Installing development dependencies..."
python -m pip install -e ".[dev]"

# Install pre-commit hooks (if .pre-commit-config.yaml exists)
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🪝 Installing pre-commit hooks..."
    python -m pip install pre-commit
    pre-commit install
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh

echo "✅ Development environment setup completed!"
echo "🎯 You can now run:"
echo "   ./scripts/test.sh     - Run tests"
echo "   ./scripts/build.sh    - Build package"
echo "   ./scripts/release.sh  - Release a new version"