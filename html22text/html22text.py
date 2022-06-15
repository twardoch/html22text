#!/usr/bin/env python3

import os
from pathlib import Path

from weasyprint import urls
from bs4 import BeautifulSoup
from html2text import HTML2Text

# check if href is relative --
# if it is relative it *should* be an html that generates a text file
def is_doc(href: str):
    tail = os.path.basename(href)
    _, ext = os.path.splitext(tail)

    absurl = urls.url_is_absolute(href)
    abspath = os.path.isabs(href)
    htmlfile = ext.startswith(".html")
    if absurl or abspath or not htmlfile:
        return False

    return True


def rel_txt_href(href: str, file_ext: str = ".txt"):
    head, tail = os.path.split(href)
    filename, _ = os.path.splitext(tail)

    internal = href.startswith("#")
    if not is_doc(href) or internal:
        return href

    return urls.iri_to_uri(os.path.join(head, f"{filename}.{file_ext}"))


def abs_asset_href(href: str, base_url: str):
    if urls.url_is_absolute(href) or os.path.isabs(href):
        return href

    return urls.iri_to_uri(urls.urljoin(base_url, href))


# makes all relative asset links absolute
def replace_asset_hrefs(soup: BeautifulSoup, base_url: str):
    for link in soup.find_all("link", href=True):
        link["href"] = abs_asset_href(link["href"], base_url)

    for asset in soup.find_all(src=True):
        asset["src"] = abs_asset_href(asset["src"], base_url)

    return soup


def prep_doc(soup: BeautifulSoup, base_url: str, file_ext: str = "txt"):
    # transforms all relative hrefs pointing to other html docs
    # into relative txt hrefs
    for a in soup.find_all("a", href=True):
        a["href"] = rel_txt_href(a["href"], file_ext)

    soup = replace_asset_hrefs(soup, base_url)
    return soup


def html22text(
    html: str, # HTML source
    input: bool = False, # If True, html is a path
    markdown: bool = False, # Output Markdown if True or plain-text if False
    base_url: str = "", # Base URL within which links to HTML will be converted to MD links
    plain_tables: bool = False, # If plain-text, write a simplified table format
    open_quote: str = "“", # Start char for <q> content in plain-text
    close_quote: str = "”", # End char for <q> content in plain-text
    block_quote: bool = False, # If True, treat <blockquote> as <q> in plain-text
    default_image_alt: str = "", # Default text for image content in plain-text
    kill_strikethrough: bool = False, # Remove <s>content</s>
    kill_tags: list = [], # Remove content of selectors
    file_ext: str = "", # Output file extension for link conversion
):
    if input:
        html = Path(html).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    if not file_ext:
        if markdown:
            file_ext = "md"
        else:
            file_ext = "txt"

    if markdown:
        soup = prep_doc(soup, base_url, file_ext)

    for tag in soup.find_all(True):
        if tag.name in ("mark", "kbd"):
            tag.replace_with(tag.get_text(""))
        if plain_tables and tag.name == "table":
            rows = []
            for tr in tag.find_all("tr"):
                cells = [td.get_text(" ") for td in tr.find_all(["th", "td"])]
                rows.append(", ".join(cells))
            tag.replace_with(". ".join(rows))
        if not markdown:
            if tag.name == "blockquote":
                if block_quote:
                    tag.name = "q"
                    tag.wrap(soup.new_tag("p"))
                else:
                    tag.name = "div"
            elif tag.name in ("ul", "ol", "figure"):
                tag.name = "div"
            elif tag.name in (
                "label",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "figcaption",
                "li",
            ):
                tag.name = "p"
            elif tag.name in ("code"):
                tag.name = "q"
    for kill_tag in kill_tags:
        for tag in soup.select(kill_tag):
            tag.replace_with("")

    # return str(soup)
    html = HTML2Text()
    html.body_width = 0
    html.bypass_tables = False
    html.close_quote = close_quote
    html.default_image_alt = default_image_alt
    html.emphasis_mark = "_" if markdown else ""
    html.escape_snob = False
    html.google_doc = False
    html.google_list_indent = 0
    html.hide_strikethrough = kill_strikethrough
    html.ignore_emphasis = not markdown
    html.ignore_images = not markdown
    html.ignore_links = not markdown
    html.ignore_mailto_links = not markdown
    html.ignore_tables = not markdown
    html.images_as_html = False
    html.images_to_alt = not markdown
    html.images_with_size = False
    html.inline_links = bool(markdown)
    html.links_each_paragraph = False
    html.mark_code = False
    html.open_quote = open_quote
    html.pad_tables = bool(markdown)
    html.protect_links = True
    html.single_line_break = False
    html.skip_internal_links = not markdown
    html.strong_mark = "**" if markdown else ""
    html.tag_callback = None
    html.ul_item_mark = "-" if markdown else ""
    html.unicode_snob = True
    html.use_automatic_links = bool(markdown)
    html.wrap_links = False
    html.wrap_list_items = False
    html.wrap_tables = False
    return html.handle(str(soup))

