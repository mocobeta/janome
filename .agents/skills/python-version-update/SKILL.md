---
name: python-version-update
description: Update a repository's supported Python versions across CI and package metadata. Use when changing the minimum Python version or the Python versions tested by CI.
---

# Update supported Python versions

Keep the declared minimum Python version, tested CI versions, and package metadata consistent with the developer's requested support policy.

## Workflow

1. Determine the intended support policy: minimum supported version and versions CI should test. Use explicit instructions from the developer or clear repository context. If either is unclear, ask the developer before editing; do not infer support policy from the newest available Python release or from a previous PR.
2. Inspect the repository's current version declarations and workflow.
   - `.github/workflows/checks.yml`: Python test matrix.
   - `README.rst`: documented minimum requirement.
   - `pyproject.toml`: `requires-python` and `Programming Language :: Python :: ...` classifiers.
   - `.python-version`: set it to the minimum supported Python version.
3. Search beyond those files for other active version constraints, including version files and other CI or packaging configuration. Update only declarations that express the affected support policy. Treat changelogs and historical release notes as history unless asked to revise them.
4. Keep the minimum requirement distinct from the CI matrix: `requires-python`, README, and `.python-version` must all match the minimum supported Python version, while CI lists the versions actually tested. Update classifiers to match the supported versions the project intends to advertise.
5. Check that requested versions are valid for the repository's CI setup and supported by its tooling. If availability or compatibility is uncertain, verify it from authoritative current sources and report any limitation before claiming support.
6. Review the complete diff for consistency and run lightweight checks such as `git diff --check`. Run project tests only when requested or when the change warrants them.

Do not silently choose a new minimum, add a version merely because it is the latest release, or change unrelated files. If the developer asks only to investigate, report candidate files without editing them.
