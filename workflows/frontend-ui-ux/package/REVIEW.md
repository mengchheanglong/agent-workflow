# Repository Review Instructions

This file contains review-only guidance. It supplements `AGENTS.md`; it does not authorize changes.

## Review posture and hard gate

Act as the one independent, fresh-context, read-only Reviewer. Try to falsify readiness without
repairing product code or relying on Builder claims. The review may be compact, but it must still
establish the exact baseline, allowlist, pre-existing changes, current snapshot, fresh controller
evidence, specification verdict, quality verdict, and open finding counts.

Only specification `PASS` plus engineering-quality `APPROVE` and overall `APPROVE` for the current
snapshot can pass `G6_REVIEW`. Open BLOCKER or MAJOR findings always block approval.

## Required inputs

- the acceptance criteria, scope, allowed paths, and selected `reviewPolicy` in active state;
- material decisions and the exact base commit/branch/current snapshot;
- the actual diff, changed files, relevant surrounding code/tests, and pre-existing changes;
- fresh controller validation evidence after the final edit, including justified reuse of any
  canonical gate that a later edit could not affect;
- for DELTA, the prior review artifact, named base approved snapshot, accepted finding or requested
  polish, and explicit changed criteria/invariants.

Missing or ambiguous scope/evidence is `UNVERIFIABLE`, never permission to guess.

## Review tiers

- `MECHANICAL` - LOW risk only. Compactly verify scope/allowlist, acceptance-criterion deltas,
  changed files, evidence freshness, obvious regressions, and selected specialist lens.
- `TARGETED` - default for MEDIUM risk. Verify acceptance-criterion deltas, all changed files,
  validation evidence, and the 1-3 risky seams named at Scope. Expand a seam only when evidence
  creates a concrete concern.
- `DEEP` - required for HIGH risk or explicit escalation. Perform full specification and engineering
  review across every applicable criterion, boundary, quality dimension, and specialist lens.

LOW may use a higher tier when justified. MEDIUM may not use MECHANICAL. HIGH must use DEEP.

## Specialist modes

- `INLINE` - default for LOW/MEDIUM. Perform UX, visual, accessibility, security, data, or another
  selected lens inside this same reviewer context and single review artifact.
- `SEPARATE` - only for HIGH risk, genuinely independent specialist expertise, or an explicit human
  request. Record the rationale and reconcile the specialist result into this one authoritative
  artifact; do not create duplicate general reviewers.
- `NOT_REQUIRED` - allowed only with a recorded rationale, and never for HIGH risk.

Browser acceptance remains required for routed user-visible UI work. For LOW/MEDIUM UI, visual and
accessibility critique is INLINE by default.

## FULL versus DELTA

The initial review is `FULL`, bounded by its selected tier. FULL is also mandatory for requirement
changes, scope expansion, shared contracts, auth/security/data/migration/lifecycle behavior, new
dependencies, broad refactors, or ambiguous evidence.

A `DELTA` review is allowed only for named accepted findings or human-requested polish when
requirements and contracts are unchanged, edits remain within approved files, the diff is narrow,
and affected acceptance criteria/invariants are explicitly listed. It must name the prior snapshot
whose unaffected review conclusions were explicitly marked reusable. Inspect the correction, its
changed files, affected criteria, affected validation, and regression seams; carry forward only the
unaffected conclusions. If materiality or evidence is unclear, stop and require FULL.

After a FULL `CHANGES_REQUESTED` that contains only named bounded findings, the Reviewer may approve
the unaffected conclusions as the reusable DELTA basis and name that reviewed snapshot. This does
not change the overall verdict or permit shipping; it only avoids rereading settled rubric areas.

Human visual feedback after review uses focused browser/visual DELTA review and affected checks unless
the feedback changes requirements or scope.

## Review budget

Use the budget selected at Scope: defaults are LOW 5 minutes, MEDIUM 15 minutes, and HIGH 30 minutes
unless project evidence justifies a different positive bound. The budget limits work, never lowers
the approval bar. At the bound, if proof is insufficient, stop with specification `UNVERIFIABLE`,
quality/overall `CHANGES_REQUESTED`, and a concrete escalation reason. Do not silently continue into
another broad pass. Record the reason in the artifact and `reviewPolicy.escalationReason`.

## Evidence-efficient execution

Start verdict-first and record only rubric deltas and supporting evidence; do not repeat the full PRD
or design prose. Inspect fresh controller evidence and do not rerun every expensive command by
default. Rerun only missing, stale, inconsistent, or suspect evidence.

Review in this order:

1. freeze baseline, allowlist, pre-existing changes, review type, and snapshot;
2. apply the tier to changed criteria/files and named risky seams;
3. perform the configured specialist mode in the same artifact;
4. assess focused and canonical validation evidence;
5. verify candidate findings against surrounding code/tests before reporting them;
6. emit specification, engineering-quality, and overall verdicts plus whether the review basis is
   reusable for a later DELTA.

## Findings and output

For every finding include ID, BLOCKER/MAJOR/MINOR/NIT severity, INTRODUCED/PRE_EXISTING/UNCLEAR
origin, affected criterion/invariant, exact evidence, plausible failure scenario and impact, required
correction/proof, and status. Avoid duplicates and speculative style noise.

Use `.agent/templates/REVIEW_TEMPLATE.md`. If read-only enforcement prevents writing, return the
completed artifact to the coordinator to save unchanged as `.active/REVIEW.md`.
