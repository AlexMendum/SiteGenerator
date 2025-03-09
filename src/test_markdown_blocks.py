import unittest

from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "### This is a level 3 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "``` This is code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_paragraph_block(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- This is an unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "- This is\n- an unordered list\n- as well"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_unordered_list_with_formatting(self):
        block = "- Item with **bold** text\n- Item with _italic_ text\n- Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_with_formatting(self):
        block = "1. **First item**\n2. *Second item*\n3. Third `item`"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote
> with multiple lines
> and some **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and some <b>bold</b> text</blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with **bold**
3. Third item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- First bullet point
- Second bullet with **bold** text
- Third bullet with `code` and _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First bullet point</li><li>Second bullet with <b>bold</b> text</li><li>Third bullet with <code>code</code> and <i>italic</i></li></ul></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3 with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3 with <i>italic</i></h3></div>",
        )

    def test_extract_title(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3 with _italic_
"""
        node = extract_title(md)
        self.assertEqual(
            node,
            "Heading 1"
        )
    
    def test_ulist_italic_and_apostrophe(self):
        md = """
- First bullet point
- Second bullet point
- Disney _didn't ruin it_ (okay, but Amazon might have)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First bullet point</li><li>Second bullet point</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()