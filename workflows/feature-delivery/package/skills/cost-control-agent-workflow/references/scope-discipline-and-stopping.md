# Scope Discipline and Stopping

## The Rule

When the user explicitly bounds the task, do exactly that and stop. Do not add unsolicited browser evidence, extra reviews, server management, or rollback discussions.

## Signals That You've Over-Delivered

- User says "you gone overboard" or "i only ask you to update the workflow"
- User says "no need to roll back, just report our current status"
- User repeats the original narrower ask after you've already done more
- User says "stop" or "never mind" mid-execution
- User says "just give me the answer" or "don't format like this"
- User says "you always do Y and I hate it" or "why are you explaining"
- User says "proceed" but you've already done work beyond what was asked
- User corrects batching: "I ask you to update the workflow" (singular) when you tried to batch multiple features

## New Signals From This Session

- **Branch naming**: User explicitly corrected `feat/*` → `feature/*`. Always confirm before branching.
- **Access model**: User corrected "Merchant = Store owner" → they are separate concepts. Merchant is user-level, Store owner is store-specific.
- **Scope discipline**: User said "i only ask you to update the workflow" after we ran browser verifications and launched dev servers. The workflow update was the ONLY ask.

## What This Looks Like in Practice

| User asks for | Do NOT also do |
|---|---|
| "Update the workflow" | Run browser verifications, launch dev servers, start extra reviews, capture evidence |
| "Report our current status" | Start repairs, browser reruns, or additional reviews |
| "Just verify" | Commit, push, merge, or deploy |
| "Update the workflow in angkoro-admin too" | Run full validation suites or browser proofs on the existing shipped feature |

## Why This Matters

Over-delivery wastes model cost (the user pays per token) and burns the user's time. It also erodes trust — the user learns that asking for a small thing triggers a large, unasked-for operation. In a cost-controlled workflow, scope discipline is a first-class requirement, not a nice-to-have.

## Recovery

If you catch yourself mid-over-delivery: stop, acknowledge, and ask whether the user wants the extra work continued. Do not assume the extra work is welcome just because it's "good practice."
