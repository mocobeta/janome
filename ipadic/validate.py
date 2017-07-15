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
from sysdic import entries_compact1, entries_compact2, entries_compact3, entries_compact_buckets
from sysdic import entries_extra1, entries_extra2, entries_extra3, entries_extra4, entries_extra5, entries_extra6, entries_extra7, entries_extra8, entries_extra9, entries_extra10, entries_extra_buckets

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

    # check dictionary entries buckets (for mmap support)
    print('Validate dictionary entries buckets...')
    _start, _end = min(entries_compact1.DATA.keys()), max(entries_compact1.DATA.keys()) + 1
    _ok1 = _start == entries_compact_buckets.DATA[1][0] and _end == entries_compact_buckets.DATA[1][1]
    _start, _end = min(entries_compact2.DATA.keys()), max(entries_compact2.DATA.keys()) + 1
    _ok2 = _start == entries_compact_buckets.DATA[2][0] and _end == entries_compact_buckets.DATA[2][1]
    _start, _end = min(entries_compact3.DATA.keys()), max(entries_compact3.DATA.keys()) + 1
    _ok3 = _start == entries_compact_buckets.DATA[3][0] and _end == entries_compact_buckets.DATA[3][1]
    print('Compact entries buckets check: %s, %s, %s' % (_ok1, _ok2, _ok3))
    _start, _end = min(entries_extra1.DATA.keys()), max(entries_extra1.DATA.keys()) + 1
    _ok1 = _start == entries_extra_buckets.DATA[1][0] and _end == entries_extra_buckets.DATA[1][1]
    _start, _end = min(entries_extra2.DATA.keys()), max(entries_extra2.DATA.keys()) + 1
    _ok2 = _start == entries_extra_buckets.DATA[2][0] and _end == entries_extra_buckets.DATA[2][1]
    _start, _end = min(entries_extra3.DATA.keys()), max(entries_extra3.DATA.keys()) + 1
    _ok3 = _start == entries_extra_buckets.DATA[3][0] and _end == entries_extra_buckets.DATA[3][1]
    _start, _end = min(entries_extra4.DATA.keys()), max(entries_extra4.DATA.keys()) + 1
    _ok4 = _start == entries_extra_buckets.DATA[4][0] and _end == entries_extra_buckets.DATA[4][1]
    _start, _end = min(entries_extra5.DATA.keys()), max(entries_extra5.DATA.keys()) + 1
    _ok5 = _start == entries_extra_buckets.DATA[5][0] and _end == entries_extra_buckets.DATA[5][1]
    _start, _end = min(entries_extra6.DATA.keys()), max(entries_extra6.DATA.keys()) + 1
    _ok6 = _start == entries_extra_buckets.DATA[6][0] and _end == entries_extra_buckets.DATA[6][1]
    _start, _end = min(entries_extra7.DATA.keys()), max(entries_extra7.DATA.keys()) + 1
    _ok7 = _start == entries_extra_buckets.DATA[7][0] and _end == entries_extra_buckets.DATA[7][1]
    _start, _end = min(entries_extra8.DATA.keys()), max(entries_extra8.DATA.keys()) + 1
    _ok8 = _start == entries_extra_buckets.DATA[8][0] and _end == entries_extra_buckets.DATA[8][1]
    _start, _end = min(entries_extra9.DATA.keys()), max(entries_extra9.DATA.keys()) + 1
    _ok9 = _start == entries_extra_buckets.DATA[9][0] and _end == entries_extra_buckets.DATA[9][1]
    _start, _end = min(entries_extra10.DATA.keys()), max(entries_extra10.DATA.keys()) + 1
    _ok10 = _start == entries_extra_buckets.DATA[10][0] and _end == entries_extra_buckets.DATA[10][1]
    print('Extra entries buckets check: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (_ok1, _ok2, _ok3, _ok4, _ok5, _ok6, _ok7, _ok8, _ok9, _ok10))
    
    # validate dictionary entries
    SYS_DIC = SystemDictionary(entries(), connections, chardef.DATA, unknowns.DATA)    
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
