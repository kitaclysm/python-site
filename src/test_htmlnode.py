import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        to_html_string = ""
        self.assertEqual(node.props_to_html(), to_html_string)
    
    def test_full(self):
        node = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://www.boot.dev", "target": "_blank"})
        to_html = " href=\"https://www.boot.dev\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), to_html)

    def test_empty_props(self):
        node = HTMLNode(tag="a", value="Boot.dev", props={})
        to_html = ""
        self.assertEqual(node.props_to_html(), to_html)

    def test_one_prop(self):
        node = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://www.boot.dev"})
        to_html = " href=\"https://www.boot.dev\""
        self.assertEqual(node.props_to_html(), to_html)
      
    def test_leaf_no_props(self):
        node = LeafNode(tag="p", value="a p tag, splendid")
        to_html = "<p>a p tag, splendid</p>"
        self.assertEqual(node.to_html(), to_html)
        
    def test_leaf_no_tag(self):
        node = LeafNode(tag=None, value="a p tag, splendid")
        to_html = "a p tag, splendid"
        self.assertEqual(node.to_html(), to_html)
        
    def test_leaf_complete(self):
        node = LeafNode(tag="a", value="Boot.dev", props={"href": "https://www.boot.dev"})
        to_html = "<a href=\"https://www.boot.dev\">Boot.dev</a>"
        self.assertEqual(node.to_html(), to_html)
        
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    
    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>child2</p></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()