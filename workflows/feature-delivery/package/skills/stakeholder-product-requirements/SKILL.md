---
name: stakeholder-product-requirements
description: "Use for stakeholder PRDs from context and decisions."
version: 1.2.0
metadata:
  hermes:
    tags: [prd, product-management, requirements, stakeholder-review, moscow]
---

# Stakeholder Product Requirements

Create professional product requirements documents that explain **what is being built, why, for whom, within which responsibility boundary, and how stakeholders will decide whether it is ready**. Keep the PRD separate from the later SRS, architecture, implementation plan, and acceptance-test suite.

## When to Use

- A stakeholder asks for a PRD rather than an SRS
- A feature list or MoSCoW review must become one coherent product document
- Prior stakeholder comments revealed unclear terms, ownership, scope, or operating flows
- The product crosses Support, Operations, Finance, Security, or Technical responsibilities
- Unresolved decisions must remain visible instead of becoming guessed requirements

**Do not use for:** a single feature's implementation specification, API contract, database design, coding plan, or test plan.

## Artifact Classification Gate

Before drafting, state which artifact is being produced:

- **Stakeholder PRD:** product purpose, users, responsibilities, outcomes, scope, requirements, risks, decisions, and release readiness
- **Feature specification/SRS:** exhaustive behavior, states, validation, errors, data, and acceptance criteria
- **Technical plan:** architecture, code paths, dependencies, migration, testing, and delivery sequence

Do not force implementation-spec sections such as commands, source layout, framework style, or database tables into a stakeholder PRD.

## Workflow

### 1. Establish authority and status

Read project sources in their declared authority order. Prefer the canonical product context and current decisions over older briefs, prototypes, and discussion history. Treat source code and tests as authority only for what currently exists.

If sources conflict, surface the conflict. Never silently choose the more detailed or older artifact.

Mark the PRD as **Draft for stakeholder review** until named decision owners approve it. Proposed owners and staffing must be labeled as proposed.

### 2. Research professional patterns without copying

Sample several credible PRD approaches and extract common functions: purpose, users, assumptions, goals, scope, requirements, non-goals, risks, dependencies, release criteria, success measures, and review process. A pre-verified source list with URL pitfalls and key positions lives in [`references/prd-method-sources.md`](references/prd-method-sources.md).

Tailor the structure to the product. “One page” means lean, not artificially short. A cross-functional internal product may need a short executive summary followed by a longer reviewable PRD.

Keep external-method citations in a short methodology section or appendix. Product claims should be grounded in approved project context and stakeholder decisions.

### 3. Surface the product model and decision gates

Write the product responsibility boundary before the feature list:

- What does the product own?
- What remains the customer's, merchant's, partner's, or another team's responsibility?
- Which workflows exist only if an unresolved business model or money-flow decision is confirmed?
- Which users are dashboard operators, which are permission roles, and which are decision stakeholders?

Use explicit conditional wording instead of guessing. Repeat material gates in scope, requirements, release criteria, and open decisions.

### 4. Draft the stakeholder PRD

Use this adaptable structure:

1. Document control and status
2. Stakeholder decisions requested
3. Executive summary and pilot hypothesis
4. Product context and responsibility boundary
5. Key terms
6. Problem statement
7. Goals and non-goals
8. Users, permission roles, operating responsibilities, and decision stakeholders
9. Product principles
10. Core user or operating journeys
11. Prioritized scope with one reason per capability
12. High-level product requirements with stable IDs
13. UX, security, privacy, and audit expectations
14. Pilot or release success measures
15. Release-readiness criteria and stop or rollback conditions
16. Constraints and dependencies
17. Risks and mitigations
18. Open decisions, why they block work, and who should decide
19. Pilot rollout and learning plan
20. Stakeholder review checklist, decision/change log, and references

See [`references/clarity-and-traceability.md`](references/clarity-and-traceability.md) for detailed wording, MoSCoW, and verification checks.

### 5. Keep requirements product-level

High-level requirements may state what an authorized user must be able to see, decide, record, or complete. They should not prescribe endpoints, tables, components, or implementation algorithms.

Explain this important distinction:

> MoSCoW determines whether a capability is committed. “Must” inside a requirement means the behavior is mandatory if that capability is included; it does not promote a Should, Could, or conditional feature to MoSCoW Must.

For each capability, make the outcome, responsible user, minimum behavior, and boundary understandable to a feature developer without turning the PRD into an SRS.

### 6. Separate release acceptance from pilot learning

Feature acceptance proves that an individual behavior works. Release readiness proves that the complete increment is safe and operable. A pilot must also explain what the team is trying to learn.

Include:

- A falsifiable pilot hypothesis connecting the admin workflow to an operator or business outcome
- Pilot cohort size and selection criteria, or an explicit open decision when unknown
- Staged rollout from internal smoke test to the smallest selected cohort
- Named observation points, midpoint review, and end-of-pilot review
- Measures with definition, source, owner, baseline, and review date rather than invented targets
- Expand / iterate / pause / stop choices at the end of the pilot
- Immediate stop or rollback triggers for unauthorized access, cross-customer data exposure, corrupted financial state, irrecoverable data loss, or repeated inability to complete a Must workflow

A polished PRD is not evidence that value, usability, feasibility, or viability has been proven. Keep discovery and operator validation active during the pilot.

### 7. Make stakeholder feedback operational

When previous reviewers asked what a term means, how a case arrives, who owns an action, what happens next, or whether a condition is detected automatically, convert that feedback into durable PRD clarity:

- Add a glossary definition
- Add a complete start-to-finish flow
- Name the operator and communication owner
- Name concrete linked objects instead of saying “related record” alone
- Separate a case from the specialist feature used to investigate it
- State whether intake is automatic, manual, or unconfirmed
- Define timing and metric semantics before using status labels
- Add the unresolved point to the decision table

### 8. Verify before delivery

Run both semantic and mechanical gates:

- Every prioritization item appears under its exact name
- Every capability has one reason
- Requirement IDs are unique
- Conditional gates are repeated consistently
- Permission roles are not confused with staffing headcount or stakeholder roles
- Prototypes are not presented as production proof
- No arbitrary target or undefined operational term is presented as approved
- Internal links and citations resolve
- Markdown and whitespace checks pass
- Workspace routing points to the new PRD without replacing the canonical product context

Freeze the PRD hash before independent adversarial review. Do not mutate the frozen artifact while review is pending. Any material revision requires a new hash and re-review.

## Common Failure Modes

- Leaving a superseded PRD live next to its replacement instead of archiving it with a banner
- Updating routing to a new PRD version while companion registers still carry the old role model without noting that the PRD wins on conflict
- Deleting a stray near-duplicate of the new FINAL PRD without diffing it first — loose workspace copies can be an older working variant with a different role model, section set, or requirement numbering, and are worth archiving rather than discarding
- Trusting a citation URL (e.g., a `.html` suffix variant) without fetching it; dead ledger URLs undermine the document's method claims

- Copying a generic template instead of adapting it to the product model
- Producing an SRS while calling it a PRD
- Listing screens without explaining the operating problem or responsibility boundary
- Hiding unresolved assumptions inside unconditional requirements
- Treating four permission roles as four employees
- Treating Product Management as a dashboard role without explicit approval
- Implying that email or messaging channels create cases automatically
- Claiming automatic detection of business problems without approved rules
- Using “delayed,” “stuck,” “active,” or “successful” without definitions
- Treating mock data or a prototype as proof of production behavior
- Updating the PRD while leaving future-agent routing pointed at stale documents

## PRD evolution after stakeholder review

A stakeholder-review draft is not the end state. Expect the document to be reworked through many lead-driven iterations and to emerge as a differently structured FINAL PRD (observed: v0.1 → v5.3 across one week of lead feedback). When that happens:

1. Treat the approved FINAL version as the new product authority; file the earlier draft under `archive/superseded-prds/` with a supersession banner rather than leaving two live versions.
2. Update routing files (README, AGENTS.md) to point at the FINAL PRD and note which older statements it replaces (e.g., a role-model change).
3. Companion documents written against the old draft (internal detail registers, evidence audits) keep stale role names and wording until remapped — record that the PRD wins on conflict instead of silently rewriting them.
4. Real restructurings observed in practice: permission roles collapsing (four named roles → two), separate modules absorbed into one (Merchant Accounts + Shopper Support → Users), money actions moving between product and merchant (refunds leave admin scope), monitoring boundaries drawn around existing tools (Uptime Kuma/Slack), and MoSCoW Must/Should replaced by a P0–P3 implementation-order ladder where all features are committed but sequenced. Verify each change landed consistently across priority ladder, requirements, flows, and final rules.

When a new FINAL version arrives from the user as a loose file (workspace root, chat attachment):

1. Copy it into the project workspace first, then diff against any existing live PRD before deleting anything — near-identical filenames can hide divergent content (an older working variant of v5.0 differed from the archived v5.0 in role model, sections, and requirement numbering).
2. Move every superseded copy to `archive/superseded-prds/` using the naming convention `PRD_vX.Y_YYYY-MM-DD.md`, even when it was never the live authority (stray duplicates count as versions worth preserving for traceability).
3. Update the archive README's version table in the same change set: what each file was, what replaced it.
4. Re-run link checks afterward — routing files and archive indexes frequently reference the moved paths.

## Completion Standard

The deliverable is complete when a nontechnical stakeholder can understand the product's reasoning and decisions, a feature developer can identify the intended outcome and boundary of each approved capability, unresolved decisions are impossible to mistake for requirements, and all verification gates pass.
