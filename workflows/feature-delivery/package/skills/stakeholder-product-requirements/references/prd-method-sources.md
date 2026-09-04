# PRD Method Sources — Verified Reference List

Professional PRD guidance reviewed and used for the Angkoro admin-system PRD cycle
(v0.1 draft → v5.3 FINAL, August 2026). Reuse these when researching PRD method; verify
URLs before registering them in a citation ledger.

## Core sources

| # | Source | URL | Contributes |
|---|---|---|---|
| 1 | Planio — lean PRD | https://plan.io/blog/one-pager-prd-product-requirements-document | Purpose / features / release criteria / constraints; explicit "what you're NOT doing" |
| 2 | Atlassian — requirements | https://www.atlassian.com/agile/product-management/requirements | Goals, assumptions, user stories, designs, open questions, out-of-scope; living document warning |
| 3 | Productboard — PRD guide | https://www.productboard.com/blog/product-requirements-document-guide | Problem → outcome → scope → constraints → acceptance criteria; implementation details belong in a later spec |
| 4 | Aha! — PRD templates | https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template | Overview, objective, context, assumptions, scope, requirements, performance, open questions |
| 5 | Figma — PRD resource | https://www.figma.com/resource-library/product-requirements-document | Personas, user flows, risks, dependencies, evaluation, release criteria |
| 6 | SVPG — Discovery vs Documentation | https://www.svpg.com/discovery-vs-documentation | A PRD is fine AFTER discovery; written instead of discovery it produces finger-pointing and no innovation |
| 7 | SVPG — The Four Big Risks | https://www.svpg.com/four-big-risks | Value / usability / feasibility / business-viability framing; internal products still carry all four risks |
| 8 | Agile Business Consortium — MoSCoW | https://www.agilebusiness.org/resource/what-is-moscow-prioritization | Must = release unsafe/illegal/unviable without it; a workable workaround ⇒ Should or Could; ~60% Must-effort ceiling; Won't recorded to prevent informal reintroduction |
| 9 | Atlassian — Definition of Done | https://www.atlassian.com/agile/project-management/definition-of-done | Release readiness (whole increment) ≠ feature acceptance (single behavior) |

## URL pitfalls

- The Consortium MoSCoW page exists ONLY at `…/resource/what-is-moscow-prioritization`
  (no `.html`). The `.html` variant returns 404. Verify each source URL with an actual
  fetch before adding it to a citation ledger; a bad variant was silently registered
  during this project and had to be hand-corrected in the ledger JSON.
- SVPG articles sometimes render mostly navigation chrome via extractors — the article
  body is short but the key claims (four risks, PRD-after-discovery) are verifiable.

## Key quotable positions

- **Planio:** "being clear on what you're not going to do can be just as important"; set
  release criteria around five areas; build timeline on constraints, not dates.
- **Atlassian:** PRDs should evolve; include assumptions and open questions; don't write
  a rigid document that stops changing.
- **Productboard:** keep the PRD about problem/outcome/customer value; push architecture,
  schemas, and detailed specs into a separate technical specification.
- **SVPG:** "the problem is that in nearly every case… the PRD is written *instead of*
  the product discovery work, rather than after."
- **Consortium:** MoSCoW's Must = Minimum Usable SubseT; Should = painful workaround but
  viable; Could = contingency pool (~20%); Won't recorded to stop informal reintroduction.
- **DoD:** definition of done is collaboratively defined, visible, regularly updated, and
  applies to increments — distinct from per-story acceptance criteria.

## Suggested ledger workflow (grounded-citations)

1. `reset` with an explicit native absolute `--ledger` path.
2. `add` each verified URL with title.
3. Draft prose with ≤3 citations per sentence; split multi-source paragraphs so the
   strict verifier treats them as separate units.
4. `render --replace-in <draft>` to regenerate the numbered Sources block.
5. `verify <draft> --strict` after every edit round, not just at the end.
