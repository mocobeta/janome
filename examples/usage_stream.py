# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
import sys

PY3 = sys.version_info[0] == 3

print(u'Tokenize (stream mode)')
t = Tokenizer()

with open('text_lemon.txt') as f:
    text = f.read()
    if not PY3:
       text = unicode(text, 'utf-8')
    for token in t.tokenize(text, stream=True):
        print(token)
