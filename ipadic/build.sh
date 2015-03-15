#!/bin/bash

IPADIC_DIR=$1
# UTF8_DIR=${IPADIC_DIR}/utf8

if [ -z ${IPADIC_DIR} ]; then
  echo "Usage: ./build.sh <mecab ipadic dir>"
  exit 0
fi

if [ ! -e ${IPADIC_DIR} ]; then
  echo "Mecab dictionary dir does not exist: ${IPADIC_DIR}"
  exit 1
fi

#if [ ! -e ${UTF8_DIR} ]; then
#  mkdir ${UTF8_DIR}
#  if [ $? -ne 0 ]; then
#    echo "Failed to create directory: ${UTF8_DIR}"
#    exit 1
#  fi
#fi

# convert dictionary encoding EUC-JP => UTF-8
#for file in `ls ${IPADIC_DIR}/*.csv | xargs -i basename {}`; do
#  utf8file="${UTF8_DIR}/${file%.*}.utf8.csv"
#  iconv -f euc-jp -t utf-8 "${IPADIC_DIR}/$file" > $utf8file
#done

# build dictionary (saved as python module.)
ls ${IPADIC_DIR}/*.csv | xargs python build.py euc-jp

echo "Done."