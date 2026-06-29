# html22text

Convert HTML to well-formatted Markdown or clean plain text.

Built on [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and
[html2text](https://github.com/Alir3z4/html2text), `html22text` adds smart
link resolution, CSS-selector content filtering, and configurable quoting.

**What it does:**

- **HTML to Markdown** — preserves headers, lists, code blocks, tables, links
- **HTML to plain text** — strips markup, preserves readable structure
- **Smart link handling** — resolves relative URLs, rewrites `.html` extensions,
  correct IRI-to-URI conversion without double-encoding
- **Content filtering** — remove any elements by CSS selector (`kill_tags`)

See [docs/preserving-stripping.md](docs/preserving-stripping.md) for a full
table of what each mode keeps and drops.

## Installation

```bash
pip install html22text
# or
uvx html22text --help
```

## Command-line usage

```bash
# Plain text from an HTML file
html22text page.html --is_input_path

# Markdown from a string
html22text "<p>Hello <b>World</b></p>" --markdown

# Markdown with link rewriting and tag removal
html22text page.html --is_input_path \
    --markdown \
    --base_url "http://example.com/" \
    --file_ext_override md \
    --kill_tags "script,nav,.ads"

# Chain a Python str method (powered by python-fire)
html22text "<p>HELLO</p>" - lower
```

Full option list: `html22text --help`

## Python API

```python
from html22text import html22text

# Markdown
md = html22text(
    "<h1>Title</h1><p><a href='page.html'>link</a></p>",
    markdown=True,
    base_url="https://example.com/",
    file_ext_override="md",
    kill_tags=["script", "style"],   # list or comma-separated string
)

# Plain text with custom quoting
txt = html22text(
    "<p>Text</p><blockquote>A quote.</blockquote>",
    markdown=False,
    block_quote=True,
    open_quote="« ",
    close_quote=" »",
)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `html_content` | `str` | — | HTML string or file path |
| `is_input_path` | `bool` | `False` | Treat `html_content` as a file path |
| `markdown` | `bool` | `False` | `True` → Markdown; `False` → plain text |
| `selector` | `str` | `"html"` | CSS selector to extract document portion |
| `base_url` | `str` | `""` | Base URL for resolving relative links |
| `open_quote` | `str` | `"“"` | Opening quote for `<q>` |
| `close_quote` | `str` | `"”"` | Closing quote for `</q>` |
| `block_quote` | `bool` | `False` | Treat `<blockquote>` like `<q>` in plain-text |
| `default_image_alt` | `str` | `""` | Alt-text placeholder for images (plain-text) |
| `kill_strikethrough` | `bool` | `False` | Remove `<s>…</s>` content |
| `kill_tags` | `str \| list[str] \| None` | `None` | CSS selectors to remove |
| `kill_images` | `bool` | `False` | Remove images entirely |
| `file_ext_override` | `str` | `""` | Replace `.html` extension in relative links |

## Development

```bash
git clone https://github.com/twardoch/html22text.git
cd html22text
pip install -e ".[dev]"

# Tests
uvx hatch test

# Lint + type-check
uvx hatch run lint:lint-all
```

Requirements: Python 3.10+.

## Documentation

- [Preserve/strip reference](docs/preserving-stripping.md) — complete table of
  what each mode keeps and drops, with examples
- [CHANGELOG](CHANGELOG.md)
- [INSTALL](INSTALL.md)

## License

MIT License — see [LICENSE](LICENSE).
