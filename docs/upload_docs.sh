#!/bin/bash

DOCS_ROOT_PATH=$1

echo "DOCS_ROOT_PATH=$DOCS_ROOT_PATH"

BASEDIR=$(cd $(dirname $0) && pwd)

cd $DOCS_ROOT_PATH
git checkout master
git pull

cp -Rp ${BASEDIR}/api/_build/html/* $DOCS_ROOT_PATH/api
cp -Rp ${BASEDIR}/ja/_build/html/* $DOCS_ROOT_PATH
cp -Rp ${BASEDIR}/en/_build/html/* $DOCS_ROOT_PATH/en

git add .
git commit -m "Update documentation"
git push origin master
