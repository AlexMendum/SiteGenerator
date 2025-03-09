import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode(tag="p", value="this is a value")
        self.assertEqual(node.props_to_html(), "")

    def test_single(self):
        node = HTMLNode(tag="a", props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_multiple(self):
        node = HTMLNode(props={"href": "www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com" target="_blank"')

    def test_no_children(self):
        node = LeafNode(tag="a", value="this is a paragraph of text")
        self.assertEqual(node.to_html(), "<a>this is a paragraph of text</a>")

    def test_no_tag(self):
        node = LeafNode(None, value="this is a paragraph of text")
        self.assertEqual(node.to_html(), "this is a paragraph of text")

    def test_parent_single_child(self):
        node = ParentNode(tag="b", children=[LeafNode("b", "Bold text")])
        self.assertEqual(node.to_html(), "<b><b>Bold text</b></b>")

    def test_parent_no_child(self):
        node = ParentNode(tag="b", children=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_tag(self):
        node = ParentNode(None, children=[LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_many_children(self):
        node = ParentNode(tag="p", children=[LeafNode("b", "Bold text"), LeafNode("i", "Italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><i>Italic text</i>Normal text</p>")

    def test_nested_parents(self):
        node = ParentNode(tag="p", children=[ParentNode(tag="p", children=[LeafNode("b", "Bold text"), LeafNode("i", "Italic text")]), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><p><b>Bold text</b><i>Italic text</i></p>Normal text</p>")




if __name__ == "__main__":
    unittest.main()