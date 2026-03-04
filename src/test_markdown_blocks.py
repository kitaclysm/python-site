import unittest

from markdown_blocks import BlockType, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_heading_true(self):
        markdown = "# Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    
    def test_heading_false(self):
        markdown = "#Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_heading_overload(self):
        markdown = "####### Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_code_true(self):
        markdown = "```\ncode code code\n```"
        self.assertEqual(BlockType.CODE, block_to_block_type(markdown))
    
    def test_code_false(self):
        markdown = "```\ncode code code\n"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_code_start(self):
        markdown = "```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_quote_true(self):
        markdown = ">A rose by any\n>other name might\n>smell as sweet"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(markdown))
    
    def test_quote_false(self):
        markdown = ">A rose by any\nother name might\n>smell as sweet"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_unordered_true(self):
        markdown = "- eggs\n- flour\n- vinegar"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(markdown))
    
    def test_unordered_false(self):
        markdown = "- eggs\n-flour\n- vinegar"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_ordered_true(self):
        markdown = "1. eggs\n2. flour\n3. vinegar"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(markdown))
    
    def test_ordered_false(self):
        markdown = "1. eggs\n2 flour\n3. vinegar"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_un_ordered(self):
        markdown = "2. eggs\n3. flour\n4. vinegar"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
    
    def test_ordered_skip(self):
        markdown = "1. eggs\n3. flour\n4. vinegar"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))


if __name__ == "__main__":
    unittest.main()