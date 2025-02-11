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

Generate documentation.

```
./docs/build_docs.sh
```

Publish to web site.

```
./docs/upload_docs.sh $DOCS_ROOT_PATH
```

7. Push the release branch and merge to main branch via GitHub.

Well done!

