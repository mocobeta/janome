# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from janome.tokenfilter import CompoundNounFilter, POSStopFilter, LowerCaseFilter, ExtractAttributeFilter
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
import os
import sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestAnalyzer(unittest.TestCase):
    def test_analyzer_default(self):
        a = Analyzer()
        self.assertIsNotNone(a.char_filters)
        self.assertTrue(len(a.char_filters) == 0)
        self.assertIsNotNone(a.tokenizer)
        self.assertIsInstance(a.tokenizer, Tokenizer)
        self.assertIsNotNone(a.token_filters)
        self.assertTrue(len(a.token_filters) == 0)

    def test_analyzer_custom(self):
        char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('\s+', '')]
        tokenizer = Tokenizer()
        token_filters = [CompoundNounFilter(), POSStopFilter(['記号', '助詞']), LowerCaseFilter()]
        a = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
        self.assertTrue(len(a.char_filters) == 2)
        self.assertIsInstance(a.char_filters[0], UnicodeNormalizeCharFilter)
        self.assertIsInstance(a.char_filters[1], RegexReplaceCharFilter)
        self.assertTrue(len(a.token_filters) == 3)
        self.assertIsInstance(a.token_filters[0], CompoundNounFilter)
        self.assertIsInstance(a.token_filters[1], POSStopFilter)
        self.assertIsInstance(a.token_filters[2], LowerCaseFilter)

    def test_analyze(self):
        char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('蛇の目', 'janome')]
        tokenizer = Tokenizer()
        token_filters = [CompoundNounFilter(), POSStopFilter(['記号', '助詞']), LowerCaseFilter(),
                         ExtractAttributeFilter('surface')]
        a = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
        tokens = a.analyze('蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。')
        self.assertEqual(['janome', 'pure', 'python', 'な', '形態素解析器', 'です'], list(tokens))


if __name__ == '__main__':
    unittest.main()
