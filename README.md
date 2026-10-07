# Agent Workflows

> Orchestrating controlled agentic workflows.

A curated collection of agent-native workflow packages for software delivery, design, review, and
automation. Each workflow is self-contained, installable into any repository, and engineered for
controlled execution with validation gates, independent review, and bounded correction loops.

---

## Workflows

### Feature Delivery

Controlled feature delivery through scoped requirements, cost-aware validation, tiered independent
review, and focused delta corrections — from first line to ship-ready.

| | |
|---|---|
| **Category** | Software Engineering |
| **Skills** | 28 specialized skills |
| **Roles** | Router · Researcher · Architect · Builder · Integrator · Reviewer |
| **State** | Machine-checked via Python validator |
| **Entrypoint** | `START_FEATURE_PROMPT.md` |

**Lifecycle:**

```text
IDLE → SCOPE → RESEARCH → [DESIGN] → BUILD → [INTEGRATE] → VALIDATE
     → REVIEW → [FIX → VALIDATE → REVIEW] → [HUMAN CHECKPOINT]
     → READY TO SHIP → SHIPPED
```

**Key capabilities:**
- Skill-routed execution with 28 engineering skills — debugging, TDD, code review, cost control,
  stakeholder requirements, spec-driven development, and more
- Risk-classified routing (LOW / MEDIUM / HIGH) with automatic review escalation
- Snapshot-based review tied to content — edits after review invalidate the verdict
- Bounded fix loops (default 2 cycles, then BLOCKED)
- Machine-checked readiness via `validate_workflow.py`
- Agent-agnostic — works with Claude, Codex, Gemini, or any capable engine

→ **[Documentation](workflows/feature-delivery/)** · **[Install](workflows/feature-delivery/README.md#install)**

---

### Frontend UI / UX

Design-specialized workflow with 15 skills and intelligent routing for building, redesigning,
critiquing, and polishing frontend interfaces.

| | |
|---|---|
| **Category** | Design |
| **Skills** | 15 design skills + skill router |
| **Routing** | Automatic via `skill-router` |
| **Entrypoint** | `AGENTS.md` |

**Lifecycle:**

```text
IDLE → ROUTE → RESEARCH → DESIGN → BUILD → VALIDATE → REVIEW → [FIX] → DONE
```

**Available skills:**

| Skill | Purpose |
|-------|---------|
| `web-design-engineer` | Full websites, dashboards, prototypes, major redesigns |
| `emil-design-eng` | Component polish, micro-interactions, UI craft |
| `animate` | Web motion, transitions, scroll/entrance animations |
| `landing-page-design` | Conversion landing pages, marketing sites |
| `build-awwwards-quality-sites` | Premium cinematic marketing sites |
| `video-to-superprompt` | Video reference → detailed implementation brief |
| `tastemaker` | Anti-generic visual direction, reference grounding |
| `better-layout` | Spacing, alignment, grouping, visual hierarchy |
| `interface-review` | UI diff and regression review |
| `critique-screen` | Rendered-screen visual critique |
| `perception-laws` | Gestalt, Fitts's Law, Hick's Law, Jakob's Law |
| `popular-web-designs` | 54 real design systems as HTML/CSS reference |
| `uxpeak-ux-ui-design` | UX audit and redesign (product/conversion psychology) |
| `standalone-html-ui-artifacts` | Portable self-contained HTML deliverables |
| `iterative-ux-review` | Screenshot → analyze → fix loop |

→ **[Documentation](workflows/frontend-ui-ux/)** · **[Install](workflows/frontend-ui-ux/README.md#install)**

---

## Repository Structure

```text
agent-workflow/
├── workflows/
│   ├── feature-delivery/        28-skill software engineering workflow
│   │   ├── README.md
│   │   ├── workflow.yaml
│   │   └── package/             installable files
│   └── frontend-ui-ux/          15-skill design workflow
│       ├── README.md
│       ├── workflow.yaml
│       └── package/             installable files
├── shared/                      shared resources (when extracted)
├── docs/                        cross-cutting documentation
├── AGENTS.md                    repository rules
└── LICENSE                      MIT
```

Each workflow follows a standard layout:

```text
workflows/<id>/
├── README.md              workflow documentation
├── workflow.yaml          metadata manifest
└── package/               files copied into the target repository
    ├── AGENTS.md          policy for agents working under this workflow
    ├── .agent/            workflow internals, roles, skills, scripts
    └── .active/           mutable runtime state (feature, review, decisions)
```

## Installation

1. Choose a workflow from the list above.
2. Copy the contents of its `package/` directory into your target repository root.
3. If the target repository already has an `AGENTS.md`, merge the workflow rules into the existing
   file — do not overwrite project-specific policy.

Each workflow README has detailed installation instructions.

## Core Principles

These principles are shared across all workflows:

- **Bounded fix loops** — maximum 2 broad fix/re-review cycles by default; after exhaustion, STOP
  and escalate to human.
- **Independent review** — Builder and Reviewer are separate contexts; the Builder may not approve
  its own work.
- **Evidence over claims** — validation requires fresh commands run after the last edit with exact
  output recorded; no fabricated results.
- **Shipping is a human decision** — agents do not commit, push, merge, or deploy unless explicitly
  authorized.

## Creating a Workflow

See [Creating a Workflow](docs/creating-a-workflow.md) and
[Workflow Conventions](docs/workflow-conventions.md).

## License

[MIT](LICENSE)
