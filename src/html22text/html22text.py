#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import cast  # For type hinting kill_tags and casting
from urllib.parse import quote as urlquote
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from bs4.element import NavigableString, PageElement, Tag  # Import specific BS4 types
from html2text import HTML2Text

SelectorSyntaxError: type[Exception]  # Forward declaration for type checkers
try:
    from bs4 import SelectorSyntaxError  # type: ignore[attr-defined, no-redef]
except ImportError:
    try:
        # Attempt fallback: soupsieve might be where it originates
        from soupsieve.util import (  # type: ignore[no-redef]
            SelectorSyntaxError as SoupsieveSelectorSyntaxError,
        )

        SelectorSyntaxError = SoupsieveSelectorSyntaxError
    except ImportError:
        # If all imports fail, define a dummy exception to allow code to run.
        # This might mask selector errors if they occur, but prevents import crashes.
        class SelectorSyntaxError(Exception):  # type: ignore[no-redef]
            """Dummy SelectorSyntaxError if not found in bs4 or soupsieve."""


# Helper function for IRI to URI conversion using urllib.parse
def _iri_to_uri_urllib(iri_string: str) -> str:
    """
    Converts an IRI (Internationalized Resource Identifier) to a URI
    (Uniform Resource Identifier) using urllib.parse.
    Handles IDNA for domain names.
    """
    if not iri_string:
        return ""
    parsed_iri = urlparse(iri_string)
    # Encode domain to Punycode if it's an IDN
    try:
        # urlparse netloc can be "hostname:port"
        hostname = parsed_iri.hostname
        if hostname:
            # Encode to IDNA (Punycode)
            encoded_hostname = hostname.encode("idna").decode("ascii")
            # Reconstruct netloc if port exists
            netloc = encoded_hostname
            if parsed_iri.port:
                netloc = f"{encoded_hostname}:{parsed_iri.port}"

            # Replace the netloc in the parsed result.
            # Namedtuples are immutable, so direct reconstruction or _replace is needed.
            parsed_iri = parsed_iri._replace(netloc=netloc)

    except UnicodeError:
        # If domain encoding fails, proceed with the original (e.g. IP, already ASCII)
        pass

    # Percent-encode the path.
    # urljoin and Path operations handle path normalization.
    # Safe chars for path: alphanumeric + common symbols not needing encoding.
    quoted_path = urlquote(parsed_iri.path, safe="/:@-._~!$&'()*+,;=")
    parsed_iri = parsed_iri._replace(path=quoted_path)

    # urlunparse will reassemble the URI
    return parsed_iri.geturl()


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

    # Use urllib.parse.urlparse to check for a scheme
    parsed_href = urlparse(href)
    absurl = bool(parsed_href.scheme)

    # For local paths, check if it's absolute using Path.is_absolute()
    # We assume href is a path-like string if not a URL
    # This logic remains the same: if it's not a scheme-based URL, check path absolutism
    abspath = False if absurl else href_path.is_absolute()
    htmlfile = ext.lower() in {".html", ".htm"}

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
    return _iri_to_uri_urllib(str(new_path))


def abs_asset_href(href: str, base_url: str) -> str:
    """Makes a possibly relative asset URL absolute.

    Args:
        href (str): URL.
        base_url (str): Base URL to resolve relative links.

    Returns:
        str: Absolute URL.
    """
    href_path = Path(href)
    parsed_href = urlparse(href)
    is_url_absolute = bool(parsed_href.scheme)

    if is_url_absolute or href_path.is_absolute():
        return _iri_to_uri_urllib(
            href
        )  # Ensure even absolute URLs are correctly IRI encoded

    # Use urllib.parse.urljoin for joining
    joined_url = urljoin(base_url, href)
    return _iri_to_uri_urllib(joined_url)


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
                # Changed to TypeError as per TRY004 suggestion
                error_message = (
                    f"Unexpected list value for 'href' attribute in <link>: "
                    f"{current_href}"
                )
                raise TypeError(error_message)

    for element in soup.find_all(src=True):
        if isinstance(element, Tag):
            asset_tag: Tag = element
            current_src = asset_tag.get("src")
            if isinstance(current_src, str):
                asset_tag["src"] = abs_asset_href(current_src, base_url)
            elif isinstance(current_src, list):  # Should not happen for 'src'
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
            # Removed check for `isinstance(current_href, list)` for anchor tags'
            # href, as this is highly unlikely for standard HTML and
            # `rel_txt_href` expects a string.

    # The RET504 for this was valid, direct return.
    return replace_asset_hrefs(soup, base_url)


def html22text(  # noqa: PLR0913, PLR0915
    html_content: str,  # Renamed from html to avoid confusion with module
    is_input_path: bool = False,  # Renamed from input
    markdown: bool = False,
    selector: str = "html",
    base_url: str = "",
    open_quote: str = "“",
    close_quote: str = "”",
    block_quote: bool = False,
    default_image_alt: str = "",
    kill_strikethrough: bool = False,
    kill_tags: str | None = None,  # Comma-separated string of selectors
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
        kill_tags (str | None, optional): If plain-text, comma-separated string
            of CSS selectors whose content should be removed. Defaults to None.
        file_ext_override (str, optional): If markdown, file extension for relative
            `.html` link conversion. Defaults to "".

    Returns:
        str: Markdown or plain-text as string.
    """
    actual_kill_tags: list[str] = []
    if kill_tags:
        actual_kill_tags = [tag.strip() for tag in kill_tags.split(',')]

    if is_input_path:
        html_content = Path(html_content).read_text(encoding="utf-8")

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

    tag_or_element: Tag | PageElement | NavigableString
    for tag_or_element in soup.find_all(True):
        if isinstance(tag_or_element, Tag):
            tag: Tag = tag_or_element  # Narrowing type

            if tag.name in ("mark", "kbd"):
                tag.replace_with(tag.get_text(""))  # type: ignore[arg-type]
            # Custom plain_tables logic removed as html2text native handling is
            # preferred.
            if not markdown and tag.name == "blockquote" and block_quote:
                # If block_quote is True for plain text, transform <blockquote>
                # to <p><q> for custom quoting. Otherwise, <blockquote> is
                # passed through for native html2text handling.
                tag.name = "q"
                tag.wrap(soup.new_tag("p"))
            # Other specific tag transformations for plain text mode have been
            # removed to rely more on html2text's default behavior.

    for kill_item in actual_kill_tags:  # Use the initialized list
        for element_to_kill in soup.select(kill_item):  # select usually returns Tags
            if isinstance(element_to_kill, Tag):
                found_tag_to_kill: Tag = element_to_kill
                found_tag_to_kill.replace_with("")  # type: ignore[arg-type]

    h = HTML2Text()

    # Universal settings
    h.body_width = 0  # No line wrapping
    h.bypass_tables = False
    h.escape_snob = False
    h.google_doc = False
    h.google_list_indent = 0
    h.images_as_html = False
    h.images_with_size = False
    h.links_each_paragraph = False
    h.protect_links = True
    h.single_line_break = False
    h.tag_callback = None
    h.unicode_snob = True
    h.wrap_links = False
    h.wrap_list_items = False
    h.wrap_tables = False

    # Settings from direct pass-through parameters
    h.close_quote = close_quote
    h.default_image_alt = default_image_alt
    h.hide_strikethrough = kill_strikethrough
    h.open_quote = open_quote

    # Conditional settings based on markdown mode or other parameters
    h.emphasis_mark = "_" if markdown else ""
    h.ignore_emphasis = not markdown
    h.ignore_images = not markdown or kill_images
    h.ignore_links = not markdown
    h.ignore_mailto_links = not markdown
    h.ignore_tables = False  # Always let html2text process tables natively
    h.images_to_alt = not markdown  # Convert images to alt text if not markdown
    h.inline_links = bool(markdown)
    h.mark_code = bool(markdown)  # Enable code marking for Markdown
    h.pad_tables = bool(markdown)
    h.skip_internal_links = not markdown
    h.strong_mark = "**" if markdown else ""
    h.ul_item_mark = "-" if markdown else ""
    h.use_automatic_links = bool(markdown)

    return cast("str", h.handle(str(soup)))
