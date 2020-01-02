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
from io import open

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.tokenizer import Tokenizer, WakatiModeOnlyException
from janome.lattice import NodeType

import unittest


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

    def test_tokenize_mmap(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer(mmap=True).tokenize(text)
        self.assertEqual(7, len(tokens))
        self._check_token(tokens[0], u'すもも', u'名詞,一般,*,*,*,*,すもも,スモモ,スモモ', NodeType.SYS_DICT)
        self._check_token(tokens[1], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[5], u'の', u'助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[6], u'うち', u'名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ', NodeType.SYS_DICT)

    def test_tokenize2(self):
        text = u'𠮷野屋'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(3, len(tokens))
        self._check_token(tokens[0], u'𠮷', u'記号,一般,*,*,*,*,𠮷,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], u'野', u'名詞,一般,*,*,*,*,野,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'屋', u'名詞,接尾,一般,*,*,*,屋,ヤ,ヤ', NodeType.SYS_DICT)

        text = u'한국어'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(1, len(tokens))
        self._check_token(tokens[0], u'한국어', u'記号,一般,*,*,*,*,한국어,*,*', NodeType.UNKNOWN)

    def test_tokenize_patched_dic(self):
        text = u'令和元年'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(2, len(tokens))
        self._check_token(tokens[0], u'令和', u'名詞,固有名詞,一般,*,*,*,令和,レイワ,レイワ', NodeType.SYS_DICT)
        self._check_token(tokens[1], u'元年', u'名詞,一般,*,*,*,*,元年,ガンネン,ガンネン', NodeType.SYS_DICT)

    def test_tokenize_unknown(self):
        text = u'2009年10月16日'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], u'2009', u'名詞,数,*,*,*,*,2009,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], u'年', u'名詞,接尾,助数詞,*,*,*,年,ネン,ネン', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'10', u'名詞,数,*,*,*,*,10,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[3], u'月', u'名詞,一般,*,*,*,*,月,ツキ,ツキ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'16', u'名詞,数,*,*,*,*,16,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], u'日', u'名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ', NodeType.SYS_DICT)

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self._check_token(tokens[0], u'マルチメディア', u'名詞,一般,*,*,*,*,マルチメディア,マルチメディア,マルチメディア', NodeType.SYS_DICT)
        self._check_token(tokens[1], u'放送', u'名詞,サ変接続,*,*,*,*,放送,ホウソウ,ホーソー', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'（', u'記号,括弧開,*,*,*,*,（,（,（', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'VHF', u'名詞,固有名詞,組織,*,*,*,VHF,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[4], u'-', u'名詞,サ変接続,*,*,*,*,-,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], u'HIGH', u'名詞,一般,*,*,*,*,HIGH,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[6], u'帯', u'名詞,接尾,一般,*,*,*,帯,タイ,タイ', NodeType.SYS_DICT)
        self._check_token(tokens[7], u'）', u'記号,括弧閉,*,*,*,*,）,）,）', NodeType.SYS_DICT)
        self._check_token(tokens[8], u'「', u'記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[9], u'モバキャス', u'名詞,固有名詞,一般,*,*,*,モバキャス,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[10], u'」', u'記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)

    def test_tokenize_unknown_no_baseform(self):
        text = u'2009年10月16日'
        tokens = Tokenizer().tokenize(text, baseform_unk=False)
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], u'2009', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], u'年', u'名詞,接尾,助数詞,*,*,*,年,ネン,ネン', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'10', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[3], u'月', u'名詞,一般,*,*,*,*,月,ツキ,ツキ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'16', u'名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], u'日', u'名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ', NodeType.SYS_DICT)

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = Tokenizer().tokenize(text, baseform_unk=False)
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

    def test_tokenize_with_simplified_userdic(self):
        text = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_simpledic.csv')
        tokens = Tokenizer(udic_file, udic_type='simpledic').tokenize(text)
        self.assertEqual(14, len(tokens))
        self._check_token(tokens[0], u'東京スカイツリー', u'カスタム名詞,*,*,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー', NodeType.USER_DICT)
        self._check_token(tokens[1], u'へ', u'助詞,格助詞,一般,*,*,*,へ,ヘ,エ', NodeType.SYS_DICT)
        self._check_token(tokens[2], u'の', u'助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[3], u'お越し', u'名詞,一般,*,*,*,*,お越し,オコシ,オコシ', NodeType.SYS_DICT)
        self._check_token(tokens[4], u'は', u'助詞,係助詞,*,*,*,*,は,ハ,ワ', NodeType.SYS_DICT)
        self._check_token(tokens[5], u'、', u'記号,読点,*,*,*,*,、,、,、', NodeType.SYS_DICT)
        self._check_token(tokens[6], u'東武スカイツリーライン', u'カスタム名詞,*,*,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン', NodeType.USER_DICT)
        self._check_token(tokens[7], u'「', u'記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[8], u'とうきょうスカイツリー駅', u'カスタム名詞,*,*,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ', NodeType.USER_DICT)
        self._check_token(tokens[9], u'」', u'記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)
        self._check_token(tokens[10], u'が', u'助詞,格助詞,一般,*,*,*,が,ガ,ガ', NodeType.SYS_DICT)
        self._check_token(tokens[11], u'便利', u'名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ', NodeType.SYS_DICT)
        self._check_token(tokens[12], u'です', u'助動詞,*,*,*,特殊・デス,基本形,です,デス,デス', NodeType.SYS_DICT)
        self._check_token(tokens[13], u'。', u'記号,句点,*,*,*,*,。,。,。', NodeType.SYS_DICT)

    def test_tokenize_large_text(self):
        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = Tokenizer().tokenize(text)

    def test_tokenize_large_text2(self):
        with open('tests/text_large.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = Tokenizer().tokenize(text)

    def test_tokenize_large_text3(self):
        with open('tests/text_large_nonjp.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = Tokenizer().tokenize(text)

    def test_tokenize_large_text_stream(self):
        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(Tokenizer().tokenize(text, stream = True))

    def test_tokenize_large_text_stream2(self):
        with open('tests/text_large.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(Tokenizer().tokenize(text, stream = True))

    def test_tokenize_large_text_stream3(self):
        with open('tests/text_large_nonjp.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(Tokenizer().tokenize(text, stream = True))

    def test_tokenize_wakati(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer(wakati = True).tokenize(text, wakati = True)
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], u'すもも')
        self.assertEqual(tokens[1], u'も')
        self.assertEqual(tokens[2], u'もも')
        self.assertEqual(tokens[3], u'も')
        self.assertEqual(tokens[4], u'もも')
        self.assertEqual(tokens[5], u'の')
        self.assertEqual(tokens[6], u'うち')

    def test_tokenize_with_userdic_wakati(self):
        text = u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = Tokenizer(udic_file, wakati = True).tokenize(text, wakati = True)
        self.assertEqual(14, len(tokens))
        self.assertEqual(tokens[0], u'東京スカイツリー')
        self.assertEqual(tokens[1], u'へ')
        self.assertEqual(tokens[2], u'の')
        self.assertEqual(tokens[3], u'お越し')
        self.assertEqual(tokens[4], u'は')
        self.assertEqual(tokens[5], u'、')
        self.assertEqual(tokens[6], u'東武スカイツリーライン')
        self.assertEqual(tokens[7], u'「')
        self.assertEqual(tokens[8], u'とうきょうスカイツリー駅')
        self.assertEqual(tokens[9], u'」')
        self.assertEqual(tokens[10], u'が')
        self.assertEqual(tokens[11], u'便利')
        self.assertEqual(tokens[12], u'です')
        self.assertEqual(tokens[13], u'。')

    def test_tokenize_wakati_mode_only(self):
        text = u'すもももももももものうち'
        tokens = Tokenizer(wakati = True).tokenize(text, wakati = False)
        # 'wakati = True' parameter is ignored.
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], u'すもも')
        self.assertEqual(tokens[1], u'も')
        self.assertEqual(tokens[2], u'もも')
        self.assertEqual(tokens[3], u'も')
        self.assertEqual(tokens[4], u'もも')
        self.assertEqual(tokens[5], u'の')
        self.assertEqual(tokens[6], u'うち')

    def test_tokenize_dotfile(self):
        text = u'すもももももももものうち'
        dotfile = os.path.join(parent_dir, 'tests/lattice.gv')
        if os.path.exists(dotfile):
            os.remove(dotfile)

        Tokenizer().tokenize(text, dotfile=dotfile)
        self.assertTrue(os.path.exists(dotfile))

    def test_tokenize_dotfile_stream(self):
        text = u'すもももももももものうち'
        dotfile = os.path.join(parent_dir, 'tests/lattice_must_not_exist.gv')
        if os.path.exists(dotfile):
            os.remove(dotfile)

        Tokenizer().tokenize(text, dotfile=dotfile, stream=True)
        self.assertFalse(os.path.exists(dotfile))

    def test_tokenize_dotfile_large_text(self):
        dotfile = os.path.join(parent_dir, 'tests/lattice_must_not_exist.gv')
        if os.path.exists(dotfile):
            os.remove(dotfile)

        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = Tokenizer().tokenize(text, dotfile=dotfile)
        self.assertFalse(os.path.exists(dotfile))

    def _check_token(self, token, surface, detail, node_type):
        self.assertEqual(surface, token.surface)
        self.assertEqual(detail, ','.join([token.part_of_speech,token.infl_type,token.infl_form,token.base_form,token.reading,token.phonetic]))
        self.assertEqual(surface + '\t' + detail, str(token))
        self.assertEqual(node_type, token.node_type)

if __name__ == '__main__':
    unittest.main()
