---
name: project-second-brain
description: "Design and maintain file-first AI second brains for projects: AGENTS.md routing, .active/ state, evergreen context, references, wiki, archives, and selective retrieval layers."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [second-brain, context, active-memory, routing, knowledge-management, agents]
    trigger_phrases:
      - second brain
      - project memory
      - active memory
      - knowledge base
      - organize project context
      - make this agent-readable
      - extract useful into our system
---

# Project Second Brain

## Verdict

Organizer reference for this profile:

```text
C:/Users/User/AppData/Local/hermes/profiles/dev/organizer/PROJECT_SECOND_BRAIN_STANDARD.md
```

Default to a **Level 2.5 file-first second brain**:

```text
Level 1: AGENTS.md / CLAUDE.md routing rules
+ Level 2: structured markdown wiki / references / decisions
+ selective Level 3: semantic search only for large snippet-retrieval corpora
- no default knowledge graph
- no uncontrolled always-on ingestion
```

Use the lowest level that removes real pain. Do not add vector DBs, graph RAG, cron memory, or always-on ingestion just because they look powerful.

## Core principle

A useful second brain answers two questions:

1. **Can the agent find the right source?**
2. **Can the human find and maintain it?**

If the answer is no, fix routing and folder architecture before adding retrieval tech.

## Recommended project shape

```text
project-root/
  AGENTS.md              # agent router and operating rules
  CLAUDE.md              # optional Claude Code mirror if needed
  README.md              # human project overview
  .active/
    README.md
    SESSION-START.md     # recovery prompt for new sessions
    CURRENT.md           # current state, constraints, framing
    NEXT.md              # immediate next actions
    DECISIONS.md         # locked decisions and rationale
    RECOMMENDATIONS.md   # current strategic suggestions
    RESEARCH.md          # distilled research, not raw dumps
    STATE.json           # machine-readable active state
  context/
    ABOUT.md             # stable project/user/business background
    PRINCIPLES.md        # durable heuristics and constraints
    DECISIONS.md         # long-term decision log if separate from .active
  projects/              # subprojects/clients/features
  references/            # source docs, specs, transcripts, external notes
  wiki/                  # topic pages and cross-links when notes exceed ~30 files
  archive/               # inactive/frozen material, searched last
```

## Multi-repo workspace orientation pass

When the user asks to understand a whole workspace/folder before starting a new task, create a compact root-level orientation package rather than only summarizing in chat.

Recommended flow:

1. Inventory the workspace while excluding dependency/build/secret-heavy folders such as `.git`, `node_modules`, `.pnpm-store`, `.next`, `dist`, `build`, caches, virtualenvs, and `.env*` files.
2. Identify real repo boundaries with `git rev-parse --show-toplevel` inside candidate subprojects. If a parent directory resolves to an unrelated repo (for example the user's home folder), record that as a git warning and route future work to the inner clean repos only.
3. Read intent-bearing files first: root/inner `AGENTS.md`, `README.md`, `package.json`/manifests, docs indexes, active task files, and module-local READMEs.
4. Write a durable root context file (for example `<PROJECT>_CONTEXT.md`) with product definitions, repo map, source-of-truth docs, command cheatsheet, current status, routing rules, and pitfalls.
5. Add or update a short root `AGENTS.md` that points future agents to the context file and explains which subrepo to use for each task class.
6. Verify by reading the new Markdown back and checking required sections exist.

Keep the output class-level and reusable: "what is this workspace and where do I work next?" Avoid dumping full inventories into the main context; put raw generated inventory in a separate file if useful.

## AGENTS.md routing template

Put explicit lookup order in `AGENTS.md`:

```markdown
# Project Routing

If the user asks what we are currently doing, read `.active/CURRENT.md` first.

If the user asks what to do next, read `.active/NEXT.md` and `.active/STATE.json`.

If the user asks for background research, read `.active/RESEARCH.md`, then `references/`.

If the user asks for durable decisions, read `.active/DECISIONS.md` and `context/DECISIONS.md`.

If the user asks about a topic and there are many notes, search `wiki/` before scanning raw references.

If active/context/wiki do not answer, search `archive/` last.

Do not ingest temporary Slack/email/customer chatter into durable context. Fetch live source data on demand.
```

## What to store durably

Store only data that should still help in a year:

- locked decisions and rationale
- stable constraints and principles
- project identity, scope, and boundaries
- reusable research conclusions
- user/business preferences that survive specific tasks
- source indexes that tell agents where live data lives

Do **not** store as durable context:

- raw chat/email/Slack noise
- temporary todos
- stale status updates
- one-off meeting chatter
- PR/issue/commit numbers unless they define durable architecture
- duplicated raw transcripts when a distilled source note is enough

## Retrieval level decision table

| Pain / need | Use |
|---|---|
| Agent keeps asking where things are | Level 1: improve `AGENTS.md` routing and folder names |
| 30+ notes and user forgets what exists | Level 2: wiki/topic index with links back to sources |
| Keyword search misses notes that clearly exist | Selective Level 3: semantic search over that folder only |
| Need full-file summaries or audits | Markdown source files; route to full document, not vector chunks |
| Need relationship chains like person → company → project → decision | Level 4 knowledge graph, only if relationship questions are frequent |
| Need background sync across live systems | Level 5 only with gates: freshness, expiry, source boundaries, and human approval |

## Vector search rule

Use vectors for **snippet retrieval**, not full-context reasoning.

Good vector cases:

- large rulebooks where only one clause is needed
- many similar transcripts where a short relevant chunk is enough
- reference corpora where semantic wording varies

Bad vector cases:

- “summarize the full March 5 meeting”
- “which week had highest sales across the whole table?”
- “audit every commitment in this project”

For full-context questions, route to the full source markdown/file first.

## Knowledge graph rule

Use graph/relationship layers only when the user repeatedly asks relationship-chain questions:

- which people are connected to which projects/clients?
- which decisions depend on which assumptions?
- which tools/capabilities overlap or conflict?
- which commitments are blocked by which dependencies?

Otherwise, markdown links and wiki indexes are cheaper and easier to maintain.

## Always-on memory rule

Always-on ingestion is dangerous unless gated. Before enabling cron/GBrain-style sync, define:

1. source boundary: what systems may be read
2. durability gate: what qualifies for permanent context
3. freshness/expiry rule: when data goes stale
4. conflict rule: what wins when old and new facts disagree
5. human approval path for durable facts

Default: live sources stay live; the second brain stores source indexes and stable conclusions.

## Demand-driven capability stack pattern

When the user wants to build an AI/Hermes/JARVIS-like capability system, skill library, research operator, or tiered roadmap, use the demand-driven capability stack pattern in:

```text
references/demand-driven-capability-stack.md
```

Default stance:

```text
Capability should follow demand, not imagination.
```

Build the user's current battlefield first, with class-level capability cards, artifact contracts, smoke cases, and `.active/` recovery. Park exciting future domains (CAD, physics, robotics, lab automation, materials discovery, etc.) until a real project needs them.

## Workflow for catching up unsaved session history into a wiki

When the user says they forgot to save recent work to the wiki, asks to “wiki everything,” or wants past Hermes sessions converted into durable context, use `references/session-history-wiki-catchup.md`.

Short version:

1. Read the project/wiki router first (`AGENTS.md`, `.active/`, `SCHEMA.md`, `index.md`, `log.md`).
2. Search recent sessions and topic-specific sessions with `session_search`; keep session ids for exact retrieval.
3. Create/update **class-level** project/workflow pages, not one page per session.
4. Add a catch-up index page with a session-id table and links to the umbrella pages.
5. Preserve durable decisions, artifact paths, verification results, current next-action state, and source-session ids.
6. Do not dump transcripts, temporary todos, or stale blow-by-blow progress.
7. Update `index.md`, `log.md`, and `SCHEMA.md` when pages/tags are added.
8. Verify page count, YAML frontmatter, wikilink resolution, and log entry before reporting done.

Treat session history as evidence of what happened in chat, not proof of current external source state; verify live repos/files/sites separately when the user asks about current truth.

## Workflow for extracting a new idea/video/article into the system

1. Distill the source into reusable rules, not a transcript dump.
2. Classify each rule:
   - durable user/project preference → memory only if compact and stable
   - repeatable procedure → skill
   - current project state → `.active/`
   - reference material → `references/` or `wiki/`
   - temporary task → todo/session only
3. Patch the smallest existing skill or active file that will cause future agents to behave differently.
4. Update router/library only if it changes future routing.
5. Verify by reading back the changed file/skill.

### Strategic-conversation closeout

When a user ends a strategic discussion with “note everything down,” do not dump the transcript or infer authorization for a new project:

1. Write one compact durable decision/reference note under the existing strategy, career, or vision domain.
2. Patch the shortest human router (`START-HERE.md`, topic README, or current-direction page) so future sessions encounter the correction first.
3. Preserve reviewed or sealed older material as historical evidence; label the new preference as current rather than rewriting history to look consistent.
4. State authority effects explicitly—especially when a shared idea was only screened and deliberately released, or when the surrounding workspace remains parked.
5. Capture the user's operating heuristic, not just the topic. Examples: action-centric founder/operator route, capital and commercial leverage, customer/payment signal, unique advantage, and record-and-release when existing teams are better positioned.
6. Read back the note and routers, resolve links, verify status/authority language, assert zero sealed-artifact changes, and leave unrelated user-owned untracked files untouched.

## New startup/project idea with adjacent-project analysis

When the user asks to create a new startup/project plan and also points to a similar existing project to learn from, use `references/adjacent-project-startup-planning.md`.

Short version:

1. Establish the new project name/path and record explicit separateness from the adjacent project in `AGENTS.md` and `.active/DECISIONS.md`.
2. Create a Markdown-first project brain before coding: README, AGENTS, `.active/`, and product/tech/architecture/data/UX/roadmap/implementation docs.
3. Inspect the adjacent project with source evidence: workspace routing docs, repo boundaries/git state, manifests, README/CLAUDE/AGENTS, architecture/data/route/API docs, and representative source files.
4. Write a dedicated `docs/09_<RELATED_PROJECT>_LEARNINGS.md` that separates “take now,” “take later,” and “avoid.”
5. Update the new project’s README/session-start/decisions/current/architecture/data-model docs so future agents see the extraction boundary.
6. Preserve the wedge: do not inherit the mature adjacent project’s full stack/scope unless validated by the new project’s actual needs.
7. Verify by reading back the docs and checking references exist.

## Source-mining old projects for reusable value

When the user asks whether an old repo/project is useful, treat it as a **salvage/source-mine** task before recommending revival or archival. See `references/source-mine-salvage-workflow.md`.

When the user narrows the mandate to "only useful for us" / "take what is useful", use the useful-only port pattern in `references/source-mine-useful-only-port.md`: port the highest-value artifact into its current real home, remove duplicate untracked copies from the old repo, and stop further extraction by default.

Default flow:

1. Verify the repo with real evidence: README/docs, git status, key modules, tests/typecheck/build where available.
2. Classify files into **extract first**, **reference only**, and **archive after extraction**.
3. Write a local `.active/` salvage package with verdict, extraction tasks, Codex prompts, verification baseline, and archive plan.
4. Add `.active/` to `.git/info/exclude` for private Hermes notes instead of modifying project `.gitignore`, unless the user wants the context committed.
5. Execute extraction tasks in bounded slices and independently verify agent output; for reusable tools, smoke/dry-run against a second representative repo.
6. If an extracted artifact belongs in another current system, port it there and verify in that destination instead of leaving the only useful copy inside the old repo.
7. Update `.active/SESSION-START.md` and the salvage map after each extraction so future sessions resume from the real state.
8. If the user says to take only what is useful, record an explicit **stop extraction here unless asked** rule and list what was intentionally not taken.
9. Do not archive/move the original repo until extraction outputs are verified and the user explicitly approves the move.

## Parking a project for resume

When the user asks to “save the state”, “park this”, “so I can continue next time”, or similar, create a compact resume package instead of relying on chat history.

For ongoing implementation/validation tasks, also end each completed slice with a concise operational closeout:

```text
Where we are
What changed
What is verified / blocked
What is next
```

Do this even when no files are being parked; it keeps Mission Control and the user's mental model aligned across multi-repo work.

Use this pattern:

1. Read the relevant active files/state first if available.
2. Write a project-specific `.active/<PROJECT>-STATE.md` with:
   - current verdict/status;
   - completed artifacts with paths;
   - next concrete action;
   - strict constraints/pitfalls;
   - pass/fail gates if validation is pending.
3. Write `.active/<PROJECT>-SESSION-START.md` with the exact files to read on resume and the one next action.
4. Update machine-readable `.active/STATE.json` with a pointer to the saved state files.
5. If the project has a wiki page/index/log, update them with only the durable resume summary and links, not a full transcript.
6. For evidence-gated projects, inspect scheduled jobs and frozen windows before stopping services. Distinguish a finite, read-only administrative tail from active work: do not terminate a sealed evidence window early, but record that its jobs cannot reply, mutate canonical state, claim an outcome, or authorize follow-on work.
7. Close machine-readable permissions as well as prose. When parked, set active/implementation/packaging/outreach flags false and preserve prior authority only as explicit historical metadata; a parked label beside `authorized: true` is unsafe.
8. Scan every live router, including root and nested `AGENTS.md` / `CLAUDE.md`, READMEs, mission indexes, builder handoffs, prompts, and current strategy memos. Historical sealed experiment artifacts remain unchanged.
9. Verify by reading back the saved state/resume files, resolving changed Markdown links, asserting zero sealed-artifact changes, running state/drift tools, and obtaining independent review for broad authority edits.

Keep the state verdict-first and operational. Do not store raw session narrative when a next-action resume note is enough.

## Finalizing a fragmented vision into one canonical goal

When the user promotes a definitive roadmap and asks to finalize a previously shattered/fragmented goal, do not add another roadmap file. Collapse the system into one canonical `GOAL.md`, one active mission, explicit component/parked roles for old branches, synchronized `.active/` and Mission Control routing, and one bounded next action. Preserve the promoted source honestly and run a semantic ad-hoc routing verifier. See `references/finalize-fragmented-vision-goal.md`.

## Correcting active context after compaction/session drift

When the user says the current session state is wrong, “messages are missing,” or names the actual project/source paths, treat that as authoritative active-state correction, not a debate.

Procedure:

1. Identify the corrected active work, completed/parked work, and next slice from the user's correction.
2. Inspect the routing files first (`AGENTS.md`, `.active/CURRENT.md`, `.active/NEXT.md`, `.active/STATE.json`) and then cross-check the implementation repo they point to with real evidence (git log/status, review files, completed artifacts). Do not answer from recent chat momentum alone.
3. If `.active/` says a mission is next but the implementation repo/review shows it already landed, call out the stale Mission Control state explicitly before proposing more work.
4. Patch `.active/CURRENT.md`, `.active/NEXT.md`, and `.active/STATE.json` immediately so future “what next?” answers do not revive completed work or the wrong parked project.
5. Search every other live routing surface for contradictory status phrases before declaring synchronization complete—especially Mission Control `TASKS.md`, root `WORKSPACE_CONTEXT.md`, and root `AGENTS.md` (`active next` vs `parked`, `passed` vs `under review`). Verify any `Updated` timestamp is not older than decisions/content inside the file.
6. If root routing files sit outside a clean Git boundary, call out their weak provenance and avoid treating their content as sealed evidence; implementation artifacts and clean-repo state remain authoritative.
7. If a handoff/delegation was completed, move it from “pending/delegated” to “completed/historical reference” in both machine state and mission Markdown, then promote the next real evidence gate.
8. Patch relevant mission files (`MISSION.md`, `SPEC.md`, `TASKS.md`, `REVIEW.md`) and indexes (`mission-control/README.md`, missions README) when they would otherwise continue routing agents to stale work.
9. Mark completed domains as completed/parked/resumable rather than active.
10. If a saved subproject state exists, keep it as resume material only; do not make it the default next action unless the user explicitly resumes that subproject.
11. When no canonical test suite exists for Markdown/JSON routing changes, run a focused ad-hoc verifier from a temp `hermes-verify-*` script that parses JSON, checks cross-file mission consistency, resolves relative links from their containing files, and searches stale status phrases. Report it as ad-hoc/static verification rather than suite green.
12. Continue from the corrected active workflow.

For detailed patterns, see `references/mission-control-implementation-state-drift.md` and `references/mission-control-state-correction.md`.

## Closing a frozen evidence-gated experiment

When a bounded experiment reaches a reviewed result, use `references/evidence-gated-experiment-closure.md`. The essential rule is:

```text
reviewed aggregate → pre-decision equality → conditional artifact → commit/push/fetch/equality → service cleanup → Mission Control reconciliation
```

Do not declare the conditional decision effective before post-commit remote equality. Preserve expired prior outcomes separately, number rejected and rerun measurements honestly, and hold later gates unless Mission Control makes a new explicit decision. During reconciliation, validate relative links from the containing file and identify port owners and interfaces before labeling a listener as an orphan process.

## After foundation completion: external-evidence packaging

When the active mission has sealed foundation/correction results, later gates (T5, custom persistence, consumer promotion, H1) remain locked, and external demand is only `NOT_ESTABLISHED`, do **not** default to more internal feature slices or ambient Agent OS builds.

Use `references/external-evidence-packaging.md`:

```text
reconcile entry docs → public-safe overview → diagram → publication blockers → clean run path → optional local smoke → hold on public flip/outreach
```

Keep future architecture ideas (e.g. “state continuous; thinking intermittent”) as concept notes under `references/`, not as silent mission expansion. Prefer demand labels `NOT_ESTABLISHED` / `NO_SIGNAL_IN_SAMPLE` over premature global absence claims.

## Correcting Mission Control to an existing implementation

When organizing a vision/research corpus into Mission Control, do **not** assume implementation should start greenfield. Also do **not** treat every document in the source corpus as current canon; if the user says the folder has grown/split into several visions, first write a split map and promote only the active branch before starting tasks. Use `references/split-vision-corpus-mission-control.md` for the organization-first workflow.

If the user names an existing active project path after the scaffold is created, immediately correct Mission Control to point at that implementation and verify it.

Procedure:

1. Treat the user-provided path as authoritative, even if folder names like `archive`, `retired`, or `old` suggest inactive status.
2. Inspect the existing implementation before planning: README/package/config, git top-level, git status/diff, and available test/lint/build scripts.
3. Patch `.active/CURRENT.md`, `.active/NEXT.md`, `.active/STATE.json`, and the relevant mission files so they stop telling agents to create a duplicate repo.
4. Add repo-local `AGENTS.md` / `.active/` only when useful; keep private `.active/` out of git via `.git/info/exclude` unless the user wants it committed.
5. Verify the existing implementation with its real commands and record results in the mission `REVIEW.md`.

Reference: `references/vision-mission-control-active-implementation-correction.md`.


## Supporting references

- `references/adjacent-project-startup-planning.md` — use when creating a Markdown-first plan for a new startup/project while source-mining a similar existing project; keeps the new project separate, writes a dedicated learnings doc, and prevents scope/stack inheritance.
- `references/session-history-wiki-catchup.md` — use when converting unsaved Hermes session history into durable wiki pages: search sessions, group by class-level project/workflow pages, write a catch-up index, update schema/index/log, and verify links/counts.
- `references/capability-stack-project-brain.md` — use when building a demand-driven capability stack, skill library, or agent harness roadmap. It gives the `capabilities/`, `contracts/`, `templates/`, `evaluations/`, `.active/`, and `backlog/` pattern plus golden routing tests and artifact contracts.
- `references/vision-corpus-to-mission-control.md` — use when mining a folder of personal vision/research PDFs/docs/diagrams into a durable synthesis and file-first Mission Control plan.
- `references/split-vision-corpus-mission-control.md` — use when the user corrects that a vision/research folder has split into multiple visions; organize a `VISION-SPLIT-MAP.md` and promote only the active branch before creating tasks.
- `references/external-evidence-packaging.md` — after foundation/correction is sealed and product gates are locked, package outsider-readable evidence without claiming demand or opening T5/Agent OS.

## Human-findable reference libraries

When the user says files are hard to find or asks to manage them cleanly, treat that as a request to change the durable navigation architecture—not merely to suggest filenames in chat.

Default response:

1. add one obvious `OPEN THIS FIRST` / `references/README.md` entry point;
2. group files by durable purpose rather than session, model, PR, or producer;
3. add short topic READMEs with read order and authority boundaries;
4. colocate mission-specific checklists and evidence with their mission;
5. preserve history with `git mv`;
6. update human routers, agent routers, machine paths, and live scheduled prompts; and
7. verify links, old-path absence, rename detection, routing checks, remote equality, and the final PR description.

Use the detailed workflow and acceptance checklist in `references/human-findable-reference-library.md`.

## Human-readable restructure rule

When organizing a project for the user, do not assume that a complete Markdown command center is human-readable. Dense tables, many numbered files, and AI-oriented command-center wording can be correct but still hard for a team to use.

For hackathon/business/team execution folders, create or offer a **human-readable layer** alongside the detailed reference layer.

When a hackathon project is still gathering prototype tests, competitor prices, business resources, or prior-winner deck examples, use the capture workflow in `references/hackathon-evidence-and-business-research-capture.md`: preserve sources, compute unit prices, write slide-redo gates, and do **not** prematurely rewrite the final slides/script before evidence is ready.

For hackathon/business/team execution folders, create or offer a **human-readable layer** alongside the detailed reference layer:

```text
project-readable/
  OPEN-THIS-FIRST.html        # optional browser-friendly dashboard
  README.md
  01-READ-FIRST/              # START-HERE, one-page plan
  02-DO-NOW/                  # immediate checklist + simple CSV
  03-TEAM-ROLES/              # each member's actions
  04-PITCH-PRESENTATION/      # slide/script/rehearsal files
  05-RESEARCH-INTERVIEWS/     # safe claims + interview scripts
  06-JUDGE-QA/                # short Q&A cards
  07-EVENT-DAY/               # packing/runbook
  90-TECHNICAL-REFERENCE/     # original dense docs, detailed CSVs, source map
```

Human-facing files should be short, action-first, and scannable:

- prefer checklists, one-page plans, and “open this first” routing;
- split by what the team is doing, not by agent task phase;
- keep the dense evidence banks, simulations, and full protocols under `90-TECHNICAL-REFERENCE/`;
- add a pointer file in the older/dense folder so humans know which folder to use;
- verify both structure and simple data templates after rewriting.

## Pitfalls

- For project scaffolds that may be committed to GitHub or shared with teammates, do not write machine-specific absolute paths such as `C:/Users/User/projects/...` into README/AGENTS/.active files. Use repo-relative paths (`.`, `docs/...`) and sibling-repo paths (`../frontend`, `../backend`) instead; if local absolute paths are useful for the current user, keep them in private session notes only.
- When splitting a project into separate frontend/backend repos, give each repo its own `AGENTS.md`, `README.md`, `.active/SESSION-START.md`, `.active/STATE.json`, and local `docs/` copy of the shared API/types contract so either team can work independently after cloning.
- Do not confuse Obsidian graph visuals with useful retrieval.
- Do not treat “more context” as automatically better.
- Do not let stale live data become durable memory.
- Do not build graph/vector infrastructure before routing files are clean.
- Do not make every folder the same level; different folders can use different retrieval patterns.
- Do not mistake “complete for an agent” for “readable for a human team”; add a simple human workflow layer when the user says the Markdown is hard to read.
