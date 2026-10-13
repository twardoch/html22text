# TODO: Streamline html22text for MVP v1.0

## Pending: first PyPI release (2026-10-13)

- [ ] Upload v1.0.1 to PyPI. Tag `v1.0.1` is pushed and `./publish.sh` built `dist/`, but PyPI
      refused the upload with `429 Too many new projects created` (a per-account limit on
      creating new projects). Retry with `uv publish dist/*`, or rebuild from the tag with
      `./build.sh` first. `vexy-mkdocs-text-export` cannot be released until this is on PyPI.

## MVP v1.0

- [x] Create `PLAN.md` with detailed steps.
- [x] Create `TODO.md` (this file).
- [x] Create `CHANGELOG.md`.
- [x] **Investigate `weasyprint.urls` Dependency:** (Completed: `weasyprint` successfully replaced with `urllib.parse`)
    - [x] Analyze usage in `is_doc`, `rel_txt_href`, `abs_asset_href`.
    - [x] Attempt replacement with `urllib.parse`.
    - [x] Test thoroughly.
    - [x] If successful, remove dependency and update configs. Otherwise, document and keep.
- [x] **Simplify `HTML2Text` Configuration:**
    - [x] Analyze parameter mapping to `HTML2Text` attributes.
    - [x] Refactor configuration logic for conciseness.
    - [x] Conservatively prune non-essential exposed parameters for MVP. (No parameters pruned).
    - [x] Update function signature, docstrings, CLI, and tests if parameters change.
- [x] **Review and Refactor Tag Manipulation Logic:**
    - [x] Evaluate `plain_tables` custom logic vs. `html2text` capabilities. (Removed custom logic).
    - [x] Review non-Markdown tag renamings (`blockquote`, `ul`, `ol`, `figure`, headers, `li`, `code`) vs. `html2text` defaults. (Simplified to rely more on `html2text`).
    - [x] Keep essential `kill_tags` and `mark`/`kbd` stripping. (Kept).
    - [x] Simplify by removing custom logic if `html2text` defaults are acceptable for MVP. (Done).
    - [x] Update tests.
- [x] **Review Helper Functions for Conciseness:**
    - [x] Post-`weasyprint` investigation, review link helpers (`is_doc`, `rel_txt_href`, `abs_asset_href`, `replace_asset_hrefs`, `prep_doc`) for minor simplifications.
    - [x] Check warning for list `href` attributes in `prep_doc`. (Removed warning).
- [x] **Final Code and Documentation Review:**
    - [x] Review comments and docstrings.
    - [x] Ensure `README.md` is accurate (API, CLI examples).
    - [x] Verify `pyproject.toml`.
- [x] **Testing and Validation:**
    - [x] Run all linters, formatters, type checks (`ruff`, `mypy`).
    - [x] Run all tests with coverage (`pytest`). (78% coverage achieved).
    - [x] Perform manual CLI testing with representative HTML samples. (CLI bug for `kill_tags` fixed).
- [x] **Update `PLAN.md` and `TODO.md`:**
    - [x] Mark all steps as complete.
- [ ] **Submit Changes:**
    - [ ] Commit with a comprehensive message to a new branch.
