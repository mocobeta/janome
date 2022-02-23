#!/bin/sh

BASEDIR=$(cd $(dirname $0) && pwd)
cd $BASEDIR

rm -rf .venv
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-docs.txt

cd ${BASEDIR}/api && make clean && make html
cd ${BASEDIR}/ja && make clean && make html
cd ${BASEDIR}/en && make clean && make html
