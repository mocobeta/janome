# -*- coding: utf-8 -*-

# Copyright [2015] [moco_beta]
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
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.dic import Dictionary
from sysdic import fstdata, entries, connections, chardef, unknowns

SYS_DIC = Dictionary(fstdata.DATA, entries.DATA, connections.DATA, chardef.DATA, unknowns.DATA)

import struct
import logging
import sys

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    words_file = sys.argv[1]
    WORDS = []
    with open(words_file) as f:
        for line in f:
            WORDS.append(line)
    invalid_count = 0
    for word in WORDS:
        (matched, outputs) = SYS_DIC.matcher.run(word.encode('utf8'))
        if not matched:
            print('No match for %s' % word)
            invalid_count += 1
        for o in outputs:
            try:
                word_id = struct.unpack('I', o)[0]
                try:
                    entry = SYS_DIC.entries[word_id]
                except:
                    print('Cannot find entry for %s, %d' % (word, word_id))
                    invalid_count += 1
            except:
                print('Invalid output for %s, %s' % (word, str(o)))
                invalid_count += 1
    print('invalid outputs = %d' % invalid_count)

