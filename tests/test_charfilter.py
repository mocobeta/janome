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

PY3 = sys.version_info[0] == 3

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.charfilter import *

import unittest

class TestCharFilter(unittest.TestCase):
    def test_regex_replace_charfilter(self):
        cf = RegexReplaceCharFilter(u'蛇の目', u'janome')
        self.assertEqual(u'janomeは形態素解析器です。', cf.apply(u'蛇の目は形態素解析器です。'))

        cf = RegexReplaceCharFilter(u'\s+', u'')
        self.assertEqual(u'abcd', cf.apply(u' a  b c   d  '))

        cf = RegexReplaceCharFilter(u'', u'')
        self.assertEqual(u'abc あいうえお', u'abc あいうえお')

    def test_unicode_normalize_charfilter(self):
        cf = UnicodeNormalizeCharFilter()
        self.assertEqual(u'Python', cf.apply(u'Ｐｙｔｈｏｎ'))
        self.assertEqual(u'メガバイト', cf.apply(u'ﾒｶﾞﾊﾞｲﾄ'))


if __name__ == '__main__':
    unittest.main()
