# this_file: INSTALL.md

# Installation Guide for html22text

## Quick Installation (Recommended)

### From PyPI

```bash
pip install html22text
```

### Using the install script

```bash
curl -fsSL https://raw.githubusercontent.com/twardoch/html22text/main/install.sh | bash
```

## Platform-Specific Installation

### Linux/macOS

```bash
# Using pip
pip install html22text

# Using pip with user installation
pip install --user html22text

# Using pipx (recommended for CLI tools)
pipx install html22text
```

### Windows

```powershell
# Using pip
pip install html22text

# Using pipx
pipx install html22text
```

## Development Installation

### Prerequisites

- Python 3.10 or higher
- Git

### From Source

```bash
git clone https://github.com/twardoch/html22text.git
cd html22text
pip install -e ".[dev]"
```

### Using the development setup script

```bash
git clone https://github.com/twardoch/html22text.git
cd html22text
./scripts/dev-setup.sh
```

## Binary Executables

Pre-built executables are available for download from the [GitHub Releases](https://github.com/twardoch/html22text/releases) page.

### Download and Install

1. Go to the [Releases](https://github.com/twardoch/html22text/releases) page
2. Download the appropriate executable for your platform:
   - `html22text-linux-latest` for Linux
   - `html22text-windows-latest.exe` for Windows
   - `html22text-macos-latest` for macOS
3. Make it executable (Linux/macOS):
   ```bash
   chmod +x html22text-linux-latest
   ```
4. Move to a directory in your PATH (optional):
   ```bash
   sudo mv html22text-linux-latest /usr/local/bin/html22text
   ```

## Verification

After installation, verify that html22text is working:

```bash
# Test the module
python -m html22text "<p>Hello <b>World</b></p>" --markdown

# Test the CLI (if installed with pip)
html22text "<p>Hello <b>World</b></p>" --markdown
```

Expected output:
```
Hello **World**
```

## Troubleshooting

### Common Issues

1. **Command not found**: If `html22text` command is not found, make sure your Python scripts directory is in your PATH, or use `python -m html22text` instead.

2. **Permission denied**: On Linux/macOS, you might need to use `sudo` for system-wide installation or use `--user` flag for user installation.

3. **Python version compatibility**: html22text requires Python 3.10 or higher. Check your Python version with `python --version`.

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/twardoch/html22text/issues) page
2. Create a new issue with detailed information about your environment and the problem
3. Include the output of `python --version` and `pip show html22text`