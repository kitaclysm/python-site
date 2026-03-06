import sys
from textnode import TextNode, TextType
from copystatic import copy_static
from gencontent import generate_pages_recursive

def main():
	basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
	copy_static("./static", "./docs", True)
	generate_pages_recursive("content", "template.html", "docs", basepath)

main()