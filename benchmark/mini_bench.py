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

import timeit
import sys

mmap = True
n = 10
if len(sys.argv) > 1 and sys.argv[1] == '-nommap':
    mmap = False
    if len(sys.argv) > 2:
        n = int(sys.argv[2])
elif len(sys.argv) > 1:
    n = int(sys.argv[1])

print("** Setup **")
print(f'mmap={mmap}, loop={n}')
print("** initialize Tokenizer object **")
print(timeit.timeit(stmt=f'Tokenizer(mmap={mmap})', setup='from janome.tokenizer import Tokenizer', number=1))

print("** execute tokenize() %d times **" % n)
setup = f"""
from janome.tokenizer import Tokenizer
t = Tokenizer(mmap={mmap})
with open('text_lemon.txt') as f:
    lines = f.readlines()
"""


def test(t, lines):
    for line in lines:
        list(t.tokenize(line))


res = timeit.repeat(stmt='test(t, lines)', setup=setup, repeat=5, number=n, globals=globals())
for i, x in enumerate(res):
    print("repeat %d: %f" % (i, x))
