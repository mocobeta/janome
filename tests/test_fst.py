import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from janome import fst
from janome.fst import Matcher

import unittest
from struct import pack
import janome.dic


class TestFST(unittest.TestCase):

    def test_create_minimum_transducer1(self):
        inputs = [
            ('apr'.encode('utf8'), pack('I', 30)),
            ('aug'.encode('utf8'), pack('I', 32)),
            ('dec'.encode('utf8'), pack('I', 31)),
            ('feb'.encode('utf8'), pack('I', 28)),
            ('feb'.encode('utf8'), pack('I', 29)),
            ('jan'.encode('utf8'), pack('I', 31)),
            ('jul'.encode('utf8'), pack('I', 31)),
            ('jun'.encode('utf8'), pack('I', 30)),
            ('may'.encode('utf8'), pack('I', 31))
        ]
        dictionary = fst.create_minimum_transducer(inputs)
        data = fst.compileFST(dictionary)

        m = Matcher(data)
        # accepted strings
        self.assertEqual((True, set([pack('I', 30)])), m.run('apr'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 32)])), m.run('aug'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('dec'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 28), pack('I', 29)])), m.run('feb'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('jan'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('jul'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 30)])), m.run('jun'.encode('utf8')))
        self.assertEqual((True, set([pack('I', 31)])), m.run('may'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('mar'))

    def test_create_minimum_transducer2(self):
        inputs = [
            ('さくら'.encode('utf8'), '白'.encode('utf8')),
            ('さくらんぼ'.encode('utf8'), '赤'.encode('utf8')),
            ('すもも'.encode('utf8'), '赤'.encode('utf8')),
            ('なし'.encode('utf8'), '茶'.encode('utf8')),
            ('もも'.encode('utf8'), '桃'.encode('utf8')),
        ]
        dictionary = fst.create_minimum_transducer(inputs)
        data = fst.compileFST(dictionary)

        m = Matcher(data)
        # accepted strings
        self.assertEqual((True, set(['白'.encode('utf8')])), m.run('さくら'.encode('utf8')))
        self.assertEqual((True, set(['白'.encode('utf8'), '赤'.encode('utf8')])), m.run('さくらんぼ'.encode('utf8')))
        self.assertEqual((True, set(['赤'.encode('utf8')])), m.run('すもも'.encode('utf8')))
        self.assertEqual((True, set(['茶'.encode('utf8')])), m.run('なし'.encode('utf8')))
        self.assertEqual((True, set(['桃'.encode('utf8')])), m.run('もも'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('みかん'.encode('utf8')))


if __name__ == '__main__':
    unittest.main()

