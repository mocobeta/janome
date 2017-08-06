from setuptools import setup
import sys
from io import open

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

fst_data = [data_file for data_file in os.listdir('sysdic') if data_file.startswith('fst.data')]

version = '0.3.5'
name = 'janome'

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: Japanese",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6"
]

setup(
    name='Janome',
    version=version,
    description='Japanese morphological analysis engine.',
    long_description=long_description,
    author='Tomoko Uchida',
    author_email='tomoko.uchida.1111@gmail.com',
    license='AL2',
    classifiers=classifiers,
    url='http://mocobeta.github.io/janome/',
    packages=['janome','sysdic'],
    package_data={'sysdic': fst_data},
    py_modules=['janome.dic','janome.fst','janome.lattice','janome.tokenizer','janome.analyzer','janome.charfilter','janome.tokenfilter'],
    scripts=['bin/janome'],
    test_suite = 'suite'
)

