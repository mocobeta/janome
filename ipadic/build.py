import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import time
from fst import *

def build_dict(enc, outfile, *files):
    entries = {}
    for file in files:
        with open(file, encoding=enc) as f:
            for line in f:
                line = line.rstrip()
                (surface, sep, tail) = line.partition(',')
                output = '.'.join(tail.split(',')[:3])
                entries[bytes(surface, encoding='utf8')] = bytes(output, encoding='utf-8')
    inputs = [(k, v) for k, v in sorted(entries.items())]

    _t1 = time.time()
    dict = create_minimum_transducer(inputs)
    logging.info('Build FST done. ' + str(time.time() - _t1) + ' sec.')
    #dict.print_dictionary()
    _t2 = time.time()
    arcs = compileFST(dict)
    logging.info('Compile FST done. ' + str(time.time() - _t2) + ' sec.')
    save(outfile, arcs)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    enc = sys.argv[1]
    outfile = sys.argv[2]
    build_dict(enc, outfile, *sys.argv[3:])
