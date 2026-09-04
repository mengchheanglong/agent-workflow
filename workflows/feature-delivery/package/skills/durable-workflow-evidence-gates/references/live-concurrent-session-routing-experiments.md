# Live Concurrent-Session Routing Experiments

Use this pattern when testing whether asynchronous work returns to the correct parent session inside one shared agent/backend process.

## 1. Reproduce the real shared boundary

Independent CLI processes do not exercise a process-wide completion queue. Freeze one backend process with two simultaneously live parent sessions over the same transport, distinct durable session keys, distinct workspaces, and deliberately reversed child completion order.

Treat model/provider identity as executor metadata. The routing oracle must use transport/session metadata and durable state, not model prose.

## 2. Gate live execution behind an immutable authority unit

Freeze and review together:

- preflight and non-claims;
- exact driver;
- provider/model and request ceiling;
- one-attempt rule and immutable clock;
- synthetic markers and expected ordering;
- disposable profile/auth/environment policy;
- event and durable-database oracle;
- cleanup and outcome precedence.

Compile and run a validation-only mode before the clock. Validation must make no credential copy, server start, session creation, provider call, or temporary-root change. If live is the only phase authorized to touch auth, validation must not even probe auth existence.

Avoid generic truthiness across mixed validation fields. A safe assertion such as `live_actions_performed: false` or `auth_read: false` is expected, not a failed prerequisite. Evaluate each invariant with explicit positive and negative conjuncts; never `all(v is not False …)` or `all(v is True …)` over heterogeneous result maps that intentionally mix booleans, strings, and integers.

## 3. Isolate identity, state, credentials, and environment

Use one uniquely named OS-temporary root for HOME, USERPROFILE, AppData, local AppData, TEMP/TMP, application home, workspaces, state DB, logs, and caches.

Allowlist the child process environment. Do not inherit parent session IDs, UI session IDs, gateway routing keys, profile selectors, API-key/token/secret variables, or proxy settings accidentally. Retain only Windows runtime essentials and the exact experiment variables.

Never clone a real profile. If provider access requires an auth store, define whether it is opaque or structurally minimized. Prefer a minimized provider-only temporary store and disable reusable refresh credentials before writing it. Never persist credential values, hashes, counts, or raw auth metadata in evidence.

## 4. Match the installed desktop routing path, then make the oracle mechanical

Inspect frozen source before freezing session source and async flags. If desktop completion ownership rewrites the routable key only when `source == "tui"`, the experiment must use `tui` for both env and `session.create`; keep experiment labels in titles/evidence, not as a fake source string.

If the model-facing `background` argument is deprecated/ignored and top-level delegation is forced asynchronous by the runtime, do not require the model to emit `background=true`. Require the no-extra-field parent call, then prove the effective path with stored dispatch results (`status=dispatched`, `mode=background`) plus the process-event/notification turn.

Use direct asynchronous-completion events before the parent model responds. Filter the exact event contract—for example, `status.update` with `kind=process`—so tool-progress or unrelated status text containing a marker cannot create a false hit. Count exact marker occurrences, not mere substring presence.

Require every frozen observation as an explicit PASS conjunct:

- two nonempty distinct live UI/session transport IDs;
- two nonempty distinct durable session keys, and DB `sessions.source` for those keys equals the frozen source;
- exactly one expected parent tool start/complete with exact args per parent;
- exactly one child identity/tool inventory/terminal invocation per parent when those events or durable tool_calls exist;
- exactly one completion marker per child, owner-only, zero on other/unowned sessions;
- reversed completion order actually observed;
- per-parent turn order `initial message.complete < own process marker < notification message.complete` when two-turn completion is part of the topology;
- zero foreign markers in each parent’s durable transcript, with truthful expected counts that account for markers already present in original prompts (fragment child markers in goals if process-status echoes goals);
- authoritative total provider-call measurement from the disposable DB when available; missing/unverifiable/>ceiling cannot PASS;
- request/tool ceilings and unauthorized-tool scope-stop rules respected;
- complete cleanup and post-cleanup classification only.

Gate `FAILS_CROSS_SESSION_DELIVERY` on verified provenance (distinct IDs, exact DB identity/links, frozen source rows). Cross markers without provenance are `INCONCLUSIVE`.

A pass is negative evidence for one frozen vector only. A cross-session marker is a routing-lineage symptom, not proof of its root cause or authorization for durable infrastructure.

## 5. Prevent the evidence driver from hanging or self-invalidating

Do not enforce startup timeout around a blocking `stdout.readline()`. Drain server stdout continuously in a background thread or asynchronous reader, extract only the readiness port/sentinel, discard raw output, and poll a queue plus process liveness against a deadline.

Cap parent and child model iterations independently. A parent cap does not automatically constrain delegated children. Derive the total request ceiling from all expected parent dispatch turns, child turns, and completion-injection turns.

If the authority freezes an immutable wall-clock, require live CLI start/deadline arguments, recheck the window before auth and each live transition, and also impose one monotonic bound over the whole attempt. Derive `within_clock` / `within_timeout` after cleanup; never hardcode them true after a single early check.

When freezing “exact PATH/env inheritance,” validate the constructed child env against an allowlist by equality. If OS-level child argv/env cannot be observed, add an AST/function-bounded installed-source semantic that the terminal path inherits backend env/PATH without replacement, and document that as the mechanical equivalent.

If source-semantic checks extract indented methods/functions, `textwrap.dedent` before `ast.parse`. Un-dedented method bodies silently fail AST parse and produce false `SOURCE_MISMATCH` / failed validation.

Write sanitized evidence only after stopping the backend and attempting deletion of the disposable root. Persist fixed phase/error categories only—never raw exception, RPC, or provider text. If cleanup fails, classify under the frozen privacy/scope outcome and permit cleanup-only recovery—never a second live attempt.

Sequence commits as two reviewed units, not one mixed commit:

1. authority commit = exact preflight/plan/driver allowlist only, after `APPROVE`;
2. start commit = dated start artifact + Mission Control routing (`.active/*`, mission TASKS/MISSION) with fixed UTC start and `start+30m` deadline;
3. only then run the frozen live command once with those exact `--start-utc` / `--deadline-utc` values;
4. seal evidence + final decision + hold routing after classification, then independent evidence review before/at final commit.

If the live attempt times out (`EVENT_WAIT` / mono bound exceeded) without provenance-gated cross delivery or unauthorized-action proof, classify `INCONCLUSIVE`, not FAIL. Null topology observations after a mid-run timeout are expected when `live_run` raises before returning session/event summaries—do not invent session IDs or upgrade the outcome. No automatic second attempt.

Post-stop auth-schema checks must tolerate cleanup that already deleted the temporary auth file: derive production-auth/profile safety from the source-profile before/after comparison; if the disposable auth path is gone because cleanup succeeded, do not require a successful temp-auth re-read for PASS/INCONCLUSIVE. Only a remaining/unreadable temp auth that should still exist is a cleanup/scope problem.

## 6. Control concurrent reviewers and orphan processes

A prompt saying “read-only” is not a mechanical sandbox. Launch reviewers with an actual read-only sandbox when available. Record their PID/process handle, and verify no stale reviewer or builder from a prior session remains before editing or committing.

For independent authority review of a small frozen file set, prefer embedding the full authority files (and minimal frozen-source excerpts) into a tool-free prompt rather than letting the reviewer explore the whole worktree with shell tools. On Windows, tool-using reviewers often stall on metadata probes; a content-embedded `codex exec --sandbox read-only -` review, or a Hermes leaf with explicit read-only paths, is more reliable.

If the standalone Codex CLI rejects every model with ChatGPT-account “model not supported,” treat that as a launch failure, stop model-name thrashing, and fall back to a Hermes leaf independent review. Do not invent APPROVE.

Any REJECT requires repair of only the listed blockers, offline revalidation, and a fresh independent review of the final tree. Never commit authority after REJECT.

If files change between read and patch:

1. stop editing;
2. identify active writers by command line;
3. terminate only clearly orphaned, task-scoped processes;
4. reread the final tree;
5. invalidate any review performed against the superseded tree;
6. rerun offline checks and request a fresh read-only review.

Never treat concurrent uncommitted changes as reviewed authority. Stage an exact path allowlist and compare it mechanically before commit.

## 7. Evidence hierarchy

1. Direct event/session metadata and durable cross-marker queries.
2. Driver-generated sanitized counts and booleans.
3. Independently rerun offline checks and final-tree review.
4. Model/reviewer narrative only as advisory interpretation.

Do not start implementation, persistence, or the next phase automatically from any routing outcome.