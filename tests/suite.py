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

import unittest
from test_fst import TestFST
from test_dic import TestDictionary
from test_lattice import TestLattice
from test_tokenizer import TestTokenizer
from test_charfilter import TestCharFilter
from test_tokenfilter import TestTokenFilter
from test_analyzer import TestAnalyzer


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFST))
    suite.addTests(unittest.makeSuite(TestDictionary))
    suite.addTests(unittest.makeSuite(TestLattice))
    suite.addTests(unittest.makeSuite(TestTokenizer))
    suite.addTests(unittest.makeSuite(TestCharFilter))
    suite.addTests(unittest.makeSuite(TestTokenFilter))
    suite.addTests(unittest.makeSuite(TestAnalyzer))
    return suite


mySuite = suite()
runner = unittest.TextTestRunner()
runner.run(mySuite)
