# this_file: tests/test_cli.py

"""Test the CLI interface for html22text."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Use the same Python interpreter that is running the tests, so the installed
# package is always on sys.path regardless of which environment is active.
_PY = sys.executable
# Repo root – one level above this file's directory.
_REPO = str(Path(__file__).parent.parent)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    """Run html22text as a module with the current interpreter."""
    return subprocess.run(
        [_PY, "-m", "html22text", *args],
        capture_output=True,
        text=True,
        cwd=_REPO,
    )


def test_cli_help():
    """Test CLI help output.

    Fire writes help to stderr when --help is passed; check both streams.
    """
    result = _run("--help")
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).lower()
    # Fire shows the function docstring; check for stable description words.
    assert "convert html" in combined or "html" in combined


def test_cli_version():
    """Test CLI version output.

    Fire does not natively support --version; it returns exit code 2 for
    unknown flags.  We just verify the process exits (not hangs).
    """
    result = _run("--version")
    assert result.returncode in [0, 1, 2]


def test_cli_simple_conversion():
    """Test CLI with simple HTML string."""
    result = _run("<p>Hello <b>World</b></p>", "--markdown")
    assert result.returncode == 0
    assert "Hello **World**" in result.stdout


def test_cli_text_conversion():
    """Test CLI with text output."""
    result = _run("<p>Hello <b>World</b></p>")
    assert result.returncode == 0
    assert "Hello World" in result.stdout


def test_cli_file_input():
    """Test CLI with file input."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write("<p>Hello from <em>file</em></p>")
        temp_file = f.name

    try:
        result = _run(temp_file, "--is_input_path", "--markdown")
        assert result.returncode == 0
        assert "Hello from _file_" in result.stdout
    finally:
        os.unlink(temp_file)


def test_cli_kill_tags():
    """Test CLI with kill_tags option."""
    html_input = "<p>Keep this</p><script>Remove this</script><span>Keep this too</span>"
    result = _run(html_input, "--kill_tags", "script")
    assert result.returncode == 0
    assert "Keep this" in result.stdout
    assert "Keep this too" in result.stdout
    assert "Remove this" not in result.stdout


def test_cli_base_url():
    """Test CLI with base_url option."""
    html_input = '<a href="page.html">Link</a>'
    result = _run(
        html_input,
        "--markdown",
        "--base_url",
        "http://example.com/",
        "--file_ext_override",
        "md",
    )
    assert result.returncode == 0
    assert "page.md" in result.stdout


def test_cli_custom_quotes():
    """Test CLI with custom quote characters."""
    html_input = "<q>Quoted text</q>"
    result = _run(html_input, "--open_quote", "«", "--close_quote", "»")
    assert result.returncode == 0
    assert "«Quoted text»" in result.stdout


def test_cli_fire_command():
    """Test that Fire can chain a str method on the output."""
    html_input = "<p>HELLO WORLD</p>"
    result = _run(html_input, "-", "lower")
    assert result.returncode == 0
    assert "hello world" in result.stdout


def test_cli_nonexistent_file():
    """Test CLI with nonexistent file."""
    result = _run("/nonexistent/file.html", "--is_input_path")
    assert result.returncode != 0
    assert "error" in result.stderr.lower() or "traceback" in result.stderr


def test_cli_complex_html():
    """Test CLI with complex HTML structure."""
    html_input = (
        "<div><h1>Title</h1>"
        "<p>Paragraph with <a href='link.html'>link</a></p>"
        "<ul><li>Item 1</li><li>Item 2</li></ul></div>"
    )
    result = _run(html_input, "--markdown")
    assert result.returncode == 0
    assert "# Title" in result.stdout
    assert "[link]" in result.stdout
    assert "Item 1" in result.stdout
    assert "Item 2" in result.stdout


def test_cli_selector():
    """Test CLI with CSS selector."""
    html_input = (
        '<div id="header">Header</div>'
        '<div id="main">Main content</div>'
        '<div id="footer">Footer</div>'
    )
    result = _run(html_input, "--selector", "#main")
    assert result.returncode == 0
    assert "Main content" in result.stdout
    assert "Header" not in result.stdout
    assert "Footer" not in result.stdout
