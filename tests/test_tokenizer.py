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

PY3 = sys.version_info[0] == 3


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(7, len(tokens))
        self._check_token(tokens[0], u'すもも', u'名詞,一般,*,*,*,*,すもも,スモモ,スモモ', NodeType.SYS_DICT)
        self._check_token(tokens[1], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[5], u'の', u'助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[6], u'うち', u'名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ', NodeType.SYS_DICT)

    def test_tokenize_unknown(self):
        text = u'2009年10月16日'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], u'2009', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], u'年', u'名詞,接尾,助数詞,*,*,*,年,ネン,ネン', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'10', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[3], u'月', u'名詞,一般,*,*,*,*,月,ツキ,ツキ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'16', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], u'日', u'名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ', NodeType.SYS_DICT)

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self._check_token(tokens[0], u'マルチメディア', u'名詞,一般,*,*,*,*,マルチメディア,マルチメディア,マルチメディア', NodeType.SYS_DICT)
        self._check_token(tokens[1], u'放送', u'名詞,サ変接続,*,*,*,*,放送,ホウソウ,ホーソー', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'（', u'記号,括弧開,*,*,*,*,（,（,（', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'VHF', u'名詞,固有名詞,組織,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[4], u'-', u'名詞,サ変接続,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], u'HIGH', u'名詞,一般,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[6], u'帯', u'名詞,接尾,一般,*,*,*,帯,タイ,タイ', NodeType.SYS_DICT)
        self._check_token(tokens[7], u'）', u'記号,括弧閉,*,*,*,*,）,）,）', NodeType.SYS_DICT)
        self._check_token(tokens[8], u'「', u'記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[9], u'モバキャス', u'名詞,固有名詞,一般,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[10], u'」', u'記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)

    def test_tokenize_with_userdic(self):
        text = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = Tokenizer(udic_file).tokenize(text)
        self.assertEqual(14, len(tokens))
        self._check_token(tokens[0], u'東京スカイツリー', u'名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー', NodeType.USER_DICT)
        self._check_token(tokens[1], u'へ', u'助詞,格助詞,一般,*,*,*,へ,ヘ,エ', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'の', u'助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'お越し', u'名詞,一般,*,*,*,*,お越し,オコシ,オコシ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'は', u'助詞,係助詞,*,*,*,*,は,ハ,ワ', NodeType.SYS_DICT)
        self._check_token(tokens[5], u'、', u'記号,読点,*,*,*,*,、,、,、', NodeType.SYS_DICT)
        self._check_token(tokens[6], u'東武スカイツリーライン', u'名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン', NodeType.USER_DICT)
        self._check_token(tokens[7], u'「', u'記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[8], u'とうきょうスカイツリー駅', u'名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ', NodeType.USER_DICT)
        self._check_token(tokens[9], u'」', u'記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)
        self._check_token(tokens[10], u'が', u'助詞,格助詞,一般,*,*,*,が,ガ,ガ', NodeType.SYS_DICT)
        self._check_token(tokens[11], u'便利', u'名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ', NodeType.SYS_DICT)
        self._check_token(tokens[12], u'です', u'助動詞,*,*,*,特殊・デス,基本形,です,デス,デス', NodeType.SYS_DICT)
        self._check_token(tokens[13], u'。', u'記号,句点,*,*,*,*,。,。,。', NodeType.SYS_DICT)

    def _check_token(self, token, surface, detail, node_type):
        self.assertEqual(surface, token.surface)
        self.assertEqual(detail,
                         str(token).split('\t')[1] if PY3
                         else str(token).split('\t')[1].decode('utf8'))
        self.assertEqual(node_type, token.node_type)

if __name__ == '__main__':
    unittest.main()
