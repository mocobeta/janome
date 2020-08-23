"""
This was contributed by @roy-freee.

zipアーカイブから直接ロードする方法

準備: wheelを作る(手動でパッケージをzip圧縮してもいい)
$ pip wheel . --no-deps --no-binary
もしくは、
$ python setup.py bdist_wheel --universal
出来上がった.whlファイルを使う

[制限事項] mmap=False を指定した場合のみ有効です。(NEologd 同梱 janome に zip import は適用できません。)

How to import the zip archive

You first build a wheel via `pip` command or `setup.py bdist_wheel`:
$ pip wheel . --no-deps --no-binary
$ python setup.py bdist_wheel --universal

You can also create a zip archived package by yourself.

[Limitation] only supported on mmap=False.
"""

import janome.tokenizer
from janome.tokenizer import Tokenizer
import sys
import glob

ARCHIVE_NAME = 'Janome-*.whl'

archive_path = glob.glob(ARCHIVE_NAME)[0]

# avoiding conflict to existing package
sys.path.insert(0, archive_path)

# mmap option shold be set to False
t = Tokenizer(mmap=False)
for token in t.tokenize('すもももももももものうち'):
    print(token)

print(janome.tokenizer.__file__)
# => Like './Janome-xxx.whl/janome/tokenizer.py'
