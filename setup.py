import shutil
import os
from janome.version import JANOME_VERSION
from janome.dic import *
from zipfile import ZipFile
from setuptools import setup
import sys
from io import open

sys.path.append('./janome')
sys.path.append('./tests')


dicdir = 'ipadic'

if os.path.exists(os.path.join(dicdir, 'sysdic.zip')):
    if os.path.exists('sysdic'):
        shutil.rmtree('sysdic')
    print('Unzip dictionary data...')
    with ZipFile(os.path.join(dicdir, 'sysdic.zip')) as zf:
        zf.extractall("janome")

name = 'janome'

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: Japanese",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"
]

setup(
    name='Janome',
    version=JANOME_VERSION,
    description='Japanese morphological analysis engine.',
    long_description=long_description,
    author='Tomoko Uchida',
    author_email='tomoko.uchida.1111@gmail.com',
    license='AL2',
    classifiers=classifiers,
    url='https://mocobeta.github.io/janome/en/',
    packages=['janome', 'janome.sysdic'],
    package_data={'janome.sysdic': ['fst.data*']},
    scripts=['bin/janome', 'bin/janome.bat'],
    test_suite='suite'
)
