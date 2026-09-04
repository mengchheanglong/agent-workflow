# PRD Clarity and Traceability Checklist

Use this reference during drafting and final review of a stakeholder-facing PRD.

## Responsibility model

- State the product model in one sentence before listing features.
- Separate what the product owns from what customers, merchants, partners, or another team own.
- If ownership depends on an unresolved business or money flow, label the capability conditional.
- Repeat the same condition in the priority table, product requirements, release criteria, risks, and open decisions.
- Do not let an example scenario silently expand the product into a marketplace, service desk, moderation platform, or finance operator.

## Conditional decision decomposition

Do not hide several responsibilities behind one question such as “Does the product control payments?” Split independent gates:

1. **Observe or record:** Does the system display, receive, or match information?
2. **Control or hold:** Does the organization control the underlying asset, state, or process?
3. **Act or transfer:** Does it perform a consequential action for another party?
4. **Reverse or dispute:** Who owns refunds, rollback, appeal, or chargeback authority?
5. **Verify destination:** Must it approve where the controlled asset or result goes?

Observation does not imply custody; custody does not imply transfer; transfer does not imply reversal authority. Give each gate its own dependent feature, permissions, release rule, decision owner, and approve/exclude outcome.

## People model

Keep four concepts distinct:

1. **External user/persona** — receives value or support
2. **Dashboard permission role** — controls data and actions
3. **Operating responsibility** — owns daily work and backup coverage
4. **Decision stakeholder** — approves product rules and scope

One person may hold several permission roles. A stakeholder does not automatically need a dedicated dashboard role. Mark every staffing proposal as proposed until management approves it.

## Terms that require definitions

Define a term when a reviewer could reasonably ask “what exactly does that mean?” Common examples:

- **Support case:** one official problem record with source, owner, status, evidence, communication, linked information, and outcome
- **Related record:** enumerate the concrete object types
- **Specialist:** name the authorized responsibility that investigates while Support retains user communication
- **Failed:** identify the system or provider state that declares failure
- **Expired:** identify the approved time window that ended
- **Unmatched:** identify the record that exists and the expected object it cannot be connected to
- **Delayed or stuck:** define start event, limit, timezone, ending event, and data source before use
- **Resolved versus closed:** define the operational difference if both states appear

Avoid vague labels such as “recent activity,” “specialized record,” “problematic order,” or “adjust the system” when concrete wording is available.

## Channel and case-flow clarity

For every intake channel, answer:

1. Who receives the notification?
2. Is case creation automatic, manual, or unconfirmed?
3. What missing information is collected?
4. Where is the official case stored?
5. Who can see and own it?
6. Which features may be used to investigate it?
7. Who sends the user-facing response and through which channel?
8. What history remains after closure?

For off-platform intake, create the initial case and preserve the original message, sender, time, and channel before asking for missing information. Otherwise the request can be lost during follow-up.

Keep one user problem as one connected case. Specialist investigation may happen in Finance, Accounts, Stores, Orders, or Technical Health without creating an unrelated duplicate support case.

## Dangerous actions and automatic monitoring

A name such as restrict, suspend, restore, refund, export, recover, or impersonate is not product semantics. Before implementation, require an action or restriction matrix that names the exact target, permitted grounds, decision owner, allowed roles, effects on related users/records/money, evidence, confirmation or stronger authentication, additional approval, notice, duration, reversal/restoration rule, and audit fields. If the matrix entry is not approved, keep the action unavailable even when read-only visibility is a Must.

Do not say “the system detects” without an approved monitoring register. For every promised automatic signal, record the source, signal, source-specific meaning, owner, automatic/manual status, affected-record link, and safe-retry rule. Unmonitored failures need a manual route and must not be presented as covered.

## MoSCoW mapping

- Copy every prioritized capability's exact approved name into the PRD.
- Preserve one short reason per capability.
- State the release meaning of Must, Should, Could, and Won't for this project.
- Clarify that requirement-level “must” defines mandatory behavior once a capability is included; it does not change that capability's MoSCoW priority.
- Identify which Should items are intended for V1 when capacity permits and which can safely move after the pilot starts.
- Preserve all Won't items, including prohibited capabilities, so they cannot silently return under renamed labels.

## Requirements quality

A product-level requirement should make these clear:

- Actor or authorized responsibility
- Object or workflow
- Minimum observable behavior
- Safety or product boundary
- Condition, if unresolved

It should not prescribe:

- Endpoint paths
- Database schemas
- Framework components
- Source-directory layout
- Exhaustive validation and error matrices
- Test implementation

Stable requirement IDs are useful for later plans and tests, but the PRD remains the product contract—not the technical specification.

## Decision register outcomes

Give every unresolved decision a stable ID and record its dependent scope, proposed owner, date, rationale, and affected artifacts. Use only explicit outcomes:

- **Approved:** the decision and dependent scope are accepted.
- **Excluded:** the dependent feature or action is removed.
- **Deferred as nonblocking:** the dependent Should or Conditional Must is not included.
- **Open:** evidence is still needed and the decision blocks approval while its dependent scope remains included.

A lead or product manager may consolidate approval but must not silently replace Finance, Security, Operations, or Management authority for domain decisions.

## Metrics and release

- Use a pilot baseline instead of inventing numeric targets without evidence.
- For each published measure, require an approved definition, source, time period, timezone, and owner.
- Release criteria should cover product scope, core workflows, safety, operating readiness, usability, and quality.
- Conditional capabilities must be either approved and ready or explicitly removed before release.
- Mock data and prototypes must be separated from pilot production data.

## Pilot hypothesis, learning, and stop gates

- State the expected operator or business change as a falsifiable hypothesis, not simply “deliver the dashboard.”
- Record cohort size and selection criteria; if management has not decided them, keep them in the open-decision table.
- Roll out through an internal smoke test, the smallest selected cohort, a midpoint review, and an end-of-pilot review.
- Observe whether core workflows can be completed, where manual workarounds remain, and whether support demand fits available capacity.
- End with an explicit expand, iterate, pause, or stop decision and record which assumptions were validated, invalidated, or remain unknown.
- Define immediate stop or rollback triggers for unauthorized access, cross-customer exposure, corrupted money state, irrecoverable data loss, or repeated failure of a Must workflow.
- Do not confuse feature acceptance criteria with whole-release readiness or pilot success.

## Research and citations

- Sample several professional PRD approaches; do not copy one vendor template.
- Use external sources to justify document method, not project-specific product claims.
- Keep research citations near the method claims they support.
- When using the strict grounded-citations verifier, keep no more than three citations in one prose unit. Place independently supported claims in separate Markdown paragraphs; several citation groups on one physical line may be treated as one unit.
- On Windows, do not build a citation-ledger path from Git Bash `$PWD` when the helper runs under Windows Python: `/c/...` may be interpreted as `C:\c\...`. Pass one explicit native absolute path such as `C:/Users/.../citation-ledger.json` through `--ledger` on reset, add, render, and verify, then confirm the location with `sources.py --ledger <path> list`.

## Mechanical verification

Run checks for:

- Missing or duplicate MoSCoW capabilities
- Duplicate requirement IDs
- Broken relative links
- Missing required PRD sections
- Missing conditional-gate wording
- Stale terms from superseded product models
- Placeholder text such as TODO or TBD
- Citation integrity
- Markdown/whitespace errors
- Workspace routing that still points to stale briefs, SRS files, or prototypes

## Independent review discipline

1. Finish the draft and mechanical checks.
2. Hash the exact PRD snapshot.
3. Send only the artifact and contract to a fresh-context adversarial reviewer.
4. Do not mutate the PRD while the blocking review is pending.
5. After findings return, re-check the current hash and classify each finding as accepted, rejected with evidence, or deferred behind a decision gate.
6. Apply accepted changes to the PRD and any canonical routing files that repeat the old statement.
7. Re-run structural, link, citation, and whitespace checks.
8. Material changes require a new hash and focused re-review.
9. Limit the micro-review to the named corrections and direct contradictions they could introduce. When it passes, stop broad review and move the draft to stakeholder review.

## Final stakeholder test

A PRD is ready for stakeholder review only when a reader can answer:

- What problem does this product solve?
- What does the product own and not own?
- Who uses and operates it?
- Why is each major capability included, conditional, deferred, or excluded?
- How do the main workflows start and end?
- Which rules are approved and which decisions remain open?
- What makes the pilot or release ready?
- What feedback or approval is requested from this reader?
