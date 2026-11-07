---
name: janome-release-notes
description: Draft Janome release notes from a release range or merged changes, following the project's GitHub release format. Use when preparing a Janome release note.
---

# Draft Janome release notes

Prepare accurate, user-facing release notes for Janome using the Markdown structure below.

## Workflow

1. Establish the release version and the range of changes to include. Use the user's instructions and repository tags or release context. If the version or range cannot be determined confidently, ask the developer before drafting.
2. Gather changes from the commits and merged pull requests in that range. Use PR descriptions and issue context when available to understand user impact. Do not invent behavior, issue references, or contributor attribution; ask when an important fact is unclear.
3. Group entries under the template sections. Put user-facing API changes, improvements, and bug fixes in their matching sections. Place tooling, documentation, packaging, and CI updates under `Build / Documentation / Other`.
4. Write concise entries that describe outcomes. Link issue or PR numbers and include contributor GitHub handles only when verified. Write `(No changes)` for an empty section.
5. Include the PyPI download link and `Contributors` section when preparing a published release note and the version and contributor list are known. Omit unavailable details rather than guessing.
6. Return the release note as a draft for review. Do not publish a GitHub release, create a tag, or upload artifacts unless the developer explicitly requests those actions.

## Markdown template

Replace placeholders with verified release details and omit the HTML comment when delivering the note.

```markdown
# Release Note {version}

Download here [PyPI](https://pypi.org/project/Janome/{version}/)

## API Changes

- [#{pull_request}](https://github.com/mocobeta/janome/pull/{pull_request}): {user-facing API change}. (@{github_handle})

## Improvements

- [#{pull_request}](https://github.com/mocobeta/janome/pull/{pull_request}): Improve {feature or existing behavior}. (@{github_handle})

## Bug Fixes

- [#{pull_request}](https://github.com/mocobeta/janome/pull/{pull_request}): Fix {bug or unexpected behavior}. (@{github_handle})

## Build / Documentation / Other

- [#{pull_request}](https://github.com/mocobeta/janome/pull/{pull_request}): {build, documentation, packaging, or other change}. (@{github_handle})

### Contributors

- @{github_handle}
```

Use one bullet per change. Add only verified entries; if a section has no entries, keep `(No changes)`. Link issues instead of PRs when the change is issue-based, and list each contributor once.
