# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

import logging
logging.basicConfig(level='INFO')

print(u'Analyzer example:')
text = u'蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。'
char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(u'蛇の目', u'janome')]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), LowerCaseFilter()]
a = Analyzer(char_filters, tokenizer, token_filters)
for token in a.analyze(text):
    print(token)

print('')
print(u'Analyzer example: Count nouns with POSKeepFilter and TokenCountFilter')
text = u'すもももももももものうち'
token_filters = [POSKeepFilter(u'名詞'), TokenCountFilter()]
a = Analyzer(token_filters=token_filters)
for k, v in a.analyze(text):
    print('%s: %d' % (k, v))