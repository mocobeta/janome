# -*- coding: utf-8 -*-

from lattice import Lattice, Node, BOS, EOS


class Token:
    def __init__(self, node):
        self.surface = node.surface
        self.part_of_speech = node.part_of_speech
        self.infl_form = node.infl_form
        self.infl_type = node.infl_type
        self.base_form = node.base_form
        self.reading = node.reading
        self.phonetic = node.phonetic

    def __str__(self):
        return '%s\t%s,%s,%s,%s' % (self.surface, self.part_of_speech, self.base_form, self.reading, self.phonetic)


class Tokenizer:
    def __init__(self):
        import ipadic
        self.sys_dic = ipadic.SYS_DIC

    def tokenize(self, text):
        text = text.strip()
        text = text.replace(' ', '')
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
        tokens = [Token(node) for node in min_cost_path[1:-1]]
        return tokens


if __name__ == '__main__':
    import sys, logging, time
    text = sys.argv[1]
    if len(sys.argv) > 2:
        loglevel = sys.argv[2]
    else:
        loglevel = 'WARN'
    logging.basicConfig(level=getattr(logging, loglevel.upper()))

    t = Tokenizer()
    _t1 = time.time()
    tokens = t.tokenize(text)
    _t2 = time.time()
    for token in tokens:
        print(token)
    logging.debug('Time: %f sec' % (_t2 - _t1))