import os

from markdown_block import markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise Exception("Invalid markdown: no title")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    items = os.listdir(dir_path_content)
    print(f"Items under {dir_path_content}: {items}")
    
    for item in items:
        from_full_path = os.path.join(dir_path_content, item)
        dest_full_path = os.path.join(dest_dir_path, item)
        print(f" * {from_full_path} -> {dest_full_path}")

        if os.path.isfile(from_full_path):
            dest_html_path = os.path.join(dest_dir_path, "index.html")
            print(f"Generating page from {from_full_path} to {dest_html_path} using {template_path}")

            with open(from_full_path, "r", encoding="utf-8") as file:
                markdown = file.read()
            with open(template_path, "r", encoding="utf-8") as file:
                template = file.read()
    
            content = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            html_output = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

            os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)

            with open(dest_html_path, "w", encoding="utf-8") as file:
                file.write(html_output)
    
            print(f"Page successfully generated at {dest_html_path}")
        
        else:
            generate_pages_recursive(from_full_path, template_path, dest_full_path)
        

 

