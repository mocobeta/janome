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

import os
import sys
from io import open
import unittest
import psutil
from janome.lattice import NodeType
from janome.tokenizer import Tokenizer
from janome.system_dic import SystemDictionary, MMapSystemDictionary

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

IS_64BIT = sys.maxsize > 2**32


class TestTokenizer(unittest.TestCase):

    def test_initialize(self):
        t = Tokenizer()
        if IS_64BIT:
            self.assertIsInstance(t.sys_dic, MMapSystemDictionary)
        else:
            self.assertIsInstance(t.sys_dic, SystemDictionary)

    def test_tokenize_nommap(self):
        text = 'すもももももももものうち'
        tokens = list(Tokenizer(mmap=False).tokenize(text))
        self.assertEqual(7, len(tokens))
        self._check_token(tokens[0], 'すもも', '名詞,一般,*,*,*,*,すもも,スモモ,スモモ', NodeType.SYS_DICT)
        self._check_token(tokens[1], 'も', '助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[2], 'もも', '名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'も', '助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[4], 'もも', '名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[5], 'の', '助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[6], 'うち', '名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ', NodeType.SYS_DICT)

    def test_tokenize_mmap(self):
        if sys.maxsize <= 2**32:
            # 32bit architecture
            return
        text = 'すもももももももものうち'
        tokens = list(Tokenizer(mmap=True).tokenize(text))
        self.assertEqual(7, len(tokens))
        self._check_token(tokens[0], 'すもも', '名詞,一般,*,*,*,*,すもも,スモモ,スモモ', NodeType.SYS_DICT)
        self._check_token(tokens[1], 'も', '助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[2], 'もも', '名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'も', '助詞,係助詞,*,*,*,*,も,モ,モ', NodeType.SYS_DICT)
        self._check_token(tokens[4], 'もも', '名詞,一般,*,*,*,*,もも,モモ,モモ', NodeType.SYS_DICT)
        self._check_token(tokens[5], 'の', '助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[6], 'うち', '名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ', NodeType.SYS_DICT)

    def test_tokenize2(self):
        text = '𠮷野屋'
        tokens = list(Tokenizer().tokenize(text))
        self.assertEqual(3, len(tokens))
        self._check_token(tokens[0], '𠮷', '記号,一般,*,*,*,*,𠮷,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], '野', '名詞,一般,*,*,*,*,野,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[2], '屋', '名詞,接尾,一般,*,*,*,屋,ヤ,ヤ', NodeType.SYS_DICT)

        text = '한국어'
        tokens = list(Tokenizer().tokenize(text))
        self.assertEqual(1, len(tokens))
        self._check_token(tokens[0], '한국어', '記号,一般,*,*,*,*,한국어,*,*', NodeType.UNKNOWN)

    def test_tokenize_patched_dic(self):
        text = '令和元年'
        tokens = list(Tokenizer().tokenize(text))
        self.assertEqual(2, len(tokens))
        self._check_token(tokens[0], '令和', '名詞,固有名詞,一般,*,*,*,令和,レイワ,レイワ', NodeType.SYS_DICT)
        self._check_token(tokens[1], '元年', '名詞,一般,*,*,*,*,元年,ガンネン,ガンネン', NodeType.SYS_DICT)

    def test_tokenize_unknown(self):
        text = '2009年10月16日'
        tokens = list(Tokenizer().tokenize(text))
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], '2009', '名詞,数,*,*,*,*,2009,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], '年', '名詞,接尾,助数詞,*,*,*,年,ネン,ネン', NodeType.SYS_DICT)
        self._check_token(tokens[2], '10', '名詞,数,*,*,*,*,10,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[3], '月', '名詞,一般,*,*,*,*,月,ツキ,ツキ', NodeType.SYS_DICT)
        self._check_token(tokens[4], '16', '名詞,数,*,*,*,*,16,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], '日', '名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ', NodeType.SYS_DICT)

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = list(Tokenizer().tokenize(text))
        self.assertEqual(11, len(tokens))
        self._check_token(tokens[0], 'マルチメディア', '名詞,一般,*,*,*,*,マルチメディア,マルチメディア,マルチメディア', NodeType.SYS_DICT)
        self._check_token(tokens[1], '放送', '名詞,サ変接続,*,*,*,*,放送,ホウソウ,ホーソー', NodeType.SYS_DICT)
        self._check_token(tokens[2], '（', '記号,括弧開,*,*,*,*,（,（,（', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'VHF', '名詞,固有名詞,組織,*,*,*,VHF,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[4], '-', '名詞,サ変接続,*,*,*,*,-,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], 'HIGH', '名詞,一般,*,*,*,*,HIGH,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[6], '帯', '名詞,接尾,一般,*,*,*,帯,タイ,タイ', NodeType.SYS_DICT)
        self._check_token(tokens[7], '）', '記号,括弧閉,*,*,*,*,）,）,）', NodeType.SYS_DICT)
        self._check_token(tokens[8], '「', '記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[9], 'モバキャス', '名詞,固有名詞,一般,*,*,*,モバキャス,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[10], '」', '記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)

    def test_tokenize_unknown_no_baseform(self):
        text = '2009年10月16日'
        tokens = list(Tokenizer().tokenize(text, baseform_unk=False))
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], '2009', '名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[1], '年', '名詞,接尾,助数詞,*,*,*,年,ネン,ネン', NodeType.SYS_DICT)
        self._check_token(tokens[2], '10', '名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[3], '月', '名詞,一般,*,*,*,*,月,ツキ,ツキ', NodeType.SYS_DICT)
        self._check_token(tokens[4], '16', '名詞,数,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], '日', '名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ', NodeType.SYS_DICT)

        text = 'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = list(Tokenizer().tokenize(text, baseform_unk=False))
        self.assertEqual(11, len(tokens))
        self._check_token(tokens[0], 'マルチメディア', '名詞,一般,*,*,*,*,マルチメディア,マルチメディア,マルチメディア', NodeType.SYS_DICT)
        self._check_token(tokens[1], '放送', '名詞,サ変接続,*,*,*,*,放送,ホウソウ,ホーソー', NodeType.SYS_DICT)
        self._check_token(tokens[2], '（', '記号,括弧開,*,*,*,*,（,（,（', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'VHF', '名詞,固有名詞,組織,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[4], '-', '名詞,サ変接続,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[5], 'HIGH', '名詞,一般,*,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[6], '帯', '名詞,接尾,一般,*,*,*,帯,タイ,タイ', NodeType.SYS_DICT)
        self._check_token(tokens[7], '）', '記号,括弧閉,*,*,*,*,）,）,）', NodeType.SYS_DICT)
        self._check_token(tokens[8], '「', '記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[9], 'モバキャス', '名詞,固有名詞,一般,*,*,*,*,*,*', NodeType.UNKNOWN)
        self._check_token(tokens[10], '」', '記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)

    def test_tokenize_with_userdic(self):
        text = '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = list(Tokenizer(udic_file).tokenize(text))
        self.assertEqual(14, len(tokens))
        self._check_token(tokens[0], '東京スカイツリー',
                          '名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー', NodeType.USER_DICT)
        self._check_token(tokens[1], 'へ', '助詞,格助詞,一般,*,*,*,へ,ヘ,エ', NodeType.SYS_DICT)
        self._check_token(tokens[2], 'の', '助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'お越し', '名詞,一般,*,*,*,*,お越し,オコシ,オコシ', NodeType.SYS_DICT)
        self._check_token(tokens[4], 'は', '助詞,係助詞,*,*,*,*,は,ハ,ワ', NodeType.SYS_DICT)
        self._check_token(tokens[5], '、', '記号,読点,*,*,*,*,、,、,、', NodeType.SYS_DICT)
        self._check_token(tokens[6], '東武スカイツリーライン',
                          '名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン', NodeType.USER_DICT)
        self._check_token(tokens[7], '「', '記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[8], 'とうきょうスカイツリー駅',
                          '名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ', NodeType.USER_DICT)
        self._check_token(tokens[9], '」', '記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)
        self._check_token(tokens[10], 'が', '助詞,格助詞,一般,*,*,*,が,ガ,ガ', NodeType.SYS_DICT)
        self._check_token(tokens[11], '便利', '名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ', NodeType.SYS_DICT)
        self._check_token(tokens[12], 'です', '助動詞,*,*,*,特殊・デス,基本形,です,デス,デス', NodeType.SYS_DICT)
        self._check_token(tokens[13], '。', '記号,句点,*,*,*,*,。,。,。', NodeType.SYS_DICT)

    def test_tokenize_with_simplified_userdic(self):
        text = '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_simpledic.csv')
        tokens = list(Tokenizer(udic_file, udic_type='simpledic').tokenize(text))
        self.assertEqual(14, len(tokens))
        self._check_token(tokens[0], '東京スカイツリー',
                          'カスタム名詞,*,*,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー', NodeType.USER_DICT)
        self._check_token(tokens[1], 'へ', '助詞,格助詞,一般,*,*,*,へ,ヘ,エ', NodeType.SYS_DICT)
        self._check_token(tokens[2], 'の', '助詞,連体化,*,*,*,*,の,ノ,ノ', NodeType.SYS_DICT)
        self._check_token(tokens[3], 'お越し', '名詞,一般,*,*,*,*,お越し,オコシ,オコシ', NodeType.SYS_DICT)
        self._check_token(tokens[4], 'は', '助詞,係助詞,*,*,*,*,は,ハ,ワ', NodeType.SYS_DICT)
        self._check_token(tokens[5], '、', '記号,読点,*,*,*,*,、,、,、', NodeType.SYS_DICT)
        self._check_token(tokens[6], '東武スカイツリーライン',
                          'カスタム名詞,*,*,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン', NodeType.USER_DICT)
        self._check_token(tokens[7], '「', '記号,括弧開,*,*,*,*,「,「,「', NodeType.SYS_DICT)
        self._check_token(tokens[8], 'とうきょうスカイツリー駅',
                          'カスタム名詞,*,*,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ', NodeType.USER_DICT)
        self._check_token(tokens[9], '」', '記号,括弧閉,*,*,*,*,」,」,」', NodeType.SYS_DICT)
        self._check_token(tokens[10], 'が', '助詞,格助詞,一般,*,*,*,が,ガ,ガ', NodeType.SYS_DICT)
        self._check_token(tokens[11], '便利', '名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ', NodeType.SYS_DICT)
        self._check_token(tokens[12], 'です', '助動詞,*,*,*,特殊・デス,基本形,です,デス,デス', NodeType.SYS_DICT)
        self._check_token(tokens[13], '。', '記号,句点,*,*,*,*,。,。,。', NodeType.SYS_DICT)

    def test_tokenize_large_text(self):
        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            Tokenizer().tokenize(text)

    def test_tokenize_large_text2(self):
        with open('tests/text_large.txt', encoding='utf-8') as f:
            text = f.read()
            Tokenizer().tokenize(text)

    def test_tokenize_large_text3(self):
        with open('tests/text_large_nonjp.txt', encoding='utf-8') as f:
            text = f.read()
            Tokenizer().tokenize(text)

    def test_tokenize_wakati(self):
        text = 'すもももももももものうち'
        tokens = list(Tokenizer(wakati=True).tokenize(text, wakati=True))
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], 'すもも')
        self.assertEqual(tokens[1], 'も')
        self.assertEqual(tokens[2], 'もも')
        self.assertEqual(tokens[3], 'も')
        self.assertEqual(tokens[4], 'もも')
        self.assertEqual(tokens[5], 'の')
        self.assertEqual(tokens[6], 'うち')

    def test_tokenize_with_userdic_wakati(self):
        text = '東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'
        udic_file = os.path.join(parent_dir, 'tests/user_ipadic.csv')
        tokens = list(Tokenizer(udic_file, wakati=True).tokenize(text, wakati=True))
        self.assertEqual(14, len(tokens))
        self.assertEqual(tokens[0], '東京スカイツリー')
        self.assertEqual(tokens[1], 'へ')
        self.assertEqual(tokens[2], 'の')
        self.assertEqual(tokens[3], 'お越し')
        self.assertEqual(tokens[4], 'は')
        self.assertEqual(tokens[5], '、')
        self.assertEqual(tokens[6], '東武スカイツリーライン')
        self.assertEqual(tokens[7], '「')
        self.assertEqual(tokens[8], 'とうきょうスカイツリー駅')
        self.assertEqual(tokens[9], '」')
        self.assertEqual(tokens[10], 'が')
        self.assertEqual(tokens[11], '便利')
        self.assertEqual(tokens[12], 'です')
        self.assertEqual(tokens[13], '。')

    def test_tokenize_wakati_mode_only(self):
        text = 'すもももももももものうち'
        tokens = list(Tokenizer(wakati=True).tokenize(text, wakati=False))
        # 'wakati = True' parameter is ignored.
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], 'すもも')
        self.assertEqual(tokens[1], 'も')
        self.assertEqual(tokens[2], 'もも')
        self.assertEqual(tokens[3], 'も')
        self.assertEqual(tokens[4], 'もも')
        self.assertEqual(tokens[5], 'の')
        self.assertEqual(tokens[6], 'うち')

    def test_tokenize_dotfile(self):
        text = 'すもももももももものうち'
        dotfile = os.path.join(parent_dir, 'tests/lattice.gv')
        if os.path.exists(dotfile):
            os.remove(dotfile)

        list(Tokenizer().tokenize(text, dotfile=dotfile))
        self.assertTrue(os.path.exists(dotfile))

    def test_tokenize_dotfile_large_text(self):
        dotfile = os.path.join(parent_dir, 'tests/lattice_must_not_exist.gv')
        if os.path.exists(dotfile):
            os.remove(dotfile)

        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            list(Tokenizer().tokenize(text, dotfile=dotfile))
        self.assertFalse(os.path.exists(dotfile))

    def test_mmap_open_files(self):
        def open_dict_files():
            p = psutil.Process()
            open_dict_files = len(list(filter(lambda x: x.path.find('janome/sysdic') >= 0, p.open_files())))

        fp_count = open_dict_files()

        tokenizers = []
        for i in range(100):
            tokenizers.append(Tokenizer(mmap=True))

        self.assertEqual(100, len(tokenizers))
        self.assertEqual(fp_count, open_dict_files())

    def _check_token(self, token, surface, detail, node_type):
        self.assertEqual(surface, token.surface)
        self.assertEqual(detail, ','.join([token.part_of_speech, token.infl_type,
                                           token.infl_form, token.base_form, token.reading, token.phonetic]))
        self.assertEqual(surface + '\t' + detail, str(token))
        self.assertEqual(node_type, token.node_type)


if __name__ == '__main__':
    unittest.main()
