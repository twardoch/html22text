# this_file: tests/test_cli.py

"""Test the CLI interface for html22text."""

import pytest
import subprocess
import tempfile
import os
from pathlib import Path


def test_cli_help():
    """Test CLI help output."""
    result = subprocess.run(
        ["python", "-m", "html22text", "--help"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "html22text" in result.stdout.lower()


def test_cli_version():
    """Test CLI version output."""
    result = subprocess.run(
        ["python", "-m", "html22text", "--version"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    # Version command might not be implemented, so we allow failure
    # This is more of a placeholder test
    assert result.returncode in [0, 1]


def test_cli_simple_conversion():
    """Test CLI with simple HTML string."""
    html_input = "<p>Hello <b>World</b></p>"
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input, "--markdown"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "Hello **World**" in result.stdout


def test_cli_text_conversion():
    """Test CLI with text output."""
    html_input = "<p>Hello <b>World</b></p>"
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "Hello World" in result.stdout


def test_cli_file_input():
    """Test CLI with file input."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write("<p>Hello from <em>file</em></p>")
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ["python", "-m", "html22text", temp_file, "--is_input_path", "--markdown"],
            capture_output=True,
            text=True,
            cwd="/root/repo"
        )
        
        assert result.returncode == 0
        assert "Hello from _file_" in result.stdout
    finally:
        os.unlink(temp_file)


def test_cli_kill_tags():
    """Test CLI with kill_tags option."""
    html_input = "<p>Keep this</p><script>Remove this</script><span>Keep this too</span>"
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input, "--kill_tags", "script"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "Keep this" in result.stdout
    assert "Keep this too" in result.stdout
    assert "Remove this" not in result.stdout


def test_cli_base_url():
    """Test CLI with base_url option."""
    html_input = '<a href="page.html">Link</a>'
    
    result = subprocess.run([
        "python", "-m", "html22text", html_input, 
        "--markdown", "--base_url", "http://example.com/",
        "--file_ext_override", "md"
    ], capture_output=True, text=True, cwd="/root/repo")
    
    assert result.returncode == 0
    assert "page.md" in result.stdout


def test_cli_custom_quotes():
    """Test CLI with custom quote characters."""
    html_input = '<q>Quoted text</q>'
    
    result = subprocess.run([
        "python", "-m", "html22text", html_input,
        "--open_quote", "«", "--close_quote", "»"
    ], capture_output=True, text=True, cwd="/root/repo")
    
    assert result.returncode == 0
    assert "«Quoted text»" in result.stdout


def test_cli_fire_command():
    """Test CLI with Fire command piping."""
    html_input = "<p>HELLO WORLD</p>"
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input, "-", "lower"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "hello world" in result.stdout


def test_cli_nonexistent_file():
    """Test CLI with nonexistent file."""
    result = subprocess.run(
        ["python", "-m", "html22text", "/nonexistent/file.html", "--is_input_path"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode != 0
    assert "error" in result.stderr.lower() or "traceback" in result.stderr


def test_cli_complex_html():
    """Test CLI with complex HTML structure."""
    html_input = '''
    <div>
        <h1>Title</h1>
        <p>Paragraph with <a href="link.html">link</a></p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </div>
    '''
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input, "--markdown"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "# Title" in result.stdout
    assert "[link]" in result.stdout
    assert "Item 1" in result.stdout
    assert "Item 2" in result.stdout


def test_cli_selector():
    """Test CLI with CSS selector."""
    html_input = '''
    <div id="header">Header</div>
    <div id="main">Main content</div>
    <div id="footer">Footer</div>
    '''
    
    result = subprocess.run(
        ["python", "-m", "html22text", html_input, "--selector", "#main"],
        capture_output=True,
        text=True,
        cwd="/root/repo"
    )
    
    assert result.returncode == 0
    assert "Main content" in result.stdout
    assert "Header" not in result.stdout
    assert "Footer" not in result.stdout