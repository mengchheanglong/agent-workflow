# Post-Foundation External Packaging (Durable Harness)

After a durable-workflow conformance foundation is sealed and later product gates are locked, prefer **external-evidence packaging** over new vectors.

## When this applies

- Gate/foundation decision sealed green (or correction sealed after honest incomplete bound).
- Custom persistence parked because an incumbent/alternative already passed.
- Consumer remains candidate-only.
- T5 / memory / multi-agent product locked for want of external signal.
- User asks “what next?” and the honest answer is not more internals.

## Packaging deliverables

1. Entry docs reconciled to the newest sealed actor/foundation decisions.
2. Public-safe overview (~10 minutes) with non-claims.
3. Architecture diagram: caller → durable runtime → canonical commit function → receipts/history/state.
4. Runbook with pins, doctor, test packs, consumer candidate warnings.
5. Publication blockers list (privacy, doctor gaps, failpoints in commit function, raw-ingress claim narrowness, private visibility).
6. Local smoke: doctor + foundation suite + actor suite + candidate consumer when topology allows.

## Do not rewrite frozen evidence

- Frozen implementation matrices and closed-clock artifacts stay historical.
- Remove them from “current status” reading paths or add addenda; do not silently edit “NOT_STARTED” scaffolding into a new present tense.
- Superseded pass/incomplete pairs must both remain visible (e.g. T4 incomplete + T4R correction).

## Claim hygiene

| Safe | Unsafe |
|---|---|
| `EXTERNAL_DEMAND_NOT_ESTABLISHED` | “Nobody needs this” / global absent without contact |
| Candidate consumer 5/5 synthetic | External user / product validation |
| Library `parseCanonicalJson` tested | Raw ingress always rejects duplicate keys |
| Test failpoints in SECURITY DEFINER function | Production-ready multi-tenant deploy |
| Category funding for durable execution | Demand for this harness |

## Restate/Postgres synthetic topology ops

- `docker` down → doctor connection refused is environment, not continuity failure.
- Restate log `node-name is required` / working dir has data from node X but default is Y: wipe **synthetic** Restate volume or set explicit node name; then `compose up --wait`.
- After IP/network change, re-validate `CK_RESTATE_DEPLOYMENT_URI` from Restate’s view of the host; historical IPs can rot.
- Registration/connectivity failures before invocation are infrastructure evidence.

## Relationship to Agent OS ideas

Continuity-class kernels prove **commit/truth** properties. Always-on OS/agent state (“state continuous; thinking intermittent”) is a separate architecture concept and must not silently become the next implementation mission during packaging.
