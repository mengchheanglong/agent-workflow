# Review Fix Prompt

Continue the current active feature. Do not start another feature and do not treat review as
permission for general cleanup.

1. Read `AGENTS.md`, `REVIEW.md`, `.agent/WORKFLOW.md`, `.agent/QUALITY_GATES.md`,
   `.active/FEATURE.md`, `.active/STATE.md`, `.active/STATE.json`, `.active/DECISIONS.md`, and the
   authoritative `.active/REVIEW.md`.
2. Confirm the review snapshot and current tree. Classify every finding as still present,
   stale/already fixed, rejected with evidence, or accepted.
3. Fix only accepted current findings and directly necessary regressions. Do not change acceptance
   criteria or redesign silently.
4. Increment `fixCycles`. If `maxFixCycles` is exhausted, set `BLOCKED` and request human direction.
   Continue only when a human raises the limit and records `fixCycleOverrideEvidence`.
5. After the last edit, read back changed boundary files and tests.
6. Re-run affected tests plus every required final validation command. Record exact output/exit codes
   as fresh `afterLastEdit` evidence.
7. Compute and record a new snapshot:

   ```bash
   python .agent/scripts/validate_workflow.py --snapshot
   ```

8. Run a fresh independent, read-only review against the new snapshot. The Builder may not approve
   its own fixes.
9. Replace `.active/REVIEW.md` with the new authoritative review and synchronize specification,
   engineering-quality, and overall verdicts plus gate evidence in both state files.
10. Only specification `PASS` + engineering-quality `APPROVE` + overall `APPROVE` may pass review.
    Stop for the Human Checkpoint when required.
11. Run `python .agent/scripts/validate_workflow.py` before any readiness claim.
12. Do not commit, push, merge, deploy, or revert unrelated/user changes unless authorized.
