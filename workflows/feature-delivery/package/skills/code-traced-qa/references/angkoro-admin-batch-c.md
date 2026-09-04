# Worked Example — Angkoro Admin prototype-v2, QA Batch C

Target: Next.js 16 App Router app at localhost:3000, source
`C:/Users/User/workspace/angkoro/dashboard/admin/prototype-v2`.
Mock store `lib/mock-store.ts` seeded from `data/seed.ts`; session fixed as
Super Admin ("Sophea Chan" = ADM-01). Batch C scope: admin accounts, security/
audit, recovery, operational health, command palette, adversarial inputs.

Result: all scoped routes HTTP 200; 10 BUG findings + 11 OK items, all code-traced.

## Findings (summary)

1. High — command palette pushes user results with group `"Users"` but the
   render-order array lists `"Merchant accounts"` → user/merchant search returns
   nothing (R1.9 violation).
2. High — Disable button rendered for every Active row, no self-guard → Super
   Admin can disable their own account; own sessions vanish while client-side
   fixed session keeps working.
3. High — `enableAdmin` / `setAdminRole` imported but zero call sites app-wide →
   disabled admin can never be re-enabled, roles unchangeable despite UI implying it.
4. Medium — security page maps full audit (seed clone included) with hardcoded
   `thisSession: true` → years-old seeded entries badged "This session"; also
   unused `AUDIT` import.
5. Medium — ConfirmAction `confirm()` has no double-submit guard → rapid
   double-click duplicates audit entries.
6. Medium — recovery approval dialog claims sessions revoked (R6.11), toast says
   "old sessions revoked", but `decideRecovery` mutates only the case record.
7. Medium — invite dialog has no duplicate-email check; weak regex only.
8. Low — `revokeAdminSession` doesn't decrement the owning admin's
   `activeSessions`; disable does → stale counts.
9. Low — recovery approvable at 0/N evidence; button gated only on case state.
10. Low — no maxLength on reason textarea; audit rendering lacks break-words →
    5000-char unbroken paste overflows panel.

OK items included: append-only audit prepend works; own-session revoke hidden;
retry hidden for Healthy + non-retryable shows "not safe"; evidence buttons
filtered to unprovided + idempotent store action; double-approve unreachable via
UI (button disappears post-decision); ADM id scheme collision-free because rows
are never removed; cmdk 1.1.1 + `.includes()` filtering = regex-safe; empty
states present; permission filtering present; whitespace-only reason rejected
(trim ≥8).

## Lessons

- The task brief's hint list ("can you disable YOUR OWN account?", "collision
  risk after disable+invite?") mapped directly to findings 2 and the OK on IDs —
  always test each hinted hypothesis against actual code rather than assuming
  the hint is accurate (the collision hint was a false alarm).
- Operator identity lives in the session provider, not the seed order — verify
  which seed row is "you" before claiming self-action bugs (brief said ADM-03;
  reality ADM-01).
