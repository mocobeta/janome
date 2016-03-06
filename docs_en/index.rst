.. janome documentation master file, created by
   sphinx-quickstart on Tue Apr  7 21:28:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: strike


Welcome to janome's documentation!
==================================

`Japanese <http://mocobeta.github.io/janome/>`_

What's Janome?
--------------

Janome (蛇の目) is a Japanese morphological analysis engine (or tokenizer, pos-tagger) written in pure Python including the built-in dictionary and the language model.

We aim to build a library which is easy to install and provides simple and consice APIs for various python applications. 

Janome uses mecab-ipadic-2.7.0-20070801 (originally created for `MeCab <http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html>`_ ) as the built-in dictionary.

Source Codes
------------

`https://github.com/mocobeta/janome <https://github.com/mocobeta/janome>`_


Requirements
------------

Python 2.7.x or Python 3.4+ interpreter

Current version
---------------

* janome: 0.2.7

Install
-------

PyPI
^^^^

.. note:: It requires 500 to 600 MB RAM for install and pre-compile dictionary data. 

`https://pypi.python.org/pypi/Janome <https://pypi.python.org/pypi/Janome>`_

.. code-block:: bash

  $ pip install janome

Usage
-----

Create janome.tokenizer.Tokenizer object and call tokenize() method with the sentences you want to analyze.

The return value is a list of Token objects. Token includes morphological information such as surface form, part-of-speech. See dir() or `source codes <https://github.com/mocobeta/janome/blob/master/janome/tokenizer.py>`_ for more details.

::

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

for Windows users
^^^^^^^^^^^^^^^^^

Use decode('utf8') if output is garbled.

::

  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize(u'すもももももももものうち'):
  ...     print(str(token).decode('utf8'))


Use user defined dictionary
---------------------------

MeCab IPADIC format
^^^^^^^^^^^^^^^^^^^

You can add custom entries to the built-in dictionary at runtime by using user defined dictionary.

Default dictionary format is equal to MeCab IPADIC format. Create a CSV file as below and pass the file path and the character encoding to Tokenizer's constructor.

See the `MeCab document <http://mecab.googlecode.com/svn/trunk/mecab/doc/dic.html>`_ for more details.

userdic.csv ::

  東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
  東武スカイツリーライン,1288,1288,4700,名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン
  とうきょうスカイツリー駅,1288,1288,4143,名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ

::

  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer("userdic.csv", udic_enc="utf8")
  >>> for token in t.tokenize(u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'):
  ...   print(token)
  ...

  東京スカイツリー         名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
  へ        助詞,格助詞,一般,*,*,*,へ,ヘ,エ
  の        助詞,連体化,*,*,*,*,の,ノ,ノ
  お越し    名詞,一般,*,*,*,*,お越し,オコシ,オコシ
  は        助詞,係助詞,*,*,*,*,は,ハ,ワ
  、        記号,読点,*,*,*,*,、,、,、
  東武スカイツリーライン    名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン
  「        記号,括弧開,*,*,*,*,「,「,「
  とうきょうスカイツリー駅  名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ
  」        記号,括弧閉,*,*,*,*,」,」,」
  が        助詞,格助詞,一般,*,*,*,が,ガ,ガ
  便利      名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ
  です      助動詞,*,*,*,特殊・デス,基本形,です,デス,デス
  。        記号,句点,*,*,*,*,。,。,。

Simplified dictionary format (v0.2.7+)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Janome provides alternative simplified dictionary format like `Kuromoji <https://www.atilika.com/en/products/kuromoji.html>`_ user dictionary. This format supports surface form, part-of-speech and reading only.

To use simplified dictionary format, create a CSV file that includes "<surface form>,<part-of-speech>,<reading>" in each line (see the example below) and pass the file path and the dictionary type (udic_type='simpledic') to Tokenizer's constructor.

user_simpledic.csv ::

   東京スカイツリー,カスタム名詞,トウキョウスカイツリー
   東武スカイツリーライン,カスタム名詞,トウブスカイツリーライン
   とうきょうスカイツリー駅,カスタム名詞,トウキョウスカイツリーエキ

::

   >>> from janome.tokenizer import Tokenizer
   >>> t = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
   >>> for token in t.tokenize(u'東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便 利です。'):
   ...   print(token)
   ...
   東京スカイツリー	カスタム名詞,*,*,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
   へ    助詞,格助詞,一般,*,*,*,へ,ヘ,エ
   の    助詞,連体化,*,*,*,*,の,ノ,ノ
   お越し    名詞,一般,*,*,*,*,お越し,オコシ,オコシ
   は    助詞,係助詞,*,*,*,*,は,ハ,ワ
   、    記号,読点,*,*,*,*,、,、,、
   東武スカイツリーライン   カスタム名詞,*,*,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン
   「    記号,括弧開,*,*,*,*,「,「,「
   とうきょうスカイツリー駅    カスタム名詞,*,*,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ
    」   記号,括弧閉,*,*,*,*,」,」,」
   が    助詞,格助詞,一般,*,*,*,が,ガ,ガ
   便利    名詞,形容動詞語幹,*,*,*,*,便利,ベンリ,ベンリ
   です    助動詞,*,*,*,特殊・デス,基本形,です,デス,デス
   。    記号,句点,*,*,*,*,。,。,。


Pre-compiled user dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With large user dictionary, it can take much time to convert CSV file to the binary data structure. You can compile the user dictionary in advance and use that at runtime.

So there is no tools for compiling user dictionary at current version, use APIs as below.

How to compile user dictionary (MeCab IPADIC format): ::

  >>> from janome.dic import UserDictionary
  >>> from sysdic import SYS_DIC
  >>> user_dict = UserDictionary("userdic.csv", "utf8", "ipadic", SYS_DIC.connections)
  >>> user_dict.save("/tmp/userdic")

How to compile user dictionary (simplified format): ::  

  >>> from janome.dic import UserDictionary
  >>> from sysdic import SYS_DIC
  >>> user_dict = UserDictionary("user_simpledic.csv", "utf8", "simpledic", SYS_DIC.connections)
  >>> user_dict.save("/tmp/userdic")

Once compiling has been successfully completed, the data is saved in '/tmp/userdic' directory. Pass the directory path to Tokenizer's constructor to use it.

::

  >>> t = Tokenizer("/tmp/userdic")

.. note:: Use same major python version both at compile time and runtime.  Forward/backward dictionary data compatibility is not guaranteed.

Use janome from the comman-line (v0.2.6+, Lunux/Mac only)
---------------------------------------------------------

Janome has executable built-in script 'janome' for command-line usage. (currently for Lunux/Mac only... patches are welcome!)

It reads a sentence at a time from standard input and outputs the analysis result. To see supported options, type "janome -h".

::

    (env)$ janome
    猫は液体である
    猫    名詞,一般,*,*,*,*,猫,ネコ,ネコ
    は    助詞,係助詞,*,*,*,*,は,ハ,ワ
    液体  名詞,一般,*,*,*,*,液体,エキタイ,エキタイ
    で    助動詞,*,*,*,特殊・ダ,連用形,だ,デ,デ
    ある  助動詞,*,*,*,五段・ラ行アル,基本形,ある,アル,アル
    (Type Ctrl-C to quit.)


Note for analyzing large document set
-------------------------------------

At current version (0.2.x), Janome can consume large memory when a very large document is passed all at onece. Please split large documents into small chunks or sentences.

It is a known issue, we'll make efforts to control memory consumption for large documents at future releases.

FAQ
---

Q. How is the accuracy of analysis?

A. Janome uses MeCab IPADIC dictionary, so the accuracy is roughly same to MeCab.

Q. How is the speed of analysis?

A. Basically depends on the input length. But according to my benchmark script, one sentence would take a few milliseconds to a few tens of milliseconds on desktop computers.

Q. What data structures and algorithms are used?

A. Janome uses FST (`Minimal Acyclic Subsequential Transducer <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698>`_) for internal dictionary data structure. I implemented the automaton by referring to `Apache Lucene <https://lucene.apache.org/core/>`_ (written in Java) and `kagome <https://github.com/ikawaha/kagome>`_ (written in Go). And for analysis engine, I implemented basic viterbi algorithm by referring the book `自然言語処理の基礎 <http://www.amazon.co.jp/%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%81%AE%E5%9F%BA%E7%A4%8E-%E5%A5%A5%E6%9D%91-%E5%AD%A6/dp/4339024511>`_ .

Q. I found bugs. Or have requests for enhancement.

A. Bug reports and requests (and of course, patches) are welcome. Raise issues at `Github repository <https://github.com/mocobeta/janome/issues>`_ or contact to `@moco_beta <https://twitter.com/moco_beta>`_.

License
------------

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See `LICENSE.txt <https://github.com/mocobeta/janome/blob/master/LICENSE.txt>`_ and `NOTICE.txt <https://github.com/mocobeta/janome/blob/master/NOTICE.txt>`_ for license details.


Copyright
-----------

Copyright(C) 2015-2016, moco_beta. All rights reserved.

History
----------

* 2016.03.05 janome Version 0.2.7 release
* 2015.10.26 janome Version 0.2.6 release
* 2015.05.11 janome Version 0.2.5 release
* 2015.05.03 janome Version 0.2.4 release
* 2015.05.03 janome Version 0.2.3 release
* 2015.04.24 janome Version 0.2.2 release
* 2015.04.24 janome Version 0.2.0 release
* 2015.04.11 janome Version 0.1.4 release
* 2015.04.08 janome Version 0.1.3 公開

Change details: `CHANGES <https://github.com/mocobeta/janome/blob/master/CHANGES.txt>`_

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

