#!/bin/bash

IPADIC_DIR=$1

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

# build dictionary (saved as python module.)
python build.py ${IPADIC_DIR} ${ENC}

echo "Build done."
