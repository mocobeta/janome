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


from __future__ import with_statement
import os, sys
from io import open
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import time
import glob
from janome.fst import *
from janome.dic import *
from struct import pack
from collections import OrderedDict

FILE_CHAR_DEF = 'char.def'
FILE_UNK_DEF = 'unk.def'
FILE_MATRIX_DEF = 'matrix.def'


def build_dict(dicdir, enc, outdir=u'.'):
    surfaces = []  # inputs/outputs for FST. the FST maps string(surface form) to int(word id)
    entries = OrderedDict()  # dictionary entries
    csv_files = glob.glob(os.path.join(dicdir, '*.csv'))
    for path in csv_files:
        with open(path, encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface, left_id, right_id, cost, \
                pos_major, pos_minor1, pos_minor2, pos_minor3, \
                infl_form, infl_type, base_form, reading, phonetic = \
                    line.split(',')
                part_of_speech = ','.join([pos_major, pos_minor1, pos_minor2, pos_minor3])
                morph_id = len(surfaces)
                surfaces.append((surface.encode('utf8'), pack('I', morph_id)))
                entries[morph_id] = (surface, int(left_id), int(right_id), int(cost), part_of_speech, infl_form, infl_type, base_form, reading, phonetic)
    inputs = sorted(surfaces)  # inputs must be sorted.

    assert len(surfaces) == len(entries)

    fst = create_minimum_transducer(inputs)
    compiledFST = compileFST(fst)
    save_fstdata(compiledFST, dir=outdir)
    save_entries(entries, dir=outdir)

    # save connection costs as dict
    matrix_file = os.path.join(dicdir, FILE_MATRIX_DEF)
    with open(matrix_file, encoding=enc) as f:
        size1, size2 = f.readline().split(' ')
        conn_costs = [[0 for _ in range(0, int(size2))] for _ in range(0, int(size1))]
        for line in f:
            line = line.strip()
            id1, id2, cost = line.split(' ')
            conn_costs[int(id1)][int(id2)] = int(cost)
    save_connections(conn_costs, dir=outdir)


def build_unknown_dict(dicdir, enc, outdir=u'.'):
    categories = {}
    coderange = []
    with open(os.path.join(dicdir, FILE_CHAR_DEF), encoding=enc) as f:
        for line in f:
            line = line.strip()
            line = line.replace('\t', ' ')
            if line.startswith('#'):
                continue
            if line.startswith('0x'):
                # codepoints for each category
                cols = [col for col in line.split(' ') if col]  # ignore empty string
                if len(cols) < 2:
                    continue
                codepoints_range = cols[0].split('..')
                codepoints_from = unichr(int(codepoints_range[0], 16))
                codepoints_to = unichr(int(codepoints_range[1], 16)) if len(codepoints_range) == 2 else codepoints_from
                cate = cols[1].strip()
                assert cate in categories
                _range = {'from': codepoints_from, 'to': codepoints_to, 'cate': cate}
                if len(cols) >= 3:
                    # has compatible categories
                    cates = []
                    for cate in cols[2:]:
                        if not cate:
                            continue
                        elif cate.startswith('#'):
                            break
                        cates.append(cate)
                    if cates:
                        assert all(cate in categories for cate in cates)
                        _range['compat_cates'] = cates
                coderange.append(_range)
            else:
                # category definition
                cols = [col for col in line.split(' ') if col]  # ignore empty string
                if len(cols) < 4:
                    continue
                invoke = True if cols[1] == '1' else False
                group = True if cols[2] == '1' else False
                length = int(cols[3])
                categories[cols[0]] = {'INVOKE': invoke, 'GROUP': group, 'LENGTH': length}

    unknowns = {}
    with open(os.path.join(dicdir, FILE_UNK_DEF), encoding=enc) as f:
        for line in f:
            line = line.strip()
            cate, left_id, right_id, cost, \
            pos_major, pos_minor1, pos_minor2, pos_minor3, _1, _2, _3 = \
                line.split(',')
            part_of_speech = ','.join([pos_major, pos_minor1, pos_minor2, pos_minor3])
            assert cate in categories
            if cate not in unknowns:
                unknowns[cate] = []
            unknowns[cate].append((int(left_id), int(right_id), int(cost), part_of_speech))

    save_chardefs((categories, coderange), dir=outdir)
    save_unknowns(unknowns, dir=outdir)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    dicdir = sys.argv[1]
    enc = sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else '.'
    build_dict(dicdir, enc, outdir)
    build_unknown_dict(dicdir, enc, outdir)
