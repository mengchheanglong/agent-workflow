# Gemini Delivery Loop

A lightweight agent workflow for spec-driven feature implementation using Gemini Flash as the builder and Gemini Pro as the independent reviewer.

## Overview

The Gemini Delivery Loop is designed for repositories where architecture and specification are owned externally (e.g., by humans or stronger reasoning models), and the agents are tasked purely with executing, validating, and reviewing the implementation.

## The Delivery Loop

```text
ChatGPT / architecture → approved docs/specs/<feature>.md
          ↓
Gemini Flash WHOLE FEATURE IMPLEMENTATION
          ↓
typecheck + tests + build
          ↓
Gemini Pro FRESH INDEPENDENT REVIEW
          ↓
[APPROVE] → ready (human/ChatGPT final decision → commit/merge)
          ↓
[CHANGES_REQUESTED]
          ↓
Gemini Flash FOCUSED FIX ONLY
          ↓
fresh validation
          ↓
Gemini Pro FOCUSED RE-REVIEW
          ↓
(Max 2 broad fix cycles) → [STILL BLOCKED/MAJOR] → STOP → bring to human/stronger model
```

## Role Definitions

-   **Architect (Human / ChatGPT / Sonnet 3.5):** Defines the specification in `docs/specs/<feature>.md`. Does not write code in this loop.
-   **Builder (Gemini Flash):** Implements the whole specification. Writes tests. Runs validation (typecheck, test, build). Fixes findings. **Cannot** change architecture, weaken tests, or merge.
-   **Reviewer (Gemini Pro):** Reviews the code from a fresh, independent context. Enforces spec compliance and engineering standards. Cannot implement features or write fixes.

## Installation

Copy the contents of the `package/` directory into the root of your target repository.

## Usage

The workflow is driven by three primary prompts, designed to be run by your agent runner/coordinator:

1.  **Implement:** Run `gemini-flash-delivery/package/.agent/prompts/IMPLEMENT.md` with Gemini Flash.
2.  **Review:** Run `gemini-flash-delivery/package/.agent/prompts/REVIEW.md` with Gemini Pro.
3.  **Fix:** Run `gemini-flash-delivery/package/.agent/prompts/FIX.md` with Gemini Flash.

## Bounded Fix Loops

Agents can sometimes get stuck in endless fix-review loops, repeatedly failing tests or introducing new regressions while fixing old ones. 

To prevent this, this workflow enforces a **Bounded Fix Loop**:
-   The Builder gets a maximum of **2 broad fix cycles**.
-   If `BLOCKER` or `MAJOR` issues remain after the 2nd cycle, the workflow halts with a `BLOCKED` status.
-   At this point, a human or a more capable model must intervene to unblock the work.

## Escalation Policy

For high-risk implementations involving:
-   Authentication / Authorization
-   Data migrations / Integrity
-   Concurrency / Race conditions
-   Privacy / PII

The workflow optionally escalates the review stage to a stronger model (e.g., Claude 3.5 Sonnet) or mandates a human review before the `APPROVE` verdict can be finalized.
