# Review Fix Prompt

Continue the current active feature. Do not start another feature and do not treat review as
permission for general cleanup.

1. Read `AGENTS.md`, `REVIEW.md`, `.agent/WORKFLOW.md`, `.agent/QUALITY_GATES.md`,
   `.active/FEATURE.md`, `.active/STATE.md`, `.active/STATE.json`, `.active/DECISIONS.md`, and the
   authoritative `.active/REVIEW.md`.
2. Confirm the review snapshot and current tree. Classify every finding as still present,
   stale/already fixed, rejected with evidence, or accepted.
3. Classify the correction before editing. Use DELTA only for named accepted findings or
   human-requested polish with unchanged requirements/contracts, approved files, a narrow diff, and
   explicit affected criteria/invariants. Requirement changes, scope expansion, shared contracts,
   auth/security/data/migration/lifecycle behavior, new dependencies, broad refactors, or ambiguous
   evidence require FULL.
4. Fix only accepted current findings and directly necessary regressions. Do not change acceptance
   criteria or redesign silently. Increment `fixCycles` only for a broad FULL reopening; never for a
   named DELTA. A broad allowance above the default 1 requires explicit human
   `fixCycleOverrideEvidence` and a raised `reviewPolicy.maxBroadReviewCycles`; otherwise set
   `BLOCKED`.
5. After the last edit, read back changed boundary files and tests.
6. Re-run affected focused/browser checks. Rerun a canonical full project gate only if this edit can
   affect it; otherwise retain its result with a concrete unaffected rationale. Record at least one
   fresh `afterLastEdit` check.
7. Compute and record a new snapshot:

   ```bash
   python .agent/scripts/validate_workflow.py --snapshot
   ```

8. Run an independent, read-only DELTA review against the new snapshot when eligible, naming the base
   approved review snapshot and changed criteria. Inspect only the correction, affected evidence,
   and regression seams, carrying forward explicitly reusable conclusions. Otherwise run authorized
   FULL review. The Builder may not approve its own fixes.
9. Replace `.active/REVIEW.md` with the new authoritative review and synchronize specification,
   engineering-quality, and overall verdicts plus gate evidence in both state files.
10. Only specification `PASS` + engineering-quality `APPROVE` + overall `APPROVE` may pass review.
    Stop for the Human Checkpoint when required.
11. Run `python .agent/scripts/validate_workflow.py` before any readiness claim.
12. Do not commit, push, merge, deploy, or revert unrelated/user changes unless authorized.
