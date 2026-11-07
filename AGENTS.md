# Repository instructions

Janome is a pure-Python Japanese morphological analyzer. The package source is in `src/janome`, and the test suite is in `tests/`.

## Development setup

- Python 3.11 or newer is required.
- Set up the development environment with `uv sync`.
- The built-in dictionary is included in the repository. Do not rebuild it unless a change touches the dictionary build scripts or dictionary data.

## Validation

Run the relevant checks for code changes:

```sh
uv run pytest tests/
uv run ruff check src/
uv run ruff format --check src/ tests/
uv run ty check src/
```

The GitHub Actions workflow runs the test suite on Python 3.11 through 3.15 and on Ubuntu, macOS, and Windows.

## Documentation

- Documentation sources are under `docs/`: `ja/` for Japanese, `en/` for English, and `api/` for the API reference. These are Sphinx projects written in reStructuredText.
- Keep the Japanese and English user guides in sync when changing user-facing documentation. Update the API reference when public APIs or their behavior change.
- Edit source files only. Do not edit generated files under `docs/*/_build/` or other build output directories.
- Build the documentation with the `docs` dependency group in `pyproject.toml`, for example: `uv run --group docs sphinx-build -b html docs/ja docs/ja/_build/html` (repeat for `docs/en` and `docs/api` as needed).
- Documentation is built and published automatically after a pull request touching `docs/` is merged into `master`; see `.github/workflows/publish-docs.yml`.
