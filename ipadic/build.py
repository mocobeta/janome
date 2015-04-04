import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from pathlib import Path
import time
from fst import *
from dic import *
from struct import pack

FILE_CHAR_DEF = 'char.def'
FILE_UNK_DEF = 'unk.def'
FILE_MATRIX_DEF = 'matrix.def'


def build_dict(dicdir, enc, outdir='.'):
    surfaces = []  # inputs/outputs for FST. the FST maps string(surface form) to int(word id)
    #entries = []   # dictionary entries
    entries = {}  # dictionary entries
    csv_files = Path(dicdir).glob('*.csv')
    for path in csv_files:
        with path.open(encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface, left_id, right_id, cost, \
                pos_major, pos_minor1, pos_minor2, pos_minor3, \
                infl_form, infl_type, base_form, reading, phonetic = \
                    line.split(',')
                part_of_speech = ','.join([pos_major, pos_minor1, pos_minor2, pos_minor3])
                morph_id = len(surfaces)
                surfaces.append((surface.encode('utf8'), pack('I', morph_id)))
                entries[morph_id] = (surface, left_id, right_id, int(cost), part_of_speech, infl_form, infl_type, base_form, reading, phonetic)
    inputs = sorted(surfaces)  # inputs must be sorted.

    assert len(surfaces) == len(entries)

    _t1 = time.time()
    fst = create_minimum_transducer(inputs)
    logging.info('Build FST done. ' + str(time.time() - _t1) + ' sec.')
    _t2 = time.time()
    compiledFST = compileFST(fst)
    logging.info('Compile FST done. ' + str(time.time() - _t2) + ' sec.')
    save_fstdata(compiledFST, compresslevel=9, dir=outdir)
    save_entries(entries, compresslevel=9, dir=outdir)

    # save connection costs as dict
    matrix_file = Path(dicdir, FILE_MATRIX_DEF)
    conn_costs = {}
    with matrix_file.open(encoding=enc) as f:
        size1, size2 = f.readline().split(' ')
        matrix_size = int(size1) * int(size2)
        for line in f:
            line = line.strip()
            id1, id2, cost = line.split(' ')
            key = '%s,%s' % (id1, id2)
            val = int(cost)
            conn_costs[key] = val
        assert len(conn_costs) == matrix_size
    save_connections(conn_costs, compresslevel=9, dir=outdir)


def pre_compile(outdir='.'):
    import py_compile
    _t1 = time.time()
    py_compile.compile(os.path.join(outdir, MODULE_FST_DATA))
    py_compile.compile(os.path.join(outdir, MODULE_ENTRIES))
    py_compile.compile(os.path.join(outdir, MODULE_CONNECTIONS))
    logging.info('Pre-compile data done. ' + str(time.time() - _t1) + ' sec.')

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    dicdir = sys.argv[1]
    enc = sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else '.'
    build_dict(dicdir, enc, outdir)
    #pre_compile(outdir)
