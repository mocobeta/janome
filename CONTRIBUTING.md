
Steps to contribute

1. Fork this repository and checkout it.

2. Set up virtualenv for development.

  ```
  $ uv sync
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
  $ uv run pytest tests/
  $ uv run ruff check src/
  $ uv run ruff format --check src/ tests/
  $ uv run python -m mypy src/janome/
  ```

5. Once the branch passes all tests :100: , create a pull request :)
