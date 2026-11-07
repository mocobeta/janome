#!/usr/bin/env bash

set -euo pipefail

BASEDIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$BASEDIR/.."

rm -rf "$BASEDIR/api/_build" "$BASEDIR/ja/_build" "$BASEDIR/en/_build" "$BASEDIR/build"

uv run --group docs sphinx-build -b html "$BASEDIR/api" "$BASEDIR/api/_build/html"
uv run --group docs sphinx-build -b html "$BASEDIR/ja" "$BASEDIR/ja/_build/html"
uv run --group docs sphinx-build -b html "$BASEDIR/en" "$BASEDIR/en/_build/html"

mkdir -p "$BASEDIR/build/reference" "$BASEDIR/build/ja" "$BASEDIR/build/en"
cp -R "$BASEDIR/api/_build/html/." "$BASEDIR/build/reference/"
cp -R "$BASEDIR/ja/_build/html/." "$BASEDIR/build/ja/"
cp -R "$BASEDIR/en/_build/html/." "$BASEDIR/build/en/"
cp "$BASEDIR/index.html" "$BASEDIR/build/index.html"

echo "Documentation built in $BASEDIR/build"
