# All-Skills Routing Protocol

## Architecture

`skill-router` uses staged context rather than placing every full skill in the prompt:

1. **Fast routes** in `SKILL.md` handle stable, high-frequency decisions.
2. **Generated catalog** in `references/skill-catalog.json` and `.md` covers every installed `SKILL.md` using its name, description, category, tags, triggers, relationships, prerequisites, and path.
3. **Deterministic shortlist** from `scripts/route_skills.py` ranks the catalog against the user's actual wording and applies narrow routing overrides for known ambiguities.
4. **Full instruction loading** with `skill_view` verifies the top candidates before the final route is selected.

The catalog supplies breadth; the full skill supplies authority. Never decide a material workflow from the catalog description alone when `skill_view` is available.

## Parse the request

Extract these fields without forcing the user to fill a form:

```yaml
domain: software | design | research | business | documents | data | systems | media | other
artifact: what must exist or change
verb: build | inspect | debug | review | research | operate | send | convert | decide | plan
phase: discovery | specification | implementation | verification | delivery | maintenance
named-project-or-source: exact project, product, platform, repository, or format
constraints: stack, device, audience, evidence, safety, cost, deadline
requested-output: answer | recommendation | plan | code | file | external action
```

Infer obvious fields from the request. Ask only when a missing field changes the route, risk, cost, or external side effect.

## Selection precedence

Apply these in order:

1. **Explicit user choice** — if the user names a skill and it fits, load it. If it conflicts with the request or is retired, explain the conflict before acting.
2. **Project-specific authority** — a Menui, Evalora, CodeWave, SimpleWeb KH, or other named-project skill precedes generic methods for that project.
3. **Artifact-specific skill** — `xlsx` beats generic data tooling for an Excel deliverable; `landing-page-design` beats a generic design workflow for a conversion landing page.
4. **Phase-specific skill** — debugging, implementation, review, and delivery are different owners. `interface-review` reviews a change; it does not build the interface.
5. **Domain method** — use a general workflow only when no narrower artifact/phase skill owns the request.
6. **Direct tool route** — use a tool without a skill when no installed skill adds meaningful procedure, constraints, or verification.

## Shortlist procedure

When the fast table has no obvious route, or several skills overlap, run from the `skill-router` directory:

```bash
python scripts/route_skills.py "<the user's request>" --top 8
```

Use JSON when another script must consume the result:

```bash
python scripts/route_skills.py "<request>" --top 8 --json
```

Interpretation:

- A dominant first result with a clear artifact/phase match can be loaded first.
- A close cluster means the descriptions overlap; load the top two or three and compare their `When to Use`, exclusions, outputs, and setup readiness.
- A lexical score is not authority. Do not choose a retired, prohibited, unavailable, wrong-platform, or wrong-phase skill merely because it ranked highly.
- If the user names a project or format, reject generic candidates that ignore that exact context.

## Full-candidate comparison

After shortlisting, call `skill_view` for the plausible candidates and compare:

| Criterion | Question |
|---|---|
| Trigger | Does its stated use case match the user's actual verb and artifact? |
| Ownership | Does it own this phase, or only an adjacent phase? |
| Deliverable | Will it produce the requested output rather than advice about it? |
| Preconditions | Are required tools, credentials, files, and platforms available? |
| Evidence | Does it require evidence the user has not supplied or tools cannot retrieve? |
| Scope | Is it narrower and more precise than another candidate? |
| User policy | Does it respect current model, project, privacy, and execution preferences? |
| Verification | Does it define how to prove the result? |

## Skill composition

Prefer the smallest non-overlapping stack:

1. **Primary owner** — owns the main artifact and phase.
2. **Specialist support** — optional; owns a distinct concern such as animation, accessibility, source validation, or delivery.
3. **Verification/delivery owner** — optional; used only when the primary skill does not cover real verification or external delivery.

Normally load one to three skills. Do not combine several general design, research, or coding workflows simply because they all scored well. State which skill is primary and why each support skill is necessary.

Examples:

- Conversion landing page with motion: `landing-page-design` primary + `animate` support.
- Screenshot critique: `critique-screen` primary; add `better-layout` only when spacing/adaptivity is a confirmed root cause.
- UI diff review: `interface-review`, not `critique-screen`, unless a rendered screen is also supplied.
- Verify whether a startup problem is real: `external-validation-research`; add `founder-thinking-mode` only for the pursue/park decision after evidence.
- Extract obligations from a scanned PDF: `ocr-and-documents` for extraction + `document-to-action-items` for obligation analysis.

## Confidence and user communication

- **Clear route:** load it and act; do not ask the user to choose from a catalog.
- **Real trade-off:** give a verdict-first default and one short explanation of the alternative.
- **Missing prerequisite:** retrieve it when tools can; otherwise ask one targeted question.
- **No match:** use the simplest direct tool route and state that no installed skill adds material value.

For recommendation requests:

```text
Verdict: use <primary skill> [with <support skill>].
Why: <artifact/phase match and one decisive constraint>.
How I’ll proceed: <next concrete action>.
Loaded/used: <skills/tools>.
```

## Catalog freshness

`references/skill-catalog.json` and `.md` are generated artifacts. Rebuild them after a skill is added, removed, renamed, moved, or materially changes its description/tags/triggers:

```bash
python scripts/rebuild_skill_catalog.py
```

`route_skills.py` automatically rebuilds when the catalog is missing or older than an installed `SKILL.md`. The maintenance workflow still runs the rebuild explicitly so catalog drift is visible and verifiable.

## Failure modes

1. **Catalog dumping:** loading all full skills destroys focus. Use shortlist → full load.
2. **Description-only routing:** descriptions are discovery hints, not complete procedures.
3. **One-word matching:** route on artifact + verb + phase, not a single token such as “design” or “review.”
4. **Over-composition:** several overlapping primary skills create conflicting workflows.
5. **Ignoring exclusions:** “not for,” retired, wrong-platform, and wrong-phase rules outweigh lexical similarity.
6. **Stale catalog:** regenerate and compare counts whenever the skill tree changes.
7. **Invented certainty:** if candidates remain tied after full loading, explain the trade-off and choose a default only when reversibility is high.
