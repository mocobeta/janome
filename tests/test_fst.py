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
            ('apr', '30'),
            ('aug', '31'),
            ('dec', '31'),
            ('feb', '28'),
            ('feb', '29'),
            ('jan', '31'),
            ('jul', '31'),
            ('jun', '30'),
            ('may', '31')
        ]
        dict = fst.create_minimum_transducer(inputs)
        vm = VM(fst.fst2instructions(dict))
        # accepted strings
        self.assertEqual((True, set(['30'])), vm.run('apr'))
        self.assertEqual((True, set(['31'])), vm.run('aug'))
        self.assertEqual((True, set(['31'])), vm.run('dec'))
        self.assertEqual((True, set(['28', '29'])), vm.run('feb'))
        self.assertEqual((True, set(['31'])), vm.run('jan'))
        self.assertEqual((True, set(['31'])), vm.run('jul'))
        self.assertEqual((True, set(['30'])), vm.run('jun'))
        self.assertEqual((True, set(['31'])), vm.run('may'))
        # not accepted string
        self.assertEqual((False, set()), vm.run('mar'))

    def test_create_minimum_transducer2(self):
        inputs = [
            ('さくら', '10'),
            ('さくらんぼ', '11'),
            ('すもも', '20'),
            ('なし', '10'),
            ('もも', '20'),
        ]
        dict = fst.create_minimum_transducer(inputs)
        vm = VM(fst.fst2instructions(dict))
        # accepted strings
        self.assertEqual((True, set(['10'])), vm.run('さくら'))
        self.assertEqual((True, set(['10', '11'])), vm.run('さくらんぼ'))
        self.assertEqual((True, set(['20'])), vm.run('すもも'))
        self.assertEqual((True, set(['10'])), vm.run('なし'))
        self.assertEqual((True, set(['20'])), vm.run('もも'))
        # not accepted string
        self.assertEqual((False, set()), vm.run('りんご'))


if __name__ == '__main__':
    unittest.main()

