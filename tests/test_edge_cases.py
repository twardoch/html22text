# this_file: tests/test_edge_cases.py

"""Test edge cases and error conditions for html22text."""

import pytest
from pathlib import Path
from html22text import html22text
from html22text.html22text import abs_asset_href, is_doc, rel_txt_href


def test_empty_html():
    """Test conversion of empty HTML."""
    assert html22text("", markdown=True) == ""
    assert html22text("", markdown=False) == ""


def test_whitespace_only_html():
    """Test conversion of whitespace-only HTML."""
    assert html22text("   \n\t  ", markdown=True) == ""
    assert html22text("   \n\t  ", markdown=False) == ""


def test_malformed_html():
    """Test conversion of malformed HTML."""
    malformed = "<p>Unclosed paragraph<div>Nested without closing"
    result_md = html22text(malformed, markdown=True)
    result_txt = html22text(malformed, markdown=False)
    
    # Should still process without crashing
    assert "Unclosed paragraph" in result_md
    assert "Nested without closing" in result_md
    assert "Unclosed paragraph" in result_txt
    assert "Nested without closing" in result_txt


def test_unicode_content():
    """Test conversion of Unicode content."""
    unicode_html = "<p>Hello 世界! 🌍 Café résumé naïve</p>"
    result_md = html22text(unicode_html, markdown=True)
    result_txt = html22text(unicode_html, markdown=False)
    
    assert "世界" in result_md
    assert "🌍" in result_md
    assert "Café résumé naïve" in result_md
    assert "世界" in result_txt
    assert "🌍" in result_txt
    assert "Café résumé naïve" in result_txt


def test_deeply_nested_html():
    """Test conversion of deeply nested HTML structures."""
    nested_html = """
    <div>
        <section>
            <article>
                <header>
                    <h1>Title</h1>
                </header>
                <main>
                    <p>Content with <em>emphasis</em> and <strong>bold</strong></p>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2 with <a href="link.html">link</a></li>
                    </ul>
                </main>
            </article>
        </section>
    </div>
    """
    result_md = html22text(nested_html, markdown=True)
    result_txt = html22text(nested_html, markdown=False)
    
    assert "# Title" in result_md
    assert "_emphasis_" in result_md
    assert "**bold**" in result_md
    assert "Title" in result_txt
    assert "emphasis" in result_txt
    assert "bold" in result_txt


def test_special_characters_in_links():
    """Test links with special characters."""
    html_with_special_chars = '''
    <p>Links with special chars:</p>
    <a href="file%20with%20spaces.html">Spaced file</a>
    <a href="file&amp;with&amp;entities.html">Entity file</a>
    <a href="file?query=value&amp;other=123">Query params</a>
    '''
    result_md = html22text(html_with_special_chars, markdown=True, base_url="http://example.com/")
    
    assert "file%20with%20spaces.html" in result_md
    assert "file&with&entities.html" in result_md
    assert "file?query=value&other=123" in result_md


def test_selector_functionality():
    """Test CSS selector functionality."""
    html_with_sections = '''
    <div id="header">Header content</div>
    <div id="main">
        <p>Main content</p>
        <div class="sidebar">Sidebar content</div>
    </div>
    <div id="footer">Footer content</div>
    '''
    
    # Test selecting only main content
    result = html22text(html_with_sections, markdown=True, selector="#main")
    assert "Main content" in result
    assert "Header content" not in result
    assert "Footer content" not in result
    assert "Sidebar content" in result  # Should include sidebar as it's within #main


def test_kill_tags_with_css_selectors():
    """Test kill_tags with various CSS selectors."""
    html_with_classes = '''
    <div class="keep">Keep this</div>
    <div class="remove">Remove this</div>
    <div id="keep-id">Keep this too</div>
    <div id="remove-id">Remove this too</div>
    <script>Remove script</script>
    '''
    
    result = html22text(
        html_with_classes, 
        markdown=False, 
        kill_tags=[".remove", "#remove-id", "script"]
    )
    
    assert "Keep this" in result
    assert "Keep this too" in result
    assert "Remove this" not in result
    assert "Remove this too" not in result
    assert "Remove script" not in result


def test_file_extension_override():
    """Test file extension override functionality."""
    html_with_links = '''
    <a href="page1.html">Page 1</a>
    <a href="dir/page2.html">Page 2</a>
    <a href="http://example.com/page3.html">External</a>
    <a href="#fragment">Fragment</a>
    '''
    
    result = html22text(
        html_with_links, 
        markdown=True, 
        file_ext_override="md"
    )
    
    assert "page1.md" in result
    assert "dir/page2.md" in result
    assert "http://example.com/page3.html" in result  # External links unchanged
    assert "#fragment" in result  # Fragments unchanged


def test_nonexistent_file_path():
    """Test handling of nonexistent file paths."""
    with pytest.raises(FileNotFoundError):
        html22text("/nonexistent/file.html", is_input_path=True)


def test_directory_as_input_path():
    """Test handling of directory as input path."""
    with pytest.raises(IsADirectoryError):
        html22text("/tmp", is_input_path=True)


def test_quote_customization():
    """Test custom quote characters."""
    html_with_quotes = '<p>Regular text</p><q>Quoted text</q><blockquote>Block quote</blockquote>'
    
    result = html22text(
        html_with_quotes,
        markdown=False,
        block_quote=True,
        open_quote="«",
        close_quote="»"
    )
    
    assert "«Quoted text»" in result
    assert "«Block quote»" in result


def test_image_handling_options():
    """Test different image handling options."""
    html_with_images = '''
    <p>Before image</p>
    <img src="image.jpg" alt="Alt text">
    <p>After image</p>
    '''
    
    # Test with images killed
    result_no_images = html22text(html_with_images, markdown=True, kill_images=True)
    assert "Before image" in result_no_images
    assert "After image" in result_no_images
    assert "image.jpg" not in result_no_images
    
    # Test with images preserved
    result_with_images = html22text(html_with_images, markdown=True, kill_images=False)
    assert "Before image" in result_with_images
    assert "After image" in result_with_images
    assert "image.jpg" in result_with_images


def test_helper_functions():
    """Test helper functions directly."""
    
    # Test is_doc function
    assert is_doc("file.html") == True
    assert is_doc("file.htm") == True
    assert is_doc("dir/file.html") == True
    assert is_doc("file.txt") == False
    assert is_doc("http://example.com/file.html") == False
    assert is_doc("/absolute/file.html") == False
    assert is_doc("#fragment") == False
    
    # Test rel_txt_href function
    assert rel_txt_href("file.html", "md") == "file.md"
    assert rel_txt_href("dir/file.html", "txt") == "dir/file.txt"
    assert rel_txt_href("file.html", ".md") == "file.md"  # Handle leading dot
    assert rel_txt_href("http://example.com/file.html", "md") == "http://example.com/file.html"
    
    # Test abs_asset_href function
    base = "http://example.com/docs/"
    assert abs_asset_href("style.css", base) == "http://example.com/docs/style.css"
    assert abs_asset_href("../images/img.png", base) == "http://example.com/images/img.png"
    assert abs_asset_href("http://other.com/img.png", base) == "http://other.com/img.png"


def test_large_html_document():
    """Test handling of large HTML documents."""
    # Create a large HTML document
    large_html = "<html><body>"
    for i in range(1000):
        large_html += f"<p>This is paragraph {i} with some <strong>bold</strong> text.</p>"
    large_html += "</body></html>"
    
    result = html22text(large_html, markdown=True)
    
    # Should handle large documents without issues
    assert "This is paragraph 0" in result
    assert "This is paragraph 999" in result
    assert "**bold**" in result


def test_html_entities():
    """Test handling of HTML entities."""
    html_with_entities = '''
    <p>&lt;script&gt;alert('xss')&lt;/script&gt;</p>
    <p>&amp; &quot; &apos; &copy; &reg;</p>
    <p>&#8364; &#8482; &#169;</p>
    '''
    
    result = html22text(html_with_entities, markdown=False)
    
    assert "<script>alert('xss')</script>" in result
    assert "&" in result
    assert '"' in result
    assert "'" in result
    assert "©" in result
    assert "®" in result
    assert "€" in result
    assert "™" in result


def test_table_handling():
    """Test table handling in both markdown and text modes."""
    html_table = '''
    <table>
        <thead>
            <tr><th>Header 1</th><th>Header 2</th></tr>
        </thead>
        <tbody>
            <tr><td>Cell 1.1</td><td>Cell 1.2</td></tr>
            <tr><td>Cell 2.1</td><td>Cell 2.2</td></tr>
        </tbody>
    </table>
    '''
    
    result_md = html22text(html_table, markdown=True)
    result_txt = html22text(html_table, markdown=False)
    
    # Both should contain table data
    assert "Header 1" in result_md
    assert "Header 2" in result_md
    assert "Cell 1.1" in result_md
    assert "Cell 2.2" in result_md
    
    assert "Header 1" in result_txt
    assert "Header 2" in result_txt
    assert "Cell 1.1" in result_txt
    assert "Cell 2.2" in result_txt


def test_code_blocks():
    """Test handling of code blocks."""
    html_with_code = '''
    <p>Regular text</p>
    <pre><code>
    def hello():
        print("Hello, World!")
        return True
    </code></pre>
    <p>More text</p>
    '''
    
    result_md = html22text(html_with_code, markdown=True)
    result_txt = html22text(html_with_code, markdown=False)
    
    assert "def hello():" in result_md
    assert "print(" in result_md
    assert "def hello():" in result_txt
    assert "print(" in result_txt


def test_nested_lists():
    """Test handling of nested lists."""
    html_nested_lists = '''
    <ul>
        <li>Item 1</li>
        <li>Item 2
            <ul>
                <li>Subitem 2.1</li>
                <li>Subitem 2.2</li>
            </ul>
        </li>
        <li>Item 3</li>
    </ul>
    '''
    
    result_md = html22text(html_nested_lists, markdown=True)
    result_txt = html22text(html_nested_lists, markdown=False)
    
    assert "Item 1" in result_md
    assert "Item 2" in result_md
    assert "Subitem 2.1" in result_md
    assert "Subitem 2.2" in result_md
    assert "Item 3" in result_md
    
    assert "Item 1" in result_txt
    assert "Item 2" in result_txt
    assert "Subitem 2.1" in result_txt
    assert "Subitem 2.2" in result_txt
    assert "Item 3" in result_txt