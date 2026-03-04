from enum import Enum
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import LeafNode, ParentNode, HTMLNode
from inline_markdown import markdown_to_blocks, text_to_textnodes
import re

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def block_to_block_type(markdown):
    lines = markdown.splitlines()
    first_line = lines[0]
    last_line = lines[-1]

    # headings
    if first_line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # code
    if first_line.startswith("```") and len(lines) > 1:
        if last_line.startswith("```"):
            return BlockType.CODE
        return BlockType.PARAGRAPH
        
    # quote
    if first_line.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    # unordered list
    if first_line.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    # ordered list
    if first_line.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_child = text_node_to_html_node(node)
        children.append(html_child)
    return children
        
def make_heading(markdown):
    split = markdown.split(" ", 1)
    level = split[0]
    content = markdown[len(level) + 1:]
    if content != "":
        children = text_to_children(content)
    else:
        raise Exception("no content for heading")
    if len(level) > 6:
        raise Exception("invalid heading level")
    return ParentNode(f"h{len(level)}", children)

def make_code(markdown):
    stripped = markdown.removeprefix("```\n")
    stripped = stripped.removesuffix("```")
    code_node = TextNode(stripped, TextType.TEXT)
    code_node = text_node_to_html_node(code_node)
    p_node = ParentNode("code", [code_node])
    gp_node = ParentNode("pre", [p_node])
    return gp_node

def make_quote(markdown):
    lines = markdown.splitlines()
    clean_lines = []
    for line in lines:
        clean_lines.append(line.removeprefix("> "))
    clean_text = " ".join(clean_lines)
    children = text_to_children(clean_text)
    quote_node = ParentNode("blockquote", children)
    return quote_node

def make_ulist(markdown):
    lines = markdown.splitlines()
    line_nodes = []
    for line in lines:
        clean_line = line.removeprefix("- ")
        clean_line = text_to_children(clean_line)
        line_nodes.append(ParentNode("li", clean_line))
    return ParentNode("ul", line_nodes)

def make_olist(markdown):
    lines = markdown.splitlines()
    line_nodes = []
    for i, line in enumerate(lines):
        clean_line = line.removeprefix(f"{i + 1}. ")
        clean_line = text_to_children(clean_line)
        line_nodes.append(ParentNode("li", clean_line))
    return ParentNode("ol", line_nodes)

def make_paragraph(markdown):
    lines = markdown.splitlines()
    line_children = text_to_children(" ".join(lines))
    return ParentNode("p", line_children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    direct_children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype is BlockType.HEADING:
                direct_children.append(make_heading(block))
        elif blocktype is BlockType.CODE:
                direct_children.append(make_code(block))
        elif blocktype is BlockType.QUOTE:
                direct_children.append(make_quote(block))
        elif blocktype is BlockType.UNORDERED_LIST:
                direct_children.append(make_ulist(block))
        elif blocktype is BlockType.ORDERED_LIST:
                direct_children.append(make_olist(block))
        elif blocktype is BlockType.PARAGRAPH:
                direct_children.append(make_paragraph(block))
    return ParentNode("div", direct_children)

