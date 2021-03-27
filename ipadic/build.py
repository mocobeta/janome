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


from multiprocessing import Pool, cpu_count
import signal
import functools
import pickle
from struct import pack
import glob
import time
import logging
import os
import sys
from io import open
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from janome.dic import (
    start_save_entries,
    save_entry,
    save_entry_buckets,
    save_fstdata,
    end_save_entries,
    save_chardefs,
    save_connections,
    save_unknowns
)
from janome.fst import (
    set_fst_log_level,
    create_minimum_transducer,
    compileFST
)


logger = logging.getLogger('dic_builder')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t%(name)s - %(levelname)s\t%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

set_fst_log_level(logging.DEBUG)

FILE_CHAR_DEF = 'char.def'
FILE_UNK_DEF = 'unk.def'
FILE_MATRIX_DEF = 'matrix.def'

ENTRY_BUCKETS_NUM = 10


def collect(dicdir, enc, outdir, workdir):
    surfaces = []  # inputs/outputs for FST. the FST maps string(surface form) to int(word id)
    csv_files = glob.glob(os.path.join(dicdir, '*.csv'))
    morph_id = 0
    for path in csv_files:
        with open(path, encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface = line.split(',')[0]
                surfaces.append((surface.encode('utf8'), pack('I', morph_id)))
                morph_id += 1
    inputs = sorted(surfaces)  # inputs must be sorted.
    inputs_size = len(surfaces)
    logger.info('input size: %d' % inputs_size)

    # split inputs
    _part = []
    _cnt = 0
    for surface, mid in inputs:
        if len(_part) >= 200000:
            with open(os.path.join(workdir, 'input%d.pkl' % _cnt), 'wb') as f:
                pickle.dump(_part, f)
            _part = []
            _cnt += 1
        _part.append((surface, mid))
    if len(_part) > 0:
        with open(os.path.join(workdir, 'input%d.pkl' % _cnt), 'wb') as f:
            pickle.dump(_part, f)

    bucket_size = (inputs_size // ENTRY_BUCKETS_NUM) + 1
    bucket_idx = 0
    buckets = {}
    bucket_offset = 0
    morph_id = 0
    start_save_entries(outdir, 0, 0)
    for path in csv_files:
        with open(path, encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface, left_id, right_id, cost, \
                    pos_major, pos_minor1, pos_minor2, pos_minor3, \
                    infl_type, infl_form, base_form, reading, phonetic = \
                    line.split(',')
                part_of_speech = ','.join([pos_major, pos_minor1, pos_minor2, pos_minor3])
                entry = (surface, int(left_id), int(right_id), int(cost), part_of_speech,
                         infl_type, infl_form, base_form, reading, phonetic)
                save_entry(outdir, bucket_idx, morph_id, entry)
                morph_id += 1
                if morph_id % bucket_size == 0:
                    end_save_entries(outdir, bucket_idx)
                    buckets[bucket_idx] = (bucket_offset, morph_id)
                    bucket_idx += 1
                    bucket_offset = morph_id
                    start_save_entries(outdir, bucket_idx, bucket_offset)
    end_save_entries(outdir, bucket_idx)
    buckets[bucket_idx] = (bucket_offset, morph_id)
    save_entry_buckets(outdir, buckets)


def save_partial_fst(arg, outdir):
    part_idx, part_file = arg
    with open(part_file, 'rb') as f:
        _part = pickle.load(f)
        _processed, fst = create_minimum_transducer(_part)
        compiledFST = compileFST(fst)
        save_fstdata(compiledFST, dir=outdir, part=part_idx)
        logger.info('processed entries=%d' % _processed)
        return _processed


def build_dict(dicdir, outdir, workdir, pool):
    _start = time.time()

    input_files = glob.glob(os.path.join(workdir, 'input*.pkl'))
    func = functools.partial(save_partial_fst, outdir=outdir)
    pool.map(func, enumerate(input_files))
    pool.close()
    pool.join()

    _elapsed = round(time.time() - _start)
    logger.info('elapsed=%dsec' % _elapsed)

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


def build_unknown_dict(dicdir, enc, outdir='.'):
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
                codepoints_from = chr(int(codepoints_range[0], 16)).encode('unicode_escape').decode('ascii')
                codepoints_to = chr(int(codepoints_range[1], 16)).encode('unicode_escape').decode(
                    'ascii') if len(codepoints_range) == 2 else codepoints_from
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
            part_of_speech = ','.join([pos_major, pos_minor1, pos_minor2, pos_minor3]
                                      ).encode('unicode_escape').decode('ascii')
            assert cate in categories
            if cate not in unknowns:
                unknowns[cate] = []
            unknowns[cate].append((int(left_id), int(right_id), int(cost), part_of_speech))

    save_chardefs((categories, coderange), dir=outdir)
    save_unknowns(unknowns, dir=outdir)


pool = None


def create_pool(processes):
    global pool
    pool = Pool(processes=processes)


def terminate(*args, **kwargs):
    global pool
    sys.stderr.write('\nStopping...')
    pool.terminate()
    pool.join()


signal.signal(signal.SIGTERM, terminate)
signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGQUIT, terminate)

if __name__ == '__main__':
    mode = sys.argv[1]
    dicdir = sys.argv[2]
    enc = sys.argv[3]
    outdir = sys.argv[4] if len(sys.argv) > 4 else 'sysdic'
    workdir = sys.argv[5] if len(sys.argv) > 5 else 'work'
    processes = int(sys.argv[6]) if len(sys.argv) > 6 else cpu_count()
    if mode == '--collect':
        collect(dicdir, enc, outdir, workdir)
    elif mode == '--build':
        logger.info('worker processes: %d' % processes)
        create_pool(processes)
        build_dict(dicdir, outdir, workdir, pool)
        build_unknown_dict(dicdir, enc, outdir)
    else:
        print('Usage: build.py [--collect|--build] <options>')
