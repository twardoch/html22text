# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `docs/` directory with Jekyll-compatible documentation:
  - `docs/index.md` — API overview and quick-start
  - `docs/preserving-stripping.md` — full table of what Markdown and plain-text
    modes preserve vs. strip, with worked examples and link-handling reference
- `kill_tags` now accepts a `list[str]` in addition to a comma-separated string,
  matching what the test suite and direct Python callers naturally pass.

### Changed
- `html22text()` return value: empty or whitespace-only output now returns `""`
  instead of `"\n"`, making empty-HTML edge cases easier to check.
- `_iri_to_uri_urllib()`: added `%` to the percent-encode safe chars so that
  already-encoded sequences (e.g. `%20`) are not double-encoded to `%2520`.
- README rewritten to ~120 lines; "Technical Details / How the Code Works" block
  moved to `docs/preserving-stripping.md`.

### Fixed
- `kill_tags` list-type argument raised `AttributeError: 'list' has no attribute
  'split'` — now handled correctly for both `str` and `list[str]` inputs.
- CLI tests hardcoded `cwd="/root/repo"` (a Linux Docker path) and `"python"`
  (not available on macOS); rewritten to use `sys.executable` and the real repo
  root.
- `test_special_characters_in_links` asserted `.html` extension after conversion
  that rewrites it to `.md`; assertion corrected to `.md`.
- Two image-only plain-text tests expected `"\n"` but the function now correctly
  returns `""` for whitespace-only output; tests updated to expect `""`.
- `test_full_workflow` blockquote assertion required the opening quote character
  to immediately precede the text, but html2text inserts a space; assertion
  loosened to check the text content only.
- `test_cli_help` checked `stdout` for "html22text" but Fire writes help to
  `stderr` and names the module `__main__.py`; assertion updated to check both
  streams for "html".



### Added
- Initial `PLAN.md`, `TODO.md`, and `CHANGELOG.md` for streamlining project.
- Robust fallback mechanism for `SelectorSyntaxError` import, attempting `bs4`, then `soupsieve.util`, then a dummy class.

### Changed
- Refactored URL handling functions (`is_doc`, `rel_txt_href`, `abs_asset_href`) to use `urllib.parse` instead of `weasyprint.urls`.
- Reorganized `HTML2Text` option settings within `html22text` function for clarity and consistency.
- Simplified HTML tag manipulation logic for plain text conversion:
    - Now relies on `html2text`'s native handling for tables, lists (`<ul>`, `<ol>`, `<li>`), headers (`<h1>`-`<h6>`), `<figure>`, `<label>`, and `<code>` tags, instead of specific pre-conversions to `<p>`, `<div>`, or `<q>`.
    - `html2text.HTML2Text.ignore_tables` is now consistently set to `False`, enabling native table processing by `html2text` for both Markdown and plain text outputs.
    - The `block_quote` parameter still controls `<blockquote>` transformation to `<q>` for plain text; otherwise, `html2text`'s default indentation for `<blockquote>` is used.
    - Stripping of `<mark>` and `<kbd>` tags (keeping their content) remains.
- Modified `html2text` to enable code marking (`[code]...[/code]`) for Markdown output by setting `HTML2Text.mark_code = True` when `markdown=True`.
- Corrected various linting and type annotation issues identified by Ruff and Mypy across the codebase.
- Changed `ValueError` to `TypeError` for unexpected list `href` attributes in `<link>` tags, as suggested by Ruff (TRY004).
- Updated tests to reflect changes in default plain text output for tables, blockquotes, and lists.

### Removed
- Removed `weasyprint` dependency from the project (`pyproject.toml`, mypy checks in `.pre-commit-config.yaml`).
- Removed the `plain_tables` parameter and its associated custom table formatting logic from the `html22text` function and its docstring; `html2text`'s native table rendering is now used.
- Removed an unlikely-to-occur check and warning for `<a>` tag `href` attributes being a list within the `prep_doc` function.

### Fixed
- Corrected CLI handling of the `kill_tags` parameter. It now accepts a single comma-separated string of CSS selectors (e.g., `--kill_tags "script,.ad"`) instead of attempting to parse multiple arguments. This resolves issues with `python-fire` misinterpreting individual characters of a selector as separate list items.
