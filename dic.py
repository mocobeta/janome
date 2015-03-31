# -*- coding: utf-8 -*-

import os
import pickle
import gzip, bz2
from struct import unpack
from fst import Matcher


FILE_FST_DATA = 'fst.data'
FILE_ENTRIES = 'entries.data'
FILE_CONNECTIONS = 'connections.data'

MODULE_FST_DATA = 'fstdata.py'
MODULE_ENTRIES = 'entries.py'
MODULE_CONNECTIONS = 'connections.py'


def save_fstdata(data, compresslevel=0, dir='.'):
    path = os.path.join(dir, FILE_FST_DATA)
    _save(path, data, compresslevel)


def save_entries(entries, compresslevel=0, dir='.'):
    path = os.path.join(dir, FILE_ENTRIES)
    _save(path, pickle.dumps(entries), compresslevel)


def save_connections(connections, compresslevel=0, dir='.'):
    path = os.path.join(dir, FILE_CONNECTIONS)
    _save(path, pickle.dumps(connections), compresslevel)


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


class Dictionary:
    def __init__(self, compiledFST, entries, connections):
        self.matcher = Matcher(compiledFST)
        self.entries = entries
        self.connections = connections

    def lookup(self, s):
        (matched, outputs) = self.matcher.run(s.encode('utf8'))
        if not matched:
            return []
        return [self.entries[unpack('I', e)[0]] for e in outputs]


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