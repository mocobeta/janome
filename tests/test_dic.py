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

import janome.dic
from janome.dic import *
from janome.sysdic import all_fstdata, entries, mmap_entries, connections, chardef, unknowns

import unittest


class TestDictionary(unittest.TestCase):
    def test_system_dictionary_ipadic(self):
        sys_dic = SystemDictionary(all_fstdata(), entries(), connections, chardef.DATA, unknowns.DATA)
        self.assertEqual(7, len(sys_dic.lookup(u'形態素'.encode('utf-8'))))
        self.assertEqual(1, sys_dic.get_trans_cost(0, 1))
        self.assertEqual({'HIRAGANA': []}, sys_dic.get_char_categories(u'は'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories(u'ハ'))
        self.assertEqual({'KATAKANA': []}, sys_dic.get_char_categories(u'ﾊ'))
        self.assertEqual({'KANJI': []}, sys_dic.get_char_categories(u'葉'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories(u'C'))
        self.assertEqual({'ALPHA': []}, sys_dic.get_char_categories(u'Ｃ'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories(u'#'))
        self.assertEqual({'SYMBOL': []}, sys_dic.get_char_categories(u'＃'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories(u'5'))
        self.assertEqual({'NUMERIC': []}, sys_dic.get_char_categories(u'５'))
        self.assertEqual({'KANJI': [], 'KANJINUMERIC': ['KANJI']}, sys_dic.get_char_categories(u'五'))
        self.assertEqual({'GREEK': []}, sys_dic.get_char_categories(u'Γ'))
        self.assertEqual({'CYRILLIC': []}, sys_dic.get_char_categories(u'Б'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories(u'𠮷'))
        self.assertEqual({'DEFAULT': []}, sys_dic.get_char_categories(u'한'))
        self.assertTrue(sys_dic.unknown_invoked_always('ALPHA'))
        self.assertFalse(sys_dic.unknown_invoked_always('KANJI'))
        self.assertTrue(sys_dic.unknown_grouping('NUMERIC'))
        self.assertFalse(sys_dic.unknown_grouping('KANJI'))
        self.assertEqual(2, sys_dic.unknown_length('HIRAGANA'))

    def test_property_types(self):
        sys_dic = SystemDictionary(all_fstdata(), entries(), connections, chardef.DATA, unknowns.DATA)
        # entry in the system dictionary
        entry = sys_dic.lookup(u'すもも'.encode('utf8'))[0]
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
        mmap_dic = MMapSystemDictionary(all_fstdata(), mmap_entries(), connections, chardef.DATA, unknowns.DATA)
        entry = mmap_dic.lookup(u'すもも'.encode('utf8'))[0]
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

        # entry in the user defined dictionary
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                                  enc='utf8', type='ipadic', connections=connections)
        entry = user_dic.lookup(u'東京スカイツリー'.encode('utf8'))[0]
        self.assertTrue(type(entry[1]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[2]) is int)
        self.assertTrue(type(entry[3]) is int)
        self.assertTrue(type(entry[4]) is int)

    def test_system_dictionary_cache(self):
        sys_dic = SystemDictionary(all_fstdata(), entries(), connections, chardef.DATA, unknowns.DATA)
        self.assertEqual(11, len(sys_dic.lookup(u'小書き'.encode('utf8'))))
        self.assertEqual(11, len(sys_dic.lookup(u'小書き'.encode('utf8'))))
        self.assertEqual(11, len(sys_dic.lookup(u'小書きにしました'.encode('utf8'))))

        self.assertEqual(10, len(sys_dic.lookup(u'みんなと'.encode('utf8'))))
        self.assertEqual(10, len(sys_dic.lookup(u'みんなと'.encode('utf8'))))

        self.assertEqual(2, len(sys_dic.lookup(u'叩く'.encode('utf8'))))
        self.assertEqual(2, len(sys_dic.lookup(u'叩く'.encode('utf8'))))

    def test_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                                  enc='utf8', type='ipadic', connections=connections)
        self.assertEqual(1, len(user_dic.lookup(u'東京スカイツリー'.encode('utf8'))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, 'tests/userdic')
        user_dic.save(to_dir=os.path.join(parent_dir, 'tests/userdic'))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup(u'とうきょうスカイツリー駅'.encode('utf8'))))

    def test_simplified_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_simpledic.csv'),
                                  enc='utf8', type='simpledic', connections=connections)
        self.assertEqual(1, len(user_dic.lookup(u'東京スカイツリー'.encode('utf8'))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, 'tests/userdic_simple')
        user_dic.save(to_dir=os.path.join(parent_dir, 'tests/userdic_simple'))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup(u'とうきょうスカイツリー駅'.encode('utf8'))))

if __name__ == '__main__':
    unittest.main()
