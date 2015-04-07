# -*- coding: utf-8 -*-

# Copyright [2015] [moco_beta]
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

    def test_tokenize_unknown(self):
        text = '2009年10月16日'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self.assertEqual('2009', tokens[0].surface)
        self.assertEqual('年', tokens[1].surface)
        self.assertEqual('10', tokens[2].surface)
        self.assertEqual('月', tokens[3].surface)
        self.assertEqual('16', tokens[4].surface)
        self.assertEqual('日', tokens[5].surface)

        text = 'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self.assertEqual('マルチメディア', tokens[0].surface)
        self.assertEqual('放送', tokens[1].surface)
        self.assertEqual('（', tokens[2].surface)
        self.assertEqual('VHF', tokens[3].surface)
        self.assertEqual('-', tokens[4].surface)
        self.assertEqual('HIGH', tokens[5].surface)
        self.assertEqual('帯', tokens[6].surface)
        self.assertEqual('）', tokens[7].surface)
        self.assertEqual('「', tokens[8].surface)
        self.assertEqual('モバキャス', tokens[9].surface)
        self.assertEqual('」', tokens[10].surface)


def test_tokenize_with_user_dic(self):
        text = '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = Tokenizer(udic_file).tokenize(text)
        self.assertEqual(14, len(tokens))
        self.assertEqual('東京スカイツリー', tokens[0].surface)
        self.assertEqual('へ', tokens[1].surface)
        self.assertEqual('の', tokens[2].surface)
        self.assertEqual('お越し', tokens[3].surface)
        self.assertEqual('は', tokens[4].surface)
        self.assertEqual('、', tokens[5].surface)
        self.assertEqual('東武スカイツリーライン', tokens[6].surface)
        self.assertEqual('「', tokens[7].surface)
        self.assertEqual('とうきょうスカイツリー駅', tokens[8].surface)
        self.assertEqual('」', tokens[9].surface)
        self.assertEqual('が', tokens[10].surface)
        self.assertEqual('便利', tokens[11].surface)
        self.assertEqual('です', tokens[12].surface)
        self.assertEqual('。', tokens[13].surface)


if __name__ == '__main__':
    unittest.main()