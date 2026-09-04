# Start Feature Prompt

Use the repository feature-delivery workflow to implement exactly one coherent feature with
production-quality discipline.

## Feature request

<PASTE ONE FEATURE REQUEST HERE>

## Instructions

1. Read `AGENTS.md`, authoritative project docs, `.agent/WORKFLOW.md`,
   `.agent/QUALITY_GATES.md`, selected role files, `REVIEW.md`, and all `.active/*` files.
2. Do not code immediately.
3. Confirm no unfinished feature exists. Continue, pause, or close it safely before initializing a
   different feature.
4. Inspect the actual repository root and record base branch/commit, pre-existing changes, allowed
   paths, and expected validation commands.
5. Initialize `.active/FEATURE.md` from the template. Define one goal, explicit scope boundaries,
   testable acceptance criteria, requirements-quality checks, risk, human checkpoint, and small
   dependency-ordered slices when needed. Prefer 3-7 acceptance criteria unless distinct risk or
   behavior requires more.
6. Synchronize `.active/STATE.md` and `.active/STATE.json`, including `gateEvidence` for every
   completed or routed-out gate; run the validator.
7. Act as Router and choose the minimum safe workflow. Record why optional stages are
   `NOT_REQUIRED`. Select `reviewPolicy`: MECHANICAL for LOW only, TARGETED by default for MEDIUM,
   DEEP for HIGH or explicit escalation; INLINE specialist mode by default for LOW/MEDIUM; budget
   defaults of 5/15/30 minutes by risk; and one broad review cycle by default.
8. Research the existing implementation and tests before design or edits. Cite repository evidence.
9. Use Architecture for MEDIUM/HIGH risk, cross-module, contract, persistence, auth, security,
   finance, privacy, or integration work.
10. Implement only approved scope. Use RED → GREEN → REFACTOR for changed behavior when an automated
    test is feasible.
11. Run focused checks during implementation/fixes. After the candidate final product edit,
    independently read back the tree and run canonical full project gates once. After any later
    narrow edit, rerun affected checks and only canonical gates it can affect; record why retained
    canonical evidence is unaffected. Do not trust a worker's success summary.
12. Compute the current snapshot with:

    ```bash
    python .agent/scripts/validate_workflow.py --snapshot
    ```

13. Run one independent, fresh-context, read-only FULL review at the selected tier using
    `.agent/roles/reviewer.md` and `REVIEW.md`. Keep specialist critique INLINE unless SEPARATE was
    authorized. Record verdicts first and concise rubric deltas in `.active/REVIEW.md`.
14. A first review may yield one bounded narrow correction. For named accepted findings or
    human-requested polish with unchanged requirements/contracts, approved files, narrow diff, and
    listed affected criteria, run affected checks, compute a new snapshot, and use DELTA review.
    DELTA does not increment `fixCycles`. Material corrections require FULL and increment
    `fixCycles`; another broad cycle requires human `fixCycleOverrideEvidence` and
    `maxBroadReviewCycles > 1`, otherwise stop `BLOCKED`.
15. Stop at required human checkpoints. Approval must identify the current snapshot/commit.
16. Only `APPROVE` plus passing gates may become `READY_TO_SHIP`.
17. Before claiming readiness or completion, run:

    ```bash
    python .agent/scripts/validate_workflow.py
    ```

18. Do not commit, push, merge, deploy, revert user work, or widen scope unless authorized.

## Final handback

Provide:

- feature and user-visible outcome;
- workflow path and risk;
- base and reviewed snapshot;
- changed files;
- exact fresh validation commands/results;
- review engine, reviewer identity, verdict, and finding counts;
- human approval status;
- remaining risks/follow-ups;
- ship evidence if shipped;
- exact next action.

If the request contains unrelated features, implement only the first coherent feature and list the
others as future work.
