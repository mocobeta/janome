#!/bin/bash

DOCS_ROOT_PATH=$1

echo "DOCS_ROOT_PATH=$DOCS_ROOT_PATH"

cp -Rp ja/_build/html/* $DOCS_ROOT_PATH
cp -Rp en/_build/html/* $DOCS_ROOT_PATH/en
cp -Rp api/_build/html/* $DOCS_ROOT_PATH/api

cd $DOCS_ROOT_PATH
git checkout master
git pull

git add .
git commit -m "Update documentation"
git push origin master
