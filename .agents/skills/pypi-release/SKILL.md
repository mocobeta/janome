---
name: pypi-release
description: Release Janome to PyPI from a dedicated release branch, including version tagging, package validation, publication, and the post-release development version bump.
---

# Release Janome to PyPI

Follow this sequence for a Janome PyPI release. Do not create release notes. Keep documentation under `docs/` unchanged.

## Workflow

1. Check the worktree before changing branches. If it has uncommitted changes, stop and ask the developer to clean or commit them. Create a dedicated branch from the latest `master` and switch to it before editing files. Name it `release/{version}` when the target version is clear; otherwise use a unique `release/YYYYMMDD-HHmm` name, then ask for the target version. Do not reuse an existing branch.
2. Determine the exact release version from the developer's instructions. Do not infer or choose a version. If it is missing or ambiguous, ask the developer after switching to the release branch. Use the final `d.d.d` form with no development suffix.
3. Update only `src/janome/version.py` to the specified release version, then commit that change on the release branch. Do not update files under `docs/` or create release notes.
4. Before creating or pushing the version tag, inspect `.github/workflows/release-notes.yml`. It currently runs for `d.d.d` tags and automatically creates a GitHub pre-release with generated release notes. If the developer's instruction is to create no release notes, stop before tagging and explain this conflict. Do not alter or bypass the workflow unless the developer explicitly directs that change.
5. If tag push is authorized after resolving the workflow conflict, confirm the version tag does not already exist. Create the tag at the release-version commit and push that tag to `origin`.
6. Run the repository checks from `AGENTS.md` and build the release package:

   ```sh
   uv run pytest tests/
   uv run ruff check src/
   uv run ruff format --check src/ tests/
   uv run ty check src/
   uv build
   uvx twine check dist/*
   ```

   Check `dist/` before building; if it contains old files, inspect them and ensure only artifacts for this release will be uploaded. Confirm there is one source distribution and one wheel with the requested version. `uv build` runs Janome's configured Hatchling hook; do not rebuild the bundled dictionary separately.
7. After the build and validation succeed, report the version and artifact names and ask the developer to approve PyPI publication. Do not upload until approval is received.
8. After approval, publish once with `uv publish`. Use PyPI Trusted Publishing when the environment is configured for it; otherwise use `UV_PUBLISH_TOKEN` from the environment or a secret manager. Never request a token in chat or print it. If credentials are unavailable, stop before upload. If the upload result is unclear, check PyPI before any retry.
9. Verify the target version and both files on PyPI. Then increment `src/janome/version.py` to the next patch development version, following the repository's `X.Y.Z-dev` convention (for example, `0.5.2` becomes `0.5.3-dev`), and commit the post-release version change on the release branch. Do not change docs.
10. Push the release branch to `origin` and create a pull request targeting `master`; do not merge the release branch into `master`. Include a concise work history in the PR description covering the version/tag, checks and build results, PyPI publication verification, and post-release development-version commit. Include a direct link to the published package: `https://pypi.org/project/Janome/{release-version}/`. Verify the link and release details before creating the PR, then report the PR URL without merging it.

## Boundaries

- A request to prepare a release is not approval to publish. Only publish after the explicit approval required in step 7.
- Do not create release notes, create or push a GitHub Release, update docs, or push the `master` branch unless explicitly authorized. Step 4's existing workflow must be handled before pushing a version tag when notes are prohibited.
- Never overwrite an existing PyPI version. If the version is already published, stop and ask for a new version.
