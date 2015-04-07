from setuptools import setup

import os
from zipfile import ZipFile
import py_compile
from janome.dic import *

dicdir = 'ipadic'

if not os.path.exists('sysdic') and os.path.exists(os.path.join('ipadic', 'sysdic.zip')):
    print('Unzip dictionary data...')
    with ZipFile(os.path.join(dicdir, 'sysdic.zip')) as zf:
        zf.extractall()

print('Precompile dictionary data...')
py_compile.compile(os.path.join('sysdic', MODULE_FST_DATA))
py_compile.compile(os.path.join('sysdic', MODULE_ENTRIES))
py_compile.compile(os.path.join('sysdic', MODULE_CONNECTIONS))
py_compile.compile(os.path.join('sysdic', MODULE_CHARDEFS))
py_compile.compile(os.path.join('sysdic', MODULE_UNKNOWNS))

version = '0.1.3'
name = 'janome'
short_description = '`janome` is a package for Japanese Morphological Analysis.'
long_description = """\
`janome` is a package for Japanese Morphological Analysis.

Requirements
------------
* Python 3.4 or later (not support 2.x)

Features
--------
See http://mocobeta.github.io/janome/ (for Japanese)

History
-------
0.1.3 (2015-4-8)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache License 2.0",
    "Programming Language :: Python",
    "Topic :: Natural Language :: Japanese",
    ]

setup(
    name='Janome',
    version='0.1.3',
    description='Japanese morphological analysis engine.',
    author='Tomoko Uchida',
    author_email='tomoko.uchida.1111@gmail.com',
    url='http://mocobeta.github.io/janome/',
    packages=['janome','sysdic'],
    py_modules=['janome.dic','janome.fst','janome.lattice','janome.tokenizer']
)

