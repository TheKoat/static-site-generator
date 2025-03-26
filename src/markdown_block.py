import re

from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    NORMAL = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        if not block:
            continue
        block = block.strip()
        new_blocks.append(block)

    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("#","##","###","####","#####","######")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.NORMAL
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.NORMAL
        return BlockType.ULIST
    elif block.startswith("1. "):
        expected_number = 1
        for line in lines:
            if not line.startswith(f"{expected_number}. "):
                return BlockType.NORMAL
            expected_number += 1
        return BlockType.OLIST
    else:
        return BlockType.NORMAL

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.NORMAL:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case _:
            raise Exception(f"Invalid BlockType: {block_type}")
    
def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    i = 0
    while block[i] == "#":
        i +=1
    if i >= len(block):
        raise ValueError(f"Invalid heading level: {i}")
    text = block[i + 1: ]
    children = text_to_children(text)
    return ParentNode(f"h{i}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(text_node)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")

    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    lines = block.split("\n")

    new_lists = []
    for line in lines:
        i = 0
        while line[i].isdigit():
            i += 1
        text = line[i+2: ].strip()
        children = text_to_children(text)
        new_lists.append(ParentNode("li", children))
    
    return ParentNode("ol", new_lists)

def ulist_to_html_node(block):
    lines = block.split("\n")

    new_lists = []
    for line in lines:
        text = line[2: ].strip()
        children = text_to_children(text)
        new_lists.append(ParentNode("li", children))
    
    return ParentNode("ul", new_lists)







    