# this_file: tests/test_version.py

"""Test version handling for html22text."""

import pytest
import re
from html22text import __version__


def test_version_format():
    """Test that version follows semantic versioning format."""
    # Version should be in format X.Y.Z or X.Y.Z-dev or similar
    version_pattern = r'^\d+\.\d+\.\d+(?:[\.\-\+].*)?$'
    
    # Allow fallback version for development
    assert __version__ == "0.0.0" or re.match(version_pattern, __version__)


def test_version_accessible():
    """Test that version is accessible from package."""
    from html22text import __version__ as version
    assert version is not None
    assert isinstance(version, str)
    assert len(version) > 0


def test_version_in_module():
    """Test that version is defined in the module."""
    import html22text
    assert hasattr(html22text, '__version__')
    assert html22text.__version__ is not None