from setuptools import setup

import os
from zipfile import ZipFile
import py_compile
from dic import *

dicdir = 'ipadic'

print('Unzip dictionary data...')
with ZipFile(os.path.join(dicdir, 'sysdic.zip')) as zf:
    zf.extractall()

setup(
    name='Janome',
    version='0.0.1',
    package_dir={'janome':''},
    packages=['janome','janome.sysdic'],
    py_modules=['janome.dic','janome.fst','janome.lattice','janome.tokenizer']
)

