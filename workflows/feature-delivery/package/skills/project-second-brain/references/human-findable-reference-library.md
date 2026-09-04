# Human-Findable Reference Library Cleanup

Use this workflow when a user says project files are hard to find, scattered, or technically organized but not human-readable.

## Goal

Create a small, obvious navigation layer while preserving authority boundaries and file history.

Organize by **durable purpose**, not by the session, model, PR, or tool that produced a file.

## Placement rules

| Material | Preferred home |
|---|---|
| Current state and next action | `.active/` |
| Mission-specific plans, evidence, and closure checklists | Beside that mission or experiment |
| Career, research, or other durable topic material | `references/<topic>/` |
| Reusable evaluation/review procedures | `references/governance/` or the established equivalent |
| Raw source corpus | `references/raw/` |
| Historical/obsolete material | `archive/` or an existing historical folder; search last |

Do not move sealed evidence merely for visual neatness. Route to it from a mutable index instead.

## Recommended shape

```text
references/
  README.md                 # OPEN THIS FIRST: question -> start page
  topic-a/
    README.md               # read order, status, boundaries
    primary-decision.md
    detailed-reference.md
    safe-template.md
  governance/
    README.md
    reusable-protocol.md
```

A root index should answer human questions, not dump every filename:

```markdown
| Question | Start here |
|---|---|
| What is active? | `.active/CURRENT.md` and `.active/NEXT.md` |
| What is the career direction? | `references/career/README.md` |
| How is this experiment closed? | the experiment-local checklist |
```

## Workflow

1. **Inspect before moving**
   - Check Git state and current branch/PR.
   - Inventory the relevant tree.
   - Find every exact filename/path usage.
   - Inspect human and agent routers (`README.md`, `AGENTS.md`, `.active/`).
   - Treat cron prompts, scripts, CI config, and other live automation as path dependencies too.

2. **Design the smallest semantic tree**
   - Prefer one root `README.md` plus a `README.md` in each meaningful topic folder.
   - Put mission-specific files with mission evidence rather than in a general reference dump.
   - Avoid creating a folder per document or per model run.

3. **Write the navigation layer first**
   - Root index: question-to-entry-point table and compact folder map.
   - Topic index: explicit read order, current status, authority boundary, and privacy/source rules.
   - Main project README: point to the root reference index.
   - Agent router: point to the same human entry page when appropriate.

4. **Move with history preserved**
   - Use `git mv` for tracked files.
   - Update internal links and repo-relative code-formatted paths.
   - Update mutable machine routing such as `.active/STATE.json` path fields.
   - Do not rewrite frozen historical artifacts just to add navigation; link from current routing surfaces.

5. **Repair live automation**
   - Update scheduled-job prompts and scripts that name moved paths.
   - Read back the stored job definition, not only its preview.
   - Verify the job remains enabled and keeps the same schedule, authority, and non-mutation constraints.

6. **Verify before committing**
   - Resolve every new Markdown link relative to its containing file.
   - Assert all machine-readable paths exist.
   - Search for every old exact path and require zero hits.
   - Confirm no curated files remain loose at the old location.
   - Validate JSON and run the project routing/drift checks.
   - Stage the complete unit and inspect `git diff --cached --summary`; expected moves should appear as renames.
   - Run `git diff --cached --check` and confirm no unstaged residue.

7. **Ship coherently**
   - Commit the organization change separately from content/authority changes where practical.
   - Push and verify local/remote equality.
   - Update the open PR description, moved-file pointers, and any recorded head hash so review evidence is not stale.

## Pitfalls

- **Clean-looking but undiscoverable:** folders without a start page still force browsing.
- **Provenance-based clutter:** `model-X-review/` or `PR-123-files/` becomes meaningless later; classify by purpose.
- **Broken hidden dependency:** a cron prompt can retain an old path even when repository search is clean.
- **Authority drift:** moving a checklist does not authorize closure or change an outcome.
- **Over-fragmentation:** use the fewest folders that create a clear human decision tree.
- **Machine-specific docs:** committed indexes should use repo-relative paths, never a local `C:/Users/...` path.
- **Stale PR evidence:** a follow-up organization commit invalidates a previously recorded remote head until the PR body is updated.

## Acceptance checklist

```text
[ ] Human can start from one obvious index
[ ] Topic pages state read order and authority boundary
[ ] Mission-specific files live with mission evidence
[ ] Git recognizes tracked moves as renames
[ ] All links and machine paths resolve
[ ] No old exact path remains
[ ] Live scheduled prompts use the new path
[ ] JSON/routing checks pass
[ ] Worktree is clean and remote-equal
[ ] PR description reflects the final structure and head
```
