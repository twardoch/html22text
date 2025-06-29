# html22text: Smart HTML to Text and Markdown Conversion

`html22text` is a Python package designed to convert HTML content into well-formatted Markdown or clean plain text. It intelligently handles complex HTML structures, links, and various formatting elements, providing a highly configurable and robust solution for your text extraction needs.

Built upon the solid foundations of `BeautifulSoup` for HTML parsing and `html2text` for the core conversion logic, `html22text` enhances these capabilities with additional features for precise link management, content filtering, and output customization. This project is developed with modern Python best practices, including comprehensive linting, type checking, testing, and CI/CD workflows.

## Table of Contents

*   [What It Does](#what-it-does)
*   [Who It's For](#who-its-for)
*   [Why It's Useful](#why-its-useful)
*   [Installation](#installation)
    *   [From PyPI (Recommended)](#from-pypi-recommended)
    *   [From Source (for development)](#from-source-for-development)
*   [Usage](#usage)
    *   [Command-Line Interface (CLI)](#command-line-interface-cli)
    *   [Python API](#python-api)
*   [Technical Details](#technical-details)
    *   [How the Code Works Precisely](#how-the-code-works-precisely)
    *   [Key Modules and Structure](#key-modules-and-structure)
    *   [Coding and Contribution Guidelines](#coding-and-contribution-guidelines)
*   [License](#license)

## What It Does

`html22text` excels at transforming messy and complex HTML into more usable text-based formats:

*   **HTML to Markdown:** Generate structured Markdown documents from HTML, preserving semantic meaning where possible (e.g., headers, lists, code blocks, links).
*   **HTML to Plain Text:** Extract clean, readable plain text from HTML, ideal for data processing or simplified display.
*   **Smart Link Handling:**
    *   Correctly resolves relative links to absolute URLs using a provided `base_url`.
    *   Can modify file extensions of relative links (e.g., converting internal `.html` links to `.md` for Markdown output).
    *   Ensures proper IRI (Internationalized Resource Identifier) to URI (Uniform Resource Identifier) conversion.
*   **Content Filtering:** Allows you to specify HTML tags (via CSS selectors) whose content should be completely removed before conversion (e.g., scripts, ads, navigation bars).
*   **Output Customization:**
    *   Offers control over quote characters for `<q>` and `<blockquote>` elements in plain text.
    *   Manages how tables are represented.
    *   Provides options for handling images (e.g., include as Markdown, convert to alt text, or remove).
*   **Modern and Robust:** Developed with a focus on modern Python standards, ensuring reliability and maintainability.

## Who It's For

`html22text` is a valuable tool for a diverse range of users and applications:

*   **Developers:** Integrating HTML content into applications, building content pipelines, or preparing text for further processing.
*   **Data Scientists:** Extracting textual data from web pages for analysis, training machine learning models, or natural language processing tasks.
*   **Content Managers:** Converting HTML documents for different publishing platforms or archiving purposes.
*   **Anyone needing to:**
    *   Quickly get a clean text version of a webpage.
    *   Automate the conversion of HTML archives to Markdown.
    *   Prepare web content for environments where HTML is not suitable.

## Why It's Useful

Web content is predominantly in HTML, which is great for rendering in browsers but often cumbersome for other tasks. `html22text` addresses this by:

*   **Simplifying Complexity:** Converts intricate HTML structures into simpler, more manageable text or Markdown.
*   **Enhancing Readability:** Produces clean output that is easy to read and process.
*   **Providing Control:** Offers fine-grained control over the conversion process, from link handling to tag removal.
*   **Leveraging Proven Libraries:** Builds on the strength of `BeautifulSoup` and `html2text` while adding significant value.
*   **Modern Development:** Adheres to current Python best practices, making it a reliable and future-proof tool.

## Installation

You can install `html22text` from PyPI or directly from the source.

### From PyPI (Recommended)

```bash
pip install html22text
```

### From Source (for development)

1.  Clone the repository:
    ```bash
    git clone https://github.com/twardoch/html22text.git
    cd html22text
    ```
2.  Install using pip (editable mode):
    ```bash
    pip install -e .
    ```
    Alternatively, using [Hatch](https://hatch.pypa.io/latest/):
    ```bash
    # Ensure you are in the cloned html22text directory
    hatch env create  # Creates a virtual environment and installs dependencies
    hatch shell       # Activates the virtual environment
    # To run tests (within hatch shell):
    # hatch run default:test
    ```

## Usage

`html22text` can be used both as a command-line tool and as a Python library.

### Command-Line Interface (CLI)

The CLI is powered by [Python Fire](https://google.github.io/python-fire/), making it flexible and easy to use.

**Basic Syntax:**

```bash
html22text HTML_CONTENT_OR_FILE_PATH [OPTIONS...] [- FIRECOMMAND]
```

*   `HTML_CONTENT_OR_FILE_PATH`: Either a string of HTML or a path to an HTML file.
*   `OPTIONS`: Various flags to control the conversion (see below).
*   `FIRECOMMAND`: Optionally, you can pipe the output to any Python string method (e.g., `lower`, `strip`).

**Invocation:**

You can invoke the tool as `html22text` (if installed in your PATH) or:

*   `python -m html22text` (if installed)
*   `python -m src.html22text.__main__` (if running from the source root directory)

**Common Options:**

*   `--is_input_path`: If specified, the first argument is treated as a file path rather than an HTML string.
*   `--markdown`: Output Markdown. If not specified, outputs plain text (default).
*   `--base_url URL`: Set a base URL for resolving relative links (e.g., `http://example.com/docs/`).
*   `--kill_tags "SELECTOR1,SELECTOR2"`: Comma-separated string of CSS selectors for tags whose content should be removed (e.g., `"script,.advert,header"`). Remember to quote the string if it contains spaces or special characters.
*   `--file_ext_override EXT`: Specify a file extension (e.g., `md`, `txt`) to replace `.html` in relative links. Useful when converting a set of interlinked HTML files.
*   `--open_quote CHARS` and `--close_quote CHARS`: Define custom characters for opening and closing quotes (e.g., `--open_quote "«" --close_quote "»"`).
*   `--block_quote`: If true (for plain text output), treat `<blockquote>` elements like `<q>` elements, applying the specified open/close quotes.
*   For a full list of options, use `html22text --help`.

**CLI Examples:**

1.  **Convert an HTML file to plain text:**
    ```bash
    html22text input.html --is_input_path
    ```

2.  **Convert an HTML string to Markdown:**
    ```bash
    html22text "<p>Hello <b>World</b></p>" --markdown
    ```

3.  **Convert `page.html` to Markdown, resolving relative links against `http://example.com` and changing linked `.html` files to `.md`:**
    ```bash
    html22text page.html --is_input_path --markdown --base_url "http://example.com" --file_ext_override md
    ```

4.  **Convert an HTML file to plain text, remove `<script>` and `<footer>` tags, and convert the output to lowercase:**
    ```bash
    html22text content.html --is_input_path --kill_tags "script,footer" - lower
    ```
    (Note: The `- lower` part is a Fire command that calls the `lower()` string method on the result.)

### Python API

You can easily integrate `html22text` into your Python projects.

**Basic Usage:**

```python
from html22text import html22text

html_source = "<h1>Title</h1><p>Hello <b><a href='page.html'>this</a> world</b>! Check out <a href='image.png'>this image</a>.</p><script>alert('ignore me');</script>"

# Example 1: Convert to Markdown
# - Assume page.html will become page.md
# - Resolve relative links against http://example.com/
# - Remove <script> and .ads elements
markdown_output = html22text(
    html_content=html_source,
    is_input_path=False,  # True if html_content were a file path
    markdown=True,        # Output Markdown
    base_url="http://example.com/",
    kill_tags="script,.ads",   # Comma-separated string of selectors
    file_ext_override="md" # Convert relative .html links to .md
)
print("--- Markdown Output ---")
print(markdown_output)

# Example 2: Convert to plain text
# - Treat <blockquote> as quoted text with custom quotes
# - Remove <script> and <header> elements
plain_text_output = html22text(
    html_content=html_source,
    is_input_path=False,
    markdown=False,       # Output plain text
    kill_tags="script,header", # Comma-separated string of selectors
    block_quote=True,     # Treat <blockquote> as <q>
    open_quote=">> ",
    close_quote=""
)
print("\\n--- Plain Text Output ---")
print(plain_text_output)
```

**Key Parameters for `html22text()` function:**

*   `html_content (str)`: The HTML string to convert or a file path (if `is_input_path=True`).
*   `is_input_path (bool)`: Set to `True` if `html_content` is a file path. Defaults to `False`.
*   `markdown (bool)`: Set to `True` for Markdown output, `False` for plain text. Defaults to `False`.
*   `selector (str)`: A CSS selector (e.g., `#main-content`, `.article-body`) to extract only a portion of the HTML before conversion. Defaults to `"html"` (processes the whole document).
*   `base_url (str)`: The base URL used to resolve relative links found in the HTML. Defaults to `""`.
*   `kill_tags (str | None)`: A comma-separated string of CSS selectors for tags whose content should be removed (e.g., `"script,style,.noprint"`). Defaults to `None`.
*   `file_ext_override (str)`: An extension (e.g., `"md"`, `"txt"`) to replace `.html` in relative links. Useful for converting linked documents. Defaults to `""` (which means `.md` if `markdown=True`, else `.txt`).
*   Refer to the function's docstring or `html22text --help` for a complete list of all parameters and their defaults.

## Technical Details

This section provides a deeper dive into the inner workings of `html22text` and guidelines for contributors.

### How the Code Works Precisely

`html22text` processes HTML through several stages to produce clean Markdown or plain text:

1.  **Input Handling:**
    *   The primary function `html22text()` accepts either an HTML string (`html_content`) or a file path (if `is_input_path=True`). If a path is provided, the file content is read.

2.  **HTML Parsing with BeautifulSoup:**
    *   The raw HTML content is parsed using `BeautifulSoup(html_content, "html.parser")`. This creates a parse tree that can be easily manipulated.
    *   An optional `selector` parameter (CSS selector string) allows processing of only a specific portion of the HTML document (e.g., `soup.select(selector)`). If a selection is made, a new BeautifulSoup object is created from the selected content.

3.  **Pre-processing and Transformations (before `html2text`):**
    *   **Link Normalization and Adjustment (primarily for Markdown output):**
        *   If `markdown=True`, the `prep_doc()` function is called. This function modifies links within the BeautifulSoup parse tree:
            *   `replace_asset_hrefs(soup, base_url)`: Iterates through tags with `src` (e.g., `<img>`, `<script>`) or `href` (e.g., `<link>`) attributes.
                *   `abs_asset_href(href, base_url)`: Converts potentially relative asset URLs into absolute URLs using `urllib.parse.urljoin(base_url, href)`. It ensures proper IRI to URI encoding via `_iri_to_uri_urllib`.
            *   Anchor tags (`<a>`):
                *   `rel_txt_href(href, file_ext)`: If an `href` is relative and points to an HTML-like file (checked by `is_doc()`), its file extension is changed (e.g., `page.html` to `page.md`). The `file_ext` is determined by `file_ext_override` or defaults to `"md"` for Markdown and `"txt"` for plain text. This also uses `_iri_to_uri_urllib`.
        *   The `_iri_to_uri_urllib` helper uses `urllib.parse.urlparse` and `urllib.parse.quote` to ensure URLs are valid URIs, including Punycode encoding for internationalized domain names (IDNs).
    *   **Tag Stripping/Transformation:**
        *   `<mark>` and `<kbd>` tags: Their content is preserved, but the tags themselves are removed (`tag.replace_with(tag.get_text(""))`).
        *   `<blockquote>` (for plain text, if `block_quote=True`): Transformed into `<p><q>...</q></p>` to allow custom quoting via `open_quote` and `close_quote` options of `html2text`. If `block_quote=False`, `<blockquote>` is passed to `html2text` for its default handling.
    *   **Content Killing (`kill_tags`):**
        *   If `kill_tags` is provided (a comma-separated string of CSS selectors), `soup.select(selector_item)` is used to find all elements matching each selector.
        *   These elements and their entire content are removed from the parse tree (`element_to_kill.replace_with("")`). This happens *before* `html2text` processing.

4.  **Core Conversion with `html2text`:**
    *   The modified BeautifulSoup object (`soup`) is converted to a string (`str(soup)`).
    *   An instance of `html2text.HTML2Text` is created and configured based on the `html22text` function's parameters and whether Markdown or plain text output is desired. Key configurations include:
        *   **Universal Settings:**
            *   `body_width = 0`: Disables line wrapping.
            *   `bypass_tables = False`: Allows `html2text` to process tables.
            *   `protect_links = True`: Tries to prevent links from being mangled.
            *   `unicode_snob = True`: Uses Unicode characters.
        *   **Plain Text Specific (`markdown=False`):**
            *   `ignore_emphasis = True`
            *   `ignore_images = kill_images` (parameter)
            *   `ignore_links = True`
            *   `images_to_alt = True` (uses `default_image_alt` parameter)
            *   `open_quote`, `close_quote`: Passed directly.
            *   `hide_strikethrough = kill_strikethrough` (parameter).
        *   **Markdown Specific (`markdown=True`):**
            *   `emphasis_mark = "_"`
            *   `strong_mark = "**"`
            *   `ignore_images = kill_images`
            *   `inline_links = True`
            *   `mark_code = True` (enables `[code]...[/code]` for inline code).
            *   `pad_tables = True`
            *   `skip_internal_links = False`
            *   `use_automatic_links = True`
    *   The `HTML2Text.handle()` method is called with the processed HTML string to get the final Markdown or plain text.

5.  **Output:**
    *   The resulting string is returned.

### Key Modules and Structure

*   **`src/html22text/html22text.py`**: Contains the core `html22text()` function and its helper functions for parsing, link manipulation, and `html2text` configuration.
*   **`src/html22text/__main__.py`**: Provides the command-line interface using `python-fire`. It defines a `cli()` function that wraps `fire.Fire(html22text)`.
*   **`src/html22text/__init__.py`**: Makes `html22text()` directly importable from the `html22text` package.
*   **`pyproject.toml`**: Defines project metadata, dependencies (like `BeautifulSoup`, `html2text`, `fire`), build system configuration (Hatch), and tool configurations (Ruff, MyPy, Pytest/Coverage).
*   **`tests/`**: Contains Pytest tests, primarily in `test_html22text.py`.

### Coding and Contribution Guidelines

Contributions are highly welcome! Please adhere to the following guidelines to ensure consistency and quality.

**1. Development Environment Setup:**

This project uses [Hatch](https://hatch.pypa.io/latest/) for environment and project management.

1.  Clone the repository:
    ```bash
    git clone https://github.com/twardoch/html22text.git
    cd html22text
    ```
2.  Create and activate a virtual environment with all dependencies:
    ```bash
    hatch env create
    hatch shell
    ```
    This installs runtime dependencies and development tools like Ruff, MyPy, and Pytest.

**2. Code Style & Linting:**

*   This project uses [Ruff](https://beta.ruff.rs/docs/) for comprehensive linting (combining Flake8, isort, and more) and formatting.
*   **Format your code:** `hatch run lint:fmt`
*   **Check for linting issues:** `hatch run lint:style`
*   Configuration is in `pyproject.toml` (`[tool.ruff]`). Please ensure your contributions adhere to these rules.

**3. Type Checking:**

*   Static type checking is enforced using [MyPy](http://mypy-lang.org/).
*   **Run type checks:** `hatch run lint:typing`
*   Configuration is in `pyproject.toml` (`[tool.mypy]`). All new code should include type hints and pass type checks.

**4. Testing:**

*   Tests are written using [Pytest](https://docs.pytest.org/) and are located in the `tests/` directory.
*   **Run tests:** `hatch run default:test`
*   **Run tests with coverage report:** `hatch run lint:cov`
    *   Coverage configuration is in `pyproject.toml` (`[tool.coverage]`).
*   All new features must be accompanied by tests. Bug fixes should include regression tests.
*   Aim to maintain or increase test coverage.

**5. Pre-commit Hooks:**

*   It's highly recommended to install and use the pre-commit hooks defined in `.pre-commit-config.yaml`. These hooks automatically run Ruff and MyPy on staged files before you commit.
*   Install pre-commit (if not already installed): `pip install pre-commit`
*   Set up the hooks in your local repository: `pre-commit install`

**6. Codebase Structure Overview:**

*   **`pyproject.toml`**: Project definition, dependencies, build settings, tool configurations.
*   **`src/html22text/`**: Main package source code.
    *   `html22text.py`: Core conversion logic.
    *   `__main__.py`: CLI entry point.
    *   `__init__.py`: Package initializer.
*   **`tests/`**: Test files.
*   **`.github/workflows/`**: GitHub Actions CI/CD workflows (e.g., `ci.yml` for running checks and tests).
*   **`.pre-commit-config.yaml`**: Configuration for pre-commit hooks.
*   **`CHANGELOG.md`**: Records notable changes for each version.

**7. Branching and Commits:**

*   Create feature branches from the `main` branch (e.g., `feature/my-new-feature` or `fix/issue-123`).
*   Write clear and concise commit messages. Consider following [Conventional Commits](https://www.conventionalcommits.org/) if you are familiar with it, though it's not strictly enforced.

**8. Submitting Changes (Pull Requests):**

1.  Create a feature branch from `main`.
2.  Make your changes, including adding or updating tests.
3.  Ensure all checks pass locally: formatting, linting, type checking, and all tests.
    ```bash
    hatch run lint:fmt --check
    hatch run lint:style
    hatch run lint:typing
    hatch run default:test # or lint:cov
    ```
4.  Commit your changes and push your branch to your fork.
5.  Open a Pull Request (PR) against the `main` branch of the `twardoch/html22text` repository.
6.  Clearly describe your changes in the PR description.
7.  The CI workflow will automatically run all checks on your PR. Ensure they pass.

**9. Changelog:**

*   For significant user-facing changes, new features, or bug fixes, add an entry to `CHANGELOG.md`. Follow the format of existing entries, based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

**10. Dependency Management:**

*   Project dependencies are managed in `pyproject.toml` under the `[project.dependencies]` section.
*   Development dependencies are managed by Hatch environments, also configured in `pyproject.toml`.
*   If you need to add or change a dependency, update `pyproject.toml` accordingly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
