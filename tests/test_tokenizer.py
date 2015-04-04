# -*- coding: utf-8 -*-

import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from tokenizer import Tokenizer

import unittest


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        text = 'すもももももももものうち'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(7, len(tokens))
        self.assertEqual('すもも', tokens[0].surface)
        self.assertEqual('も', tokens[1].surface)
        self.assertEqual('もも', tokens[2].surface)
        self.assertEqual('も', tokens[3].surface)
        self.assertEqual('もも', tokens[4].surface)
        self.assertEqual('の', tokens[5].surface)
        self.assertEqual('うち', tokens[6].surface)


if __name__ == '__main__':
    unittest.main()