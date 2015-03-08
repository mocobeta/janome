import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
import fst
from fst import VM

import unittest


class TestFST(unittest.TestCase):

    def test_create_minimum_transducer1(self):
        inputs = [
            ('apr'.encode('utf-8'), '30'.encode('utf-8')),
            ('aug'.encode('utf-8'), '31'.encode('utf-8')),
            ('dec'.encode('utf-8'), '31'.encode('utf-8')),
            ('feb'.encode('utf-8'), '28'.encode('utf-8')),
            ('feb'.encode('utf-8'), '29'.encode('utf-8')),
            ('jan'.encode('utf-8'), '31'.encode('utf-8')),
            ('jul'.encode('utf-8'), '31'.encode('utf-8')),
            ('jun'.encode('utf-8'), '30'.encode('utf-8')),
            ('may'.encode('utf-8'), '31'.encode('utf-8'))
        ]
        dict = fst.create_minimum_transducer(inputs)
        vm = VM(fst.fst2instructions(dict))
        # accepted strings
        self.assertEqual((True, set(['30'.encode('utf-8')])), vm.run('apr'.encode('utf-8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), vm.run('aug'.encode('utf-8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), vm.run('dec'.encode('utf-8')))
        self.assertEqual((True, set(['28'.encode('utf-8'), '29'.encode('utf-8')])), vm.run('feb'.encode('utf-8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), vm.run('jan'.encode('utf-8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), vm.run('jul'.encode('utf-8')))
        self.assertEqual((True, set(['30'.encode('utf-8')])), vm.run('jun'.encode('utf-8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), vm.run('may'.encode('utf-8')))
        # not accepted string
        self.assertEqual((False, set()), vm.run('mar'))

    def test_create_minimum_transducer2(self):
        inputs = [
            ('さくら'.encode('utf-8'), '10'.encode('utf-8')),
            ('さくらんぼ'.encode('utf-8'), '11'.encode('utf-8')),
            ('すもも'.encode('utf-8'), '20'.encode('utf-8')),
            ('なし'.encode('utf-8'), '10'.encode('utf-8')),
            ('もも'.encode('utf-8'), '20'.encode('utf-8')),
        ]
        dict = fst.create_minimum_transducer(inputs)
        vm = VM(fst.fst2instructions(dict))
        # accepted strings
        self.assertEqual((True, set(['10'.encode('utf-8')])), vm.run('さくら'.encode('utf-8')))
        self.assertEqual((True, set(['10'.encode('utf-8'), '11'.encode('utf-8')])), vm.run('さくらんぼ'.encode('utf-8')))
        self.assertEqual((True, set(['20'.encode('utf-8')])), vm.run('すもも'.encode('utf-8')))
        self.assertEqual((True, set(['10'.encode('utf-8')])), vm.run('なし'.encode('utf-8')))
        self.assertEqual((True, set(['20'.encode('utf-8')])), vm.run('もも'.encode('utf-8')))
        # not accepted string
        self.assertEqual((False, set()), vm.run('りんご'.encode('utf-8')))


if __name__ == '__main__':
    unittest.main()

