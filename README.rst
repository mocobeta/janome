========
janome
========

Janome is a Japanese morphological analysis engine written in pure Python.

For general documentation: http://mocobeta.github.io/janome/ (for Japanese)

Requirements
=============

Python 3.4 or above is required.

Install
========

[Note] This consumes about 3 to 4 GB memory for building.

.. code:: bash

  (venv) $ python setup.py install
  Finished processing dependencies for Janome==0.1.3

  (venv) $ pip freeze
  Janome==0.1.3

Run
====

.. code:: bash

  (venv) $ python
  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize('すもももももももものうち'):
  ...     print(token)
  ...
  すもも 名詞,一般,*,*,*,*,すもも,スモモ,スモモ
  も    助詞,係助詞,*,*,*,*,も,モ,モ
  もも  名詞,一般,*,*,*,*,もも,モモ,モモ
  も    助詞,係助詞,*,*,*,*,も,モ,モ
  もも  名詞,一般,*,*,*,*,もも,モモ,モモ
  の    助詞,連体化,*,*,*,*,の,ノ,ノ
  うち  名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ

License
========

Apache License 2.0

Copyright
==========

Copyright(C) 2015, moco_beta. All rights reserved.
