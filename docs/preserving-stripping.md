---
layout: default
title: What gets preserved and what gets stripped
---

# What gets preserved and what gets stripped

`html22text` converts HTML to Markdown or plain text.  The tables below show
which HTML constructs survive in each output mode.

---

## Markdown mode (`markdown=True`)

| HTML construct | Markdown output | Notes |
|---|---|---|
| `<h1>…<h6>` | `# …` through `###### …` | ATX-style headers |
| `<p>` | Paragraph separated by blank lines | |
| `<strong>`, `<b>` | `**…**` | |
| `<em>`, `<i>` | `_…_` | |
| `<a href="…">` | `[text](url)` | Relative `.html` links rewritten if `file_ext_override` set |
| `<img src="…" alt="…">` | `![alt](src)` | Removed when `kill_images=True` |
| `<code>` | `` `…` `` | Inline code |
| `<pre><code>` | Fenced code block | |
| `<ul>` / `<ol>` / `<li>` | `-` or `1.` list items | |
| `<blockquote>` | `> …` indentation | |
| `<table>` | Pipe-table (`|…|`) | |
| `<mark>`, `<kbd>` | Plain text content only | Tags stripped, text kept |
| `<s>` (strikethrough) | Kept if `kill_strikethrough=False` | |
| `<q>` | Wrapped with `open_quote` / `close_quote` | |
| `<script>`, `<style>` | **Stripped** by default | Pass `kill_tags=["script","style"]` |
| HTML comments | **Stripped** | |
| HTML entities (`&amp;`, `&lt;`, …) | Decoded to Unicode | |
| IRI/IDN hostnames | Converted to Punycode URI | |

### Example — Markdown

```python
from html22text import html22text

html = """
<h1>Title</h1>
<p>A paragraph with <strong>bold</strong> and <em>italic</em>.</p>
<ul>
  <li>Item one</li>
  <li>Item two with <a href="page.html">a link</a></li>
</ul>
<blockquote>A quoted passage.</blockquote>
<script>trackMe();</script>
"""

print(html22text(html, markdown=True, kill_tags=["script"]))
```

Output:

```markdown
# Title

A paragraph with **bold** and _italic_.

- Item one
- Item two with [a link](page.html)

> A quoted passage.
```

---

## Plain-text mode (`markdown=False`)

| HTML construct | Plain-text output | Notes |
|---|---|---|
| `<h1>…<h6>` | Header text with `#` prefix | html2text still uses ATX syntax |
| `<p>` | Text separated by blank lines | |
| `<strong>`, `<b>` | Plain text only (markers removed) | `strong_mark=""` |
| `<em>`, `<i>` | Plain text only (markers removed) | `emphasis_mark=""` |
| `<a href="…">` | Link text only | href discarded |
| `<img>` | Discarded | Image alt text also dropped |
| `<code>`, `<pre>` | Text content preserved | No backtick markers |
| `<ul>` / `<ol>` / `<li>` | Indented text items | No `-` / `1.` markers |
| `<blockquote>` | Indented block by default | Wrap with `open_quote`/`close_quote` when `block_quote=True` |
| `<q>` | Wrapped with `open_quote` / `close_quote` | Default `"…"` |
| `<table>` | Pipe-table (html2text renders tables in both modes) | |
| `<mark>`, `<kbd>` | Plain text content only | |
| HTML entities | Decoded to Unicode | |

### Example — plain text

```python
from html22text import html22text

html = """
<h2>Section</h2>
<p>Some text with <em>emphasis</em>.</p>
<blockquote>An important note.</blockquote>
<q>A short quote.</q>
"""

print(html22text(html, markdown=False, block_quote=True, open_quote="«", close_quote="»"))
```

Output:

```
## Section

Some text with emphasis.

«An important note.»

«A short quote.»
```

---

## Content filtering with `kill_tags`

The `kill_tags` parameter accepts a comma-separated string **or** a list of
CSS selectors.  Matched elements and all their children are removed before
conversion.

```python
html = """
<nav class="site-nav"><a href="/">Home</a></nav>
<main>
  <p>Article text.</p>
  <aside class="ad">Buy now!</aside>
</main>
"""

result = html22text(
    html,
    markdown=True,
    kill_tags=["nav", ".ad"],   # list form
)
# kill_tags="nav,.ad"            # string form — equivalent
```

Result:

```markdown
Article text.
```

---

## Link handling

| Scenario | Behaviour |
|---|---|
| Relative `.html` link + `file_ext_override="md"` | `page.html` → `page.md` |
| Relative link + `base_url` | Resolved to absolute URL |
| Percent-encoded link (`%20`) | Preserved as-is (no double-encoding) |
| HTML entity in href (`&amp;`) | Decoded to `&` by the HTML parser |
| Absolute URL | Unchanged (IRI→URI Punycode applied to IDN hostname) |
| Fragment (`#section`) | Unchanged |
| mailto link | Kept in Markdown mode; discarded in plain-text mode |
