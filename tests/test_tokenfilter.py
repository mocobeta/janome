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
import unittest
from janome.tokenfilter import (
    LowerCaseFilter,
    UpperCaseFilter,
    POSStopFilter,
    POSKeepFilter,
    CompoundNounFilter,
    ExtractAttributeFilter,
    TokenCountFilter
)
from janome.tokenizer import Tokenizer

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestTokenFilter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.t = Tokenizer()

    def test_lowercase_filter(self):
        tf = LowerCaseFilter()
        tokens = tf.apply(self.t.tokenize('Python JavaScript'))
        self.assertEqual(['python', ' ', 'javascript'], list(map(lambda token: token.surface, tokens)))
        tokens = tf.apply(self.t.tokenize('Python JavaScript'))
        self.assertEqual(['python', ' ', 'javascript'], list(map(lambda token: token.base_form, tokens)))

    def test_uppercase_filter(self):
        tf = UpperCaseFilter()
        tokens = tf.apply(self.t.tokenize('Python JavaScript'))
        self.assertEqual(['PYTHON', ' ', 'JAVASCRIPT'], list(map(lambda token: token.surface, tokens)))
        tokens = tf.apply(self.t.tokenize('Python JavaScript'))
        self.assertEqual(['PYTHON', ' ', 'JAVASCRIPT'], list(map(lambda token: token.base_form, tokens)))

    def test_pos_stop_filter(self):
        tf = POSStopFilter(['助詞', '記号', '動詞,非自立'])
        tokens = tf.apply(self.t.tokenize('行ってしまった。'))
        self.assertEqual(['動詞,自立,*,*', '助動詞,*,*,*'], list(map(lambda token: token.part_of_speech, tokens)))

    def test_pos_keep_filter(self):
        tf = POSKeepFilter(['名詞,固有名詞', '動詞,自立'])
        tokens = tf.apply(self.t.tokenize('東京駅で降りる'))
        self.assertEqual(['名詞,固有名詞,地域,一般', '動詞,自立,*,*'], list(map(lambda token: token.part_of_speech, tokens)))

    def test_compound_noun_filter(self):
        tf = CompoundNounFilter()
        tokens = tf.apply(self.t.tokenize('浜松町駅から東京モノレールで羽田空港ターミナルへ向かう'))
        self.assertEqual(['浜松町駅', 'から', '東京モノレール', 'で', '羽田空港ターミナル', 'へ', '向かう'],
                         list(map(lambda token: token.surface, tokens)))

    def test_extract_attribute_filter(self):
        tf = ExtractAttributeFilter('surface')
        self.assertEqual(['風', '立ち', 'ぬ'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('part_of_speech')
        self.assertEqual(['名詞,一般,*,*', '動詞,自立,*,*', '助動詞,*,*,*'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('infl_type')
        self.assertEqual(['*', '五段・タ行', '不変化型'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('infl_form')
        self.assertEqual(['*', '連用形', '基本形'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('base_form')
        self.assertEqual(['風', '立つ', 'ぬ'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('reading')
        self.assertEqual(['カゼ', 'タチ', 'ヌ'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        tf = ExtractAttributeFilter('phonetic')
        self.assertEqual(['カゼ', 'タチ', 'ヌ'], list(tf.apply(self.t.tokenize('風立ちぬ'))))

        # invalid attribute name
        with self.assertRaises(Exception):
            ExtractAttributeFilter('foo')

    def test_count_token_filter(self):
        tf = TokenCountFilter()
        d = dict(tf.apply(self.t.tokenize('すもももももももものうち')))
        self.assertEqual(1, d['すもも'])
        self.assertEqual(2, d['もも'])
        self.assertEqual(2, d['も'])
        self.assertEqual(1, d['の'])
        self.assertEqual(1, d['うち'])

        # sort by frequency
        tf = TokenCountFilter(sorted=True)
        counts = list(map(lambda x: x[1], tf.apply(self.t.tokenize('すもももももももものうち'))))
        self.assertEqual([2, 2, 1, 1, 1], counts)

        tf = TokenCountFilter('base_form')
        d = dict(tf.apply(self.t.tokenize('CountFilterで簡単に単語数が数えられます')))
        self.assertEqual(1, d['CountFilter'])
        self.assertEqual(1, d['で'])
        self.assertEqual(1, d['簡単'])
        self.assertEqual(1, d['に'])
        self.assertEqual(1, d['単語'])
        self.assertEqual(1, d['数'])
        self.assertEqual(1, d['が'])
        self.assertEqual(1, d['数える'])
        self.assertEqual(1, d['られる'])
        self.assertEqual(1, d['ます'])

        # invalid attribute name
        with self.assertRaises(Exception):
            TokenCountFilter('foo')


if __name__ == '__main__':
    unittest.main()
