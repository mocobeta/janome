# Copyright 2022 moco_beta
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
from janome.sysdic import all_fstdata, entries, mmap_entries, connections, chardef, unknowns
from janome.system_dic import SystemDictionary, MMapSystemDictionary
from janome.fst import Matcher

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestSystemDictionary(unittest.TestCase):

    def test_dictionary_ipadic(self):
        matcher = Matcher(all_fstdata())
        sys_dic = SystemDictionary.instance()
        self.assertEqual(7, len(sys_dic.lookup('形態素'.encode('utf-8'), matcher)))
        self.assertEqual(1, sys_dic.get_trans_cost(0, 1))
        self.assertEqual({'HIRAGANA': []}, sys_dic.get_char_categories('は'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories('ハ'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories('ﾊ'))
        self.assertEqual({'KANJI': []}, sys_dic.get_char_categories('葉'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories('C'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories('Ｃ'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories('#'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories('＃'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories('5'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories('５'))
        self.assertEqual({'KANJI': [], 'KANJINUMERIC': ['KANJI']}, sys_dic.get_char_categories('五'))
        self.assertEqual({'GREEK': []}, sys_dic.get_char_categories('Γ'))
        self.assertEqual({'CYRILLIC': []}, sys_dic.get_char_categories('Б'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories('𠮷'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories('한'))
        self.assertTrue(sys_dic.unknown_invoked_always('ALPHA'))
        self.assertFalse(sys_dic.unknown_invoked_always('KANJI'))
        self.assertTrue(sys_dic.unknown_grouping('NUMERIC'))
        self.assertFalse(sys_dic.unknown_grouping('KANJI'))
        self.assertEqual(2, sys_dic.unknown_length('HIRAGANA'))

    def test_mmap_dictionary_ipadic(self):
        matcher = Matcher(all_fstdata())
        sys_dic = MMapSystemDictionary.instance()
        self.assertEqual(7, len(sys_dic.lookup('形態素'.encode('utf-8'), matcher)))
        self.assertEqual(1, sys_dic.get_trans_cost(0, 1))
        self.assertEqual({'HIRAGANA': []}, sys_dic.get_char_categories('は'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories('ハ'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories('ﾊ'))
        self.assertEqual({'KANJI': []}, sys_dic.get_char_categories('葉'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories('C'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories('Ｃ'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories('#'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories('＃'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories('5'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories('５'))
        self.assertEqual({'KANJI': [], 'KANJINUMERIC': ['KANJI']}, sys_dic.get_char_categories('五'))
        self.assertEqual({'GREEK': []}, sys_dic.get_char_categories('Γ'))
        self.assertEqual({'CYRILLIC': []}, sys_dic.get_char_categories('Б'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories('𠮷'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories('한'))
        self.assertTrue(sys_dic.unknown_invoked_always('ALPHA'))
        self.assertFalse(sys_dic.unknown_invoked_always('KANJI'))
        self.assertTrue(sys_dic.unknown_grouping('NUMERIC'))
        self.assertFalse(sys_dic.unknown_grouping('KANJI'))
        self.assertEqual(2, sys_dic.unknown_length('HIRAGANA'))

    def test_property_types(self):
        matcher = Matcher(all_fstdata())
        sys_dic = SystemDictionary.instance()
        # entry in the system dictionary
        entry = sys_dic.lookup('すもも'.encode('utf8'), matcher)[0]
        self.assertTrue(type(entry[1]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[2]) is int)
        self.assertTrue(type(entry[3]) is int)
        self.assertTrue(type(entry[4]) is int)

        entry_extra = sys_dic.lookup_extra(entry[0])
        self.assertTrue(type(entry_extra[0]) is str)
        self.assertTrue(type(entry_extra[1]) is str)
        self.assertTrue(type(entry_extra[2]) is str)
        self.assertTrue(type(entry_extra[3]) is str)
        self.assertTrue(type(entry_extra[4]) is str)
        self.assertTrue(type(entry_extra[5]) is str)

        # unknown entry
        entry = sys_dic.unknowns.get(u'HIRAGANA')[0]
        self.assertTrue(type(entry[3]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[1]) is int)
        self.assertTrue(type(entry[2]) is int)

        # mmap dict etnry
        matcher = Matcher(all_fstdata())
        mmap_dic = MMapSystemDictionary.instance()
        entry = mmap_dic.lookup(u'すもも'.encode('utf8'), matcher)[0]
        self.assertTrue(type(entry[1]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[2]) is int)
        self.assertTrue(type(entry[3]) is int)
        self.assertTrue(type(entry[4]) is int)

        entry_extra = mmap_dic.lookup_extra(entry[0])
        self.assertTrue(type(entry_extra[0]) is str)
        self.assertTrue(type(entry_extra[1]) is str)
        self.assertTrue(type(entry_extra[2]) is str)
        self.assertTrue(type(entry_extra[3]) is str)
        self.assertTrue(type(entry_extra[4]) is str)
        self.assertTrue(type(entry_extra[5]) is str)

    def test_dictionary_cache(self):
        matcher = Matcher(all_fstdata())
        sys_dic = SystemDictionary.instance()
        self.assertEqual(11, len(sys_dic.lookup('小書き'.encode('utf8'), matcher)))
        self.assertEqual(11, len(sys_dic.lookup('小書き'.encode('utf8'), matcher)))
        self.assertEqual(11, len(sys_dic.lookup('小書きにしました'.encode('utf8'), matcher)))

        self.assertEqual(10, len(sys_dic.lookup('みんなと'.encode('utf8'), matcher)))
        self.assertEqual(10, len(sys_dic.lookup('みんなと'.encode('utf8'), matcher)))

        self.assertEqual(2, len(sys_dic.lookup('叩く'.encode('utf8'), matcher)))
        self.assertEqual(2, len(sys_dic.lookup('叩く'.encode('utf8'), matcher)))
