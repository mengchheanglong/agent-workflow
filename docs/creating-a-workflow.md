# Creating a Workflow

Each workflow lives under `workflows/<workflow-id>/` and follows a standard structure.

## Required structure

```text
workflows/<workflow-id>/
├── README.md          documentation about the workflow
├── workflow.yaml      metadata manifest
└── package/           files installed into a target repository
    └── ...
```

## `workflow.yaml`

Every workflow must have a manifest:

```yaml
name: Human-Readable Name
id: kebab-case-id
version: 1.0.0
description: >
  One or two sentences describing what the workflow does.
category: software-engineering
agents:
  - generic                    # or specific agent roles
requires:
  git: true                    # runtime dependencies
entrypoint: START_PROMPT.md    # file an agent reads first
```

## `package/`

The `package/` directory contains everything that gets copied into a target repository. Design it so
that copying its contents into a repository root produces a working installation.

Guidelines:

- Use `.agent/` for workflow internals (process docs, prompts, scripts, templates).
- Use `.active/` for mutable runtime state when the workflow needs it.
- Root-level files (`AGENTS.md`, `REVIEW.md`, prompts) should be the user-facing entry points.
- All paths inside package files should be relative to the installation root, not this repository.

## `README.md`

The workflow README should cover:

- what the workflow does and when to use it;
- the installation process;
- how to start, continue, and complete work;
- role definitions if the workflow uses multiple agents;
- any prerequisites or dependencies.

## Naming conventions

- Workflow IDs use `kebab-case`: `feature-delivery`, `gemini-delivery`, `deep-review`.
- Files use existing markdown conventions from the repository.
- Avoid generic names like `workflow-1`; use descriptive names.

## Testing

If the workflow includes scripts or validators, include tests under `package/.agent/tests/`.
Tests should be runnable from the installed location, not only from this repository.
