# html22text

Python package to convert HTML into Markdown or plain text in a smart way.

```python
from html22text import html22text

html = "<p>Hello <b>world</b>!</p>"
text = html22text(
    html,
    base_url="",
    markdown=True,
    plain_tables=False,
    open_quote="“",
    close_quote="”",
    default_image_alt="",
    hide_strikethrough=True,
    kill_tags=['pre', 'p.admonition-title'],
    file_ext"md",
)
print(text)
```

