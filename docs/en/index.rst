.. janome documentation master file, created by
   sphinx-quickstart on Tue Apr  7 21:28:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: strike


Welcome to janome's documentation! (English)
=============================================

`日本語 <http://mocobeta.github.io/janome/>`_

What's Janome?
--------------

Janome (蛇の目) is a Japanese morphological analysis engine (or tokenizer, pos-tagger) written in pure Python including the built-in dictionary and the language model.

We aim to build a library which is easy to install and provides simple and consice APIs for various python applications. 

Janome uses mecab-ipadic-2.7.0-20070801 as the built-in dictionary.

Source Codes
------------

`https://github.com/mocobeta/janome <https://github.com/mocobeta/janome>`_

API reference
-------------

`http://mocobeta.github.io/janome/api/ <http://mocobeta.github.io/janome/api/>`_

Requirements
------------

Python 2.7.x or Python 3.3+ interpreter

Current version
---------------

* janome: 0.3.3

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

The return value is a list of Token objects. Token includes morphological information such as surface form, part-of-speech. See `reference <http://mocobeta.github.io/janome/api/janome.html#janome.tokenizer.Token>`_ for more details.

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


Use with user defined dictionary
---------------------------------

MeCab IPADIC format
^^^^^^^^^^^^^^^^^^^

You can add custom entries to the built-in dictionary at runtime by using user defined dictionary.

Default dictionary format is equal to MeCab IPADIC format. Create a CSV file as below and pass the file path and the character encoding to Tokenizer's constructor.

See the `MeCab document <http://taku910.github.io/mecab/dic.html>`_ for more details.

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

For now, there is no tools for compiling user dictionary. Use `APIs <http://mocobeta.github.io/janome/api/janome.html#janome.dic.UserDictionary>`_ as below.

How to compile user dictionary (MeCab IPADIC format): ::

  >>> from janome.dic import UserDictionary
  >>> import sysdic
  >>> user_dict = UserDictionary("userdic.csv", "utf8", "ipadic", sysdic.connections)
  >>> user_dict.save("/tmp/userdic")

How to compile user dictionary (simplified format): ::  

  >>> from janome.dic import UserDictionary
  >>> import sysdic
  >>> user_dict = UserDictionary("user_simpledic.csv", "utf8", "simpledic", sysdic.connections)
  >>> user_dict.save("/tmp/userdic")

Once compiling has been successfully completed, the data is saved in '/tmp/userdic' directory. Pass the directory path to Tokenizer's constructor to use it.

::

  >>> t = Tokenizer("/tmp/userdic")

.. note:: Use same major python version at both compile time and runtime.  Forward/backward dictionary data compatibility is not guaranteed.

Streaming mode (v0.3.1+)
-------------------------

When 'stream = True' option is given to tokenize() method, it runs in streaming mode. In streaming mode, partial analyzed results are returned through `generator <https://wiki.python.org/moin/Generators>`_ interface.

Use this option when you analyze very large text data.

.. code-block:: python

  t = Tokenizer()
  with open('very_large_text.txt') as f:
      txt = f.read()
      for token in t.tokenize(txt, stream=True):
          print(token)


'wakati-gaki' mode (v0.3.1+)
-------------------------------

When 'wakati = True' option is given to tokenize() method, it runs in 'wakati-gaki' ('分かち書き') mode. In wakati-gaki mode, tokenize() method returns sufrace forms only. Return type is list of string, not list of Token.

::

  >>> t = Tokenizer()
  >>> tokens = t.tokenize(u'分かち書きモードがつきました！', wakati=True)
  >>> tokens
  ['分かち書き', 'モード', 'が', 'つき', 'まし', 'た', '！']

If you use 'wakati-gaki' mode only, it is recommended to give 'wakati = True' option to Tokenizer.__init__(). When Tokenizer object is initialized as below, extra information (detailed part of speech, reading, etc.) for tokens are not loaded from dictionary so the memory usage is reduced.

::

  >>> t = Tokenizer(wakati=True)

When this option is set to Tokenizer object, tokenize() method always runs in wakati-gaki mode ('wakati = False' option to tokenize() method is ignored.) 

'wakati-gaki' mode works well with streaming mode. tokenize() method returns generator of string when it is given 'stream=True' and 'wakati=True' options.

.. code-block:: python

  t = Tokenizer()
  for token in t.tokenize(txt, stream=True, wakati=True):
      print(token)


Memory-mapped file support (v0.3.3+)
----------------------------------------

If 'mmap=True' option is given to Tokenizer.__init__(), dictionary entries are not loaded to process space but searched through memory-mapped file.

Use janome from the command-line (v0.2.6+, Lunux/Mac only)
----------------------------------------------------------

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

.. note:: This memory leak problem is solved at v0.3. The analysed results with janome version 0.3 or over can be a bit different from ones with version 0.2. You may want to examine streaming and/or wakati-gaki mode to reduce memory usage more.

In older version (< 0.3), Janome can consume large memory when a very large document is passed all at once. Please split large documents (larger than tens of killobytes) into small chunks or sentences.

FAQ
---

Q. How is the accuracy of analysis?

A. Janome uses MeCab IPADIC dictionary, so the accuracy is roughly same to MeCab.

Q. How is the speed of analysis?

A. Basically depends on the input length. But according to my benchmark script, one sentence would take a few milliseconds to a few tens of milliseconds on desktop computers.

Q. What data structures and algorithms are used?

A. Janome uses FST (`Minimal Acyclic Subsequential Transducer <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698>`_) for internal dictionary data structure. I implemented the automaton by referring to `Apache Lucene <https://lucene.apache.org/core/>`_ (written in Java) and `kagome <https://github.com/ikawaha/kagome>`_ (written in Go). And for analysis engine, I implemented basic viterbi algorithm by referring the book `自然言語処理の基礎 <http://www.amazon.co.jp/%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%81%AE%E5%9F%BA%E7%A4%8E-%E5%A5%A5%E6%9D%91-%E5%AD%A6/dp/4339024511>`_ .

Q. I found bugs. Or have requests for enhancement.

A. Bug reports and requests (and of course, patches) are welcome. Create issues in `Github repository <https://github.com/mocobeta/janome/issues>`_ or contact to `@moco_beta <https://twitter.com/moco_beta>`_.

For Contributors
----------------

See `https://github.com/mocobeta/janome/wiki <https://github.com/mocobeta/janome/wiki>`_

License
------------

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See `LICENSE.txt <https://github.com/mocobeta/janome/blob/master/LICENSE.txt>`_ and `NOTICE.txt <https://github.com/mocobeta/janome/blob/master/NOTICE.txt>`_ for license details.


Copyright
-----------

Copyright(C) 2015, moco_beta. All rights reserved.

History
----------

* 2017.07.23 janome Version 0.3.3 was released
* 2017.07.05 janome Version 0.3.2 was released 
* 2017.07.02 janome Version 0.3.1 was released
* 2017.06.30 janome Version 0.3.0 was released
* 2016.05.07 janome Version 0.2.8 was released
* 2016.03.05 janome Version 0.2.7 was released
* 2015.10.26 janome Version 0.2.6 was released
* 2015.05.11 janome Version 0.2.5 was released
* 2015.05.03 janome Version 0.2.4 was released
* 2015.05.03 janome Version 0.2.3 was released
* 2015.04.24 janome Version 0.2.2 was released
* 2015.04.24 janome Version 0.2.0 was released
* 2015.04.11 janome Version 0.1.4 was released
* 2015.04.08 janome Version 0.1.3 was released

Change details: `CHANGES <https://github.com/mocobeta/janome/blob/master/CHANGES.txt>`_

.. image:: bronze-25C9.png
   :alt: Badge(FISHEYE)
   :target: http://www.unicode.org/consortium/adopt-a-character.html	 

`About this badge <http://mocobeta-backup.tumblr.com/post/153598031477/u-25c9-sponsorship-en>`_

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

