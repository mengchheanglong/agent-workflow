# Agent Workflows — Repository Rules

This repository contains multiple agent workflow packages.

## Structure

- `workflows/<name>/package/` — installable files for each workflow
- `workflows/<name>/README.md` — workflow documentation
- `workflows/<name>/workflow.yaml` — workflow metadata
- `shared/` — shared resources (when two or more workflows need them)
- `docs/` — cross-cutting documentation

## Contributing

- Each workflow is self-contained in its `package/` directory.
- Do not cross-reference between workflow packages at runtime.
- Extract shared patterns into `shared/` only when two or more workflows genuinely reuse them.
- Each workflow must have a `README.md` and `workflow.yaml`.
- Preserve existing project-specific rules when installing a workflow into a target repository.
