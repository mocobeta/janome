# -*- coding: utf-8 -*-

from .lattice import Lattice, Node, BOS, EOS, NodeType


class Token:
    def __init__(self, node):
        self.surface = node.surface
        self.part_of_speech = node.part_of_speech
        self.infl_form = node.infl_form
        self.infl_type = node.infl_type
        self.base_form = node.base_form
        self.reading = node.reading
        self.phonetic = node.phonetic
        self.node_type = node.node_type.name

    def __str__(self):
        return '%s\t%s,%s,%s,%s,%s,%s' % \
               (self.surface, self.part_of_speech, self.infl_form, self.infl_type, self.base_form, self.reading, self.phonetic)


class Tokenizer:
    def __init__(self, max_unknown_length=1024):
        from sysdic import SYS_DIC
        self.sys_dic = SYS_DIC
        self.max_unknown_length = max_unknown_length

    def tokenize(self, text):
        text = text.strip()
        lattice = Lattice(len(text), self.sys_dic)
        pos = 0
        while pos < len(text):
            # system dictionary
            entries = self.sys_dic.lookup(text[pos:])
            for e in entries:
                lattice.add(Node(e, NodeType.SYS_DICT))
            matched = len(entries) > 0

            # unknown
            cate, _ = self.sys_dic.char_category(text[pos])
            if cate and (not matched or self.sys_dic.unkown_invoked_always(cate)):
                # unknown word length
                # if not grouping, set to 1.
                length = self.sys_dic.unknown_length(cate) if self.sys_dic.unknown_grouping(cate) else 1
                assert length >= 0
                if length == 0:
                    length = self.max_unknown_length
                # buffer for unknown word
                buf = text[pos]
                for p in range(pos + 1, min(len(text), pos + length + 1)):
                    _cate, _compat_cates = self.sys_dic.char_category(text[p])
                    if cate == _cate or cate in _compat_cates:
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
