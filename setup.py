from setuptools import setup

import os
from zipfile import ZipFile
import py_compile
from janome.dic import *

dicdir = 'ipadic'

print('Unzip dictionary data...')
with ZipFile(os.path.join(dicdir, 'sysdic.zip')) as zf:
    zf.extractall()

print('Precompile dictionary data...')
py_compile.compile(os.path.join('sysdic', MODULE_FST_DATA))
py_compile.compile(os.path.join('sysdic', MODULE_ENTRIES))
py_compile.compile(os.path.join('sysdic', MODULE_CONNECTIONS))
py_compile.compile(os.path.join('sysdic', MODULE_CHARDEFS))
py_compile.compile(os.path.join('sysdic', MODULE_UNKNOWNS))

setup(
    name='Janome',
    version='0.0.1',
    packages=['janome','sysdic'],
    py_modules=['janome.dic','janome.fst','janome.lattice','janome.tokenizer']
)

