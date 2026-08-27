# Gemini Delivery Workflow

This document defines the core delivery loop for the Gemini Delivery workflow.

## The Delivery Loop

The workflow moves through defined stages, tracking state to ensure independent implementation, validation, and review.

## Lightweight Status Values

The current state is tracked using these status values:
-   `IDLE`: No active work.
-   `BUILD`: Gemini Flash is implementing the feature.
-   `VALIDATE`: Running typechecks, tests, and builds.
-   `REVIEW`: Gemini Pro is conducting an independent review.
-   `FIX`: Gemini Flash is addressing review findings.
-   `BLOCKED`: The feature requires human or escalation model intervention (e.g., max fix cycles reached).
-   `DONE`: Reviewed, approved, and ready for human merge.

## Feature Discovery

1.  Read `.active/CURRENT.md` to identify the active feature name.
2.  Locate the approved specification at `docs/specs/<feature>.md`.
3.  Transition to `BUILD` status.

## Builder Rules (Gemini Flash)

**Allowed:**
-   Read the repository, `.active/` state, and `docs/specs/`.
-   Implement the *whole* approved spec in one continuous effort.
-   Write unit and integration tests alongside implementation.
-   Run validation commands (tests, typechecks, build).
-   Fix its own obvious implementation errors discovered during validation.
-   Update required documentation and state tracking files.

**Not Allowed:**
-   Change the feature architecture or specification.
-   Silently weaken tests or type constraints to force a passing state.
-   Declare its own implementation "approved".
-   Expand the scope of work beyond the specification.
-   Commit, push, or merge code.

## Validation Requirements

Before a feature can be handed off for review, the Builder must ensure a clean validation state:
1.  Typecheck passes.
2.  All tests pass (including new tests written for the feature).
3.  The project builds successfully.

## Review Trigger

Once validation is clean, the status transitions to `REVIEW`. The code is handed to Gemini Pro. 
-   **Invalidation:** Any code change made by any actor after a review has started or completed automatically invalidates the review. A fresh validation and re-review are required.

## Fix Loop

If the Reviewer issues `CHANGES_REQUESTED`:
1.  Status transitions to `FIX`.
2.  Builder addresses the specific findings.
3.  Builder runs focused validation and full validation.
4.  Status transitions back to `REVIEW`.
5.  **Bounded Limit:** Maximum of 2 broad fix cycles (`maxFixCycles: 2`). If `BLOCKER` or `MAJOR` issues remain after 2 cycles, status becomes `BLOCKED`.

## High-Risk Escalation Policy

If the feature involves auth, data integrity, permissions, concurrency, or migrations, an escalation review by a stronger model (e.g., Claude 3.5 Sonnet) or a human is required before final `APPROVE`.

## State Tracking

State is tracked in a lightweight JSON file: `.active/STATE.json`.

```json
{
  "status": "BUILD",
  "feature": "feature-name",
  "fixCycles": 0,
  "maxFixCycles": 2,
  "lastValidation": "pending",
  "review": "pending"
}
```

## Shipping

Agents **do not** merge. When status is `DONE`, a human or a high-level coordinator makes the final decision to commit, push, or merge the feature branch.
