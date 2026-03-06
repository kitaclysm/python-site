from textnode import TextNode, TextType
from copystatic import copy_static
from gencontent import generate_page

def main():
	copy_static("./static", "./public", True)
	generate_page("content/index.md", "template.html", "public/index.html")

main()