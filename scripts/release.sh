#!/bin/bash
# this_file: scripts/release.sh

set -e  # Exit on error

# Check if tag is provided
if [ -z "$1" ]; then
    echo "❌ Usage: $0 <version-tag>"
    echo "   Example: $0 v1.2.3"
    exit 1
fi

VERSION_TAG="$1"

# Validate version tag format
if [[ ! "$VERSION_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+.*$ ]]; then
    echo "❌ Invalid version tag format. Use vX.Y.Z format (e.g., v1.2.3)"
    exit 1
fi

echo "🚀 Starting release process for $VERSION_TAG..."

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Not on main branch. Please switch to main branch first."
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build the package
echo "🔨 Building package..."
./scripts/build.sh

# Create and push git tag
echo "🏷️  Creating git tag $VERSION_TAG..."
git tag -a "$VERSION_TAG" -m "Release $VERSION_TAG"

echo "📤 Pushing tag to origin..."
git push origin "$VERSION_TAG"

echo "✅ Release process completed!"
echo "🎉 Version $VERSION_TAG has been tagged and pushed."
echo "📚 GitHub Actions will now build and publish the release."
echo "🔗 Check the GitHub repository for the release status."