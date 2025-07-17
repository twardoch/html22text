# this_file: tests/test_integration.py

"""Integration tests for html22text."""

import tempfile
import os
import subprocess
from pathlib import Path
import pytest
from html22text import html22text


def test_full_workflow():
    """Test the complete workflow from HTML to text/markdown."""
    
    # Complex HTML content
    complex_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>body { font-family: Arial; }</style>
    </head>
    <body>
        <header>
            <h1>Main Title</h1>
            <nav>
                <a href="home.html">Home</a>
                <a href="about.html">About</a>
            </nav>
        </header>
        
        <main>
            <article>
                <h2>Article Title</h2>
                <p>This is a paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
                
                <ul>
                    <li>List item 1</li>
                    <li>List item 2 with <a href="link.html">a link</a></li>
                    <li>List item 3</li>
                </ul>
                
                <blockquote>
                    This is a blockquote with some important information.
                </blockquote>
                
                <pre><code>
def hello_world():
    print("Hello, World!")
    return True
                </code></pre>
                
                <table>
                    <tr><th>Header 1</th><th>Header 2</th></tr>
                    <tr><td>Cell 1</td><td>Cell 2</td></tr>
                </table>
            </article>
        </main>
        
        <footer>
            <p>Copyright 2024</p>
        </footer>
        
        <script>
            console.log("This should be removed");
        </script>
    </body>
    </html>
    """
    
    # Test markdown conversion
    markdown_result = html22text(
        complex_html,
        markdown=True,
        kill_tags=["script", "style"],
        base_url="https://example.com/",
        file_ext_override="md"
    )
    
    # Verify markdown output
    assert "# Main Title" in markdown_result
    assert "## Article Title" in markdown_result
    assert "**bold text**" in markdown_result
    assert "_italic text_" in markdown_result
    assert "home.md" in markdown_result
    assert "about.md" in markdown_result
    assert "link.md" in markdown_result
    assert "console.log" not in markdown_result
    assert "font-family" not in markdown_result
    
    # Test plain text conversion
    text_result = html22text(
        complex_html,
        markdown=False,
        kill_tags=["script", "style"],
        block_quote=True,
        open_quote='"',
        close_quote='"'
    )
    
    # Verify text output
    assert "Main Title" in text_result
    assert "Article Title" in text_result
    assert "bold text" in text_result
    assert "italic text" in text_result
    assert '"This is a blockquote' in text_result
    assert "console.log" not in text_result
    assert "font-family" not in text_result


def test_file_input_output():
    """Test file input and output operations."""
    
    html_content = """
    <html>
    <body>
        <h1>File Test</h1>
        <p>This content is from a file.</p>
        <a href="relative.html">Relative Link</a>
        <script>Remove this</script>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_file = f.name
    
    try:
        # Test file input
        result = html22text(
            temp_file,
            is_input_path=True,
            markdown=True,
            kill_tags=["script"],
            base_url="https://example.com/",
            file_ext_override="md"
        )
        
        assert "# File Test" in result
        assert "This content is from a file." in result
        assert "relative.md" in result
        assert "Remove this" not in result
        
    finally:
        os.unlink(temp_file)


def test_edge_cases_integration():
    """Test edge cases in integration."""
    
    # Empty HTML
    assert html22text("", markdown=True) == ""
    assert html22text("", markdown=False) == ""
    
    # Only whitespace
    assert html22text("   \n\t  ", markdown=True) == ""
    assert html22text("   \n\t  ", markdown=False) == ""
    
    # HTML with only script tags
    script_only = "<script>console.log('test');</script>"
    result = html22text(script_only, markdown=True, kill_tags=["script"])
    assert result.strip() == ""
    
    # HTML with entities
    entity_html = "<p>&lt;script&gt;alert('xss')&lt;/script&gt;</p>"
    result = html22text(entity_html, markdown=False)
    assert "<script>alert('xss')</script>" in result


def test_real_world_html():
    """Test with real-world HTML patterns."""
    
    # Simulate a blog post
    blog_html = """
    <article class="post">
        <header>
            <h1>Blog Post Title</h1>
            <p class="meta">Published on <time>2024-01-01</time> by <author>John Doe</author></p>
        </header>
        
        <div class="content">
            <p>This is the first paragraph of the blog post.</p>
            
            <h2>Section 1</h2>
            <p>Content of section 1 with <a href="https://example.com">external link</a>.</p>
            
            <h2>Section 2</h2>
            <p>Content of section 2 with <a href="internal.html">internal link</a>.</p>
            
            <div class="code-block">
                <pre><code>
# Python code example
def process_data(data):
    return [x.strip() for x in data if x]
                </code></pre>
            </div>
        </div>
        
        <footer class="post-footer">
            <p>Tags: <a href="tag1.html">tag1</a>, <a href="tag2.html">tag2</a></p>
        </footer>
        
        <aside class="sidebar">
            <h3>Related Posts</h3>
            <ul>
                <li><a href="post1.html">Post 1</a></li>
                <li><a href="post2.html">Post 2</a></li>
            </ul>
        </aside>
    </article>
    """
    
    # Test extracting main content
    main_content = html22text(
        blog_html,
        markdown=True,
        selector=".content",
        base_url="https://blog.example.com/",
        file_ext_override="md"
    )
    
    assert "Blog Post Title" not in main_content  # Title is outside .content
    assert "Section 1" in main_content
    assert "Section 2" in main_content
    assert "external link" in main_content
    assert "internal.md" in main_content
    assert "def process_data" in main_content
    
    # Test full article
    full_article = html22text(
        blog_html,
        markdown=True,
        base_url="https://blog.example.com/",
        file_ext_override="md"
    )
    
    assert "# Blog Post Title" in full_article
    assert "tag1.md" in full_article
    assert "tag2.md" in full_article
    assert "post1.md" in full_article
    assert "post2.md" in full_article


def test_performance_with_large_document():
    """Test performance with a large HTML document."""
    
    # Create a large HTML document
    large_html = "<html><body>"
    for i in range(1000):
        large_html += f"""
        <div class="item-{i}">
            <h3>Item {i}</h3>
            <p>This is item number {i} with some <strong>bold</strong> text.</p>
            <ul>
                <li>Sub-item 1</li>
                <li>Sub-item 2</li>
            </ul>
        </div>
        """
    large_html += "</body></html>"
    
    # Should handle large documents without issues
    result = html22text(large_html, markdown=True)
    
    assert "# Item 0" in result
    assert "# Item 999" in result
    assert "**bold**" in result
    assert result.count("Sub-item 1") == 1000
    assert result.count("Sub-item 2") == 1000


def test_unicode_and_special_characters():
    """Test handling of Unicode and special characters."""
    
    unicode_html = """
    <html>
    <body>
        <h1>Unicode Test 🌍</h1>
        <p>Testing various Unicode characters:</p>
        <ul>
            <li>Chinese: 你好世界</li>
            <li>Arabic: مرحبا بالعالم</li>
            <li>Russian: Привет, мир</li>
            <li>Emoji: 🎉 🚀 ✨</li>
            <li>Mathematical: ∑ ∆ ∞</li>
        </ul>
        
        <p>Special HTML entities:</p>
        <ul>
            <li>&amp; &lt; &gt; &quot; &apos;</li>
            <li>&copy; &reg; &trade;</li>
            <li>&#8364; &#8482; &#169;</li>
        </ul>
    </body>
    </html>
    """
    
    result = html22text(unicode_html, markdown=True)
    
    # Check Unicode characters are preserved
    assert "🌍" in result
    assert "你好世界" in result
    assert "مرحبا بالعالم" in result
    assert "Привет, мир" in result
    assert "🎉 🚀 ✨" in result
    assert "∑ ∆ ∞" in result
    
    # Check HTML entities are properly decoded
    assert "& < > \" '" in result
    assert "© ® ™" in result
    assert "€ ™ ©" in result


def test_malformed_html_handling():
    """Test handling of malformed HTML."""
    
    malformed_html = """
    <html>
    <body>
        <h1>Unclosed header
        <p>Paragraph without closing tag
        <div>
            <span>Nested without proper closing
        </div>
        <ul>
            <li>Item 1
            <li>Item 2
        </ul>
    </body>
    """
    
    # Should handle malformed HTML gracefully
    result = html22text(malformed_html, markdown=True)
    
    assert "Unclosed header" in result
    assert "Paragraph without closing tag" in result
    assert "Nested without proper closing" in result
    assert "Item 1" in result
    assert "Item 2" in result