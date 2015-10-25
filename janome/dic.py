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
import os
import io
import pickle
import gzip
from struct import pack, unpack
from .fst import Matcher, create_minimum_transducer, compileFST
import traceback
import logging
import sys

PY3 = sys.version_info[0] == 3

SYSDIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sysdic")

FILE_FST_DATA = 'fst.data'
# FILE_ENTRIES = 'entries.data'
# FILE_CONNECTIONS = 'connections.data'

MODULE_FST_DATA = 'fstdata.py'
MODULE_ENTRIES = 'entries%d.py'
MODULE_CONNECTIONS = 'connections%d.py'
MODULE_CHARDEFS = 'chardef.py'
MODULE_UNKNOWNS = 'unknowns.py'

FILE_USER_FST_DATA = 'user_fst.data'
FILE_USER_ENTRIES_DATA = 'user_entries.data'

def save_fstdata(data, dir='.'):
    _save(os.path.join(dir, FILE_FST_DATA), data, 9)
    # _save_as_module(os.path.join(dir, MODULE_FST_DATA), data)


def save_entries(entries, dir=u'.'):
    #_save(os.path.join(dir, FILE_ENTRIES), pickle.dumps(entries), compresslevel)
    # split whole entries to 10 buckets to reduce memory usage while installing.
    # TODO: find better ways...
    bucket_size = (len(entries) // 10) + 1
    offset = 0
    for i in range(1, 11):
        _save_entries_as_module(
            os.path.join(dir, MODULE_ENTRIES % i),
            {k:v for (k,v) in entries.items()[offset:offset+bucket_size]})
        offset += bucket_size


def save_connections(connections, dir=u'.'):
    #_save(os.path.join(dir, FILE_CONNECTIONS), pickle.dumps(connections), compresslevel)
    # split whole connections to 2 buckets to reduce memory usage while installing.
    # TODO: find better ways...
    bucket_size = (len(connections) // 2) + 1
    offset = 0
    for i in range(1, 3):
        _save_as_module(os.path.join(dir, MODULE_CONNECTIONS % i),
                        connections[offset:offset+bucket_size])
        offset += bucket_size


def save_chardefs(chardefs, dir=u'.'):
    _save_as_module(os.path.join(dir, MODULE_CHARDEFS), chardefs)


def save_unknowns(unknowns, dir=u'.'):
    _save_as_module(os.path.join(dir, MODULE_UNKNOWNS), unknowns)


def _save(file, data, compresslevel):
    if not data:
        return
    with gzip.open(file, 'wb', compresslevel) as f:
        f.write(data)
        f.flush()


def _load(file):
    if not os.path.exists(file):
        return None
    with gzip.open(file, 'rb') as f:
        data = f.read()
        return data


def _save_as_module(file, data):
    if not data:
        return
    with open(file, 'w') as f:
        f.write(u'DATA=')
        f.write(str(data) if PY3 else unicode(data))
        f.flush()


def _save_entries_as_module(file, entries):
    with open(file, 'w') as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('DATA={')
        for k, v in entries.items():
            s = u"%d:(u'%s',%s,%s,%d,'%s','%s','%s','%s','%s','%s')," % (
                k, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9])
            f.write(s if PY3 else s.encode('utf-8'))
        f.write('}\n')
        f.flush()


class Dictionary(object):
    u"""
    Base dictionary class
    """
    def __init__(self, compiledFST, entries, connections):
        self.compiledFST = compiledFST
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
            logging.error('outputs=%s' % str(outputs) if PY3 else unicode(outputs))
            traceback.format_exc()
            sys.exit(1)

    def get_trans_cost(self, id1, id2):
        return self.connections[id1][id2]


class SystemDictionary(Dictionary):
    u"""
    System dictionary class
    """
    def __init__(self, entries, connections, chardefs, unknowns):
        Dictionary.__init__(self, _load(os.path.join(SYSDIC_DIR, FILE_FST_DATA)), entries, connections)
        self.char_categories = chardefs[0]
        self.char_ranges = chardefs[1]
        self.unknowns = unknowns

    def get_char_categories(self, c):
        res = {}
        for chr_range in self.char_ranges:
            if chr_range['from'] <= c <= chr_range['to']:
                cate = chr_range['cate']
                compate_cates = chr_range['compat_cates'] if 'compat_cates' in chr_range else []
                res[cate] = compate_cates
        return res

    def unkown_invoked_always(self, cate):
        if cate in self.char_categories:
            return self.char_categories[cate]['INVOKE']
        return False

    def unknown_grouping(self, cate):
        if cate in self.char_categories:
            return self.char_categories[cate]['GROUP']
        return False

    def unknown_length(self, cate):
        if cate in self.char_categories:
            return self.char_categories[cate]['LENGTH']
        return -1


class UserDictionary(Dictionary):
    u"""
    User dictionary class (uncompiled)
    """
    def __init__(self, user_dict, enc, type, connections):
        build_method = getattr(self, 'build' + type)
        compiledFST, entries = build_method(user_dict, enc)
        Dictionary.__init__(self, compiledFST, entries, connections)

    def buildipadic(self, user_dict, enc):
        surfaces = []
        entries = {}
        with io.open(user_dict, encoding=enc) as f:
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
        return compiledFST, entries

    def save(self, to_dir, compressionlevel=9):
        if os.path.exists(to_dir) and not os.path.isdir(to_dir):
            raise Exception('Not a directory : %s' % to_dir)
        elif not os.path.exists(to_dir):
            os.makedirs(to_dir, mode=int('0755', 8))
        _save(os.path.join(to_dir, FILE_USER_FST_DATA), self.compiledFST, compressionlevel)
        _save(os.path.join(to_dir, FILE_USER_ENTRIES_DATA), pickle.dumps(self.entries), compressionlevel)


class CompiledUserDictionary(Dictionary):
    u"""
    User dictionary class (compiled)
    """
    def __init__(self, dic_dir, connections):
        compiledFST, entries = self.load_dict(dic_dir)
        Dictionary.__init__(self, compiledFST, entries, connections)

    def load_dict(self, dic_dir):
        if not os.path.exists(dic_dir) or not os.path.isdir(dic_dir):
            raise Exception('No such directory : ' % dic_dir)
        compiledFST = _load(os.path.join(dic_dir, FILE_USER_FST_DATA))
        entries = pickle.loads(_load(os.path.join(dic_dir, FILE_USER_ENTRIES_DATA)))
        return compiledFST, entries
