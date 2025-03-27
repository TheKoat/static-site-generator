import os
import sys

from copystatic import copy_from_static_to_public
from generate import generate_pages_recursive

SRC_DIR = "./static"
DEST_DIR = "./docs"
TEMPLATE_FILE = "./template.html"
CONTENT_DIR = "./content"


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_from_static_to_public(DEST_DIR, SRC_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, DEST_DIR, basepath)


main()
