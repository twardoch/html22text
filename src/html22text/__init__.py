# this_file: src/html22text/__init__.py
from importlib.metadata import PackageNotFoundError, version

from .html22text import html22text

__all__ = ["__version__", "html22text"]

try:
    # hatch-vcs derives the version from the git tag at build time.
    __version__ = version("html22text")
except PackageNotFoundError:  # running from a source tree without installation
    __version__ = "0.0.0"
