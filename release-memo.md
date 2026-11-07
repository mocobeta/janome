## Release procedure

Before starting the release, set `UV_PUBLISH_TOKEN` in the environment used to run the `pypi-release` skill.

1. Use the `pypi-release` skill in `.agents/skills/pypi-release/SKILL.md` to prepare a PyPI release. For example:

```text
Use the `pypi-release` skill to prepare the Janome 0.5.2 release for PyPI.
```

2. Review and merge the pull request created by the `pypi-release` skill.

3. Update the documentation for every release in a separate pull request. After it is merged into `master`, Cloudflare Pages automatically builds and deploys the documentation.

How it works: The skill prepares the release on a dedicated branch, runs the project checks, creates a release tag, and builds the package. It requests approval before publishing to PyPI. After publication, it updates the development version and changelog, then opens a pull request for review. Documentation changes are handled separately.

The release flow is shown below:

```mermaid
flowchart TD
    subgraph Manual[Manual]
        A[Start pypi-release skill]
        C[Approve PyPI publication]
        G[Review and merge release pull request]
        H[Update documentation in a separate pull request]
        I[Merge documentation pull request to master]
    end

    subgraph Automated[Automated]
        B[Prepare release branch, run checks, create tag, and build package]
        D[Publish to PyPI]
        E[Update development version and changelog]
        F[Open release pull request]
        J[Cloudflare Pages builds and deploys documentation]
    end

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J

    classDef manual fill:#fff3cd,stroke:#856404,color:#212529
    classDef automated fill:#d4edda,stroke:#155724,color:#212529
    class A,C,G,H,I manual
    class B,D,E,F,J automated
```
