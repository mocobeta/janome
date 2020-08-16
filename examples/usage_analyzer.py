from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenfilter import LowerCaseFilter, CompoundNounFilter, POSKeepFilter, TokenCountFilter

import logging
logging.basicConfig(level='INFO')

print('Analyzer example:')
text = '蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。'
char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('蛇の目', 'janome')]
tokenizer = Tokenizer()
token_filters = [CompoundNounFilter(), LowerCaseFilter()]
a = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
for token in a.analyze(text):
    print(token)

print('')
print('Analyzer example: Count nouns with POSKeepFilter and TokenCountFilter')
text = 'すもももももももものうち'
token_filters = [POSKeepFilter(['名詞']), TokenCountFilter()]
a = Analyzer(token_filters=token_filters)
for k, v in a.analyze(text):
    print('%s: %d' % (k, v))
