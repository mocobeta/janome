#!/bin/sh

BASEDIR=$(cd $(dirname $0) && pwd)
cd $BASEDIR

rm -rf .venv
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-docs.txt
pip install -e ..

cd ${BASEDIR}/api && make clean && make html
cd ${BASEDIR}/ja && make clean && make html
cd ${BASEDIR}/en && make clean && make html

rm -rf ${BASEDIR}/build
mkdir -p ${BASEDIR}/build
cp ${BASEDIR}/_redirects ${BASEDIR}/build/
cp -Rp ${BASEDIR}/ja/_build/html/* ${BASEDIR}/build/
cp -Rp ${BASEDIR}/en/_build/html/ ${BASEDIR}/build/en
cp -Rp ${BASEDIR}/api/_build/html/ ${BASEDIR}/build/reference

echo "All build finished. Assets are in ${BASEDIR}/build"
  