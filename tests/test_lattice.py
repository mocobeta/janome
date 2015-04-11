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

from janome.lattice import *
from sysdic import SYS_DIC
import unittest


class TestLattice(unittest.TestCase):
    def test_initialize_lattice(self):
        lattice = Lattice(5, SYS_DIC)
        self.assertEqual(7, len(lattice.snodes))
        self.assertTrue(isinstance(lattice.snodes[0][0], BOS))
        self.assertEqual(8, len(lattice.enodes))
        self.assertTrue(isinstance(lattice.enodes[1][0], BOS))

    def test_add_forward_end(self):
        s = u'すもも'
        lattice = Lattice(len(s), SYS_DIC)
        entries = SYS_DIC.lookup(s)
        for entry in entries:
            lattice.add(Node(entry))
        self.assertEqual(9, len(lattice.snodes[1]))
        self.assertEqual(7, len(lattice.enodes[2]))
        self.assertEqual(1, len(lattice.enodes[3]))
        self.assertEqual(1, len(lattice.enodes[4]))

        self.assertEqual(1, lattice.forward())

        entries = SYS_DIC.lookup(s[1:])
        for entry in entries:
            lattice.add(Node(entry))
        self.assertEqual(4, len(lattice.snodes[2]))
        self.assertEqual(3, len(lattice.enodes[3]))
        self.assertEqual(3, len(lattice.enodes[4]))

        self.assertEqual(1, lattice.forward())

        entries = SYS_DIC.lookup(s[2:])
        for entry in entries:
            lattice.add(Node(entry))
        self.assertEqual(2, len(lattice.snodes[3]))
        self.assertEqual(5, len(lattice.enodes[4]))

        self.assertEqual(1, lattice.forward())

        lattice.end()
        self.assertTrue(isinstance(lattice.snodes[4][0], EOS))
        self.assertTrue(isinstance(lattice.enodes[5][0], EOS))

    def test_backward(self):
        s = u'すもももももももものうち'
        lattice = Lattice(len(s), SYS_DIC)
        pos = 0
        while pos < len(s):
            entries = SYS_DIC.lookup(s[pos:])
            for e in entries:
                lattice.add(Node(e))
            pos += lattice.forward()
        lattice.end()
        min_cost_path = lattice.backward()
        self.assertEqual(9, len(min_cost_path))
        self.assertTrue(isinstance(min_cost_path[0], BOS))
        self.assertEqual(u'すもも', min_cost_path[1].surface)
        self.assertEqual(u'も', min_cost_path[2].surface)
        self.assertEqual(u'もも', min_cost_path[3].surface)
        self.assertEqual(u'も', min_cost_path[4].surface)
        self.assertEqual(u'もも', min_cost_path[5].surface)
        self.assertEqual(u'の', min_cost_path[6].surface)
        self.assertEqual(u'うち', min_cost_path[7].surface)
        self.assertTrue(isinstance(min_cost_path[8], EOS))


if __name__ == '__main__':
    unittest.main()

