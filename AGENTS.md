# Repository instructions

Janome is a pure-Python Japanese morphological analyzer. The package source is in `src/janome`, and the test suite is in `tests/`.

## Development setup

- Python 3.11 or newer is required.
- Set up the development environment with `uv sync`.
- The built-in dictionary is included in the repository. Do not rebuild it unless a change touches the dictionary build scripts or dictionary data.

## Validation

Run the relevant checks for code changes:

```sh
uv run python -m unittest discover tests/
uv run python -m flake8 src/janome/
uv run python -m mypy src/janome/
```

The GitHub Actions workflow runs the test suite on Python 3.11 through 3.15 and on Ubuntu, macOS, and Windows.
