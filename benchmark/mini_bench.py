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

setup = """
from janome.tokenizer import Tokenizer
t = Tokenizer()
# janome (蛇の目) は, Pure Python で書かれた, 辞書内包の形態素解析器です.
s = u'janome (\u86c7\u306e\u76ee) \u306f, Pure Python \u3067\u66f8\u304b\u308c\u305f, \u8f9e\u66f8\u5185\u5305\u306e\u5f62\u614b\u7d20\u89e3\u6790\u5668\u3067\u3059.'
"""


if __name__ == '__main__':
    import timeit, sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print("** execute timeit() with number=%d **" % n)
    res = timeit.repeat(stmt='t.tokenize(s)', setup=setup, repeat=5, number=n)
    for i, x in enumerate(res):
        print("repeat %d: %f" % (i, x))
