.. janome documentation master file, created by
   sphinx-quickstart on Tue Apr  7 21:28:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: strike

.. meta::
  :description: Janome (蛇の目; ◉) は，Pure Python で書かれた，辞書内包の形態素解析器です。依存ライブラリなしで簡単にインストールでき，アプリケーションに組み込みやすいシンプルな API を備える形態素解析ライブラリを目指しています。
  :keywords: python, janome, 形態素解析
  :http-equiv=Content-Type: text/html; charset=UTF-8

Welcome to janome's documentation! (Japanese)
==============================================

`English <http://janome.mocobeta.dev/en/>`_

Janome とは
-----------

.. image:: ../img/janome_small.jpg
  :scale: 20
  :align: right

Janome (蛇の目; ◉) は，Pure Python で書かれた，辞書内包の形態素解析器です。

依存ライブラリなしで簡単にインストールでき，アプリケーションに組み込みやすいシンプルな API を備える形態素解析ライブラリを目指しています。

内包辞書として mecab-ipadic-2.7.0-20070801 を使っています。なお，v0.3.8+ では新元号「令和」がシステム辞書に追加されています。

ソースコードリポジトリ
--------------------------

`https://github.com/mocobeta/janome <https://github.com/mocobeta/janome>`_

気に入ったらリポジトリにも★つけていってください！ :)

API リファレンス
--------------------------

`https://janome.mocobeta.dev/reference/ <http://janome.mocobeta.dev/reference/>`_


動作に必要なソフトウェア
--------------------------

Python 3.7+ インタプリタ

最新バージョン
-----------------

* 0.5.0

インストール
---------------

PyPI
^^^^

`https://pypi.python.org/pypi/Janome <https://pypi.python.org/pypi/Janome>`_

.. code-block:: bash

  $ pip install janome

.. note:: 

  pip でのビルド時に 500 ~ 600 MB 程度のメモリを必要とします。利用可能なメモリ容量にご注意ください。（バージョン 0.2.6 より，RAM 2GB 程度のマシンや 32 bit 環境でもインストールできるようになりました。）


チュートリアル
------------------

初心者向けチュートリアル＆ハンズオン教材「Janome ではじめるテキストマイニング」を公開しました。

* `GitHub リポジトリ <https://github.com/mocobeta/janome-tutorial>`_
* `チュートリアル資料(HTML) <http://mocobeta.github.io/slides-html/janome-tutorial/tutorial-slides.html>`_

ハンズオンには Google Colab を使っており Web ブラウザがあれば実行できます。janome CLI / API の基本的な使い方，ユーザー辞書・ワードカウント・Analyzer など janome の少しだけ高度な使い方，日本語 WordCloud といった内容について，手を動かしながら身につけられます。

使い方
-----------

janome.tokenizer パッケージの Tokenizer オブジェクトを作り，tokenize() メソッドに解析したい文字列を渡します。

戻り値は Token オブジェクトのイテレータ (generator) です。Token は表層形や品詞といった形態素情報を含みます。詳しくは `リファレンス <http://janome.mocobeta.dev/reference/janome.html#janome.tokenizer.Token>`_ を参照してください。

::

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

for Windows users
^^^^^^^^^^^^^^^^^

文字化けする場合は ``decode('utf8')`` をかけてください。

::

  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer()
  >>> for token in t.tokenize('すもももももももものうち'):
  ...     print(str(token).decode('utf8'))


ユーザー定義辞書を使う
-------------------------

MeCab IPADIC フォーマット
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトユーザー定義辞書のフォーマットは，MeCab 辞書と同じです。たとえば以下のような CSV ファイルを作成し，Tokenizer クラスの初期化時にファイルパスとエンコーディングを指定します。

辞書フォーマットは MeCab の `ドキュメント <http://taku910.github.io/mecab/dic.html>`_ をご参照ください。

userdic.csv ::

  東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
  東武スカイツリーライン,1288,1288,4700,名詞,固有名詞,一般,*,*,*,東武スカイツリーライン,トウブスカイツリーライン,トウブスカイツリーライン
  とうきょうスカイツリー駅,1288,1288,4143,名詞,固有名詞,一般,*,*,*,とうきょうスカイツリー駅,トウキョウスカイツリーエキ,トウキョウスカイツリーエキ

::

  >>> from janome.tokenizer import Tokenizer
  >>> t = Tokenizer("userdic.csv", udic_enc="utf8")
  >>> for token in t.tokenize('東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便利です。'):
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

**[参考リンク]**

* `データ解析、プログラミング学習中: Janomeのユーザー辞書を作る <http://eneprog.blogspot.com/2018/08/janomepython.html>`_ (ユーザー辞書ファイルの作成方法)
  
  * 補足: こちらの記事では左/右文脈ID に -1 を指定していますが，`MeCab: 単語の追加方法 <http://taku910.github.io/mecab/dic.html>`_ に記載のように，MeCab IPADIC に含まれる ``left-id.def`` (または ``right-id.def``) から該当する品詞IDを選ぶ (例：「名詞,固有名詞,一般」なら 1288) とコスト計算がより適切になるでしょう。

* `データ解析、プログラミング学習中: エネルギー基本計画の特徴を見てみる。その4 複合語を考慮してwordcloud <http://eneprog.blogspot.com/2018/09/4-wordcloudpythonjanome.html>`_ (ユーザー辞書の活用例)

簡略辞書フォーマット (v0.2.7 以上)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Kuromoji <https://www.atilika.com/ja/kuromoji/>`_ のユーザー辞書に似た，簡略化された辞書フォーマットです（ただし Janome には search mode がないため，search mode 用の項目はありません）。表層形，品詞，読みのみを記述し，詳細品詞やスコアは指定できません。

簡略辞書フォーマットを使うには，以下のような「*<表層形>,<品詞>,<読み>*」を並べた CSV ファイルを用意し，Tokenizer 初期化時にファイルパスと辞書タイプ（``udic_type='simpledic'``）を指定してください。

user_simpledic.csv ::

   東京スカイツリー,カスタム名詞,トウキョウスカイツリー
   東武スカイツリーライン,カスタム名詞,トウブスカイツリーライン
   とうきょうスカイツリー駅,カスタム名詞,トウキョウスカイツリーエキ

::

   >>> from janome.tokenizer import Tokenizer
   >>> t = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
   >>> for token in t.tokenize('東京スカイツリーへのお越しは、東武スカイツリーライン「とうきょうスカイツリー駅」が便 利です。'):
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

ユーザー定義辞書は，巨大になるとバイナリコンパイルに時間がかかるため，あらかじめコンパイルしておき，コンパイル済みの辞書を使うことも可能です。

現在のところ，コンパイルのためのツールはありませんが， `API <http://janome.mocobeta.dev/reference/janome.html#janome.dic.UserDictionary>`_ を使ってコンパイルが行えます。 ``progress_handler`` オプションは v0.4.1 以上でサポートされます。

辞書のコンパイル(MeCab IPADIC format) ::

  >>> from janome.dic import UserDictionary
  >>> from janome.progress import SimpleProgressIndicator
  >>> from janome import sysdic
  >>> user_dict = UserDictionary("userdic.csv", "utf8", "ipadic", sysdic.connections, progress_handler=SimpleProgressIndicator(update_frequency=0.01))
  Reading user dictionary from CSV: 100.0% | 17149/17149
  Running create_minimum_transducer: 100.0% | 17149/17149
  >>> user_dict.save("/tmp/userdic")

辞書のコンパイル(simplified format) ::

  >>> from janome.dic import UserDictionary
  >>> from janome.progress import SimpleProgressIndicator
  >>> from janome import sysdic
  >>> user_dict = UserDictionary("user_simpledic.csv", "utf8", "simpledic", sysdic.connections, progress_handler=SimpleProgressIndicator(update_frequency=0.01))
  Reading user dictionary from CSV: 100.0% | 17149/17149
  Running create_minimum_transducer: 100.0% | 17149/17149
  >>> user_dict.save("/tmp/userdic")

これで， */tmp/userdic* 以下にコンパイル済みのユーザー辞書が保存されます。使うときは Tokenizer のコンストラクタにディレクトリのパスを指定します。

::

  >>> t = Tokenizer("/tmp/userdic")

.. note:: コンパイル済みユーザー辞書は，コンパイル時と読み取り時で同一のメジャーバージョンの Python を使ってください。辞書の前方/後方互換性は保証されないため，Python のメジャーバージョンが異なると読めない可能性があります。

Analyzer フレームワーク (v0.3.4 以上)
----------------------------------------------------------------

Analyzer は，形態素解析の前処理・後処理をテンプレ化するためのフレームワークです。Analyzer フレームワークは下記のクラスを含みます。

* 文字の正規化などの前処理を行う `CharFilter <http://janome.mocobeta.dev/reference/janome.html#janome.charfilter.CharFilter>`_ クラス
* 小文字化，品詞によるトークンのフィルタリングなど，形態素解析後の後処理を行う `TokenFilter <http://janome.mocobeta.dev/reference/janome.html#janome.tokenfilter.TokenFilter>`_ クラス
* CharFilter, Tokenizer, TokenFilter を組み合わせてカスタム解析フローを組み立てる `Analyzer <http://janome.mocobeta.dev/reference/janome.html#janome.analyzer.Analyzer>`_ クラス

Analyzer の使い方
^^^^^^^^^^^^^^^^^^^^

Analyzer 初期化時に，CharFilter のリスト，初期化済み Tokenizer オブジェクト，TokenFilter のリストを指定します。0 個以上，任意の数の CharFilter や TokenFilter を指定できます。
Analyzer を初期化したら，analyze() メソッドに解析したい文字列を渡します。戻り値はトークンの generator です（最後に指定した TokenFilter の出力により，generator の返す要素の型が決まります）。

以下の実行例では，前処理としてユニコード正規化と正規表現による文字列置換を行い，形態素解析を実行後に，名詞の連続のまとめあげ（複合名詞化），品詞によるフィルタリング，表層形の小文字化という後処理を行っています。

.. note:: CharFilter や TokenFilter は，リストに指定した順で適用されるため，順番には注意してください。

::

  >>> from janome.tokenizer import Tokenizer
  >>> from janome.analyzer import Analyzer
  >>> from janome.charfilter import *
  >>> from janome.tokenfilter import *
  >>> text = '蛇の目はPure Ｐｙｔｈｏｎな形態素解析器です。'
  >>> char_filters = [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter('蛇の目', 'janome')]
  >>> tokenizer = Tokenizer()
  >>> token_filters = [CompoundNounFilter(), POSStopFilter(['記号','助詞']), LowerCaseFilter()]
  >>> a = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
  >>> for token in a.analyze(text):
  ...     print(token)
  ... 
  janome  名詞,固有名詞,組織,*,*,*,*,*,*
  pure    名詞,固有名詞,組織,*,*,*,*,*,*
  python  名詞,一般,*,*,*,*,*,*,*
  な       助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ
  形態素解析器  名詞,複合,*,*,*,*,形態素解析器,ケイタイソカイセキキ,ケイタイソカイセキキ
  です     助動詞,*,*,*,特殊・デス,基本形,です,デス,デス


Analyzer の利用例: ワードカウント (v0.3.5 以上)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TokenCountFilter を使うと，入力文字列中の単語出現頻度を数えることができます。以下は，文字列中の名詞の出現回数を数える例です（POSKeepFilterで名詞のみフィルタしています）。戻り値の各要素は，単語（表層形）とその出現回数のタプルになります。

::

  >>> from janome.tokenizer import Tokenizer
  >>> from janome.analyzer import Analyzer
  >>> from janome.tokenfilter import *
  >>> text = 'すもももももももものうち'
  >>> token_filters = [POSKeepFilter(['名詞']), TokenCountFilter()]
  >>> a = Analyzer(token_filters=token_filters)
  >>> for k, v in a.analyze(text):
  ...   print('%s: %d' % (k, v))
  ...
  すもも: 1
  もも: 2
  うち: 1

TokenCountFilter の初期化時に ``sorted=True`` を指定すると，出現回数の多い順に返されます。ソートの計算コストがかかるため，出現回数でのソートが不要の場合は False としてください。指定がない場合のデフォルト値は False です。

::

  >>> token_filters = [TokenCountFilter(sorted=True)]

また， TokenCountFilter 初期化時に ``att='base_form'`` を指定すると，基本形の数を数えます。動詞や形容動詞の数を数えたい場合は，このオプションを指定すると良いでしょう。指定がない場合のデフォルト値は ``surface`` (表層形) です。

::

  >>> token_filters = [TokenCountFilter(att='base_form')]

その他，組み込みの CharFilter や TokenFilter についてはリファレンスを参照してください。また，CharFilter や TokenFilter を拡張すれば，任意のフィルター処理を実装することもできます。

**[参考リンク]**

* `け日記：Python janomeのanalyzerが便利 <http://ohke.hateblo.jp/entry/2017/11/02/230000>`_ (Analyzer 活用，独自フィルターの作成について詳しく解説されています。)
* `データ解析、プログラミング学習中: janome Analayzerで複合語（複合名詞）を考慮して形態素解析を行う。 <http://eneprog.blogspot.com/2018/07/janome-analayzerpython.html>`_ (CompoundNounFilter の活用例があります。)

ストリーミングモード (v0.3.1 以上 v0.3.10 まで)
-------------------------------------------------------

.. note:: v0.4.0 から，ストリーミングモードのみサポートしており， ``stream`` オプションは廃止されました。

tokenize() メソッドに ``stream = True`` オプションを与えると，ストリーミングモードで動作します。ストリーミングモードでは，部分的な解析が完了する都度，解析結果を返します。戻り値はリストではなく `generator <https://wiki.python.org/moin/Generators>`_ になります。

内部的にすべての Token のリストを保持しなくなるため，巨大な文書を解析する場合でも，メモリ消費量が一定以下に抑制されます。

.. code-block:: python

  t = Tokenizer()
  with open('very_large_text.txt') as f:
      txt = f.read()
      for token in t.tokenize(txt, stream=True):
          print(token)


分かち書きモード (v0.3.1 以上)
--------------------------------------------------------

tokenize() メソッドに ``wakati = True`` オプションを与えると，分かち書きモード（表層形のみを返すモード）で動作します。分かち書きモードで解析した場合の戻り値は，Token オブジェクトのリストではなく文字列 (str) のリストになります。

::

  >>> t = Tokenizer()
  >>> tokens = t.tokenize(u'分かち書きモードがつきました！', wakati=True)
  >>> tokens
  ['分かち書き', 'モード', 'が', 'つき', 'まし', 'た', '！']

分かち書きモードしか使わない場合，Tokenizer オブジェクト初期化時に ``wakati = True`` オプションを与えると，詳細品詞・読みなど，不要なデータを辞書からロードしなくなります。普通にすべての辞書データをロードして初期化した場合より，少し（50MB程度）メモリ使用量が抑制されます。

::

  >>> t = Tokenizer(wakati=True)

なお, このオプションを与えて Tokenizer を初期化した場合，tokenize() メソッドは常に分かち書きモードで動作します（tokenize 時に ``wakati = False`` と指定しても無視されます）。

分かち書きモードはストリームモードと併用することができます。その場合の戻り値は文字列 (str) の generator となります。

.. code-block:: python

  t = Tokenizer()
  for token in t.tokenize(txt, stream=True, wakati=True):
      print(token)


(experimental) NEologd 辞書を使う (v0.3.3 以上)
--------------------------------------------------------

NEologd 辞書を内包した janome パッケージを作成する手順を以下で公開しています。実験的なものなので，諸々了解のうえお試しください :)

`NEologd 辞書を内包した janome をビルドする方法 <https://github.com/mocobeta/janome/wiki/(very-experimental)-NEologd-%E8%BE%9E%E6%9B%B8%E3%82%92%E5%86%85%E5%8C%85%E3%81%97%E3%81%9F-janome-%E3%82%92%E3%83%93%E3%83%AB%E3%83%89%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95>`_

v0.3.7 より，janome コマンド (後述) が NEologd 辞書内包版にも対応しました。NEologd 内包版は mmap モード (後述) のみで動作するため， ``-m`` オプションをつけて実行してください。

::

    $ echo "渋谷ヒカリエで待ち合わせ" | janome -m

Memory-mapped file サポート (v0.3.3 以上)
-------------------------------------------------------------------

.. note:: v0.4.0 以上では， 64bit アーキテクチャにおいて ``mmap=True`` がデフォルトになりました（32bit アーキテクチャでのデフォルトは ``False``）。

Tokenizer オブジェクトの初期化時に ``mmap=True`` オプションを与えると，辞書エントリは Memory-mapped file としてアクセスされるようになります。

Tokenizer の初期化時，プロセス空間に辞書エントリをロードしないため，初期化が高速になります。

Graphviz ファイル (DOT ファイル) 出力 (v0.3.7 以上)
-------------------------------------------------------------------

Tokenizer.tokenize() メソッドに ``dotfile=<dotfile output path>`` オプションを与えると，解析時のラティスグラフを `Graphviz <https://graphviz.gitlab.io/>`_ の DOT ファイルに変換して指定のパスに出力します。パフォーマンス上の理由により，ストリーミングモードで実行時，またはとても長いテキストを与えた場合は，このオプションは無視されます。

この機能は，janome コマンド（後述）から利用するのが便利です。

コマンドラインから使う (Linux/Mac v0.2.6 以上，Windows v0.3.7 以上)
-------------------------------------------------------------------

コマンドラインから実行可能なスクリプト ``janome`` がついています。

簡単に動作を確認したいときにお使いください。

標準入力から文字列を受け取り，形態素解析を実行します。指定できるオプションを見るには "janome -h" とタイプしてください。また，"janome --version" でインストールされているバージョンが確認できます(v0.3.7 以上)。

Linux/Mac
^^^^^^^^^

::

    (env)$ janome
    猫は液体である
    猫    名詞,一般,*,*,*,*,猫,ネコ,ネコ
    は    助詞,係助詞,*,*,*,*,は,ハ,ワ
    液体  名詞,一般,*,*,*,*,液体,エキタイ,エキタイ
    で    助動詞,*,*,*,特殊・ダ,連用形,だ,デ,デ
    ある  助動詞,*,*,*,五段・ラ行アル,基本形,ある,アル,アル
    (Ctrl-C で終了)

Windows
^^^^^^^

文字化けする場合， ``-e sjis`` オプションをつけるといいでしょう。

::

    >janome -e sjis
    ウィンドウズでも簡単インストール
    ウィンドウズ    名詞,固有名詞,一般,*,*,*,ウィンドウズ,ウィンドウズ,ウィンドウズ
    で      助詞,格助詞,一般,*,*,*,で,デ,デ
    も      助詞,係助詞,*,*,*,*,も,モ,モ
    簡単    名詞,形容動詞語幹,*,*,*,*,簡単,カンタン,カンタン
    インストール    名詞,一般,*,*,*,*,インストール,インストール,インストール
    (Type Ctrl-Z to quit.)

ラティス可視化
^^^^^^^^^^^^^^^^^

.. note:: この機能を実行するには，Graphviz が必要です。 `こちら <https://graphviz.gitlab.io/download/>`_ の手順で事前にインストールしてください。

``-g`` オプションをつけると，解析後にラティスグラフがファイルに出力されます。デフォルトの出力先はカレントディレクトリ，フォーマットは PNG です。

:: 

    $ echo "カレーは飲み物" | janome -g
    カレー	名詞,一般,*,*,*,*,カレー,カレー,カレー
    は	助詞,係助詞,*,*,*,*,は,ハ,ワ
    飲み物	名詞,一般,*,*,*,*,飲み物,ノミモノ,ノミモノ
    Graph was successfully output to lattice.gv.png

lattice.gv.png (クリックで拡大)

.. image:: ../img/lattice.gv.png
   :scale: 20

ファイルの出力先を指定したい場合は ``--gv-out`` オプションを，Graphviz のフォーマットを指定する場合は ``--gv-format`` オプションをつけてください。サポートされるフォーマットは `Graphviz のドキュメント <https://graphviz.gitlab.io/_pages/doc/info/output.html>`_ を参照してください。

:: 

    $ echo "カレーは飲み物" | janome -g --gv-out /tmp/a.gv --gv-format svg
    ...
    Graph was successfully output to /tmp/a.gv.svg

PyInstaller でアプリケーションにバンドルする (v0.3.9+)
-------------------------------------------------------------

`PyInstaller <https://www.pyinstaller.org/>`_ で janome をアプリケーションにバンドルして，実行可能ファイルとして配布できます。

Tokenizer 初期化時に ``mmap=False`` オプションをつけてください。

::

    (venv) $ janome --version
    janome 0.3.9
    (venv) $ pyinstaller -v
    3.4

    (venv) $ cat test.py 
    # -*- utf-8
    from janome.tokenizer import Tokenizer
    t = Tokenizer(mmap=False)
        for token in t.tokenize('令和元年'):
        print(token)

    (venv) $ pyinstaller --onefile test.py 
    44 INFO: PyInstaller: 3.4
    44 INFO: Python: 3.6.6
    ...

    (venv) $ ls dist/
    test
    (venv) $ ./dist/test 
    令和	名詞,固有名詞,一般,*,*,*,令和,レイワ,レイワ
    元年	名詞,一般,*,*,*,*,元年,ガンネン,ガンネン

よくある（かもしれない）質問
---------------------------------

Q. Tokenizer の初期化が遅いんだけど。

A. インタプリタ起動直後の，初回の Tokenizer インスタンス生成時に，システム辞書を読み込むのですが，現在のバージョンでは1~2秒かかる仕様です。2回目以降はシステム辞書がすでに読み込まれているため速くなります。今後改善していきたいのですが，現行ではご勘弁ください. (そのため, インタプリタをしょっちゅう再起動するようなユースケースだと厳しいです。) => v0.3.3 以上の mmap サポートを使うと初期化が高速になるため，必要に応じて検討ください。

Q. 解析結果の精度は。

A. 辞書，言語モデルともに MeCab のデフォルトシステム辞書をそのまま使わせていただいているため，バグがなければ，MeCab と同等の解析結果になると思います。

Q. 形態素解析の速度は。

A. 文章の長さによりますが，手元の PC では 1 センテンスあたり数ミリ〜数十ミリ秒でした。mecab-python の10倍程度（長い文章だとそれ以上）遅い，というくらいでしょうか。今のところは，大量の文書を高速にバッチ処理する用途には向いていません。MeCab をお使いください。

Q. 実装（データ構造，アルゴリズム）について。

A. 辞書は，FST (正確には Minimal Acyclic Subsequential Transducer, `論文 <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698>`_) を使っています。実装は `Apache Lucene <https://lucene.apache.org/core/>`_ (Kuromoji) と `kagome <https://github.com/ikawaha/kagome>`_ を参考にさせていただきました。エンジンはオーソドックスなビタビで，ほぼ `自然言語処理の基礎 <http://www.amazon.co.jp/%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%81%AE%E5%9F%BA%E7%A4%8E-%E5%A5%A5%E6%9D%91-%E5%AD%A6/dp/4339024511>`_ の3章だけ読んで書きました。

Janome は Lucene の単語辞書やクエリパーサで使われている FST について調べていて生まれました。もしも内部実装にご興味があれば，以下もどうぞ。

* `Pyconjp2015 - Python で作って学ぶ形態素解析 <http://www.slideshare.net/tomokouchida505/pyconjp2015-python>`_

Q. Python 2 系への対応は。

A. デスヨネー。 => 対応しました。janomePy2 をご利用ください。=> janome 本体が Python2.7 にも対応しました。 => v0.4.0 以降，Python 2.7 のサポートは停止されました。

Q. 学習器ついてないの。

A. 今のところありません。

Q. Janome ってどういう意味。

A. ikawaha さんの，Go で書かれた形態素解析器 kagome にあやかりつつ，蛇（Python）をかけて命名しました。日本語の Ja ともかかっているのは takuya-a さんに言われて気づきました :)

Q. `neologd <https://github.com/neologd/mecab-ipadic-neologd>`_ 内包版はないの。

A. やりたいです! => `NEologd 辞書を内包した janome をビルドする方法 <https://github.com/mocobeta/janome/wiki/(very-experimental)-NEologd-%E8%BE%9E%E6%9B%B8%E3%82%92%E5%86%85%E5%8C%85%E3%81%97%E3%81%9F-janome-%E3%82%92%E3%83%93%E3%83%AB%E3%83%89%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95>`_

Q. バグ見つけた or なんか変 or 改善要望

A. `Gitter room <https://gitter.im/janome-python/ja>`_ でつぶやくか，Github リポジトリに `Issue <https://github.com/mocobeta/janome/issues>`_ 立ててください。

For Contributors
----------------

See `https://github.com/mocobeta/janome/blob/master/CONTRIBUTING.md <https://github.com/mocobeta/janome/blob/master/CONTRIBUTING.md>`_

作者について
--------------

`プロフィール <https://blog.mocobeta.dev/about/>`_

License
------------

Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.

See `LICENSE.txt <https://github.com/mocobeta/janome/blob/master/LICENSE.txt>`_ and `NOTICE.txt <https://github.com/mocobeta/janome/blob/master/NOTICE.txt>`_ for license details.


Copyright
-----------

Copyright(C) 2015-2025, Tomoko Uchida. All rights reserved.

History
----------

* 2023.07.01 janome Version 0.5.0 released `[Release Note] <https://github.com/mocobeta/janome/releases/tag/0.5.0>`_
* 2022.02.23 janome Version 0.4.2 released `[Release Note] <https://github.com/mocobeta/janome/releases/tag/0.4.2>`_
* 2020.09.21 janome Version 0.4.1 released
* 2020.08.23 janome Version 0.4.0 released
* 2019.11.03 janome Version 0.3.10 released
* 2019.05.12 janome Version 0.3.9 released
* 2019.04.03 janome Version 0.3.8 released
* 2018.12.11 janome Version 0.3.7 released
* 2017.12.07 janome Version 0.3.6 released
* 2017.08.06 janome Version 0.3.5 released
* 2017.07.29 janome Version 0.3.4 released
* 2017.07.23 janome Version 0.3.3 released
* 2017.07.05 janome Version 0.3.2 released 
* 2017.07.02 janome Version 0.3.1 released
* 2017.06.30 janome Version 0.3.0 released
* 2016.05.07 janome Version 0.2.8 released
* 2016.03.05 janome Version 0.2.7 released
* 2015.10.26 janome Version 0.2.6 released
* 2015.05.11 janome Version 0.2.5 released
* 2015.05.03 janome Version 0.2.4 released
* 2015.05.03 janome Version 0.2.3 released
* 2015.04.24 janome Version 0.2.2 released
* 2015.04.24 janome Version 0.2.0 released
* 2015.04.11 janome Version 0.1.4 released
* 2015.04.08 janome Version 0.1.3 released

詳細: `CHANGES <https://github.com/mocobeta/janome/blob/master/CHANGES.txt>`_

.. image:: ../img/bronze-25C9.png
   :alt: Badge(FISHEYE)
   :target: https://home.unicode.org/adopt-a-character/about-adopt-a-character/
