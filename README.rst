=======
Janome
=======

.. image:: https://travis-ci.org/mocobeta/janome.svg?branch=master
    :target: https://travis-ci.org/mocobeta/janome

.. image:: https://ci.appveyor.com/api/projects/status/47d4avyw07voo331/branch/master?svg=true
    :target: https://ci.appveyor.com/project/mocobeta/janome/branch/master

.. image:: https://coveralls.io/repos/github/mocobeta/janome/badge.svg?branch=master
    :target: https://coveralls.io/github/mocobeta/janome?branch=master

.. image:: https://badges.gitter.im/org.png
    :target: https://gitter.im/janome-python/ja

.. image:: https://img.shields.io/pypi/dm/Janome.svg
    :target: https://pypistats.org/packages/janome

Janome is a Japanese morphological analysis engine written in pure Python.

General documentation:

https://mocobeta.github.io/janome/en/ (English)

https://mocobeta.github.io/janome/ (Japanese)

Requirements
=============

Python 2.7.x or 3.3+ is required.

Install
========

[Note] This consumes about 500 MB memory for building.

.. code:: bash

  (venv) $ python setup.py install

Run
====

.. code:: bash

  (env) $ python
  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize(u'すもももももももものうち'):
  ...     print(token)
  ...
  すもも 名詞,一般,*,*,*,*,すもも,スモモ,スモモ
  も    助詞,係助詞,*,*,*,*,も,モ,モ
  もも  名詞,一般,*,*,*,*,もも,モモ,モモ
  も    助詞,係助詞,*,*,*,*,も,モ,モ
  もも  名詞,一般,*,*,*,*,もも,モモ,モモ
  の    助詞,連体化,*,*,*,*,の,ノ,ノ
  うち  名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ

.. code:: bash

  (env) $ python
  >>> from janome.tokenizer import Tokenizer
  >>> from janome.analyzer import Analyzer
  >>> from janome.charfilter import *
  >>> from janome.tokenfilter import *
  >>> text = u'蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。'
  >>> char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(u'蛇の目', u'janome')]
  >>> tokenizer = Tokenizer()
  >>> token_filters = [CompoundNounFilter(), POSStopFilter(['記号','助詞']), LowerCaseFilter()]
  >>> a = Analyzer(char_filters, tokenizer, token_filters)
  >>> for token in a.analyze(text):
  ...     print(token)
  ...
  janome  名詞,固有名詞,組織,*,*,*,*,*,*
  pure    名詞,固有名詞,組織,*,*,*,*,*,*
  python  名詞,一般,*,*,*,*,*,*,*
  な       助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ
  形態素解析器  名詞,複合,*,*,*,*,形態素解析器,ケイタイソカイセキキ,ケイタイソカイセキキ
  です     助動詞,*,*,*,特殊・デス,基本形,です,デス,デス

For contributors
=================

Please see this wiki page:

https://github.com/mocobeta/janome/wiki#for-contributors

License
========

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See LICENSE.txt and NOTICE.txt for license details.

Acknowledgement
================

Special thanks to @ikawaha, @takuyaa, @nakagami and @janome_oekaki.

Copyright
==========

Copyright(C) 2015, Tomoko Uchida. All rights reserved.
