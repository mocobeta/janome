========
janome
========

Janome is a Japanese morphological analysis engine written in pure Python.

Requirements
=============

Python 3.4 or above is required.

Install
========

.. code:: bash

  (venv)$ python -V
  Python 3.4.2

  (venv) $ python setup.py install
  Finished processing dependencies for Janome==0.0.1

  (venv) $ pip freeze
  Janome==0.0.1

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
  も   	助詞,係助詞,*,*,*,*,も,モ,モ
  もも 	名詞,一般,*,*,*,*,もも,モモ,モモ
  も	    助詞,係助詞,*,*,*,*,も,モ,モ
  もも	  名詞,一般,*,*,*,*,もも,モモ,モモ
  の	    助詞,連体化,*,*,*,*,の,ノ,ノ
  うち	  名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ

or

.. code:: bash

  $ echo 'すもももももももものうち' | janome/scripts/janome
  すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
  も 		助詞,係助詞,*,*,*,*,も,モ,モ
  もも		名詞,一般,*,*,*,*,もも,モモ,モモ
  も	  	助詞,係助詞,*,*,*,*,も,モ,モ
  もも		名詞,一般,*,*,*,*,もも,モモ,モモ
  の		  助詞,連体化,*,*,*,*,の,ノ,ノ
  うち		名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ


Test
======

.. code:: bash

  (venv) $ python tests/test_janome.py 
  .
  ----------------------------------------------------------------------
  Ran 1 test in 0.000s

  OK

Uninstall
===========

.. code:: bash

  (venv) $ pip uninstall janome
  Uninstalling Janome:
    /path/to/venv/lib/python3.4/site-packages/Janome-0.0.1-py3.4.egg
  Proceed (y/n)? y
    Successfully uninstalled Janome

