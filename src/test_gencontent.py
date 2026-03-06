import unittest

from gencontent import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(Exception):
            extract_title("")
    
    def test_easy(self):
        self.assertEqual("hello", extract_title("# hello"))
    
    def test_not_first(self):
        self.assertEqual("hello", extract_title("## some other text\n# hello"))
    
    def test_floating_head(self):
        with self.assertRaises(Exception):
            extract_title("some text without an # h1")


if __name__ == "__main__":
    unittest.main()