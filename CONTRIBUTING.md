
Steps to contribute

1. Fork this repository and checkout it.

2. Set up virtualenv for development.

  ```
  $ python -m venv .venv
  $ . .venv/bin/activate
  (.venv) $ pip install -r requirements-dev.txt
  (.venv) $ pip install -e .
  ```

3. (Optional) Build and validate the built-in dictionary.

  If you do not modify dictionary building scripts, you can skip this step and just use `sysdic.zip` which is included in the repository.

  Download mecab-ipadic from here, and extract to janome/ipadic directory.
  http://sourceforge.net/projects/mecab/files/mecab-ipadic/2.7.0-20070801/

  ```
  $ cd janome/ipadic
  $ tar xzf mecab-ipadic-2.7.0-20070801.tar.gz
  $ ./build.sh mecab-ipadic-2.7.0-20070801
  $ cd ..
  $ rm -rf sysdic; unzip ./ipadic/sysdic.zip    // extract the built-in dictionary to janome root
  $ . .venv/bin/activate
  (.venv) $ pip install -e .   // install janome module for development
  (.venv) $ cd ipadic 
  (.venv) $ ./validate.sh mecab-ipadic-2.7.0-20070801
  ```

4. Fix codes, run tests and linter.

  ```
  $ cd janome  // change directory to janome root
  $ python -m unittest discover tests/
  $ python -m flake8 janome/
  $ python -m mypy janome/*.py
  ```

5. Once the branch passes all tests :100: , create a pull request :)

If you have any questions, please post comments to Gitter room (below). Thanks!

Japanese room: https://gitter.im/janome-python/ja

English room: https://gitter.im/janome-python/en