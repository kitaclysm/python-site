import unittest

from htmlnode import HTMLNode, LeafNode

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
        
if __name__ == "__main__":
    unittest.main()