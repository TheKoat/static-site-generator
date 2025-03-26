import os

from copystatic import copy_from_static_to_public
from generate import generate_pages_recursive

SRC_DIR = "./static"
DEST_DIR = "./public"
TEMPLATE_FILE = "./template.html"
CONTENT_DIR = "./content"


def main():
    copy_from_static_to_public(DEST_DIR, SRC_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, DEST_DIR)


main()
