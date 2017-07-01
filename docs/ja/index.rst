.. janome documentation master file, created by
   sphinx-quickstart on Tue Apr  7 21:28:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: strike

Welcome to janome's documentation! (Japanese)
==============================================

`English <http://mocobeta.github.io/janome/en/>`_

Janome とは
-----------

Janome (蛇の目) は, Pure Python で書かれた, 辞書内包の形態素解析器です.

依存ライブラリなしで簡単にインストールでき, アプリケーションに組み込みやすいシンプルな API を備える形態素解析ライブラリを目指しています.

内包辞書として mecab-ipadic-2.7.0-20070801 を使っています.

ソースコードリポジトリ
--------------------------

`https://github.com/mocobeta/janome <https://github.com/mocobeta/janome>`_

API リファレンス
--------------------------

`http://mocobeta.github.io/janome/api/ <http://mocobeta.github.io/janome/api/>`_


動作に必要なソフトウェア
--------------------------

Python 2.7.x または Python 3.3+ インタプリタ

バージョン
-----------------

* janome: 0.3.1

インストール
---------------

PyPI
^^^^

.. note:: pip でのビルド時に 500 ~ 600 MB 程度のメモリを必要とします. 利用可能なメモリ容量にご注意ください. (バージョン 0.2.6 より, RAM 2GB 程度のマシンや 32 bit 環境でもインストールできるようになりました.)

`https://pypi.python.org/pypi/Janome <https://pypi.python.org/pypi/Janome>`_

.. code-block:: bash

  $ pip install janome


使い方
-----------

janome.tokenizer パッケージの Tokenizer オブジェクトを作り, tokenize() メソッドに解析したい文字列を渡します.

戻り値は Token オブジェクトのリストです. Token は表層形や品詞といった形態素情報を含みます. 詳しくは `リファレンス <http://mocobeta.github.io/janome/api/janome.html#janome.tokenizer.Token>`_ を参照してください。

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

文字化けする場合は decode('utf8') をかけてください.

::

  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize(u'すもももももももものうち'):
  ...     print(str(token).decode('utf8'))


ユーザー定義辞書を使う
-------------------------

MeCab IPADIC フォーマット
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトユーザー定義辞書のフォーマットは, MeCab 辞書と同じです. たとえば以下のような CSV ファイルを作成し, Tokenizer クラスの初期化時にファイルパスとエンコーディングを指定します.

辞書フォーマットは MeCab の `ドキュメント <http://taku910.github.io/mecab/dic.html>`_ をご参照ください.

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

簡略辞書フォーマット (v0.2.7 以上)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kuromoji のユーザー辞書に似た, 簡略化された辞書フォーマットです(ただし Janome には search mode がないため, search mode 用の項目はありません). 表層形, 品詞, 読みのみを記述し, 詳細品詞やスコアは指定できません.

簡略辞書フォーマットを使うには,以下のような「<表層形>,<品詞>,<読み>」を並べた CSV ファイルを用意し, Tokenizer 初期化時にファイルパスと辞書タイプ(udic_type='simpledic')を指定してください.

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


コンパイル済みのユーザー辞書を使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ユーザー定義辞書は, 巨大になるとバイナリコンパイルに時間がかかるため, あらかじめコンパイルしておき, コンパイル済みの辞書を使うことも可能です.

現在のところ, コンパイルのためのツールはありませんが, `API <http://mocobeta.github.io/janome/api/janome.html#janome.dic.UserDictionary>`_ を使ってコンパイルが行えます.

.. note:: v0.3.1 から, ユーザー辞書コンパイル時の API が少し変わっているため注意してください.

辞書のコンパイル(MeCab IPADIC format) ::

  >>> from janome.dic import UserDictionary
  >>> import sysdic
  >>> user_dict = UserDictionary("userdic.csv", "utf8", "ipadic", sysdic.connections)
  >>> user_dict.save("/tmp/userdic")

辞書のコンパイル(simplified format) ::

  >>> from janome.dic import UserDictionary
  >>> import sysdic
  >>> user_dict = UserDictionary("user_simpledic.csv", "utf8", "simpledic", sysdic.connections)
  >>> user_dict.save("/tmp/userdic")

これで, /tmp/userdic 以下にコンパイル済みのユーザー辞書が保存されます. 使うときは Tokenizer のコンストラクタにディレクトリのパスを指定します.

::

  >>> t = Tokenizer("/tmp/userdic")

.. note:: コンパイル済みユーザー辞書は, コンパイル時と読み取り時で同一のメジャーバージョンの Python を使ってください. 辞書の前方/後方互換性は保証されないため, Python のメジャーバージョンが異なると読めない可能性があります.

ストリームモード (v0.3.1 以上)
-------------------------------------------------------

tokenize() メソッドに 'stream = True' オプションを与えると, ストリームモードで動作します．ストリームモードでは, 部分的な解析が完了する都度, 解析結果を返します. 戻り値はリストではなく `generator <https://wiki.python.org/moin/Generators>`_ になります．

内部的にすべての Token のリストを保持しなくなるため, 巨大な文書を解析する場合に使うと, メモリ消費量が一定以下に抑制されます.

.. code-block:: python

  t = Tokenizer()
  with open('very_large_text.txt') as f:
      txt = f.read()
      for token in t.tokenize(txt, stream=True):
          print(token)


分かち書きモード (v0.3.1 以上)
--------------------------------------------------------

tokenize() メソッドに 'wakati = True' オプションを与えると, 分かち書きモード（表層形のみを返すモード）で動作します. 分かち書きモードで解析した場合の戻り値は, Token オブジェクトのリストではなく文字列のリストになります.

::

  >>> t = Tokenizer()
  >>> tokens = t.tokenize(u'分かち書きモードがつきました！', wakati=True)
  >>> tokens
  ['分かち書き', 'モード', 'が', 'つき', 'まし', 'た', '！']

分かち書きモードしか使わない場合, Tokenizer オブジェクト初期化時に 'wakati = True' オプションを与えると, 詳細品詞・読みなど, 不要なデータを辞書からロードしなくなります. 普通にすべての辞書データをロードして初期化した場合より, 少し（50MB程度）メモリ使用量が抑制されます.

::

  >>> t = Tokenizer(wakati=True)

なお, このオプションを与えて Tokenizer を初期化した場合, tokenize() メソッドは常に分かち書きモードで動作します（tokenize 時に 'wakati = False' と指定しても無視されます）.

分かち書きモードはストリームモードと併用することができます.

.. code-block:: python

  t = Tokenizer()
  for token in t.tokenize(txt, stream=True, wakati=True):
      print(token)


コマンドラインから使う (v0.2.6 以上, Lunux/Mac only)
--------------------------------------------------------

コマンドラインから実行可能なスクリプト janome がついています. (Linux/Mac のみ. Windows 版(bat)は少々お待ちください.)

簡単に動作を確認したいときにお使いください.

標準入力から文字列を受け取り、形態素解析を実行します. 指定できるオプションを見るには "janome -h" とタイプしてください.

::

    (env)$ janome
    猫は液体である
    猫    名詞,一般,*,*,*,*,猫,ネコ,ネコ
    は    助詞,係助詞,*,*,*,*,は,ハ,ワ
    液体  名詞,一般,*,*,*,*,液体,エキタイ,エキタイ
    で    助動詞,*,*,*,特殊・ダ,連用形,だ,デ,デ
    ある  助動詞,*,*,*,五段・ラ行アル,基本形,ある,アル,アル
    (Ctrl-C で終了)


大きな文書を解析する際の注意 (v0.2.8 以下)
---------------------------------------------------------

.. note:: バージョン 0.3 では，大きな文書を解析したときにメモリを大量に消費（リーク）してしまう問題が解決されました. 内部バッファに収まらないサイズの文書が与えられた場合, 部分的に解析することでメモリ使用量を抑制しています. この修正の影響で, 0.2 系と 0.3 系以上 では, 大きなドキュメントを解析したときの解析結果が若干異なる可能性があります. よりメモリ使用量を抑制したい場合は「ストリームモード」を使ってください.

古いバージョン(< 0.3)では, 入力全体を読んでラティスを構築するため, 入力文字列が大きくなると多くのリソースを消費します. 数十キロバイト以上の文書を解析する場合は, なるべく適度に分割して与えてください. 

よくある（かもしれない）質問
---------------------------------

Q. Tokenizer の初期化が遅いんだけど.

A. インタプリタ起動直後の, 初回の Tokenizer インスタンス生成時に, システム辞書を読み込むのですが, 現在のバージョンでは1~2秒かかる仕様です. 2回目以降はシステム辞書がすでに読み込まれているため速くなります. 今後改善していきたいのですが, 現行ではご勘弁ください. (そのため, インタプリタをしょっちゅう再起動するようなユースケースだと厳しいです.)

Q. 解析結果の精度は.

A. 辞書, 言語モデルともに MeCab のデフォルトシステム辞書をそのまま使わせていただいているため, バグがなければ, MeCab と同等の解析結果になると思います.

Q. 形態素解析の速度は.

A. 文章の長さによりますが, 手元の PC では 1 センテンスあたり数ミリ〜数十ミリ秒でした. mecab-python の10倍程度(長い文章だとそれ以上)遅い, というくらいでしょうか. 性能向上させていきたいですが, いまのところは速度を追うのがメインの目的ではないです.

Q. 実装（データ構造, アルゴリズム）について.

A. 辞書は, FST (正確には Minimal Acyclic Subsequential Transducer, `論文 <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698>`_) を使っています. 実装は `Apache Lucene <https://lucene.apache.org/core/>`_ (Kuromoji) と `kagome <https://github.com/ikawaha/kagome>`_ を参考にさせていただきました. エンジンはオーソドックスなビタビで, ほぼ `自然言語処理の基礎 <http://www.amazon.co.jp/%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%81%AE%E5%9F%BA%E7%A4%8E-%E5%A5%A5%E6%9D%91-%E5%AD%A6/dp/4339024511>`_ の3章だけ読んで書きました.

Janome は Lucene の単語辞書やクエリパーサで使われている FST について調べていて生まれました. もしも内部実装にご興味があれば, 以下もどうぞ.

* `Lucene FST のアルゴリズム (1) ～図解編～ <http://mocobeta-backup.tumblr.com/post/111076688132/lucene-fst-1>`_
* `Lucene FST のアルゴリズム (2) 〜実装編〜 <http://mocobeta-backup.tumblr.com/post/113693778372/lucene-fst-2>`_
* `Pyconjp2015 - Python で作って学ぶ形態素解析 <http://www.slideshare.net/tomokouchida505/pyconjp2015-python>`_

Q. Python 2 系への対応は.

A. デスヨネー. => 対応しました. janomePy2 をご利用ください. => janome 本体が Python2.7 にも対応しました.

Q. 学習器ついてないの.

A. 今のところありません.

Q. Janome ってどういう意味.

A. ikawaha さんの, Go で書かれた形態素解析器 kagome にあやかりつつ, 蛇(Python)をかけて命名しました. 日本語のJaともかかっているのは takuya-a さんに言われて気づきました :)

Q. `neologd <https://github.com/neologd/mecab-ipadic-neologd>`_ 内包版はないの.

A. やりたいです!

Q. バグ見つけた or なんか変 or 改善要望

A. `@moco_beta <https://twitter.com/moco_beta>`_ 宛につぶやくか, Github リポジトリに `Issue <https://github.com/mocobeta/janome/issues>`_ 立ててください.

For Contributors
----------------

See `https://github.com/mocobeta/janome/wiki <https://github.com/mocobeta/janome/wiki>`_

やりたいことリスト
---------------------

* 単語グラフ(ラティス)の可視化
* neologd 対応
* UniDic 対応
* N-Best パス
* API ドキュメント
* SEARCH モード (検索のリコール向上を目的としたモード)
* Lucene の Analyzer みたいに, 文字フィルタやトークンフィルタがあったら便利そう

License
------------

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See `LICENSE.txt <https://github.com/mocobeta/janome/blob/master/LICENSE.txt>`_ and `NOTICE.txt <https://github.com/mocobeta/janome/blob/master/NOTICE.txt>`_ for license details.


Copyright
-----------

Copyright(C) 2015, moco_beta. All rights reserved.

History
----------

* 2017.07.02 janome Version 0.3.1 リリース
* 2017.06.30 janome Version 0.3.0 リリース
* 2016.05.07 janome Vesrion 0.2.8 リリース
* 2016.03.05 janome Version 0.2.7 リリース
* 2015.10.26 janome Version 0.2.6 リリース
* 2015.05.11 janome Version 0.2.5 リリース
* 2015.05.03 janome Version 0.2.4 リリース
* 2015.05.03 janome Version 0.2.3 リリース
* 2015.04.24 janome Version 0.2.2 リリース
* 2015.04.24 janome Version 0.2.0 リリース / janomePy2 は deprecated (数日中に PyPI から削除します.)
* 2015.04.11 janome Version 0.1.4 リリース / janomePy2 0.1.4 公開
* 2015.04.08 janome Version 0.1.3 公開

詳細: `CHANGES <https://github.com/mocobeta/janome/blob/master/CHANGES.txt>`_

.. image:: bronze-25C9.png
   :alt: Badge(FISHEYE)
   :target: http://www.unicode.org/consortium/adopt-a-character.html

`このバッジについて <http://mocobeta-backup.tumblr.com/post/145913418922/u-25c9-sponsorship>`_

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

