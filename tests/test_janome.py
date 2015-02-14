import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
import janome

import unittest


class TestJanome(unittest.TestCase):
    def test_greeting_msg(self):
        name = 'alice'
        self.assertEqual('Hello alice !', janome.greeting_msg(name))


if __name__ == '__main__':
    unittest.main()
