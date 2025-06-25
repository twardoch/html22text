# html22text

Python package to convert HTML into Markdown or plain text in a smart way. It leverages the power of `BeautifulSoup` for HTML parsing and `html2text` for the core conversion logic, with added features for link management and content filtering.

## Rationale

Web content is often in HTML, but for many applications like data processing, AI model training, or simplified content display, a plain text or Markdown representation is more suitable. `html22text` aims to provide a robust and configurable tool for this conversion, addressing common needs such as:

*   Converting HTML to clean Markdown or readable plain text.
*   Handling relative and absolute links appropriately.
*   Allowing selective removal of HTML tags and their content.
*   Offering control over formatting details like quotes and table representation.

This project modernizes an existing tool, bringing in current best practices for Python packaging, linting, type checking, testing, and CI/CD.

## Features

*   Convert HTML to Markdown or plain text.
*   Smart handling of links and image sources, including base URL support.
*   Option to kill specified HTML tags and their content.
*   Customizable quote characters and blockquote treatment.
*   Command-line interface and Python API.
*   Modernized codebase with type hinting, linting, and testing.

## Installation

### From PyPI (Recommended)

```bash
pip install html22text
```

### From Source (for development)

```bash
git clone https://github.com/twardoch/html22text.git
cd html22text
pip install -e .
```
Alternatively, using [Hatch](https://hatch.pypa.io/latest/):
```bash
git clone https://github.com/twardoch/html22text.git
cd html22text
hatch env create # Creates a virtual environment and installs dependencies
hatch shell      # Activates the virtual environment
# To run tests:
# hatch run default:test
```

## Usage

### Command-Line

The command-line interface is powered by [Python Fire](https://google.github.io/python-fire/).
You can pass HTML content directly or specify a file path.

```bash
html22text HTML_CONTENT_OR_FILE_PATH [OPTIONS...] [- FIRECOMMAND]
```

**Common Options:**

*   `--is_input_path`: If specified, the first argument is treated as a file path.
*   `--markdown`: Output Markdown (default is plain text).
*   `--base_url URL`: Base URL for resolving relative links.
*   `--kill_tags "TAG1,TAG2,..."`: Comma-separated string of CSS selectors for tags whose content should be removed (e.g., `"script,.advert"`). Quote the string if it contains spaces or special characters.
*   `--file_ext_override EXT`: Output file extension for link conversion (e.g., `md`, `txt`).
*   See `html22text --help` for all available options derived from the Python API.

**Example:**

Convert the `index.html` file to plain text, treating `<blockquote>` as quoted text, and then convert the result to lowercase:

```bash
html22text index.html --is_input_path --block_quote --open_quote='"' --close_quote='"' - lower
```
(Note: The `- lower` part is a Fire command to call the `lower()` string method on the result.)

You may invoke the tool as `html22text` or as `python3 -m html22text.cli` (if installed) or `python3 -m src.html22text.__main__` (from source root). The `pyproject.toml` defines `html22text` as the script name.

The `FIRECOMMAND` allows you to pipe the output of `html22text` to any Python string method, for example:
`capitalize | casefold | center | count | encode | endswith | expandtabs | find | format | format_map | index | isalnum | isalpha | isascii | isdecimal | isdigit | isidentifier | islower | isnumeric | isprintable | isspace | istitle | isupper | join | ljust | lower | lstrip | maketrans | partition | removeprefix | removesuffix | replace | rfind | rindex | rjust | rpartition | rsplit | rstrip | split | splitlines | startswith | strip | swapcase | title | translate | upper | zfill`

### Python API

```python
from html22text import html22text

html_source = "<p>Hello <b><a href='page.html'>this</a> world</b>!</p>"
# Example: Convert to Markdown, assuming page.html will become page.md
markdown_text = html22text(
    html_content=html_source,
    is_input_path=False,  # True if html_content is a file path
    markdown=True,        # Output Markdown
    base_url="http://example.com/", # Base for resolving links like 'image.png'
    kill_tags=['script', 'style'], # Remove script and style tags
    file_ext_override="md" # Convert relative .html links to .md
)
print(markdown_text)

# Example: Convert to plain text
plain_text = html22text(
    html_content=html_source,
    is_input_path=False,
    markdown=False, # Output plain text
    block_quote=True, # Treat <blockquote> as <q>
    open_quote=">> ",
    close_quote=""
)
print(plain_text)
```

## Contributing

Contributions are welcome! Please follow these guidelines:

### Development Setup
1.  Clone the repository: `git clone https://github.com/twardoch/html22text.git`
2.  Change into the directory: `cd html22text`
3.  Create and activate a virtual environment using Hatch:
    ```bash
    hatch env create
    hatch shell
    ```
    This installs all dependencies, including development tools.

### Code Style & Linting
This project uses [Ruff](https://beta.ruff.rs/docs/) for linting and formatting.
*   To format your code: `hatch run lint:fmt`
*   To check for linting issues: `hatch run lint:style`
*   Pre-commit hooks are configured to run these checks automatically.

### Type Checking
Static type checking is done with [MyPy](http://mypy-lang.org/).
*   To run type checks: `hatch run lint:typing`
*   Pre-commit hooks also run MyPy.

### Testing
Tests are written using [Pytest](https://docs.pytest.org/).
*   To run tests: `hatch run default:test`
*   To run tests with coverage: `hatch run lint:cov` (uses the lint environment which has pytest-cov)

### Pre-commit Hooks
It's highly recommended to install and use the pre-commit hooks:
```bash
pip install pre-commit  # If not already installed
pre-commit install    # Sets up the git hooks in your local repo
```
This will automatically run Ruff and MyPy on staged files before you commit.

### Codebase Structure
*   **`pyproject.toml`**: Defines project metadata, dependencies, and build system (Hatch). It also configures tools like Ruff, MyPy, and Hatch environments.
*   **`src/html22text/`**: Contains the main source code.
    *   **`html22text.py`**: The core module with the `html22text()` function that performs the HTML to text/Markdown conversion.
    *   **`__main__.py`**: Provides the command-line interface using `python-fire`.
    *   **`__init__.py`**: Makes `html22text()` available for import.
*   **`tests/`**: Contains test files (e.g., `test_html22text.py`).
*   **`.github/workflows/`**: Contains GitHub Actions CI/CD workflows (e.g., `ci.yml`).
*   **`.pre-commit-config.yaml`**: Configuration for pre-commit hooks.

### Submitting Changes
1.  Create a feature branch.
2.  Make your changes, including tests for new functionality.
3.  Ensure all checks (linting, type checking, tests) pass.
4.  Commit your changes and push to your fork.
5.  Open a pull request to the main repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
