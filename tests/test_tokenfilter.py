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
from janome.tokenfilter import *

import unittest

class TestTokenFilter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.t = Tokenizer()

    def test_lowercase_filter(self):
        tf = LowerCaseFilter()
        tokens = tf.apply(self.t.tokenize(u'Python JavaScript'))
        self.assertEqual([u'python', u' ', u'javascript'], list(map(lambda token: token.surface, tokens)))
        tokens = tf.apply(self.t.tokenize(u'Python JavaScript'))
        self.assertEqual([u'python', u' ', u'javascript'], list(map(lambda token: token.base_form, tokens)))

    def test_uppercase_filter(self):
        tf = UpperCaseFilter()
        tokens = tf.apply(self.t.tokenize(u'Python JavaScript'))
        self.assertEqual([u'PYTHON', u' ', u'JAVASCRIPT'], list(map(lambda token: token.surface, tokens)))
        tokens = tf.apply(self.t.tokenize(u'Python JavaScript'))
        self.assertEqual([u'PYTHON', u' ', u'JAVASCRIPT'], list(map(lambda token: token.base_form, tokens)))

    def test_pos_stop_filter(self):
        tf = POSStopFilter([u'助詞', u'記号', u'動詞,非自立'])
        tokens = tf.apply(self.t.tokenize(u'行ってしまった。'))
        self.assertEqual([u'動詞,自立,*,*', u'助動詞,*,*,*'], list(map(lambda token: token.part_of_speech, tokens)))

    def test_pos_keep_filter(self):
        tf = POSKeepFilter([u'名詞,固有名詞', u'動詞,自立'])
        tokens = tf.apply(self.t.tokenize(u'東京駅で降りる'))
        self.assertEqual([u'名詞,固有名詞,地域,一般', u'動詞,自立,*,*'], list(map(lambda token: token.part_of_speech, tokens)))

    def test_compound_noun_filter(self):
        tf = CompoundNounFilter()
        tokens = tf.apply(self.t.tokenize(u'浜松町駅から東京モノレールで羽田空港ターミナルへ向かう'))
        self.assertEqual([u'浜松町駅', u'から', u'東京モノレール', u'で', u'羽田空港ターミナル', u'へ', u'向かう'],
                        list(map(lambda token: token.surface, tokens)))

    def test_extract_attribute_filter(self):
        tf = ExtractAttributeFilter('surface')
        self.assertEqual([u'風', u'立ち', u'ぬ'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))

        tf = ExtractAttributeFilter('part_of_speech')
        self.assertEqual([u'名詞,一般,*,*', u'動詞,自立,*,*', u'助動詞,*,*,*'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))

        tf = ExtractAttributeFilter('infl_type')
        self.assertEqual([u'*', u'五段・タ行', u'不変化型'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))
        
        tf = ExtractAttributeFilter('infl_form')
        self.assertEqual([u'*', u'連用形', u'基本形'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))

        tf = ExtractAttributeFilter('base_form')
        self.assertEqual([u'風', u'立つ', u'ぬ'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))
        
        tf = ExtractAttributeFilter('reading')
        self.assertEqual([u'カゼ', u'タチ', u'ヌ'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))

        tf = ExtractAttributeFilter('phonetic')
        self.assertEqual([u'カゼ', u'タチ', u'ヌ'], list(tf.apply(self.t.tokenize(u'風立ちぬ'))))

        # invalid attribute name
        with self.assertRaises(Exception):
            ExtractAttributeFilter('foo')


    def test_count_token_filter(self):
        tf = TokenCountFilter()
        d = dict(tf.apply(self.t.tokenize(u'すもももももももものうち')))
        self.assertEqual(1, d[u'すもも'])
        self.assertEqual(2, d[u'もも'])
        self.assertEqual(2, d[u'も'])
        self.assertEqual(1, d[u'の'])
        self.assertEqual(1, d[u'うち'])

        # sort by frequency
        tf = TokenCountFilter(sorted=True)
        counts = list(map(lambda x: x[1], tf.apply(self.t.tokenize(u'すもももももももものうち'))))
        self.assertEqual([2,2,1,1,1], counts)

        tf = TokenCountFilter('base_form')
        d = dict(tf.apply(self.t.tokenize(u'CountFilterで簡単に単語数が数えられます')))
        self.assertEqual(1, d[u'CountFilter'])
        self.assertEqual(1, d[u'で'])
        self.assertEqual(1, d[u'簡単'])
        self.assertEqual(1, d[u'に'])
        self.assertEqual(1, d[u'単語'])
        self.assertEqual(1, d[u'数'])
        self.assertEqual(1, d[u'が'])
        self.assertEqual(1, d[u'数える'])
        self.assertEqual(1, d[u'られる'])
        self.assertEqual(1, d[u'ます'])

        # invalid attribute name
        with self.assertRaises(Exception):
            TokenCountFilter('foo')

if __name__ == '__main__':
    unittest.main()
