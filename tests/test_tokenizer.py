# -*- coding: utf-8 -*-

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

import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.tokenizer import Tokenizer

import unittest


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(7, len(tokens))
        self.assertEqual(u'すもも', tokens[0].surface)
        self.assertEqual(u'も', tokens[1].surface)
        self.assertEqual(u'もも', tokens[2].surface)
        self.assertEqual(u'も', tokens[3].surface)
        self.assertEqual(u'もも', tokens[4].surface)
        self.assertEqual(u'の', tokens[5].surface)
        self.assertEqual(u'うち', tokens[6].surface)

    def test_tokenize_unknown(self):
        text = u'2009年10月16日'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self.assertEqual(u'2009', tokens[0].surface)
        self.assertEqual(u'年', tokens[1].surface)
        self.assertEqual(u'10', tokens[2].surface)
        self.assertEqual(u'月', tokens[3].surface)
        self.assertEqual(u'16', tokens[4].surface)
        self.assertEqual(u'日', tokens[5].surface)

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self.assertEqual(u'マルチメディア', tokens[0].surface)
        self.assertEqual(u'放送', tokens[1].surface)
        self.assertEqual(u'（', tokens[2].surface)
        self.assertEqual(u'VHF', tokens[3].surface)
        self.assertEqual(u'-', tokens[4].surface)
        self.assertEqual(u'HIGH', tokens[5].surface)
        self.assertEqual(u'帯', tokens[6].surface)
        self.assertEqual(u'）', tokens[7].surface)
        self.assertEqual(u'「', tokens[8].surface)
        self.assertEqual(u'モバキャス', tokens[9].surface)
        self.assertEqual(u'」', tokens[10].surface)


    def test_tokenize_with_user_dic(self):
        text = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = Tokenizer(udic_file).tokenize(text)
        self.assertEqual(14, len(tokens))
        self.assertEqual(u'東京スカイツリー', tokens[0].surface)
        self.assertEqual(u'へ', tokens[1].surface)
        self.assertEqual(u'の', tokens[2].surface)
        self.assertEqual(u'お越し', tokens[3].surface)
        self.assertEqual(u'は', tokens[4].surface)
        self.assertEqual(u'、', tokens[5].surface)
        self.assertEqual(u'東武スカイツリーライン', tokens[6].surface)
        self.assertEqual(u'「', tokens[7].surface)
        self.assertEqual(u'とうきょうスカイツリー駅', tokens[8].surface)
        self.assertEqual(u'」', tokens[9].surface)
        self.assertEqual(u'が', tokens[10].surface)
        self.assertEqual(u'便利', tokens[11].surface)
        self.assertEqual(u'です', tokens[12].surface)
        self.assertEqual(u'。', tokens[13].surface)


if __name__ == '__main__':
    unittest.main()
