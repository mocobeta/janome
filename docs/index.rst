.. janome documentation master file, created by
   sphinx-quickstart on Tue Apr  7 21:28:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: strike

Welcome to janome's documentation!
==================================

janome とは
-----------

janome (蛇の目) は, Pure Python で書かれた, 辞書内包の形態素解析器です.

依存ライブラリなしで簡単にインストールでき, アプリケーションに組み込みやすいシンプルな API を備える形態素解析ライブラリを目指しています.

内包辞書として mecab-ipadic-2.7.0-20070801 を使っています.

ソースコードリポジトリ
--------------------------

`https://github.com/mocobeta/janome <https://github.com/mocobeta/janome>`_


動作に必要なソフトウェア
--------------------------

Python 2.7 または Python 3.4+ インタプリタ

バージョン
-----------------

:strike:`janome (for Python 3) と janomePy2 (for Python 2.7) があります. minor version が同じなら同等の動作をします.`

janome が Python 2.7, Python 3.4 両方に対応したので, janomePy2 は不要になりました. Python 2.7 系, 3 系のどちらでも janome をご利用ください.

* janome: 0.2.6
* :strike:`janomePy2: 0.1.4`

インストール
---------------

PyPI
^^^^

:strike:`pip でのビルド時に 3~4 GB程度のメモリを必要とします. 貧弱なマシンや, 他の重い処理が走っているときに同時にビルドするとマシンが凍る可能性がありますのでご注意ください. (改善検討中...)`

:strike:`上記の理由により, 現行バージョンでは 32 bit 版 Python だとビルド時に Meomory Error でこけます. 64 bit 版を使ってください.`

.. note:: pip でのビルド時に 500 ~ 600 MB 程度のメモリを必要とします. 利用可能なメモリ容量にご注意ください. (バージョン 0.2.6 より, RAM 2GB 程度のマシンや 32 bit 環境でもインストールできるようになりました.)

`https://pypi.python.org/pypi/Janome <https://pypi.python.org/pypi/Janome>`_

.. code-block:: bash

  $ pip install janome

:strike:`for Python 2.7 users: https://pypi.python.org/pypi/JanomePy2`


使い方
-----------

janome.tokenizer パッケージの Tokenizer オブジェクトを作り, tokenize() メソッドに解析したい文字列を渡します.

戻り値は Token オブジェクトのリストです. Token は表層形や品詞といった形態素情報を含みます. 詳しくは dir() や `ソースコード <https://github.com/mocobeta/janome/blob/master/janome/tokenizer.py>`_ をご参照ください.

::

  (venv) $ python
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

  > python
  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize(u'すもももももももものうち'):
  ...     print(str(token).decode('utf8'))


ユーザー定義辞書を使う
-------------------------

ユーザー定義辞書のフォーマットは, MeCab 辞書と同じです. たとえば以下のような CSV ファイルを作成し, Tokenizer クラスの初期化時にファイルパスとエンコーディングを指定します.

辞書フォーマットは MeCab の `ドキュメント <http://mecab.googlecode.com/svn/trunk/mecab/doc/dic.html>`_ をご参照ください.

userdic.csv ::

  東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
  東武スカイツリーライン,1288,1288,4700,名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン
  とうきょうスカイツリー駅,1288,1288,4143,名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ

::

  (venv) $ python
  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer(udic="userdic.csv", udic_enc="utf8")
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


コンパイル済みのユーザー辞書を使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ユーザー定義辞書は, 巨大になるとバイナリコンパイルに時間がかかるため, あらかじめコンパイルしておき, コンパイル済みの辞書を使うことも可能です.

現在のところ, コンパイルのためのツールはありませんが, API を使ってコンパイルが行えます.

辞書のコンパイル ::

  >>> from janome.dic import UserDictionary
  >>> from sysdic import SYS_DIC
  >>> user_dict = UserDictionary("userdic.csv", "utf8", "ipadic", SYS_DIC.connections)
  >>> user_dict.save("/tmp/userdic")

これで, /tmp/userdic 以下にコンパイル済みのユーザー辞書が保存されます. 使うときは Tokenizer のコンストラクタにディレクトリのパスを指定します.

::

  >>> t = Tokenizer("/tmp/userdic")

.. note:: コンパイル済みユーザー辞書は, コンパイル時と読み取り時で同一のメジャーバージョンの Python を使ってください. 辞書の前方/後方互換性は保証されないため, Python のメジャーバージョンが異なると読めない可能性があります.

コマンドラインから使う (experimental)
------------------------------------------

v0.2.6 より, コマンドラインから実行可能なスクリプト janome がついています. (Linux/Mac のみ. Windows 版(bat)は少々お待ちください.)

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


大きな文書を解析する際の注意
--------------------------------

現行バージョン(0.2系)では, 入力全体を読んでラティスを構築するため, 入力文字列が大きくなると多くのリソースを消費します. 数十キロバイト以上の文書を解析する場合は, なるべく適度に分割して与えてください. 次のバージョン(0.3系)で, 大きな入力が与えられた場合は, 部分的な解析を行う(最適解を求めることを諦め, 近似解を求める)ことでメモリ消費を一定以下に抑える回避策をとる予定です.

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

* 2015.10.26 janome Version 0.2.6 リリース
* 2015.05.11 janome Version 0.2.5 リリース
* 2015.05.03 janome Version 0.2.4 リリース
* 2015.05.03 janome Version 0.2.3 リリース
* 2015.04.24 janome Version 0.2.2 リリース
* 2015.04.24 janome Version 0.2.0 リリース / janomePy2 は deprecated (数日中に PyPI から削除します.)
* 2015.04.11 janome Version 0.1.4 リリース / janomePy2 0.1.4 公開
* 2015.04.08 janome Version 0.1.3 公開

詳細: `CHANGES <https://github.com/mocobeta/janome/blob/master/CHANGES.txt>`_

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

