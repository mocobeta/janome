---
name: janome-release-notes
description: Draft Janome release notes from a release range or merged changes, following the project's GitHub release format. Use when preparing a Janome release note.
---

# Draft Janome release notes

Prepare accurate, user-facing release notes for Janome using the Markdown structure below.

## Workflow

1. Establish the target release version and identify the latest published stable release before it. Use GitHub Releases and select the non-draft, non-prerelease release with the latest `published_at` time. Ignore all drafts and pre-releases when choosing the previous release. If the previous stable release or its publication date cannot be determined confidently, ask the developer before drafting.
2. Include only pull requests merged after the previous stable release was published. Use each PR's `merged_at` time, not its creation or last update time. When a target tag or commit is known, also limit the list to PRs included in that target release. Exclude PRs already merged by the previous stable release date.
3. Gather the included changes from their merged pull requests and commits. Use PR descriptions and issue context when available to understand user impact. Do not invent behavior, issue references, or contributor attribution; ask when an important fact is unclear.
4. Group entries under the template sections. Put user-facing API changes, improvements, and bug fixes in their matching sections. Place tooling, documentation, packaging, and CI updates under `Build / Documentation / Other`.
5. Write concise entries that describe outcomes. Link issue or PR numbers and include contributor GitHub handles only when verified. Write `(No changes)` for an empty section.
6. Include the PyPI download link and `Contributors` section when preparing a published release note and the version and contributor list are known. Omit unavailable details rather than guessing.
7. Before returning the note, compare its PR numbers with the complete expected PR set for the range established in step 2. Check that every expected PR is included exactly once and that no PR outside that set is included. Correct omissions, out-of-range entries, and duplicates before answering. If the complete expected set cannot be verified, do not claim the check passed; resolve the range or ask the developer.
8. Return the release note as a draft for review. Do not publish a GitHub release, create a tag, or upload artifacts unless the developer explicitly requests those actions.

For example, if `0.5.0` is the latest stable release and `0.5.1` is a pre-release, use `0.5.0` as the previous release when preparing notes for `0.5.2`. Include PRs merged after `0.5.0` was published, even if they were merged before `0.5.1`; exclude PRs merged before `0.5.0` was published and PRs not included in the target tag's history.

## Markdown template

Replace placeholders with verified release details and omit the HTML comment when delivering the note.

```markdown
## Install

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
