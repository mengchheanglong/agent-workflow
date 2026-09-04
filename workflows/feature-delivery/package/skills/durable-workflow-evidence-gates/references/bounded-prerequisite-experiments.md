# Bounded Prerequisite Experiments

Use this pattern when a behavioral gate depends on proving that an existing regression, fixture, or toolchain can execute first. The prerequisite is evidence about testability, not evidence about the product behavior itself.

## 1. Separate prerequisite from behavior

Name and freeze a prerequisite slice independently from the behavioral experiment. Its pass means only that the named check executed under the frozen environment. Its failure or inconclusive result must not be reported as a product safeguard failure, behavioral reproduction, or authorization for implementation.

Freeze:

- exact source commit and target paths;
- tracked-clean checks plus Git blob IDs for source attribution;
- dependency lock and package-manager command;
- interpreter discovery policy;
- network/download policy;
- environment-variable allowlist;
- one-attempt rule;
- timeout/deadline and no-reset rule;
- cleanup oracle;
- fixed failure categories and total outcome precedence;
- downstream locks.

## 2. Validate the command before the clock

Planning-time probes may validate command shape without collecting authoritative experiment evidence. On Windows/MSYS, distinguish shell paths from native paths before freezing environment variables or `git -C` arguments. If using `env -i`, explicitly decide how the package manager discovers the interpreter; credential scrubbing can also remove ordinary toolchain discovery.

Keep caches, package-manager state, temporary homes, application-data directories, and optional managed runtimes beneath one disposable root. Explicitly choose whether runtime downloads are forbidden or redirected there. Never allow an implicit user/global install.

Request independent review of the actual frozen command, not only the prose. Reviewer checks should include working directory, path format, interpreter selection, download behavior, relative test paths, cleanup, and outcome mapping.

## 3. Make the decision vocabulary total

Every fixed failure category must map to exactly one outcome. Include precedence for:

1. immutable deadline reached with evidence/review unfinished;
2. privacy, scope, attribution, cleanup, pre-deadline timeout, dependency, network, or toolchain noise;
3. behavioral assertion failure after successful setup;
4. full pass plus cleanup and review.

Use category names exactly as frozen. A semantically similar new label is still evidence drift.

## 4. One attempt means one setup/test attempt

After the authorized setup or test command runs, do not repair and rerun it inside the same slice. A parser, sanitizer, or cleanup helper may be corrected only to process the already-existing output and remove already-created temporary state. Record that recovery explicitly and prove it did not rerun archive, dependency sync, or tests.

If automatic cleanup fails:

- locate only the experiment's uniquely named root;
- sanitize existing output before persistence;
- confirm whether test output exists;
- remove the root;
- verify root absence and source/repository integrity;
- classify the experiment under the frozen vocabulary.

## 5. Protect commits during concurrent repository activity

Repository-wide cleanliness can change while an independent reviewer or another session works. Before commit:

- stage an exact allowlist, never `git add .`;
- compare the staged path set mechanically with the frozen set;
- run checks scoped to those paths;
- leave unrelated modified/untracked files untouched;
- report out-of-scope paths without attributing ownership;
- verify the experiment paths are clean after commit.

Concurrent unrelated changes are a provenance caveat, not proof of task contamination by themselves.

## 6. Reconcile every truth surface

Before sealing, search for stale active language across machine state, current/next views, mission/task summaries, and workspace routers. A closed status in JSON is insufficient if a human-readable file still says the experiment may execute.

Require a final contradiction sweep and independent approval after the last vocabulary or routing repair. Then record the approval and commit only the reviewed decision paths.

## Minimal supported claims

A prerequisite pass supports: the named regression executed under the frozen source/toolchain contract.

A prerequisite inconclusive result supports: the check could not produce behavioral evidence for the recorded setup/toolchain reason.

Neither result alone reproduces a user incident, validates an architecture, establishes demand, or opens the next gate.
