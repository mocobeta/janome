# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

import logging
logging.basicConfig(level='INFO')

text = u'蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。'
char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(u'蛇の目', u'janome')]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), LowerCaseFilter()]
a = Analyzer(char_filters, tokenizer, token_filters)
for token in a.analyze(text):
    print(token)
