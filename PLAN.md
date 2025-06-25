# PLAN: Streamline html22text for MVP v1.0

This document outlines the detailed plan to streamline the `html22text` codebase, focusing on creating a performant, focused v1.0 (MVP) that does its job very well.

## Guiding Principles:
*   **Focus on MVP:** Prioritize core functionality and robustness for the most common use cases (HTML to Markdown, HTML to plain text).
*   **Conservatism:** Avoid removing code if its utility is uncertain or if it contributes significantly to the "smart" conversion capabilities beyond basic `html2text` behavior.
*   **Performance:** Consider performance implications, especially regarding dependencies.
*   **Maintainability:** Improve code clarity and reduce complexity where possible.

## Detailed Steps:

**1. Setup and Initial Analysis:**
    *   [x] Create `PLAN.md` (this file).
    *   [x] Create `TODO.md` with a simplified checklist.
    *   [x] Create `CHANGELOG.md` for tracking changes.
    *   [x] Review existing codebase (done, leading to this plan).

**2. Investigate `weasyprint.urls` Dependency:**
    *   [x] **Task:** Evaluate if `weasyprint.urls` can be replaced by the standard library's `urllib.parse` for URL manipulation tasks within `html22text.py` (`is_doc`, `rel_txt_href`, `abs_asset_href`). (Completed: `weasyprint` successfully replaced with `urllib.parse`)
    *   **Rationale:** `weasyprint` is a relatively heavy dependency. If its specific URL functions (like advanced IRI/URI handling) are not strictly necessary over what `urllib.parse` offers for this project's scope, removing it would simplify the dependency tree and potentially improve performance/installation ease.
    *   **Sub-steps:**
        1.  [x] Identify all functions using `weasyprint.urls`: `is_doc`, `rel_txt_href`, `abs_asset_href`.
        2.  [x] For each function, analyze the specific `weasyprint.urls` calls (e.g., `url_is_absolute`, `urljoin`, `iri_to_uri`).
        3.  [x] Attempt to reimplement the logic using `urllib.parse` (e.g., `urlparse`, `urljoin`, `quote`, `unquote`). Pay attention to how `iri_to_uri` is handled; `urllib.parse.quote` might be sufficient if only simple IRI-to-URI conversion is needed.
        4.  [x] Test thoroughly:
            *   [x] Ensure existing tests in `test_path_handling_internals` pass or are updated.
            *   [x] Consider edge cases: internationalized domain names (IDNs), IRIs with non-ASCII characters.
        5.  [x] If successful and tests pass:
            *   [x] Remove `weasyprint` from `dependencies` in `pyproject.toml`.
            *   [x] Remove `weasyprint` from `additional_dependencies` in `.pre-commit-config.yaml` for mypy.
            *   [x] Remove the mypy override for `weasyprint.*` in `pyproject.toml`.
            *   [x] Run all tests and linters.
            *   [x] Update `CHANGELOG.md`.
        6.  [ ] If `weasyprint.urls` provides indispensable features (e.g., superior IRI handling critical for the project) that `urllib.parse` cannot easily replicate, document this finding and retain the dependency. (Not applicable, replacement was successful)

**3. Simplify `HTML2Text` Configuration in `html22text` function:**
    *   [x] **Task:** Refactor the instantiation and configuration of the `html2text.HTML2Text` object to reduce redundancy and potentially simplify the main `html22text` function's parameter list.
    *   [x] **Rationale:** Many parameters in `html22text` directly map to `HTML2Text` options, and their settings often depend on the `markdown` boolean flag. This can be made more concise.
    *   [x] **Sub-steps:**
        1.  [x] List all `h.<attribute> = value` assignments.
        2.  [x] Group them:
            *   [x] Settings applied regardless of `markdown` mode.
            *   [x] Settings specific to `markdown=True`.
            *   [x] Settings specific to `markdown=False`.
        3.  [x] Identify `html22text` parameters that are passed directly to `HTML2Text` attributes.
        4.  [x] **Conservative Pruning (MVP Focus):**
            *   [x] Are there any parameters (and corresponding `HTML2Text` options) that are very niche or whose default `html2text` behavior is generally good enough for an MVP? (Decision: Kept existing parameters as they offer valuable control.)
            *   [x] Example: `google_doc`, `google_list_indent`, `images_as_html`, `images_with_size`, `links_each_paragraph`, `pad_tables`, `protect_links`, `single_line_break`, `tag_callback`, `wrap_links`, `wrap_list_items`, `wrap_tables`. Many ofthese are already hardcoded or defaulted by `html2text`. Review if exposing them adds significant value for MVP.
            *   [x] Focus on retaining options that provide significant control over common Markdown/text conversion scenarios (e.g., link handling, image handling, quote styles).
        5.  [x] Refactor the code: (Minor refactoring done, mainly restoring `ignore_tables` logic initially).
            ```python
            h = HTML2Text()
            h.body_width = 0 # Example of a general setting
            # ... other general settings ...

            if markdown:
                h.emphasis_mark = "_"
                h.strong_mark = "**"
                # ... other markdown-specific settings ...
            else: # Plain text
                h.ignore_emphasis = True
                h.ignore_links = True
                # ... other text-specific settings ...

            # Apply settings from parameters that are retained
            h.open_quote = open_quote # If open_quote parameter is kept
            ```
        6.  [x] If parameters are removed: (No parameters removed in this step beyond what was already hardcoded).
            *   [x] Update the `html22text` function signature.
            *   [x] Update its docstring.
            *   [x] Update CLI help text (implicitly via Fire).
            *   [x] Update `README.md` examples if affected.
            *   [x] Adjust or remove tests for the removed parameters.
        7.  [x] Update `CHANGELOG.md`.

**4. Review and Refactor Tag Manipulation Logic:**
    *   [x] **Task:** Analyze the custom HTML tag transformations performed using BeautifulSoup before passing the HTML to `html2text`, and remove transformations if `html2text` can handle them adequately or if they are not essential for an MVP.
    *   [x] **Rationale:** Simplifying this pre-processing step makes the code cleaner and relies more on the core competency of the `html2text` library.
    *   [x] **Sub-steps:**
        1.  [x] **`plain_tables`:**
            *   [x] Current: Manually iterates `<tr>`, `<th>`, `<td>` to create a comma-separated string representation of tables. (Logic was commented out).
            *   [x] `html2text` options: `h.bypass_tables` (currently `False`), `h.ignore_tables` (set based on `markdown`), `h.pad_tables`.
            *   [x] Investigate: What is `html2text`'s default plain text output for tables when `ignore_tables=False` and `bypass_tables=False`? Is it acceptable for an MVP? (Yes, native output is good).
            *   [x] If `html2text`'s output is sufficient (even if different), consider removing the `plain_tables` parameter and custom logic. This would be a significant simplification. (Done, `plain_tables` parameter and logic removed. `ignore_tables` set to `False` always).
        2.  [x] **Tag Renaming/Handling (primarily for `if not markdown:`):**
            *   [x] `mark`, `kbd`: `tag.replace_with(tag.get_text(""))`. This seems fine and is a common requirement to strip these. (Kept).
            *   [x] `blockquote`: If `block_quote` is true, it's turned into `<q>` and wrapped in `<p>`. If false, into `<div>`. (Logic refined: if `block_quote` is true, transform to `<p><q>`; otherwise, let `html2text` handle `<blockquote>` natively).
                *   [x] `html2text` behavior: How does it handle `<blockquote>` in text mode by default? Does it offer quote character options? The `open_quote` and `close_quote` parameters are passed to `html2text`. The `block_quote` parameter essentially decides if `<blockquote>` should use these quotes. This might be a valuable feature to keep.
            *   [x] `ul`, `ol`, `figure` to `div`: (Removed this transformation. Let `html2text` handle natively).
                *   [x] `html2text` behavior: How does it handle these in text mode? It likely has reasonable list formatting and might just strip `figure` or extract its content.
                *   [x] If `html2text`'s default is acceptable, these renamings can be removed.
            *   [x] `label`, `h1`-`h6`, `figcaption`, `li` to `p`: (Removed this transformation. Let `html2text` handle natively).
                *   [x] `html2text` behavior: It should handle headers and list items appropriately for text output (e.g., newlines, prefixes for `li`). Converting them all to `<p>` first might be redundant or counterproductive.
                *   [x] Investigate and simplify if `html2text`'s defaults are good.
            *   [x] `code` to `q`: (Removed this transformation. Let `html2text` handle natively).
                *   [x] `html2text` behavior: It has `mark_code` (currently `False`). How does it render `<code>` or `<pre>` blocks in text mode? Turning `<code>` into `<q>` seems unusual; inline code is typically rendered as is or with special markers if `mark_code` is true. This needs justification or removal.
        3.  [x] **`kill_tags`:** The logic `for kill_item in actual_kill_tags: ... soup.select(kill_item).replace_with("")` is standard and essential. (Kept, and CLI parsing for it was fixed).
        4.  [x] **Implementation:**
            *   [x] For each identified custom transformation, comment it out temporarily.
            *   [x] Run relevant tests or create new small test cases to observe `html2text`'s default behavior for those tags in both Markdown and text mode.
            *   [x] Decide whether to keep or remove the custom transformation based on MVP goals and conservatism.
        5.  [x] Update tests and `CHANGELOG.md`.

**5. Review Helper Functions for Conciseness (Post-`weasyprint` investigation):**
    *   [x] **Task:** After the `weasyprint.urls` decision and potential rewrite using `urllib.parse`, review the link helper functions (`is_doc`, `rel_txt_href`, `abs_asset_href`) and the functions that use them (`replace_asset_hrefs`, `prep_doc`) for any further minor simplifications or readability improvements.
    *   [x] **Rationale:** Ensure these functions are clean and efficient.
    *   [x] **Sub-steps:**
        1.  [x] Read through the code of these functions.
        2.  [x] Check for any overly complex logic that could be expressed more simply.
        3.  [x] Verify that type hints are accurate and helpful.
        4.  [x] The warning for list `href` attributes in `prep_doc`: `isinstance(current_href, list)` for an anchor tag's `href`. This is highly unlikely with standard HTML parsing. Consider if this check is necessary or if it can be removed as BeautifulSoup typically returns a string for `href`. If kept, ensure the warning is informative. (Removed this warning).
        5.  [x] Update `CHANGELOG.md` if any changes are made.

**6. Final Code and Documentation Review:**
    *   [x] **Task:** Perform a holistic review of the codebase and documentation after the streamlining changes.
    *   [x] **Rationale:** Ensure consistency, correctness, and clarity.
    *   [x] **Sub-steps:**
        1.  [x] Read through `src/html22text/html22text.py` one last time.
        2.  [x] Check comments: Are they explaining "why" not just "what"? Are they up-to-date?
        3.  [x] Check docstrings: Is the main `html22text` docstring accurate given any parameter changes? Are other docstrings clear? (Docstring for `kill_tags` updated to reflect comma-separated string).
        4.  [x] `README.md`:
            *   [x] Verify installation instructions.
            *   [x] Verify CLI examples and API examples. (CLI for `kill_tags` updated).
            *   [x] Ensure feature list is accurate.
        5.  [x] `pyproject.toml`:
            *   [x] Confirm dependencies are correct.
            *   [x] Ensure project metadata is accurate.
        6.  [x] Update `CHANGELOG.md` with any final touch-ups. (Consolidated).

**7. Testing and Validation:**
    *   [x] **Task:** Run all automated checks and perform manual validation.
    *   [x] **Rationale:** Catch any regressions or issues introduced during refactoring.
    *   [x] **Sub-steps:**
        1.  [x] Run Ruff formatter: `hatch run lint:fmt --check` (or `hatch run lint:fmt` to apply changes).
        2.  [x] Run Ruff linter: `hatch run lint:style`. Fix any issues.
        3.  [x] Run MyPy type checker: `hatch run lint:typing`. Fix any issues.
        4.  [x] Run Pytest with coverage: `hatch run lint:cov`.
            *   [x] Ensure all tests pass.
            *   [x] Review coverage report. Aim to maintain or improve coverage. (Coverage at 78%).
        5.  [x] Manual Testing:
            *   [x] Prepare a few diverse HTML samples (simple paragraph, links, images, lists, a basic table, some tags to be killed).
            *   [x] Use the CLI to convert them to Markdown.
            *   [x] Use the CLI to convert them to plain text.
            *   [x] Verify the output looks reasonable and aligns with the expected MVP behavior. (Identified and fixed `kill_tags` CLI issue).

**8. Update `PLAN.md` and `TODO.md`:**
    *   [x] **Task:** Mark all completed steps.
    *   [x] **Rationale:** Track progress.

**9. Submit Changes:**
    *   **Task:** Commit the streamlined code.
    *   **Rationale:** Finalize the refactoring effort.
    *   **Sub-steps:**
        1.  Stage all changes.
        2.  Write a comprehensive commit message summarizing the streamlining effort and key changes.
        3.  Use a descriptive branch name (e.g., `refactor/streamline-mvp`).
        4.  (If applicable in a team setting) Push the branch and create a Pull Request.

This plan aims for a balance between significant streamlining for an MVP and a conservative approach to preserve the core value of `html22text`.
