import unittest

from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
    # split_nodes_delimiter
    def test_empty(self):
        old_nodes = []
        split_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(split_nodes, [])
    
    def test_one_standard(self):
        old_nodes = [TextNode("A sentence of **expected** text", TextType.TEXT)]
        split_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(split_nodes, [
            TextNode("A sentence of ", TextType.TEXT),
            TextNode("expected", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])

    def test_one_multi_delim(self):
        old_nodes = [TextNode("Some **bold** text and some more **bold** text", TextType.TEXT)]
        split_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(split_nodes, [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and some more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])
      
    def test_multi_old_multi_delim(self):
        old_nodes = [
            TextNode("A sentence with `pseudo code` that is code", TextType.TEXT),
            TextNode("A sentence with *italic* text", TextType.TEXT)
        ]
        split_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("A sentence with ", TextType.TEXT),
            TextNode("pseudo code", TextType.CODE),
            TextNode(" that is code", TextType.TEXT),
            TextNode("A sentence with *italic* text", TextType.TEXT),
        ])
    
    def test_multi_old_same_delim(self):
        old_nodes = [
            TextNode("A sentence with `pseudo code` that is code", TextType.TEXT),
            TextNode("A sentence with `code` text", TextType.TEXT)
        ]
        split_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("A sentence with ", TextType.TEXT),
            TextNode("pseudo code", TextType.CODE),
            TextNode(" that is code", TextType.TEXT),
            TextNode("A sentence with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    def test_wrong_type(self):
        old_nodes = [TextNode("A sentence with a **bold** word", TextType.BOLD)]
        split_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(split_nodes, old_nodes)
    
    def test_missing_delimiter(self):
        old_nodes = [TextNode("A sentence with a **missing delimiter", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    
    # extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # extract_markdown_links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://en.wikipedia.org/wiki/HTML_element)"
        )
        self.assertListEqual([("link", "https://en.wikipedia.org/wiki/HTML_element")], matches)

if __name__ == "__main__":
    unittest.main()