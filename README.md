# html22text

Python package to convert HTML into Markdown or plain text in a smart way.

## Installation

```
pip install git+https://github.com/twardoch/html22text
```

## Usage

### Command-line

```
html22text HTML [--input --markdown --base_url --plain_tables
                         --open_quote --close_quote --block_quote
                         --default_image_alt --kill_strikethrough
                         --kill_tags --file_ext ]
```

`HTML` may be HTML text or, if `--input` is specified, a path to a HTML file.

You may invoke the tool as `html22text` or as `python3 -m html22text`.

### Python

```python
from html22text import html22text

html = "<p>Hello <b><a href='.'>this</a> world</b>!</p>"
text = html22text(
    html, # HTML source
    input=False, # If True, html is a path
    markdown=True,
    base_url="", # Base URL within which links to HTML will be converted to MD links
    plain_tables=False, # If plain-text, write a simplified table format
    open_quote="“", # Start char for <q> content in plain-text
    close_quote="”", # End char for <q> content in plain-text
    block_quote=False, # If True, treat <blockquote> as <q> in plain-text
    default_image_alt="", # Default text for image content in plain-text
    kill_strikethrough=True, # Remove <s>content</s>
    kill_tags=['pre', 'p.admonition-title'], # Remove content of selectors
    file_ext="md", # Output file extension for link conversion
)

print(text)
```
