# Adjacent-project startup planning and source-mining workflow

Use when the user wants to create a new project/startup and explicitly points to an existing related project to learn from.

## Trigger

Examples:

- “I have a new project/startup idea; first check this workspace and this related project.”
- “Build plan/architecture/docs first in this new folder, but analyze old/similar project to see what we can take.”
- “This new product is similar to X; learn from X but keep it separate.”

## Workflow

1. **Establish project identity and boundary**
   - Confirm the new project name/path.
   - Record that it is separate from the existing/adjacent project unless the user says otherwise.
   - Add the boundary to `AGENTS.md` and `.active/DECISIONS.md` early so future agents do not merge ownership, stack, or scope.

2. **Create Markdown-first project brain before coding**
   - Use a compact package:
     - `AGENTS.md`
     - `README.md`
     - `.active/CURRENT.md`
     - `.active/NEXT.md`
     - `.active/DECISIONS.md`
     - `.active/SESSION-START.md`
     - `docs/01_PRODUCT_SPEC.md`
     - `docs/02_TECH_STACK_DECISION.md`
     - `docs/03_ARCHITECTURE.md`
     - `docs/04_DATA_MODEL.md`
     - `docs/05_UX_FLOWS.md`
     - `docs/06_ROADMAP_AND_SPRINTS.md`
     - `docs/07_IMPLEMENTATION_PLAN.md`
     - `docs/08_BRAND_POSITIONING.md`
   - Keep paths repo-relative in files that may be committed; only mention absolute local paths in private context if needed.

3. **Inspect the related project with source evidence**
   - Read workspace routing docs first, then repo-specific README/AGENTS/CLAUDE/package/docs.
   - Check real git top-level/status only inside inner repos; flag parent-repo contamination.
   - Read architecture, data model, endpoint docs, route matrix, and representative source files for the overlapping domain.
   - Do not read or print `.env*`/secrets.

4. **Write a dedicated learnings doc**
   - Add `docs/09_<RELATED_PROJECT>_LEARNINGS.md` or similar.
   - Separate:
     - what to take now;
     - what to take later;
     - what to avoid;
     - files to inspect again during implementation;
     - final product boundary.
   - Update `README.md`, `.active/SESSION-START.md`, `.active/DECISIONS.md`, `.active/CURRENT.md`, and relevant architecture/data-model docs to point to it.

5. **Preserve wedge and avoid scope creep**
   - When the related project is broader, explicitly name the new project’s smaller wedge.
   - Record heavyweight adjacent-project systems as “later only after validation,” not as default architecture.
   - Common examples to defer: separate backend framework, queues, full payments, subscriptions, roles/teams, marketplace, inventory, wallet/ledger/escrow.

6. **Verify the docs**
   - Read back the new/updated docs.
   - Run a small ad-hoc existence/reference check if no formal tests exist.
   - Report the concrete files changed and the resulting decisions.

## Output shape

The final answer should be verdict-first:

- New project docs created/updated.
- Related project analyzed.
- What to reuse vs avoid.
- Where the detailed learnings doc lives.
- Next product decisions before coding.

## Pitfalls

- Do not copy code or proprietary implementation from the adjacent project unless explicitly asked and allowed.
- Do not let a mature adjacent project’s stack become the default for the new MVP.
- Do not treat similarity as ownership; record separateness in routing docs.
- Do not write a chat-only analysis when the user asked to build a folder of Markdown docs.
- Do not overfit one session into a new narrow skill; keep this as a class-level project-brain workflow.
