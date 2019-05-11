#!/bin/bash

SYSDIC_DIR=$1

function join_by_comma { local IFS=","; echo "$*"; }

function fst_modules() {
    local ret=()
    for f in `ls ${SYSDIC_DIR}/fst_data*.py`; do
        f=${f#${SYSDIC_DIR}/}
        f=${f%.py}
        ret+=($f)
    done
    echo ${ret[@]}
}

modules=`fst_modules`

echo ""
echo "def all_fstdata():"
echo "    import base64"
echo "    from . import $(join_by_comma ${modules[@]})"
echo "    res=[]"
for m in ${modules[@]}; do
    echo "    res.append(base64.b64decode(${m}.DATA))"
done
echo "    return res"
