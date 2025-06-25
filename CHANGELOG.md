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
- Reorganized `HTML2Text` option settings within `html22text` function for clarity.
- Modified `html2text` to enable code marking (`[code]...[/code]`) for Markdown output by setting `HTML2Text.mark_code = True` when `markdown=True`.
- Corrected various linting and type annotation issues identified by Ruff and Mypy across the codebase.
- Changed `ValueError` to `TypeError` for unexpected list `href` attributes, as suggested by Ruff (TRY004).

### Removed
- Removed `weasyprint` dependency from the project (`pyproject.toml`, mypy checks in `.pre-commit-config.yaml`).
