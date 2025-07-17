#!/bin/bash
# this_file: install.sh

set -e

echo "🚀 Installing html22text..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "🐍 Python version: $python_version"

# Install from PyPI
echo "📦 Installing html22text from PyPI..."
python3 -m pip install --user html22text

# Verify installation
echo "✅ Verifying installation..."
python3 -c "import html22text; print(f'html22text version: {html22text.__version__}')"

# Test CLI
echo "🧪 Testing CLI..."
python3 -m html22text "<p>Hello <b>World</b></p>" --markdown

echo "✅ Installation completed successfully!"
echo "🎯 You can now use html22text:"
echo "   python3 -m html22text --help"
echo "   html22text --help  (if ~/.local/bin is in your PATH)"