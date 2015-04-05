# -*- coding: utf-8 -*-

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
        s = 'すもも'
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
        s = 'すもももももももものうち'
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
        self.assertEqual('すもも', min_cost_path[1].surface)
        self.assertEqual('も', min_cost_path[2].surface)
        self.assertEqual('もも', min_cost_path[3].surface)
        self.assertEqual('も', min_cost_path[4].surface)
        self.assertEqual('もも', min_cost_path[5].surface)
        self.assertEqual('の', min_cost_path[6].surface)
        self.assertEqual('うち', min_cost_path[7].surface)
        self.assertTrue(isinstance(min_cost_path[8], EOS))


if __name__ == '__main__':
    unittest.main()

