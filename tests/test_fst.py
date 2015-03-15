import os, sys

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
import fst
from fst import Matcher

import unittest


class TestFST(unittest.TestCase):

    def test_create_minimum_transducer1(self):
        dict_file = '/tmp/dict1.dat'
        inputs = [
            ('apr'.encode('utf8'), '30'.encode('utf8')),
            ('aug'.encode('utf8'), '31'.encode('utf8')),
            ('dec'.encode('utf8'), '31'.encode('utf8')),
            ('feb'.encode('utf8'), '28'.encode('utf8')),
            ('feb'.encode('utf8'), '29'.encode('utf8')),
            ('jan'.encode('utf8'), '31'.encode('utf8')),
            ('jul'.encode('utf8'), '31'.encode('utf8')),
            ('jun'.encode('utf8'), '30'.encode('utf8')),
            ('may'.encode('utf8'), '31'.encode('utf8'))
        ]
        dictionary = fst.create_minimum_transducer(inputs)
        data = fst.compileFST(dictionary)

        m = Matcher(data)
        # accepted strings
        self.assertEqual((True, set(['30'.encode('utf-8')])), m.run('apr'.encode('utf8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), m.run('aug'.encode('utf8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), m.run('dec'.encode('utf8')))
        self.assertEqual((True, set(['28'.encode('utf-8'), '29'.encode('utf8')])), m.run('feb'.encode('utf8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), m.run('jan'.encode('utf8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), m.run('jul'.encode('utf8')))
        self.assertEqual((True, set(['30'.encode('utf-8')])), m.run('jun'.encode('utf8')))
        self.assertEqual((True, set(['31'.encode('utf-8')])), m.run('may'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('mar'))

    def test_create_minimum_transducer2(self):
        dict_file = '/tmp/dict2.dat'
        inputs = [
            ('さくら'.encode('utf8'), '10'.encode('utf8')),
            ('さくらんぼ'.encode('utf8'), '11'.encode('utf8')),
            ('すもも'.encode('utf8'), '20'.encode('utf8')),
            ('なし'.encode('utf8'), '10'.encode('utf8')),
            ('もも'.encode('utf8'), '20'.encode('utf8')),
        ]
        dictionary = fst.create_minimum_transducer(inputs)
        data = fst.compileFST(dictionary)
        fst.save(dict_file, data)
        self.assertGreater(os.path.getsize(dict_file), 0)

        m = Matcher(file=dict_file)
        # accepted strings
        self.assertEqual((True, set(['10'.encode('utf8')])), m.run('さくら'.encode('utf8')))
        self.assertEqual((True, set(['10'.encode('utf8'), '11'.encode('utf8')])), m.run('さくらんぼ'.encode('utf8')))
        self.assertEqual((True, set(['20'.encode('utf8')])), m.run('すもも'.encode('utf8')))
        self.assertEqual((True, set(['10'.encode('utf8')])), m.run('なし'.encode('utf8')))
        self.assertEqual((True, set(['20'.encode('utf8')])), m.run('もも'.encode('utf8')))
        # not accepted string
        self.assertEqual((False, set()), m.run('りんご'.encode('utf8')))


if __name__ == '__main__':
    unittest.main()

