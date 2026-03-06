from textnode import TextNode, TextType
from copystatic import copy_static
from gencontent import generate_pages_recursive

def main():
	copy_static("./static", "./public", True)
	generate_pages_recursive("content", "template.html", "public")

main()