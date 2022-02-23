## Release operations

1. Make sure that all tests are OK.

```
$ python setup.py test
```

2. Build the release modules and upload them to PyPI.

```
$ rm dist/*
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

```
$ twine upload dist/*
```

3. Publish documentation.

Generate documentation.

```
./docs/build_docs.sh
```

Publish to web site.

```
$ ./docs/upload_docs.sh $DOCS_ROOT_PATH
```

4. Create a tag for the release.

```
$ git tag x.x.x
$ git push --tags
```

Well done!

