## Release operations

1. Make sure that all tests are OK.

```
$ python setup.py test
```

2. Update CHANGES.txt and documentation.

3. Build the release candidates and upload them to TestPyPI.

https://packaging.python.org/guides/using-testpypi/

```
$ cat janome/version.py
JANOME_VERSION='x.x.xrc1'
$ rm dist/*
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

4. Confirm the release candidate works correctly with Python 3.

```
$ pip install -i https://test.pypi.org/simple/ Janome==x.x.xrc1
$ pip freeze
Janome==x.x.xrc1
$ echo "リリースするぞ！" | janome
```

5. Create a tag for the release.

```
$ cat janome/version.py
JANOME_VERSION='x.x.x'
$ git tag x.x.x
$ git push --tags
```

6. Build the release modules and upload them to PyPI.

```
$ rm dist/*
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

```
$ twine upload dist/*
```

7. Publish documentation.

Generate documentation.

```
./docs/build_docs.sh
```

Publish to web site.

```
$ ./docs/upload_docs.sh $DOCS_ROOT_PATH
```

Well done!

