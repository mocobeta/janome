# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
import sys
from io import open

PY3 = sys.version_info[0] == 3

print(u'Tokenize (stream mode)')
t = Tokenizer()

with open('text_lemon.txt', encoding='utf-8') as f:
    text = f.read()
    if not PY3:
       text = unicode(text)
    for token in t.tokenize(text, stream=True):
        print(token)
