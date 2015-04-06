# -*- coding: utf-8 -*-

import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.dic import *
from sysdic import fstdata, entries, connections, chardef, unknowns

import unittest


class TestDictionary(unittest.TestCase):
    def test_system_dictionary(self):
        sys_dic = SystemDictionary(fstdata.DATA, entries.DATA, connections.DATA, chardef.DATA, unknowns.DATA)
        self.assertEqual(7, len(sys_dic.lookup('形態素')))
        self.assertEqual(1, sys_dic.get_trans_cost('0', '1'))
        self.assertEqual(('HIRAGANA', []), sys_dic.char_category('あ'))
        self.assertTrue(sys_dic.unkown_invoked_always('ALPHA'))
        self.assertFalse(sys_dic.unkown_invoked_always('KANJI'))
        self.assertTrue(sys_dic.unknown_grouping('NUMERIC'))
        self.assertFalse(sys_dic.unknown_grouping('KANJI'))
        self.assertEqual(2, sys_dic.unknown_length('HIRAGANA'))

    def test_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                                  enc='utf8', type='ipadic', connections=connections)
        self.assertEqual(1, len(user_dic.lookup('東京スカイツリー')))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, 'tests/userdic')
        user_dic.save(to_dir=os.path.join(parent_dir, 'tests/userdic'))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup('とうきょうスカイツリー駅')))


if __name__ == '__main__':
    unittest.main()