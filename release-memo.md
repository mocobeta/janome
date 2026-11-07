## Release operations

1. Create the release branch.

```
git switch -c release-x.x.x
```

2. Make sure that all tests are OK.

```
python -m unittest discover tests/
```

3. Fix version and create a new tag for the release.

```
vim janome/version.py

git tag x.x.x
git push --tags
```

4. Build the release modules and upload them to PyPI.

```
rm dist/*
python -m build
```

```
twine upload dist/*
```

5. Create the GitHub release.

https://github.com/mocobeta/janome/releases

6. Update and publish documentation.

From the Janome repository root, build the API, Japanese, and English HTML documentation.

```
uv run --group docs sphinx-build -b html docs/api docs/api/_build/html
uv run --group docs sphinx-build -b html docs/ja docs/ja/_build/html
uv run --group docs sphinx-build -b html docs/en docs/en/_build/html
```

Clone the website repository into a temporary directory. `DOCS_ROOT_PATH` is the clone's `janome` directory.

```
TEMP_DIR=$(mktemp -d)
git clone --branch master https://github.com/mocobeta/mocobeta.github.io.git "$TEMP_DIR/mocobeta.github.io"
DOCS_ROOT_PATH="$TEMP_DIR/mocobeta.github.io/janome"
mkdir -p "$DOCS_ROOT_PATH/api" "$DOCS_ROOT_PATH/en"
rsync -a --delete \
  --exclude='/.buildinfo' --exclude='/.doctrees/' \
  --exclude='/.gitignore' --exclude='/index.md' \
  --exclude='/api/' --exclude='/en/' \
  docs/ja/_build/html/ "$DOCS_ROOT_PATH/"
rsync -a --delete \
  --exclude='/.buildinfo' --exclude='/.doctrees/' \
  --exclude='/.gitignore' --exclude='/index.md' \
  docs/api/_build/html/ "$DOCS_ROOT_PATH/api/"
rsync -a --delete \
  --exclude='/.buildinfo' --exclude='/.doctrees/' \
  --exclude='/.gitignore' --exclude='/index.md' \
  docs/en/_build/html/ "$DOCS_ROOT_PATH/en/"
```

Review the website repository changes, then commit and push the documentation update.

```
git -C "$TEMP_DIR/mocobeta.github.io" add janome
git -C "$TEMP_DIR/mocobeta.github.io" commit -m "Update documentation"
git -C "$TEMP_DIR/mocobeta.github.io" pull --rebase origin master
git -C "$TEMP_DIR/mocobeta.github.io" push origin master
```

7. Push the release branch and merge to main branch via GitHub.

Well done!

