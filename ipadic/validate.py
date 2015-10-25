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


import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.dic import SystemDictionary
from sysdic import entries, connections, chardef, unknowns

SYS_DIC = SystemDictionary(entries(), connections(), chardef.DATA, unknowns.DATA)

import struct
import logging
import sys
import io
import glob

PY3 = sys.version_info[0] == 3

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    dicdir = sys.argv[1]
    enc = sys.argv[2]

    # validate dictionary entries
    print('Validate dictionary entries...')
    csv_files = glob.glob(os.path.join(dicdir, '*.csv'))
    invalid_count = 0
    for path in csv_files:
        with io.open(path, encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface = line.split(',')[0]

                (matched, outputs) = SYS_DIC.matcher.run(surface.encode('utf8'))
                if not matched:
                    print('No match for %s' % surface)
                    invalid_count += 1
                for o in outputs:
                    try:
                        word_id = struct.unpack('I', o)[0]
                        try:
                            entry = SYS_DIC.entries[word_id]
                            if not surface.startswith(entry[0]):
                                raise Exception('Must not match!')
                        except KeyError:
                            print('Cannot find entry for %s, %d' % (surface.encode('utf8'), word_id))
                            invalid_count += 1
                    except Exception:
                        print('Invalid output for %s, %s' % (surface.encode('utf8'), str(o)))
                        invalid_count += 1
    print('invalid outputs = %d' % invalid_count)

    # validate connection costs
    print('Validate connection costs...')
    matrix_file = os.path.join(dicdir, 'matrix.def')
    invalid_count = 0
    with io.open(matrix_file, encoding=enc) as f:
        f.readline()
        for line in f:
            line.strip()
            id1, id2, cost = line.split(' ')
            try:
                if SYS_DIC.connections[int(id1)][int(id2)] != int(cost):
                    inv_cost = SYS_DIC.connections[int(id1)][int(id2)]
                    print('Invalid connection cost %d for (%s, %s)' % (inv_cost, id1, id2))
                    invalid_count += 1
            except:
                print('Cannot find connection cost for (%s, %s' % (id1, id2))
                invalid_count += 1
    print('invalid counts = %d' % invalid_count)
