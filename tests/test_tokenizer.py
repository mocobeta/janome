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
from janome.lattice import NodeType

import unittest


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(7, len(tokens))
        self.assertEqual(u'すもも', tokens[0].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[0].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[0].node_type)
        self.assertEqual(u'も', tokens[1].surface)
        self.assertEqual(u'助詞,係助詞,*,*', tokens[1].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[1].node_type)
        self.assertEqual(u'もも', tokens[2].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[2].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[2].node_type)
        self.assertEqual(u'も', tokens[3].surface)
        self.assertEqual(u'助詞,係助詞,*,*', tokens[3].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[3].node_type)
        self.assertEqual(u'もも', tokens[4].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[4].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[4].node_type)
        self.assertEqual(u'の', tokens[5].surface)
        self.assertEqual(u'助詞,連体化,*,*', tokens[5].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[5].node_type)
        self.assertEqual(u'うち', tokens[6].surface)
        self.assertEqual(u'名詞,非自立,副詞可能,*', tokens[6].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[6].node_type)

    def test_tokenize_unknown(self):
        text = u'2009年10月16日'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self.assertEqual(u'2009', tokens[0].surface)
        self.assertEqual(u'名詞,数,*,*', tokens[0].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[0].node_type)
        self.assertEqual(u'年', tokens[1].surface)
        self.assertEqual(u'名詞,接尾,助数詞,*', tokens[1].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[1].node_type)
        self.assertEqual(u'10', tokens[2].surface)
        self.assertEqual(u'名詞,数,*,*', tokens[2].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[2].node_type)
        self.assertEqual(u'月', tokens[3].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[3].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[3].node_type)
        self.assertEqual(u'16', tokens[4].surface)
        self.assertEqual(u'名詞,数,*,*', tokens[4].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[4].node_type)
        self.assertEqual(u'日', tokens[5].surface)
        self.assertEqual(u'名詞,接尾,助数詞,*', tokens[5].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[5].node_type)


        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self.assertEqual(u'マルチメディア', tokens[0].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[0].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[0].node_type)
        self.assertEqual(u'放送', tokens[1].surface)
        self.assertEqual(u'名詞,サ変接続,*,*', tokens[1].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[1].node_type)
        self.assertEqual(u'（', tokens[2].surface)
        self.assertEqual(u'記号,括弧開,*,*', tokens[2].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[2].node_type)
        self.assertEqual(u'VHF', tokens[3].surface)
        self.assertEqual(u'名詞,固有名詞,組織,*', tokens[3].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[3].node_type)
        self.assertEqual(u'-', tokens[4].surface)
        self.assertEqual(u'名詞,サ変接続,*,*', tokens[4].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[4].node_type)
        self.assertEqual(u'HIGH', tokens[5].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[5].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[5].node_type)
        self.assertEqual(u'帯', tokens[6].surface)
        self.assertEqual(u'名詞,接尾,一般,*', tokens[6].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[6].node_type)
        self.assertEqual(u'）', tokens[7].surface)
        self.assertEqual(u'記号,括弧閉,*,*', tokens[7].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[7].node_type)
        self.assertEqual(u'「', tokens[8].surface)
        self.assertEqual(u'記号,括弧開,*,*', tokens[8].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[8].node_type)
        self.assertEqual(u'モバキャス', tokens[9].surface)
        self.assertEqual(u'名詞,固有名詞,一般,*', tokens[9].part_of_speech)
        self.assertEqual(NodeType.UNKNOWN, tokens[9].node_type)
        self.assertEqual(u'」', tokens[10].surface)
        self.assertEqual(u'記号,括弧閉,*,*', tokens[10].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[10].node_type)


    def test_tokenize_with_user_dic(self):
        text = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = Tokenizer(udic_file).tokenize(text)
        self.assertEqual(14, len(tokens))
        self.assertEqual(u'東京スカイツリー', tokens[0].surface)
        self.assertEqual(u'名詞,固有名詞,一般,*', tokens[0].part_of_speech)
        self.assertEqual(NodeType.USER_DICT, tokens[0].node_type)
        self.assertEqual(u'へ', tokens[1].surface)
        self.assertEqual(u'助詞,格助詞,一般,*', tokens[1].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[1].node_type)
        self.assertEqual(u'の', tokens[2].surface)
        self.assertEqual(u'助詞,連体化,*,*', tokens[2].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[2].node_type)
        self.assertEqual(u'お越し', tokens[3].surface)
        self.assertEqual(u'名詞,一般,*,*', tokens[3].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[3].node_type)
        self.assertEqual(u'は', tokens[4].surface)
        self.assertEqual(u'助詞,係助詞,*,*', tokens[4].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[4].node_type)
        self.assertEqual(u'、', tokens[5].surface)
        self.assertEqual(u'記号,読点,*,*', tokens[5].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[5].node_type)
        self.assertEqual(u'東武スカイツリーライン', tokens[6].surface)
        self.assertEqual(u'名詞,固有名詞,一般,*', tokens[6].part_of_speech)
        self.assertEqual(NodeType.USER_DICT, tokens[6].node_type)
        self.assertEqual(u'「', tokens[7].surface)
        self.assertEqual(u'記号,括弧開,*,*', tokens[7].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[7].node_type)
        self.assertEqual(u'とうきょうスカイツリー駅', tokens[8].surface)
        self.assertEqual(u'名詞,固有名詞,一般,*', tokens[8].part_of_speech)
        self.assertEqual(NodeType.USER_DICT, tokens[8].node_type)
        self.assertEqual(u'」', tokens[9].surface)
        self.assertEqual(u'記号,括弧閉,*,*', tokens[9].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[9].node_type)
        self.assertEqual(u'が', tokens[10].surface)
        self.assertEqual(u'助詞,格助詞,一般,*', tokens[10].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[10].node_type)
        self.assertEqual(u'便利', tokens[11].surface)
        self.assertEqual(u'名詞,形容動詞語幹,*,*', tokens[11].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[11].node_type)
        self.assertEqual(u'です', tokens[12].surface)
        self.assertEqual(u'助動詞,*,*,*', tokens[12].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[12].node_type)
        self.assertEqual(u'。', tokens[13].surface)
        self.assertEqual(u'記号,句点,*,*', tokens[13].part_of_speech)
        self.assertEqual(NodeType.SYS_DICT, tokens[13].node_type)


if __name__ == '__main__':
    unittest.main()
