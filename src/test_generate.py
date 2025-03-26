import unittest

from generate import extract_title


class TestGenerate(unittest.TestCase):
    
    def test_extract_title(self):
        md = """
# This is an h1

This is a paragraph

## This is an h2

"""
        title = extract_title(md)
        self.assertEqual(title, "This is an h1")


if __name__ == "__main__":
    unittest.main()

    