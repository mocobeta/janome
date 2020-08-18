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

import sys
import timeit

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10

print("** initialize Tokenizer object **")
print(timeit.timeit(stmt='Tokenizer(mmap=True)', setup='from janome.tokenizer import Tokenizer', number=1))

print("** execute tokenize() %d times **" % n)
setup = """
from janome.tokenizer import Tokenizer
t = Tokenizer(mmap=True)
with open('text_lemon.txt') as f:
    s = f.read()
"""
res = timeit.repeat(stmt='list(t.tokenize(s))', setup=setup, repeat=5, number=n)
for i, x in enumerate(res):
    print("repeat %d: %f" % (i, x))
