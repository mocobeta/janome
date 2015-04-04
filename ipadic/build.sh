#!/bin/bash

IPADIC_DIR=$1
OUT_DIR=sysdic

if [ -z ${IPADIC_DIR} ]; then
  echo "Usage: ./build.sh <mecab ipadic dir>"
  exit 0
fi

if [ ! -e ${IPADIC_DIR} ]; then
  echo "Mecab dictionary dir does not exist: ${IPADIC_DIR}"
  exit 1
fi

ENC=$2
if [ -z ${ENC} ]; then
  ENC=euc-jp
fi

if [ -e ${OUT_DIR} ]; then
  rm -rf ${OUT_DIR}
fi
if [ -e "${OUT_DIR}.zip" ]; then
  rm "${OUT_DIR}.zip"
fi
mkdir ${OUT_DIR}

cp "__init__.py.tmpl" "${OUT_DIR}/__init__.py"

# build dictionary (saved as python module.)
python build.py ${IPADIC_DIR} ${ENC} ${OUT_DIR}

zip -r "${OUT_DIR}.zip" ${OUT_DIR}

echo "Build done."
