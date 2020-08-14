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
from struct import pack
import unittest
from janome.fst import Matcher
from janome import fst

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class TestFST(unittest.TestCase):

    def test_create_minimum_transducer1(self):
        inputs1 = [
            ('apr'.encode('utf8'), pack('I', 30)),
            ('aug'.encode('utf8'), pack('I', 31)),
            ('dec'.encode('utf8'), pack('I', 31)),
            ('feb'.encode('utf8'), pack('I', 28))
        ]
        inputs2 = [
            ('feb'.encode('utf8'), pack('I', 29)),
            ('jan'.encode('utf8'), pack('I', 31)),
            ('jul'.encode('utf8'), pack('I', 31)),
            ('jun'.encode('utf8'), pack('I', 30)),
            ('may'.encode('utf8'), pack('I', 31))
        ]
        processed, dictionary1 = fst.create_minimum_transducer(inputs1)
        processed, dictionary2 = fst.create_minimum_transducer(inputs2)
        data = [fst.compileFST(dictionary1), fst.compileFST(dictionary2)]

        m = Matcher(data)
        # accepted strings
        self.assertEqual((True, set([pack('I', 30)])), m.run('apr'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('aug'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('dec'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 28), pack('I', 29)])), m.run('feb'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('jan'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('jul'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 30)])), m.run('jun'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('may'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('mar'))

    def test_create_minimum_transducer2(self):
        inputs1 = [
            ('さくら'.encode('utf8'), '白'.encode('utf8')),
            ('さくらんぼ'.encode('utf8'), '赤'.encode('utf8')),
            ('すもも'.encode('utf8'), '赤'.encode('utf8'))
        ]
        inputs2 = [
            ('なし'.encode('utf8'), '茶'.encode('utf8')),
            ('もも'.encode('utf8'), '桃'.encode('utf8'))
        ]

        processed, dictionary1 = fst.create_minimum_transducer(inputs1)
        processed, dictionary2 = fst.create_minimum_transducer(inputs2)
        data = [fst.compileFST(dictionary1), fst.compileFST(dictionary2)]

        m = Matcher(data)
        # accepted strings
        self.assertEqual((True, set(['白'.encode('utf8')])), m.run('さくら'.encode('utf8')))
        self.assertEqual((True, set(['白'.encode('utf8'), '赤'.encode('utf8')])), m.run('さくらんぼ'.encode('utf8')))
        self.assertEqual((True, set(['白'.encode('utf8')])), m.run('さくらさく'.encode('utf8')))
        self.assertEqual((True, set(['赤'.encode('utf8')])), m.run('すもも'.encode('utf8')))
        self.assertEqual((True, set(['茶'.encode('utf8')])), m.run('なし'.encode('utf8')))
        self.assertEqual((True, set(['桃'.encode('utf8')])), m.run('もも'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('みかん'.encode('utf8')))

    def test_common_prefix_match(self):
        inputs = [
            ('す'.encode('utf8'), pack('I', 1)),
            ('すも'.encode('utf8'), pack('I', 2)),
            ('すもも'.encode('utf8'), pack('I', 3))
        ]
        processed, dictionary = fst.create_minimum_transducer(inputs)
        data = [fst.compileFST(dictionary)]

        m = Matcher(data)
        # matches 'す', 'すも', 'すもも'
        expected_outputs = set([pack('I', 1), pack('I', 2), pack('I', 3)])
        self.assertEqual((True, expected_outputs), m.run('すもも'.encode('utf8'), True))

    def test_perfect_match(self):
        inputs = [
            ('す'.encode('utf8'), pack('I', 1)),
            ('すも'.encode('utf8'), pack('I', 2)),
            ('すもも'.encode('utf8'), pack('I', 3))
        ]
        processed, dictionary = fst.create_minimum_transducer(inputs)
        data = [fst.compileFST(dictionary)]

        m = Matcher(data)
        # matches 'すもも'
        expected_outputs = set([pack('I', 3)])
        self.assertEqual((True, expected_outputs), m.run('すもも'.encode('utf8'), False))

    def test_matcher_cache(self):
        inputs = [
            ('す'.encode('utf8'), pack('I', 1)),
            ('すも'.encode('utf8'), pack('I', 2)),
            ('すもも'.encode('utf8'), pack('I', 3))
        ]
        processed, dictionary = fst.create_minimum_transducer(inputs)
        data = [fst.compileFST(dictionary)]

        m = Matcher(data)
        # matches 'す', 'すも', 'すもも'
        self.assertEqual(
            (True, set([pack('I', 1), pack('I', 2), pack('I', 3)])),
            m.run('すもも'.encode('utf8'), True))
        self.assertEqual(
            (True, set([pack('I', 1), pack('I', 2)])),
            m.run('すもうとり'.encode('utf8'), True))
        self.assertEqual(
            (True, set([pack('I', 1), pack('I', 2), pack('I', 3)])),
            m.run('すもも'.encode('utf8'), True))
        self.assertEqual(
            (True, set([pack('I', 1), pack('I', 2), pack('I', 3)])),
            m.run('すもももももももものうち'.encode('utf8'), True))
        self.assertEqual(
            (True, set([pack('I', 1)])),
            m.run('す'.encode('utf8'), True))


if __name__ == '__main__':
    unittest.main()
