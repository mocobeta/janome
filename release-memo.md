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
    subgraph LocalMachine[Local machine]
        subgraph Manual[Manual actions]
            A[Start pypi-release skill]
            F[Approve PyPI publication]
            J[Review and merge release pull request]
            K[Update documentation in a separate pull request]
            L[Merge documentation pull request to master]
        end

        subgraph AgentSkill[Agent skill]
            B[Prepare release branch, set release version, and commit]
            C[Push version tag]
            D[Run checks and build package]
            G[Publish to PyPI and update GitHub Release]
            H[Verify PyPI, update development version and changelog]
            I[Open release pull request]
        end
    end

    subgraph GitHubActions[GitHub Actions]
        E[Generate release notes and create a pre-release]
    end

    subgraph Cloudflare[Cloudflare Pages]
        M[Build and deploy documentation]
    end

    A --> B --> C --> E --> D --> F --> G --> H --> I --> J --> K --> L --> M

    classDef manual fill:#fff3cd,stroke:#856404,color:#212529
    classDef skill fill:#d4edda,stroke:#155724,color:#212529
    classDef github fill:#dbeafe,stroke:#1d4ed8,color:#212529
    classDef cloudflare fill:#fce7f3,stroke:#be185d,color:#212529
    class A,F,J,K,L manual
    class B,C,D,G,H,I skill
    class E github
    class M cloudflare
```
