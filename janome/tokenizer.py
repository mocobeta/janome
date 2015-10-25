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


import sys
import os
from .lattice import Lattice, Node, BOS, EOS, NodeType
from .dic import UserDictionary, CompiledUserDictionary

PY3 = sys.version_info[0] == 3

class Token:
    def __init__(self, node):
        self.surface = node.surface
        self.part_of_speech = node.part_of_speech
        self.infl_form = node.infl_form
        self.infl_type = node.infl_type
        self.base_form = node.base_form
        self.reading = node.reading
        self.phonetic = node.phonetic
        self.node_type = node.node_type

    def __str__(self):
        if PY3:
            return '%s\t%s,%s,%s,%s,%s,%s' % \
               (self.surface, self.part_of_speech, self.infl_form, self.infl_type, self.base_form, self.reading, self.phonetic)
        elif self.node_type == NodeType.SYS_DICT:
            return '%s\t%s,%s,%s,%s,%s,%s' % \
               (self.surface.encode('utf-8'),
                self.part_of_speech, self.infl_form, self.infl_type, self.base_form, self.reading, self.phonetic)
        else:
            return '%s\t%s,%s,%s,%s,%s,%s' % \
               (self.surface.encode('utf-8'),
                self.part_of_speech.encode('utf-8'),
                self.infl_form.encode('utf-8'),
                self.infl_type.encode('utf-8'),
                self.base_form.encode('utf-8'),
                self.reading.encode('utf-8'),
                self.phonetic.encode('utf-8'))


class Tokenizer:
    def __init__(self, udic='', udic_enc='utf8', udic_type='ipadic', max_unknown_length=1024):
        from sysdic import SYS_DIC
        self.sys_dic = SYS_DIC
        if udic:
            if udic.endswith('.csv'):
                # build user dictionary from CSV
                self.user_dic = UserDictionary(udic, udic_enc, udic_type, SYS_DIC.connections)
            elif os.path.isdir(udic):
                # load compiled user dictionary
                self.user_dic = CompiledUserDictionary(udic, SYS_DIC.connections)
            else:
                self.user_dic = None
        else:
            self.user_dic = None
        self.max_unknown_length = max_unknown_length

    def tokenize(self, text):
        text = text.strip()
        lattice = Lattice(len(text), self.sys_dic)
        pos = 0
        while pos < len(text):
            # user dictionary
            if self.user_dic:
                entries = self.user_dic.lookup(text[pos:])
                for e in entries:
                    lattice.add(Node(e, NodeType.USER_DICT))
                matched = len(entries) > 0

            # system dictionary
            entries = self.sys_dic.lookup(text[pos:])
            for e in entries:
                lattice.add(Node(e, NodeType.SYS_DICT))
            matched = len(entries) > 0

            # unknown
            cates = self.sys_dic.get_char_categories(text[pos])
            if cates:
                for cate in cates:
                    if matched and not self.sys_dic.unkown_invoked_always(cate):
                        continue
                    # unknown word length
                    length = self.sys_dic.unknown_length(cate) \
                        if not self.sys_dic.unknown_grouping(cate) else self.max_unknown_length
                    assert length >= 0
                    # buffer for unknown word
                    buf = text[pos]
                    for p in range(pos + 1, min(len(text), pos + length + 1)):
                        _cates =  self.sys_dic.get_char_categories(text[p])
                        if cate in _cates or any(cate in _compat_cates for _compat_cates in _cates.values()):
                            buf += text[p]
                        else:
                            break
                    unknown_entries = self.sys_dic.unknowns.get(cate)
                    assert unknown_entries
                    for entry in unknown_entries:
                        left_id, right_id, cost, part_of_speech = entry
                        dummy_dict_entry = (buf, left_id, right_id, cost, part_of_speech, '*', '*', '*', '*', '*')
                        lattice.add(Node(dummy_dict_entry, NodeType.UNKNOWN))

            pos += lattice.forward()
        lattice.end()
        min_cost_path = lattice.backward()
        assert isinstance(min_cost_path[0], BOS)
        assert isinstance(min_cost_path[-1], EOS)
        tokens = [Token(node) for node in min_cost_path[1:-1]]
        return tokens
