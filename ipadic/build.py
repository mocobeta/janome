import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from pathlib import Path
import time
from fst import *
from dict import *
from struct import pack

FILE_CHAR_DEF = 'char.def'
FILE_UNK_DEF = 'unk.def'
FILE_MATRIX_DEF = 'matrix.def'


def build_dict(dicdir, enc):
    surfaces = []  # inputs/outputs for FST. the FST maps string(surface form) to int(word id)
    entries = []   # dictionary entries
    csv_files = Path(dicdir).glob('*.csv')
    for path in csv_files:
        with path.open(encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                surface, leftId, rightId, cost, \
                pos, posDetail1, posDetail2, posDetail3, \
                inflForm, inflType, baseForm, reading, phonetic = \
                    line.split(',')
                posExpr = ','.join([pos, posDetail1, posDetail2, posDetail3])
                word_id = len(surfaces)
                surfaces.append((surface.encode('utf8'), pack('I', word_id)))
                entries.append((leftId, rightId, int(cost), posExpr, inflForm, inflType, baseForm, reading, phonetic))
    inputs = sorted(surfaces)  # inputs must be sorted.

    assert len(surfaces) == len(entries)

    _t1 = time.time()
    fst = create_minimum_transducer(inputs)
    logging.info('Build FST done. ' + str(time.time() - _t1) + ' sec.')
    _t2 = time.time()
    compiledFST = compileFST(fst)
    logging.info('Compile FST done. ' + str(time.time() - _t2) + ' sec.')
    save_fstdata(compiledFST, compresslevel=9)
    save_entries(entries, compresslevel=9)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    dicdir = sys.argv[1]
    enc = sys.argv[2]
    build_dict(dicdir, enc)
