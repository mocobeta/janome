# -*- coding: utf-8 -*-

import os
import pickle
import gzip, bz2
from struct import unpack
from fst import Matcher
import traceback
import logging
import sys


FILE_FST_DATA = 'fst.data'
FILE_ENTRIES = 'entries.data'
FILE_CONNECTIONS = 'connections.data'

MODULE_FST_DATA = 'fstdata.py'
MODULE_ENTRIES = 'entries.py'
MODULE_CONNECTIONS = 'connections.py'


def save_fstdata(data, compresslevel=0, dir='.'):
    #_save(os.path.join(dir, FILE_FST_DATA), data, compresslevel)
    _save_as_module(os.path.join(dir, MODULE_FST_DATA), data)


def save_entries(entries, compresslevel=0, dir='.'):
    #_save(os.path.join(dir, FILE_ENTRIES), pickle.dumps(entries), compresslevel)
    _save_as_module(os.path.join(dir, MODULE_ENTRIES), entries)


def save_connections(connections, compresslevel=0, dir='.'):
    #_save(os.path.join(dir, FILE_CONNECTIONS), pickle.dumps(connections), compresslevel)
    _save_as_module(os.path.join(dir, MODULE_CONNECTIONS), connections)


def _save(file, data, compresslevel):
    if not data:
        return
    with gzip.open(file, 'wb', compresslevel) as f:
        f.write(data)
        f.flush()


def _save_as_module(file, data):
    if not data:
        return
    with open(file, 'w') as f:
        f.write('DATA=')
        f.write(str(data))
        f.flush()

"""
class DictEntry:
    def __init__(self, entry):
        surface, left_id, right_id, cost, part_of_speech, infl_form, infl_type, base_form, reading, phonetic = entry
        self.surface = surface
        self.left_id = left_id
        self.right_id = right_id
        self.cost = cost
        self.part_of_speech = part_of_speech
        self.infl_form = infl_form
        self.infl_type = infl_type
        self.base_form = base_form
        self.reading = reading
        self.phonetic = phonetic

    def __str__(self):
        return "(%s,%s,%s,%d,%s,%s,%s,%s,%s,%s)" % \
               (self.surface, self.left_id, self.right_id, self.cost, self.part_of_speech,
               self.infl_form, self.infl_type, self.base_form, self.reading, self.phonetic)
"""

class Dictionary:
    def __init__(self, compiledFST, entries, connections):
        self.matcher = Matcher(compiledFST)
        self.entries = entries
        self.connections = connections

    def lookup(self, s):
        (matched, outputs) = self.matcher.run(s.encode('utf8'))
        if not matched:
            return []
        try:
            return [self.entries[unpack('I', e)[0]] for e in outputs]
        except Exception as e:
            logging.error('Cannot load dictionary data. The dictionary may be corrupted?')
            logging.error('input=%s' % s)
            logging.error('outputs=%s' % str(outputs))
            traceback.format_exc()
            sys.exit(1)

    def get_trans_cost(self, id1, id2):
        key = '%s,%s' % (id1, id2)
        return self.connections.get(key)


class SystemDictionary(Dictionary):
    def __init__(self, dicdir):
        compiledFST = None
        with gzip.open(os.path.join(dicdir, FILE_FST_DATA), 'rb') as f:
            compiledFST = f.read()
        assert compiledFST is not None
        entries = None
        with gzip.open(os.path.join(dicdir, FILE_ENTRIES), 'rb') as f:
            entries = pickle.load(f)
        assert entries is not None
        connections = None
        with gzip.open(os.path.join(dicdir, FILE_CONNECTIONS), 'rb') as f:
            connections = pickle.load(f)
        assert connections is not None
        Dictionary.__init__(self, compiledFST, entries, connections)