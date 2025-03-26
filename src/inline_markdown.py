import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_images(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        
        match = matches[0]
        image_markdown = f"![{match[0]}]({match[1]})"

        parts = old_node.text.split(image_markdown, 1)

        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
        new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))

        if len(parts) > 1 and parts[1]:
            remaining_node = TextNode(parts[1], TextType.TEXT)
            new_nodes.extend(split_nodes_image([remaining_node]))
                    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_links(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
        
        match = matches[0]
        link_markdown = f"[{match[0]}]({match[1]})"

        parts = old_node.text.split(link_markdown, 1)

        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
        new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))

        if len(parts) > 1 and parts[1]:
            remaining_node = TextNode(parts[1], TextType.TEXT)
            new_nodes.extend(split_nodes_link([remaining_node]))
                    
    return new_nodes

