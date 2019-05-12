## Release operations

1. Make sure that all tests are OK.

```
$ python -m unittest discover tests/ 
```

2. Update CHANGES.txt.

3. Create the release tag.

4. Push the changes and tags to the repository.

5. Build the release candidates and upload them to TestPyPI.

https://packaging.python.org/guides/using-testpypi/

```
$ cat janome/version.py
JANOME_VERSION='x.x.x-rc'
$ rm dist/*
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

6. Confirm the release candidate works correctly with Python2/3.

```
$ pip install -i https://test.pypi.org/simple/ Janome==x.x.xrc0
$ echo "リリースするぞ！" | janome
```

7. Create a tag for the release.

```
$ cat janome/version.py
JANOME_VERSION='x.x.x'
$ git tag x.x.x
$ git push --tags
```

8. Build the release modules and upload them to PyPI.

```
$ rm dist/*
$ python setup.py sdist
$ python setup.py bdist_wheel --universal
```

```
$ twine upload dist/*
```

9. Update documentation.

Well done!

