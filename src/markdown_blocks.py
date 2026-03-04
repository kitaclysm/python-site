from enum import Enum
from htmlnode import LeafNode
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
