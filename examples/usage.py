# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer

print(u'Tokenize (system dictionary)')
t = Tokenizer()
for token in t.tokenize(u'すもももももももものうち'):
  print(token)

print('')
print(u'Tokenize (mmap system dictionary)')
t = Tokenizer(mmap=True)
for token in t.tokenize(u'すもももももももものうち'):
  print(token)

print('')
print(u'Tokenize (wakati mode)')
for token in t.tokenize(u'すもももももももものうち', wakati = True):
  print(token)

print('')
print(u'Tokenize with user dictionary')
t = Tokenizer("user_ipadic.csv", udic_enc="utf8")
for token in t.tokenize(u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'):
  print(token)

print('')
print(u'Tokenize with user dictionary (wakati mode)')
t = Tokenizer("user_ipadic.csv", udic_enc="utf8")
for token in t.tokenize(u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。', wakati = True):
  print(token)

print('')
print(u'Tokenize with simplified user dictionary')
t = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
for token in t.tokenize(u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'):
  print(token)
