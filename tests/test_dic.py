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
from janome.sysdic import all_fstdata, entries, mmap_entries, connections, chardef, unknowns
from janome.dic import (
    SystemDictionary,
    MMapSystemDictionary,
    UserDictionary,
    CompiledUserDictionary,
    FILE_USER_FST_DATA,
    FILE_USER_ENTRIES_DATA
)
from janome.fst import Matcher
from janome.progress import SimpleProgressIndicator, logger as p_logger

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestDictionary(unittest.TestCase):
    def test_system_dictionary_ipadic(self):
        matcher = Matcher(all_fstdata())
        sys_dic = SystemDictionary(entries(), connections, chardef.DATA, unknowns.DATA)
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
        sys_dic = SystemDictionary(entries(), connections, chardef.DATA, unknowns.DATA)
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
        mmap_dic = MMapSystemDictionary(mmap_entries(), connections, chardef.DATA, unknowns.DATA)
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

        # entry in the user defined dictionary
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                                  enc='utf8', type='ipadic', connections=connections)
        entry = user_dic.lookup('東京スカイツリー'.encode('utf8'))[0]
        self.assertTrue(type(entry[1]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[2]) is int)
        self.assertTrue(type(entry[3]) is int)
        self.assertTrue(type(entry[4]) is int)

    def test_system_dictionary_cache(self):
        matcher = Matcher(all_fstdata())
        sys_dic = SystemDictionary(entries(), connections, chardef.DATA, unknowns.DATA)
        self.assertEqual(11, len(sys_dic.lookup('小書き'.encode('utf8'), matcher)))
        self.assertEqual(11, len(sys_dic.lookup('小書き'.encode('utf8'), matcher)))
        self.assertEqual(11, len(sys_dic.lookup('小書きにしました'.encode('utf8'), matcher)))

        self.assertEqual(10, len(sys_dic.lookup('みんなと'.encode('utf8'), matcher)))
        self.assertEqual(10, len(sys_dic.lookup('みんなと'.encode('utf8'), matcher)))

        self.assertEqual(2, len(sys_dic.lookup('叩く'.encode('utf8'), matcher)))
        self.assertEqual(2, len(sys_dic.lookup('叩く'.encode('utf8'), matcher)))

    def test_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                                  enc='utf8', type='ipadic', connections=connections)
        self.assertEqual(1, len(user_dic.lookup('東京スカイツリー'.encode('utf8'))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, 'tests/userdic')
        user_dic.save(to_dir=os.path.join(parent_dir, 'tests/userdic'))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup('とうきょうスカイツリー駅'.encode('utf8'))))

    def test_user_dictionary_with_progress(self):
        # create user dictionary from csv with progress indicator
        progress_indicator = SimpleProgressIndicator(update_frequency=1.0)
        with self.assertLogs(logger=p_logger) as cm:
            # create user dictionary
            large_user_dic = UserDictionary(
                user_dict=os.path.join(parent_dir, 'tests/user_ipadic.csv'),
                enc='utf8', type='ipadic', connections=connections,
                progress_handler=progress_indicator)

            entry_count = len(large_user_dic.entries)
            # output for each entry and for complete (entry_count + 1)
            self.assertEqual((entry_count + 1) * 2, len(cm.output))
            # reset after complete
            self.assertIsNone(progress_indicator.value)

            for i in range(0, (entry_count + 1) * 2):
                if i < entry_count:
                    # progress for reading csv
                    self.assertIn('Reading user dictionary from CSV', cm.output[i])
                    self.assertIn(f'{i + 1}/{entry_count}', cm.output[i])
                elif i == entry_count:
                    # on compete loading csv
                    self.assertIn(f'{entry_count}/{entry_count}', cm.output[i])
                elif i < entry_count * 2 + 1:
                    # progress for create_minimum_transducer
                    self.assertIn('Running create_minimum_transducer', cm.output[i])
                    self.assertIn(f'{i - entry_count}/{entry_count}', cm.output[i])
                elif i == entry_count * 2 + 1:
                    # on compete loading create_minimum_transducer
                    self.assertIn(f'{entry_count}/{entry_count}', cm.output[i])

        # same result as without progress indicator
        self.assertEqual(1, len(large_user_dic.lookup('東京スカイツリー'.encode('utf8'))))

    def test_simplified_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(user_dict=os.path.join(parent_dir, 'tests/user_simpledic.csv'),
                                  enc='utf8', type='simpledic', connections=connections)
        self.assertEqual(1, len(user_dic.lookup('東京スカイツリー'.encode('utf8'))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, 'tests/userdic_simple')
        user_dic.save(to_dir=os.path.join(parent_dir, 'tests/userdic_simple'))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup('とうきょうスカイツリー駅'.encode('utf8'))))

    def test_simplified_user_dictionary_with_progress(self):
        # create simplified user dictionary from csv with progress indicator
        progress_indicator = SimpleProgressIndicator(update_frequency=1.0)
        with self.assertLogs(logger=p_logger) as cm:
            # create user dictionary
            large_user_dic = UserDictionary(
                user_dict=os.path.join(parent_dir, 'tests/user_simpledic.csv'),
                enc='utf8', type='simpledic', connections=connections,
                progress_handler=progress_indicator)

            entry_count = len(large_user_dic.entries)
            # output for each entry and for complete (entry_count + 1)
            self.assertEqual((entry_count + 1) * 2, len(cm.output))
            # value is reset after complete
            self.assertIsNone(progress_indicator.value)

            for i in range(0, (entry_count + 1) * 2):
                if i < entry_count:
                    # progress for reading csv
                    self.assertIn('Reading user dictionary from CSV', cm.output[i])
                    self.assertIn(f'{i + 1}/{entry_count}', cm.output[i])
                elif i == entry_count:
                    # on compete loading csv
                    self.assertIn(f'{entry_count}/{entry_count}', cm.output[i])
                elif i < entry_count * 2 + 1:
                    # progress for create_minimum_transducer
                    self.assertIn('Running create_minimum_transducer', cm.output[i])
                    self.assertIn(f'{i - entry_count}/{entry_count}', cm.output[i])
                elif i == entry_count * 2 + 1:
                    # on compete loading create_minimum_transducer
                    self.assertIn(f'{entry_count}/{entry_count}', cm.output[i])

        # same result as without progress indicator
        self.assertEqual(1, len(large_user_dic.lookup('東京スカイツリー'.encode('utf8'))))


if __name__ == '__main__':
    unittest.main()
