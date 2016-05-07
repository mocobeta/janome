from setuptools import setup
import sys

sys.path.append('./janome')
sys.path.append('./tests')

import os
from zipfile import ZipFile
from janome.dic import *

dicdir = 'ipadic'

if not os.path.exists('sysdic') and os.path.exists(os.path.join('ipadic', 'sysdic.zip')):
    print('Unzip dictionary data...')
    with ZipFile(os.path.join(dicdir, 'sysdic.zip')) as zf:
        zf.extractall()

version = '0.2.8'
name = 'janome'
short_description = '`janome` is a package for Japanese Morphological Analysis.'
long_description = """\
`janome` is a package for Japanese Morphological Analysis.

Requirements
------------
* Python 2.7.x and Python 3.3+

Features and history
--------------------
See http://mocobeta.github.io/janome/en

"""

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache License 2.0",
    "Programming Language :: Python",
    "Topic :: Natural Language :: Japanese",
    ]

setup(
    name='Janome',
    version=version,
    description='Japanese morphological analysis engine.',
    author='Tomoko Uchida',
    author_email='tomoko.uchida.1111@gmail.com',
    url='http://mocobeta.github.io/janome/',
    packages=['janome','sysdic'],
    package_data={'sysdic': ['fst.data']},
    py_modules=['janome.dic','janome.fst','janome.lattice','janome.tokenizer'],
    scripts=['bin/janome'],
    test_suite = 'suite'
)

