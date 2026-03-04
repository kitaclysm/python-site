import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
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

    # split image text
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        new_nodes
        )
    
    # split link text
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
        new_nodes
        )

    # empty image
    def test_empty_image(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node],new_nodes)

# more tests for split_nodes_image and split_nodes_link
# Multiple Items: What if a single node has two or three images in it?
# "This has ![one](url1) and ![two](url2)"

# No Text Between Items: What happens if two images are right next to each other?
# "![img1](url1)![img2](url2)"

# Start and End: Does it work if the image is the very first thing in the string? Or the very last?
# "![first](url) is at the start"
# "The end is ![last](url)"

# Non-Text Nodes: What if you pass in a list that already contains a TextType.BOLD node? Your function should leave it alone and return it as-is.
# The "Almost" Match: For links, what if there is an image? split_nodes_link should ignore ![image](url) and only split on [link](url). (Your extract_markdown_links function already handles this with that clever regex!)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        noded_text = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], noded_text
        )
    
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

if __name__ == "__main__":
    unittest.main()