---
layout: default
title: html22text
---

# html22text

Convert HTML to well-formatted Markdown or clean plain text.

Built on [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and
[html2text](https://github.com/Alir3z4/html2text), `html22text` adds smart
link resolution, CSS-selector content filtering, and configurable quoting.

## Quick start

```bash
pip install html22text
```

```python
from html22text import html22text

# Markdown output
md = html22text("<p>Hello <b>world</b>!</p>", markdown=True)
# → "Hello **world**!\n"

# Plain-text output
txt = html22text("<p>Hello <b>world</b>!</p>", markdown=False)
# → "Hello world!\n"
```

## Pages

- [What gets preserved and what gets stripped](preserving-stripping.md)

## API reference

```
html22text(
    html_content,        # HTML string or file path
    is_input_path=False, # True → html_content is a file path
    markdown=False,      # True → Markdown output; False → plain text
    selector="html",     # CSS selector for content extraction
    base_url="",         # Resolve relative links to this base
    open_quote="“", # Opening quote char for <q>
    close_quote="”",# Closing quote char for </q>
    block_quote=False,   # Treat <blockquote> like <q> in plain-text mode
    default_image_alt="",# Alt text placeholder for images (plain-text)
    kill_strikethrough=False, # Remove <s>…</s> content
    kill_tags=None,      # CSS selectors to remove (str or list)
    kill_images=False,   # Remove images entirely
    file_ext_override="",# Replace .html extension in relative links
) -> str
```

Full documentation: <https://github.com/twardoch/html22text>
