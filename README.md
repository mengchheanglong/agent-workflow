# Agent Workflows

Orchestrating controlled agentic workflows.

A collection of controlled agent workflows for software development, review, and automation. Each
workflow is a self-contained package installable into a target repository.

## Workflows

### [Feature Delivery](workflows/feature-delivery/)

Full feature lifecycle: scope → research → design → build → validate → independent review → bounded
fix loops → human checkpoint → ship. Agent-agnostic with machine-checked state validation.

### [Gemini Delivery Loop](workflows/gemini-flash-delivery/)

Spec-driven implementation using Gemini Flash, independent Gemini Pro review, bounded fix loops, and
optional high-risk escalation. Lighter than Feature Delivery — designed for repositories that already
own their architecture and feature specs.

## Structure

```text
workflows/       individual workflow packages
shared/          shared schemas, templates, scripts (when needed)
docs/            cross-cutting documentation
```

## Installation

Each workflow has its own README with installation instructions. Copy the contents of a workflow's
`package/` directory into your target repository root.

If the target repository already has an `AGENTS.md`, merge the workflow rules into the existing file
rather than overwriting project-specific policy.

## Adding a workflow

See [Creating a Workflow](docs/creating-a-workflow.md).
