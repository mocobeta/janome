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
import csv
import io
import sys
import tempfile
import unittest
from janome.sysdic import connections
from janome.dic import UserDictionary, CompiledUserDictionary, FILE_USER_FST_DATA, FILE_USER_ENTRIES_DATA
from janome.fst import Matcher
from janome.progress import SimpleProgressIndicator, logger as p_logger

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestUserDictionary(unittest.TestCase):
    def test_quoted_csv_entries(self):
        for surface in ("plain", "3,3-Dimethylpentane", 'say "hello"', 'quoted, "word"'):
            for dict_type in ("ipadic", "simpledic"):
                with self.subTest(surface=surface, dict_type=dict_type):
                    if dict_type == "ipadic":
                        fields = [
                            surface,
                            0,
                            0,
                            -100000,
                            "noun",
                            "*",
                            "*",
                            "*",
                            "*",
                            "*",
                            surface,
                            "READING",
                            "READING",
                        ]
                    else:
                        fields = [surface, "noun", "READING"]
                    stream = io.StringIO()
                    csv.writer(stream).writerow(fields)
                    parse = getattr(UserDictionary, "line_to_entry_" + dict_type)
                    entry = parse(stream.getvalue().rstrip("\r\n"))
                    self.assertEqual(entry[0], surface)
                    self.assertEqual(entry[7], surface)
                    self.assertEqual(entry[8:], ("READING", "READING"))

    def test_quoted_csv_dictionary_lookup(self):
        surface = "3,3-Dimethylpentane"
        for dict_type in ("ipadic", "simpledic"):
            with self.subTest(dict_type=dict_type), tempfile.TemporaryDirectory() as directory:
                path = os.path.join(directory, "dictionary.csv")
                if dict_type == "ipadic":
                    fields = [surface, 0, 0, -100000, "noun", "*", "*", "*", "*", "*", surface, "READING", "READING"]
                else:
                    fields = [surface, "noun", "READING"]
                with open(path, "w", encoding="utf8", newline="") as stream:
                    csv.writer(stream).writerow(fields)
                dictionary = UserDictionary(path, "utf8", dict_type, connections)
                matches = dictionary.lookup(surface.encode("utf8"))
                self.assertEqual(len(matches), 1)
                self.assertEqual(dictionary.entries[0][0], surface)
                self.assertEqual(dictionary.entries[0][8:], ("READING", "READING"))

    def test_property_types(self):
        user_dic = UserDictionary(
            user_dict=os.path.join(parent_dir, "tests/user_ipadic.csv"),
            enc="utf8",
            type="ipadic",
            connections=connections,
        )
        entry = user_dic.lookup("東京スカイツリー".encode("utf8"))[0]
        self.assertTrue(type(entry[1]) is str)
        self.assertTrue(type(entry[0]) is int)
        self.assertTrue(type(entry[2]) is int)
        self.assertTrue(type(entry[3]) is int)
        self.assertTrue(type(entry[4]) is int)

    def test_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(
            user_dict=os.path.join(parent_dir, "tests/user_ipadic.csv"),
            enc="utf8",
            type="ipadic",
            connections=connections,
        )
        self.assertEqual(1, len(user_dic.lookup("東京スカイツリー".encode("utf8"))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, "tests/userdic")
        user_dic.save(to_dir=os.path.join(parent_dir, "tests/userdic"))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup("とうきょうスカイツリー駅".encode("utf8"))))

    def test_user_dictionary_with_progress(self):
        # create user dictionary from csv with progress indicator
        progress_indicator = SimpleProgressIndicator(update_frequency=1.0)
        with self.assertLogs(logger=p_logger) as cm:
            # create user dictionary
            large_user_dic = UserDictionary(
                user_dict=os.path.join(parent_dir, "tests/user_ipadic.csv"),
                enc="utf8",
                type="ipadic",
                connections=connections,
                progress_handler=progress_indicator,
            )

            entry_count = len(large_user_dic.entries)
            # output for each entry and for complete (entry_count + 1)
            self.assertEqual((entry_count + 1) * 2, len(cm.output))
            # reset after complete
            self.assertIsNone(progress_indicator.value)

            for i in range(0, (entry_count + 1) * 2):
                if i < entry_count:
                    # progress for reading csv
                    self.assertIn("Reading user dictionary from CSV", cm.output[i])
                    self.assertIn(f"{i + 1}/{entry_count}", cm.output[i])
                elif i == entry_count:
                    # on compete loading csv
                    self.assertIn(f"{entry_count}/{entry_count}", cm.output[i])
                elif i < entry_count * 2 + 1:
                    # progress for create_minimum_transducer
                    self.assertIn("Running create_minimum_transducer", cm.output[i])
                    self.assertIn(f"{i - entry_count}/{entry_count}", cm.output[i])
                elif i == entry_count * 2 + 1:
                    # on compete loading create_minimum_transducer
                    self.assertIn(f"{entry_count}/{entry_count}", cm.output[i])

        # same result as without progress indicator
        self.assertEqual(1, len(large_user_dic.lookup("東京スカイツリー".encode("utf8"))))

    def test_simplified_user_dictionary(self):
        # create user dictionary from csv
        user_dic = UserDictionary(
            user_dict=os.path.join(parent_dir, "tests/user_simpledic.csv"),
            enc="utf8",
            type="simpledic",
            connections=connections,
        )
        self.assertEqual(1, len(user_dic.lookup("東京スカイツリー".encode("utf8"))))

        # save compiled dictionary
        dic_dir = os.path.join(parent_dir, "tests/userdic_simple")
        user_dic.save(to_dir=os.path.join(parent_dir, "tests/userdic_simple"))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_FST_DATA)))
        self.assertTrue(os.path.exists(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))

        # load compiled dictionary
        compiled_user_dic = CompiledUserDictionary(dic_dir, connections=connections)
        self.assertEqual(1, len(compiled_user_dic.lookup("とうきょうスカイツリー駅".encode("utf8"))))

    def test_simplified_user_dictionary_with_progress(self):
        # create simplified user dictionary from csv with progress indicator
        progress_indicator = SimpleProgressIndicator(update_frequency=1.0)
        with self.assertLogs(logger=p_logger) as cm:
            # create user dictionary
            large_user_dic = UserDictionary(
                user_dict=os.path.join(parent_dir, "tests/user_simpledic.csv"),
                enc="utf8",
                type="simpledic",
                connections=connections,
                progress_handler=progress_indicator,
            )

            entry_count = len(large_user_dic.entries)
            # output for each entry and for complete (entry_count + 1)
            self.assertEqual((entry_count + 1) * 2, len(cm.output))
            # value is reset after complete
            self.assertIsNone(progress_indicator.value)

            for i in range(0, (entry_count + 1) * 2):
                if i < entry_count:
                    # progress for reading csv
                    self.assertIn("Reading user dictionary from CSV", cm.output[i])
                    self.assertIn(f"{i + 1}/{entry_count}", cm.output[i])
                elif i == entry_count:
                    # on compete loading csv
                    self.assertIn(f"{entry_count}/{entry_count}", cm.output[i])
                elif i < entry_count * 2 + 1:
                    # progress for create_minimum_transducer
                    self.assertIn("Running create_minimum_transducer", cm.output[i])
                    self.assertIn(f"{i - entry_count}/{entry_count}", cm.output[i])
                elif i == entry_count * 2 + 1:
                    # on compete loading create_minimum_transducer
                    self.assertIn(f"{entry_count}/{entry_count}", cm.output[i])

        # same result as without progress indicator
        self.assertEqual(1, len(large_user_dic.lookup("東京スカイツリー".encode("utf8"))))


if __name__ == "__main__":
    unittest.main()
