---
name: janome-docs-update
description: Update Janome's Japanese and English release documentation and open a draft pull request. Use after a release when preparing the documentation update for master.
---

# Update Janome release documentation

Use this skill to prepare the documentation update for a Janome release. The result is a draft pull request targeting `master`; do not merge it.

## Workflow

1. Check that the worktree is clean. If it is not, stop and ask the developer to clean or commit the existing changes. Fetch the latest `origin/master` and create a new branch from it, named `docs/release-{version}`. Do not reuse an existing branch.
2. Determine the released version and publication date from the published GitHub Release. Use an explicitly supplied version if given, but verify its release details. If the release or its date cannot be verified, stop and ask rather than guessing.
3. In both `docs/ja/index.rst` and `docs/en/index.rst`, update the `最新バージョン` / `Latest version` entry and add a matching top entry under `History` using the GitHub Release publication date (`YYYY.MM.DD`), version, and link to that release. Preserve the existing history entries and formatting.
4. If the supported Python versions changed, check `requires-python` in `pyproject.toml` and the CI version matrix, then update the Japanese and English requirements text to match the current minimum supported Python version. Do not change project support settings as part of this documentation task.
5. Build the documentation with `docs/build_docs.sh`. Review the diff to confirm both languages describe the same release and that no unrelated files changed. Fix any build errors before continuing.
6. Commit the documentation changes, push the branch, and open a draft pull request targeting `master`. Follow any repository pull request template if one is present. Include the release version and a concise summary of the Japanese and English documentation updates. Do not mark the pull request ready for review or merge it.

## Boundaries

- Change only the release information in the Japanese and English guides, plus the Python requirement text when supported Python versions changed.
- Do not change package code, release notes, `CHANGES.txt`, or Python support configuration.
- Stop before creating the pull request if release details cannot be verified or the documentation build fails.
