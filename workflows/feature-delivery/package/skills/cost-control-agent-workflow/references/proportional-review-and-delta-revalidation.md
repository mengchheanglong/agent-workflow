# Proportional Review and Delta Revalidation

Use this reference when a feature workflow is correct but review/re-review dominates elapsed time or model cost.

## Audit before deleting gates

Inspect actual artifacts and state first:

- number of broad engineering/specification reviews;
- number of separate visual/specialist reviews;
- fix-cycle count and pending next review;
- repeated typecheck/lint/build/browser commands;
- whether each edit was material or narrow polish;
- whether snapshot churn came from product bytes, commit/tracking representation, or evidence files;
- measured tokens/cost if available. Never invent dollar savings.

A strong over-review signal is several authoritative + specialist artifact pairs for the same feature, especially when later cycles cover only CSS, copy, focus, or evidence binding.

## Default proportional policy

| Risk | Review tier | Specialist mode | Suggested budget |
|---|---|---|---:|
| LOW | MECHANICAL | INLINE or justified NOT_REQUIRED | 5 min |
| MEDIUM | TARGETED | INLINE | 15 min |
| HIGH | DEEP | INLINE or justified SEPARATE | 30 min |

Budget limits work; it never lowers the approval bar. At the bound, insufficient proof becomes `UNVERIFIABLE` / `CHANGES_REQUESTED` with a concrete escalation reason.

For normal features, prefer 3–7 acceptance criteria. More criteria require distinct behavior or risk, not prose fragmentation.

## One broad review plus one delta

Default lifecycle:

1. focused checks during implementation;
2. canonical project gates once after the candidate final product edit;
3. one independent FULL review at the selected tier;
4. at most one bounded correction;
5. one DELTA review when eligible;
6. human checkpoint when required.

`fixCycles` should count broad FULL reopenings, not a named DELTA correction. Extra broad cycles require explicit human override evidence.

### DELTA eligibility

DELTA is allowed only when all are true:

- correction addresses named accepted findings or explicit human polish;
- requirements and contracts are unchanged;
- changed paths remain approved;
- diff is narrow;
- affected criteria/invariants are listed;
- prior approved snapshot/artifact is named;
- affected validation and regression seams are clear.

DELTA inspects the correction, affected files/checks, and regression seams, carrying forward only prior conclusions explicitly proved reusable.

### FULL-review triggers

Require FULL when any are present:

- requirement or scope change;
- shared contract/interface/schema;
- auth, security, permission, data, migration, finance, or lifecycle behavior;
- new dependency;
- broad refactor;
- ambiguous snapshot/evidence equivalence;
- multiple substantive findings or repo-wide reasoning.

## UI specialist composition

For LOW/MEDIUM UI work, put visual hierarchy, accessibility, responsive behavior, and browser evidence in the same independent reviewer context and authoritative artifact. Do not spawn a second general visual reviewer by default.

Use a separate specialist only for HIGH risk, genuinely different expertise, or explicit human request. Human-requested visual polish after approval gets focused browser/visual DELTA verification unless it changes requirements or scope.

## Validation reuse

- Run cheap focused checks during build/fix loops.
- Run repository-required canonical gates after the final product edit.
- A later narrow edit reruns affected checks and every canonical command the repository explicitly requires after the last edit.
- A reviewer inspects controller-owned evidence; it does not rerun every expensive command unless evidence is missing, stale, inconsistent, or suspect.
- Retained evidence must include a concrete unaffected rationale and at least one fresh affected check.

## Snapshot-only binding recipe

A commit, newly tracked file, line-ending normalization, or corrected snapshot algorithm may change a delivery digest without changing product bytes. Do not automatically launch two new full reviews.

Prove, read-only:

1. exact current branch, HEAD, status, baseline, and live snapshot;
2. product paths are clean at HEAD;
3. working-tree changes are only recorded pre-existing/excluded files;
4. prior approved product files match the current product tree;
5. deterministic gates are current and coherent;
6. browser/visual evidence still applies because rendered product bytes did not change;
7. no BLOCKER/MAJOR remains.

Then run one independent TARGETED DELTA review that names:

- base approved snapshot;
- current reviewed snapshot;
- changed criterion such as “bind unchanged product bytes/evidence to current snapshot”;
- evidence of byte/tree equivalence;
- INLINE specialist conclusion;
- separate specification, quality, and overall verdicts.

If equivalence cannot be established, stop and request FULL review or missing proof.

## False snapshot-only claims: focused repair path

Treat “commit/tracking representation only” as a hypothesis, not evidence. Before rebinding prior approval:

1. inspect `git show <current-head> -- <reviewed-product-paths>` and the base-to-HEAD product diff;
2. compare the changed seams with the claims and screenshots in the prior review artifact;
3. distinguish a clean working tree from unchanged product bytes—a committed product change is clean at HEAD but still invalidates prior evidence;
4. preserve the failed DELTA artifact instead of overwriting it;
5. invalidate only the affected criteria and specialist conclusions.

If product bytes changed but the change is still narrow, do not automatically reopen the full review. Capture focused exact-snapshot browser evidence for the affected rendered invariants. Useful deterministic probes include:

- document `clientWidth` and primary-action x-position before, during, and after a dialog;
- overlay bounds against the full viewport edge;
- dialog center and viewport containment at desktop and mobile sizes;
- animation-frame sampling of dialog center drift during close (scale is acceptable; diagonal travel is not when prohibited);
- initial focus and focus return;
- horizontal overflow, console errors, and page errors;
- screenshot inspection limited to the named seams.

Save raw metrics plus a concise evidence index, then run one independent bounded DELTA re-review of the failed finding only. Carry forward unaffected conclusions; do not launch a duplicate general visual reviewer or rerun the full browser matrix.

A prior human visual approval remains tied to its named snapshot. Any later rendered product change makes it stale even when focused automated and independent review pass. Move to `HUMAN_CHECKPOINT` and request current-snapshot confirmation rather than silently rebinding the old approval.

## Machine-state fields

For a machine-checked workflow, useful fields include:

```json
{
  "reviewPolicy": {
    "tier": "TARGETED",
    "specialistMode": "INLINE",
    "budgetMinutes": 15,
    "maxBroadReviewCycles": 1,
    "escalationReason": null
  },
  "review": {
    "type": "DELTA",
    "baseApprovedSnapshot": "sha256:...",
    "changedCriteria": ["AC12 — bind unchanged product bytes to current snapshot"]
  }
}
```

Validator invariants should include risk/tier compatibility, positive budget, explicit override above one broad cycle, independent reviewer, current reviewed snapshot, specification PASS, quality APPROVE, overall APPROVE, and zero open BLOCKER/MAJOR.

## Session case study

One medium-risk frontend refinement accumulated six authoritative/visual review pairs and was preparing a seventh after narrow polish and commit-time snapshot churn. Replacing the default with one integrated review plus at most one DELTA reduces reviewer-context count from 12 to 1–2 (about 83–92% fewer contexts). This is a workload estimate, not a token or dollar guarantee.

The crucial correction was not “remove review.” It was:

- integrate overlapping reviewer lenses;
- classify materiality before invalidation;
- preserve reusable evidence;
- bind snapshot-only changes with DELTA;
- keep final project gates, browser acceptance, independent approval, WIP protection, and human checkpoint.
