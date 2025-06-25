# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
