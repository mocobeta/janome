# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
import sys
from io import open

print(u'Tokenize (stream mode)')
t = Tokenizer()

with open('text_lemon.txt', encoding='utf-8') as f:
    text = f.read()
    for token in t.tokenize(text, stream=True):
        print(token)
