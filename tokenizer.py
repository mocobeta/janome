# -*- coding: utf-8 -*-

from lattice import Lattice, Node, BOS, EOS

class Token:
    def __init__(self, dict_entry):
        self.surface = dict_entry.surface
        self.part_of_speech = dict_entry.part_of_speech
        self.infl_form = dict_entry.infl_form
        self.infl_type = dict_entry.infl_type
        self.base_form = dict_entry.base_form
        self.reading = dict_entry.reading
        self.phonetic = dict_entry.phonetic

    def __str__(self):
        return '%s\t%s,%s,%s,%s' % (self.surface, self.part_of_speech, self.base_form, self.reading, self.phonetic)


class Tokenizer:
    def __init__(self):
        import ipadic
        self.sys_dic = ipadic.SYS_DIC

    def tokenize(self, text):
        lattice = Lattice(len(text), self.sys_dic)
        pos = 0
        while pos < len(text):
            entries = self.sys_dic.lookup(text[pos:])
            for e in entries:
                lattice.add(Node(e))
            pos += lattice.forward()
        lattice.end()
        min_cost_path = lattice.backward()
        assert isinstance(min_cost_path[0], BOS)
        assert isinstance(min_cost_path[-1], EOS)
        tokens = [Token(node.entry) for node in min_cost_path[1:-1]]
        return tokens


if __name__ == '__main__':
    import sys
    text = sys.argv[1]
    tokens = Tokenizer().tokenize(text)
    for token in tokens:
        print(token)