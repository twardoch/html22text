# PLAN: Splitting `html22text.py`

This plan outlines how to refactor the `src/html22text/html22text.py` file by moving URL-related utility functions into a new module, `src/html22text/url_utils.py`. The goal is cleaner code organization without changing any behavior.

## Guiding Principles:
*   **No functional changes** – Everything should work exactly as before.
*   **Better modularity** – Group related functions in dedicated modules.
*   **Improved readability** – Reduce file size and keep core logic focused.
*   **Preserve test coverage** – Existing tests will verify nothing breaks.

## Detailed Steps:

### Step 1: Create New Module
Create `src/html22text/url_utils.py`.

**Action:**
1.  Create file: `/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/html22text/src/html22text/url_utils.py`

### Step 2: Move Functions
Move these six functions from `html22text.py` to `url_utils.py`:
*   `_iri_to_uri_urllib`
*   `is_doc`
*   `rel_txt_href`
*   `abs_asset_href`
*   `replace_asset_hrefs`
*   `prep_doc`

**Action:**
1.  Open `src/html22text/html22text.py`.
2.  Cut those function definitions and their docstrings.
3.  Open `src/html22text/url_utils.py`.
4.  Paste functions there.
5.  Add required imports:
    ```python
    from pathlib import Path
    from urllib.parse import quote as urlquote, urljoin, urlparse
    from bs4 import BeautifulSoup
    from bs4.element import Tag
    ```

### Step 3: Update Imports in `html22text.py`
Replace removed functions with imports from the new module.

**Action:**
1.  Open `src/html22text/html22text.py`.
2.  Remove old function definitions.
3.  Add import:
    ```python
    from .url_utils import (
        _iri_to_uri_urllib,
        is_doc,
        rel_txt_href,
        abs_asset_href,
        replace_asset_hrefs,
        prep_doc,
    )
    ```
4.  Remove now-unused imports (e.g., `Path`, `urlparse`, etc.) if they aren't used elsewhere.

### Step 4: Fix Test Imports
Tests in `tests/test_html22text.py` import some of the moved functions directly.

**Action:**
1.  Open `tests/test_html22text.py`.
2.  Change this line:
    ```python
    from html22text.html22text import abs_asset_href, is_doc, rel_txt_href
    ```
    to:
    ```python
    from html22text.url_utils import abs_asset_href, is_doc, rel_txt_href
    ```

### Step 5: Run Tests
Verify that refactoring didn't break anything.

**Action:**
1.  Run:
    ```bash
    hatch run lint:cov
    ```
2.  Confirm all tests pass and coverage is still acceptable.

### Step 6: Check `pyproject.toml`
Hatch should automatically include the new module, but double-check.

**Action:**
1.  Open `pyproject.toml`.
2.  Look at `[tool.hatch.build.targets.wheel]`.
3.  Confirm `packages = ["src/html22text"]` is set – no change needed if so.

### Step 7: Update Changelog and TODO
Record what was done.

**Action:**
1.  Open `CHANGELOG.md`.
2.  Add under `[Unreleased]`:
    ```markdown
    ### Changed
    - Moved URL utility functions (`_iri_to_uri_urllib`, `is_doc`, `rel_txt_href`, `abs_asset_href`, `replace_asset_hrefs`, `prep_doc`) to `src/html22text/url_utils.py`.
    ```
3.  Open `TODO.md`.
4.  Mark completed tasks. Optionally add a note about splitting test files later.

### Step 8: Commit Changes
Save progress with a clear message.

**Action:**
1.  Stage:
    *   `src/html22text/html22text.py`
    *   `src/html22text/url_utils.py`
    *   `tests/test_html22text.py`
    *   `CHANGELOG.md`
    *   `TODO.md`
2.  Commit with message:  
    `"Refactor: Extract URL utilities to url_utils.py"`