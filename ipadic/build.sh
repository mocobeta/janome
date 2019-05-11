#!/bin/bash

IPADIC_DIR=$1
OUT_DIR=sysdic
WORKING_DIR=work
WORKER_PROCESS=2

if [ -z ${IPADIC_DIR} ]; then
  echo "Usage: ./build.sh <mecab ipadic dir>"
  exit 0
fi

if [ ! -e ${IPADIC_DIR} ]; then
  echo "Mecab dictionary dir does not exist: ${IPADIC_DIR}"
  exit 1
fi

if [[ "${IPADIC_DIR%%/}" =~ mecab-ipadic-2.7.0-20070801$ ]]; then
  # apply patch to mecab-ipadic
  patch -u -N ${IPADIC_DIR%%/}/Noun.proper.csv < Noun.proper.csv.patch
fi

ENC=$2
if [ -z ${ENC} ]; then
  ENC=euc-jp
fi

if [ -e ${OUT_DIR} ]; then
  rm -rf ${OUT_DIR}
fi
mkdir ${OUT_DIR}
if [ -e "${OUT_DIR}.zip" ]; then
  rm "${OUT_DIR}.zip"
fi

if [ -e ${WORKING_DIR} ]; then
  rm -rf ${WORKING_DIR}
fi
mkdir ${WORKING_DIR}

# build dictionary (saved as python module.)
python build.py --collect ${IPADIC_DIR} ${ENC} ${OUT_DIR} ${WORKING_DIR}
python build.py --build ${IPADIC_DIR} ${ENC} ${OUT_DIR} ${WORKING_DIR} ${WORKER_PROCESS}

INIT_PY="${OUT_DIR}/__init__.py"
cp "__init__.py.tmpl" ${INIT_PY}
./_import_fstdata_method.sh ${OUT_DIR} >> ${INIT_PY}

zip -r "${OUT_DIR}.zip" ${OUT_DIR}

echo "Build done."
