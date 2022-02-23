=======
Janome
=======

.. image:: https://github.com/mocobeta/janome/workflows/Checks/badge.svg
    :target: https://github.com/mocobeta/janome/actions?query=workflow%3AChecks

.. image:: https://coveralls.io/repos/github/mocobeta/janome/badge.svg?branch=master
    :target: https://coveralls.io/github/mocobeta/janome?branch=master

.. image:: https://badges.gitter.im/org.png
    :target: https://gitter.im/janome-python

.. image:: https://img.shields.io/pypi/dm/Janome.svg
    :target: https://pypistats.org/packages/janome

.. image:: https://img.shields.io/conda/v/conda-forge/janome
    :target: https://anaconda.org/conda-forge/janome

Janome is a Japanese morphological analysis engine written in pure Python.

General documentation:

https://mocobeta.github.io/janome/en/ (English)

https://mocobeta.github.io/janome/ (Japanese)

Requirements
=============

Python 3.7+ is required.

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

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See LICENSE.txt and NOTICE.txt for license details.

Acknowledgement
================

Special thanks to @ikawaha, @takuyaa, @nakagami and @janome_oekaki.

Copyright
==========

Copyright(C) 2022, Tomoko Uchida. All rights reserved.
