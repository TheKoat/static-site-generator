import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node = HTMLNode("a", 
                        "This is a test", 
                        None, 
                        {"href": "https://www.google.com", "target": "_blank"}
                         )
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    
    def test_value(self):
        node = HTMLNode("a", 
                        "This is a test", 
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_repr(self):
        node = HTMLNode("a", 
                        "This is a test", 
                        None, 
                        {"href": "https://www.google.com", "target": "_blank"}
                         )
        self.assertEqual(node.__repr__(), "HTMLNode(a, This is a test, children: None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Hello, world!</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_nesting_parents(self):
        child_node1 = LeafNode("p", "This is a test.")
        child_node2 = ParentNode("article", [child_node1])
        child_node3 = ParentNode("section", [child_node2])
        parent_node = ParentNode("div", [child_node3])
        self.assertEqual(parent_node.to_html(), "<div><section><article><p>This is a test.</p></article></section></div>")

    def test_to_html_nesting_multiple_children(self):
        child_node1 = LeafNode("b", "child 1")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "child 2")
        child_node4 = ParentNode("p", [child_node1, child_node2, child_node3])
        parent_node = ParentNode("div", [child_node4])
        self.assertEqual(parent_node.to_html(), "<div><p><b>child 1</b>Normal text<i>child 2</i></p></div>")

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_without_tag(self):
        child_node1 = LeafNode("b", "child 1")
        child_node2 = LeafNode("i", "child 2")
        parent_node = ParentNode(None, [child_node1, child_node2])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()

    