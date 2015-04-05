# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer

if __name__ == '__main__':
    import sys
    text = ''.join(sys.argv[1:])

    t = Tokenizer()
    tokens = t.tokenize(text)
    for token in tokens:
        print(token)

