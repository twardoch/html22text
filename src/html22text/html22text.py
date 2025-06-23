#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, Union, cast # For type hinting kill_tags and casting

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, PageElement # Import specific BS4 types
from html2text import HTML2Text
from weasyprint import urls


def is_doc(href: str) -> bool:
    """Check if href is relative and points to an HTML-like file.

    If it is relative it *should* be an html that generates a text file.

    Args:
        href (str): input URL

    Returns:
        bool: True if relative and HTML-like.
    """
    href_path = Path(href)
    ext = href_path.suffix

    absurl = urls.url_is_absolute(href)
    # For local paths, check if it's absolute using Path.is_absolute()
    # We assume href is a path-like string if not a URL
    abspath = False if absurl else href_path.is_absolute()
    htmlfile = ext.lower() in (".html", ".htm")  # Use .lower() for case-insensitivity

    return not (absurl or abspath or not htmlfile)


def rel_txt_href(href: str, file_ext: str = ".txt") -> str:
    """Converts a relative HTML href to a relative text href.

    Args:
        href (str): URL.
        file_ext (str, optional): Target file extension. Defaults to ".txt".

    Returns:
        str: URL.
    """
    href_path = Path(href)
    filename = href_path.stem

    internal = href.startswith("#")
    if not is_doc(href) or internal:
        return href

    # Construct new path using Path objects for robustness
    new_path = href_path.with_name(f"{filename}.{file_ext.lstrip('.')}")
    return cast(str, urls.iri_to_uri(str(new_path)))


def abs_asset_href(href: str, base_url: str) -> str:
    """Makes a possibly relative asset URL absolute.

    Args:
        href (str): URL.
        base_url (str): Base URL to resolve relative links.

    Returns:
        str: Absolute URL.
    """
    href_path = Path(href)
    if urls.url_is_absolute(href) or href_path.is_absolute():
        return href

    return cast(str, urls.iri_to_uri(urls.urljoin(base_url, href)))


def replace_asset_hrefs(soup: BeautifulSoup, base_url: str) -> BeautifulSoup:
    """Makes all relative asset links absolute in the soup.

    Args:
        soup (BeautifulSoup): Parsed HTML.
        base_url (str): Base URL.

    Returns:
        BeautifulSoup: Modified soup.
    """
    for element in soup.find_all("link", href=True):
        if isinstance(element, Tag):
            link_tag: Tag = element
            current_href = link_tag.get("href")
            if isinstance(current_href, str):
                link_tag["href"] = abs_asset_href(current_href, base_url)
            elif isinstance(current_href, list):  # Should not happen for 'href'
                raise ValueError(f"Unexpected list value for 'href' attribute in <link>: {current_href}")

    for element in soup.find_all(src=True):
        if isinstance(element, Tag):
            asset_tag: Tag = element
            current_src = asset_tag.get("src")
            if isinstance(current_src, str):
                asset_tag["src"] = abs_asset_href(current_src, base_url)
            elif isinstance(current_src, list): # Should not happen for 'src'
                asset_tag["src"] = abs_asset_href(str(current_src[0]), base_url)

    return soup


def prep_doc(
    soup: BeautifulSoup, base_url: str, file_ext: str = "txt"
) -> BeautifulSoup:
    """Transforms relative HTML doc hrefs to relative text hrefs.

    Args:
        soup (BeautifulSoup): Parsed HTML.
        base_url (str): Base URL.
        file_ext (str, optional): Target file extension. Defaults to "txt".

    Returns:
        BeautifulSoup: Modified soup.
    """
    for element in soup.find_all("a", href=True):
        if isinstance(element, Tag):
            anchor_tag: Tag = element
            current_href = anchor_tag.get("href")
            if isinstance(current_href, str):
                anchor_tag["href"] = rel_txt_href(current_href, file_ext)
            elif isinstance(current_href, list):  # Should not happen for 'href'
                import warnings
                warnings.warn(
                    f"Anchor tag with unexpected list 'href': {current_href}. Skipping transformation.",
                    UserWarning
                )

    # The RET504 for this was valid, direct return.
    return replace_asset_hrefs(soup, base_url)


def html22text(  # noqa: PLR0912, PLR0913, PLR0915
    html_content: str,  # Renamed from html to avoid confusion with module
    is_input_path: bool = False,  # Renamed from input
    markdown: bool = False,
    selector: str = "html",
    base_url: str = "",
    plain_tables: bool = False,
    open_quote: str = "“",
    close_quote: str = "”",
    block_quote: bool = False,
    default_image_alt: str = "",
    kill_strikethrough: bool = False,
    kill_tags: list[str] | None = None,  # B006 fix
    kill_images: bool = False,
    file_ext_override: str = "",  # Renamed file_ext to avoid confusion
) -> str:
    """Convert HTML text or file to Markdown or plain-text text.

    Args:
        html_content (str): Input HTML text or file path.
        is_input_path (bool, optional): `html_content` is a file path.
            Defaults to False.
        markdown (bool, optional): Output Markdown if True or plain-text if False.
            Defaults to False.
        selector (str, optional): Select the portion of HTML to extract.
            Defaults to "html".
        base_url (str, optional): Base URL for link conversion. Defaults to "".
        plain_tables (bool, optional): If plain-text, force plain table formatting.
            Defaults to False.
        open_quote (str, optional): If plain-text, char to use for `<q>`.
            Defaults to "“".
        close_quote (str, optional): If plain-text, char to use for `</q>`.
            Defaults to "”".
        block_quote (bool, optional): If plain-text, treat `<blockquote>` as `<q>`.
            Defaults to False.
        default_image_alt (str, optional): If plain-text, default text placeholder
            for images. Defaults to "".
        kill_strikethrough (bool, optional): If plain-text, remove content of
            `<s></s>`. Defaults to False.
        kill_tags (list | None, optional): If plain-text, remove content of
            specified selectors. Defaults to None, then initialized to [].
        file_ext_override (str, optional): If markdown, file extension for relative
            `.html` link conversion. Defaults to "".

    Returns:
        str: Markdown or plain-text as string.
    """
    actual_kill_tags = kill_tags if kill_tags is not None else []

    if is_input_path:
        html_content = Path(html_content).read_text(encoding="utf-8")

    from bs4 import SelectorSyntaxError

    soup = BeautifulSoup(html_content, "html.parser")
    with contextlib.suppress(IndexError, SelectorSyntaxError):  # SIM105
        # Ensure we operate on a copy if selection happens, to avoid modifying original
        selected_tag = soup.select(selector)
        if selected_tag:  # Check if selector found anything
            soup = BeautifulSoup(selected_tag[0].encode("utf-8"), "html.parser")

    current_file_ext = file_ext_override
    if not current_file_ext:  # SIM108 applied here
        current_file_ext = "md" if markdown else "txt"

    if markdown:
        soup = prep_doc(soup, base_url, current_file_ext)

    tag_or_element: Union[Tag, PageElement, NavigableString]
    for tag_or_element in soup.find_all(True):
        if isinstance(tag_or_element, Tag):
            tag: Tag = tag_or_element # Narrowing type

            if tag.name in ("mark", "kbd"):
                tag.replace_with(tag.get_text(""))  # type: ignore[arg-type]
            if plain_tables and tag.name == "table":
                rows = []
                for tr_element in tag.find_all("tr"):
                    if isinstance(tr_element, Tag):
                        tr_tag: Tag = tr_element
                        td_cells = []
                        for td_element in tr_tag.find_all(["th", "td"]):
                            if isinstance(td_element, Tag):
                                td_cells.append(td_element.get_text(" "))
                        rows.append(", ".join(td_cells))
                tag.replace_with(". ".join(rows))  # type: ignore[arg-type]
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
                elif tag.name == "code":  # Note: was "code", changed to "q"
                    tag.name = "q"

    for kill_item in actual_kill_tags:  # Use the initialized list
        for element_to_kill in soup.select(kill_item): # select usually returns Tags
            if isinstance(element_to_kill, Tag):
                found_tag_to_kill: Tag = element_to_kill
                found_tag_to_kill.replace_with("") # type: ignore[arg-type]

    h = HTML2Text()
    h.body_width = 0
    h.bypass_tables = False
    h.close_quote = close_quote
    h.default_image_alt = default_image_alt
    h.emphasis_mark = "_" if markdown else ""
    h.escape_snob = False
    h.google_doc = False
    h.google_list_indent = 0
    h.hide_strikethrough = kill_strikethrough
    h.ignore_emphasis = not markdown
    h.ignore_images = not markdown or kill_images
    h.ignore_links = not markdown
    h.ignore_mailto_links = not markdown
    h.ignore_tables = not markdown
    h.images_as_html = False
    h.images_to_alt = not markdown
    h.images_with_size = False
    h.inline_links = bool(markdown)
    h.links_each_paragraph = False
    h.mark_code = False
    h.open_quote = open_quote
    h.pad_tables = bool(markdown)
    h.protect_links = True
    h.single_line_break = False
    h.skip_internal_links = not markdown
    h.strong_mark = "**" if markdown else ""
    h.tag_callback = None
    h.ul_item_mark = "-" if markdown else ""
    h.unicode_snob = True
    h.use_automatic_links = bool(markdown)
    h.wrap_links = False
    h.wrap_list_items = False
    h.wrap_tables = False
    return cast(str, h.handle(str(soup)))
