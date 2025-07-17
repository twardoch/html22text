#!/bin/bash
# this_file: scripts/build.sh

set -e  # Exit on error

echo "🔨 Building html22text..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Create build directory
mkdir -p dist

# Build the package
echo "📦 Building package..."
python -m build

echo "✅ Build completed successfully!"
echo "📁 Build artifacts:"
ls -la dist/

# Verify the build
echo "🔍 Verifying build..."
python -m twine check dist/*

echo "✅ Build verification completed!"