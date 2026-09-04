#!/usr/bin/env python
"""Validate the repository-local feature-delivery workflow.

Usage:
    python .agent/scripts/validate_workflow.py
    python .agent/scripts/validate_workflow.py --root <repo-root>
    python .agent/scripts/validate_workflow.py --snapshot

The validator is intentionally standard-library only. It validates package structure,
.active/STATE.json, and ship-readiness invariants. The snapshot command computes a
stable SHA-256 over tracked changes relative to the recorded base commit plus untracked
files, excluding .active/ so recording evidence does not invalidate itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


VALID_STATUSES = {
    "IDLE",
    "SCOPING",
    "RESEARCH",
    "DESIGN",
    "BUILD",
    "INTEGRATE",
    "VALIDATE",
    "REVIEW",
    "FIX",
    "HUMAN_CHECKPOINT",
    "BLOCKED",
    "PAUSED",
    "READY_TO_SHIP",
    "SHIPPED",
    "CANCELLED",
}
VALID_RISKS = {"UNASSESSED", "LOW", "MEDIUM", "HIGH"}
VALID_GATE_STATES = {"NOT_RUN", "PASS", "FAIL", "NOT_REQUIRED"}
VALID_SPEC_VERDICTS = {"NOT_REVIEWED", "PASS", "FAIL", "UNVERIFIABLE"}
VALID_QUALITY_VERDICTS = {"NOT_REVIEWED", "CHANGES_REQUESTED", "DO_NOT_MERGE", "APPROVE"}
VALID_VERDICTS = {"NOT_REVIEWED", "CHANGES_REQUESTED", "DO_NOT_MERGE", "APPROVE"}
VALID_REVIEW_TIERS = {"UNSET", "MECHANICAL", "TARGETED", "DEEP"}
VALID_SPECIALIST_MODES = {"UNSET", "INLINE", "SEPARATE", "NOT_REQUIRED"}
VALID_REVIEW_TYPES = {"NOT_REVIEWED", "FULL", "DELTA"}
GATES = (
    "G0_SCOPE",
    "G1_RESEARCH",
    "G2_DESIGN",
    "G3_BUILD",
    "G4_INTEGRATION",
    "G5_VALIDATION",
    "G6_REVIEW",
    "G7_HUMAN",
    "G8_SHIP_READY",
)
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "REVIEW.md",
    "START_FEATURE_PROMPT.md",
    "REVIEW_FIX_PROMPT.md",
    ".agent/WORKFLOW.md",
    ".agent/QUALITY_GATES.md",
    ".agent/REFERENCES.md",
    ".agent/adapters/claude-code.md",
    ".agent/adapters/codex.md",
    ".agent/adapters/generic-reviewer-prompt.md",
    ".agent/roles/router.md",
    ".agent/roles/researcher.md",
    ".agent/roles/architect.md",
    ".agent/roles/builder.md",
    ".agent/roles/integrator.md",
    ".agent/roles/reviewer.md",
    ".agent/templates/FEATURE_TEMPLATE.md",
    ".agent/templates/DECISION_TEMPLATE.md",
    ".agent/templates/REVIEW_TEMPLATE.md",
    ".agent/scripts/validate_workflow.py",
    ".agent/tests/test_validate_workflow.py",
    ".active/FEATURE.md",
    ".active/STATE.md",
    ".active/STATE.json",
    ".active/DECISIONS.md",
    ".active/REVIEW.md",
)
SHIP_STATUSES = {"READY_TO_SHIP", "SHIPPED"}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _get(mapping: Any, key: str, default: Any = None) -> Any:
    return mapping.get(key, default) if isinstance(mapping, dict) else default


def validate_state(state: dict[str, Any]) -> list[str]:
    """Return validation errors for a parsed STATE.json object."""
    errors: list[str] = []

    if state.get("schemaVersion") != 2:
        errors.append("schemaVersion must be 2")

    status = state.get("status")
    risk = state.get("risk")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")
    if risk not in VALID_RISKS:
        errors.append(f"risk must be one of {sorted(VALID_RISKS)}")

    review_policy = state.get("reviewPolicy")
    if not isinstance(review_policy, dict):
        errors.append("reviewPolicy must be an object")
        review_policy = {}
    tier = review_policy.get("tier")
    specialist_mode = review_policy.get("specialistMode")
    budget_minutes = review_policy.get("budgetMinutes")
    max_broad_cycles = review_policy.get("maxBroadReviewCycles")
    escalation_reason = review_policy.get("escalationReason")
    specialist_rationale = review_policy.get("specialistRationale")
    if tier not in VALID_REVIEW_TIERS:
        errors.append(f"reviewPolicy.tier must be one of {sorted(VALID_REVIEW_TIERS)}")
    if specialist_mode not in VALID_SPECIALIST_MODES:
        errors.append(
            f"reviewPolicy.specialistMode must be one of {sorted(VALID_SPECIALIST_MODES)}"
        )
    if budget_minutes is not None and (
        not isinstance(budget_minutes, int) or isinstance(budget_minutes, bool) or budget_minutes < 1
    ):
        errors.append("reviewPolicy.budgetMinutes must be null or a positive integer")
    if not isinstance(max_broad_cycles, int) or isinstance(max_broad_cycles, bool) or max_broad_cycles < 1:
        errors.append("reviewPolicy.maxBroadReviewCycles must be a positive integer")
    elif max_broad_cycles > 1 and not _is_nonempty_string(state.get("fixCycleOverrideEvidence")):
        errors.append(
            "reviewPolicy.maxBroadReviewCycles above 1 requires fixCycleOverrideEvidence"
        )
    if escalation_reason is not None and not _is_nonempty_string(escalation_reason):
        errors.append("reviewPolicy.escalationReason must be null or a non-empty string")
    if specialist_rationale is not None and not _is_nonempty_string(specialist_rationale):
        errors.append("reviewPolicy.specialistRationale must be null or a non-empty string")

    if tier == "MECHANICAL" and risk != "LOW":
        errors.append("reviewPolicy.tier MECHANICAL is allowed only for LOW risk")
    if risk == "HIGH" and tier != "DEEP":
        errors.append("HIGH risk requires reviewPolicy.tier DEEP")
    if tier == "DEEP" and risk in {"LOW", "MEDIUM"} and not _is_nonempty_string(escalation_reason):
        errors.append("DEEP review for LOW or MEDIUM risk requires reviewPolicy.escalationReason")
    if specialist_mode == "NOT_REQUIRED" and not _is_nonempty_string(specialist_rationale):
        errors.append("specialistMode NOT_REQUIRED requires reviewPolicy.specialistRationale")
    if specialist_mode == "SEPARATE" and not _is_nonempty_string(specialist_rationale):
        errors.append("specialistMode SEPARATE requires reviewPolicy.specialistRationale")
    if risk == "HIGH" and specialist_mode == "NOT_REQUIRED":
        errors.append("HIGH risk may not use specialistMode NOT_REQUIRED")

    gates = state.get("gates")
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
        gates = {}
    for gate in GATES:
        gate_state = gates.get(gate)
        if gate_state not in VALID_GATE_STATES:
            errors.append(f"{gate} must be one of {sorted(VALID_GATE_STATES)}")

    gate_evidence = state.get("gateEvidence")
    if not isinstance(gate_evidence, dict):
        errors.append("gateEvidence must be an object")
        gate_evidence = {}
    for gate in GATES:
        if gates.get(gate) in {"PASS", "FAIL", "NOT_REQUIRED"}:
            evidence = gate_evidence.get(gate)
            if not isinstance(evidence, list) or not any(_is_nonempty_string(item) for item in evidence):
                errors.append(f"{gate} {gates.get(gate)} requires gateEvidence")

    review = state.get("review")
    if not isinstance(review, dict):
        errors.append("review must be an object")
        review = {}
    verdict = review.get("verdict")
    if verdict not in VALID_VERDICTS:
        errors.append(f"review.verdict must be one of {sorted(VALID_VERDICTS)}")
    spec_verdict = review.get("specVerdict")
    if spec_verdict not in VALID_SPEC_VERDICTS:
        errors.append(f"review.specVerdict must be one of {sorted(VALID_SPEC_VERDICTS)}")
    quality_verdict = review.get("qualityVerdict")
    if quality_verdict not in VALID_QUALITY_VERDICTS:
        errors.append(f"review.qualityVerdict must be one of {sorted(VALID_QUALITY_VERDICTS)}")
    review_type = review.get("type")
    if review_type not in VALID_REVIEW_TYPES:
        errors.append(f"review.type must be one of {sorted(VALID_REVIEW_TYPES)}")
    base_approved_snapshot = review.get("baseApprovedSnapshot")
    if base_approved_snapshot is not None and not _is_nonempty_string(base_approved_snapshot):
        errors.append("review.baseApprovedSnapshot must be null or a non-empty string")
    changed_criteria = review.get("changedCriteria")
    if not isinstance(changed_criteria, list) or not all(
        _is_nonempty_string(item) for item in changed_criteria
    ):
        errors.append("review.changedCriteria must be an array of non-empty strings")

    fix_cycles = state.get("fixCycles")
    if not isinstance(fix_cycles, int) or fix_cycles < 0:
        errors.append("fixCycles must be a non-negative integer")
    if (
        isinstance(fix_cycles, int)
        and isinstance(max_broad_cycles, int)
        and fix_cycles + 1 > max_broad_cycles
        and status not in {"BLOCKED", "PAUSED", "CANCELLED"}
    ):
        errors.append(
            f"broad review cycles exceeded authorized maximum of {max_broad_cycles}; "
            "set BLOCKED or record a human-approved override"
        )

    feature = state.get("feature")
    if not isinstance(feature, dict):
        errors.append("feature must be an object")
        feature = {}

    if status == "IDLE":
        if feature.get("name") or feature.get("slug"):
            errors.append("IDLE state must not identify an active feature")
        return errors

    if not _is_nonempty_string(feature.get("name")):
        errors.append("active state requires feature.name")
    if not _is_nonempty_string(feature.get("slug")):
        errors.append("active state requires feature.slug")
    if risk == "UNASSESSED" and status not in {"SCOPING", "BLOCKED", "PAUSED", "CANCELLED"}:
        errors.append(f"risk must be assessed before status {status}")

    # Collaboration is optional; absent (or SOLO) means a single-contributor feature. GROUP mode
    # adds team-ownership evidence without hardcoding any repository's branch names.
    collaboration = state.get("collaboration")
    if collaboration is not None:
        if not isinstance(collaboration, dict):
            errors.append("collaboration must be an object when present")
            collaboration = {}
        mode = collaboration.get("mode")
        if mode is not None and mode not in {"SOLO", "GROUP"}:
            errors.append("collaboration.mode must be SOLO or GROUP")
        if mode == "GROUP" and gates.get("G0_SCOPE") == "PASS":
            for field in ("owner", "taskRef", "featureBranch"):
                if not _is_nonempty_string(collaboration.get(field)):
                    errors.append(f"GROUP G0_SCOPE PASS requires collaboration.{field}")

    human = state.get("humanApproval")
    if not isinstance(human, dict):
        errors.append("humanApproval must be an object")
        human = {}
    if risk == "HIGH" and human.get("required") != "YES":
        errors.append("HIGH risk requires human approval")

    actors = state.get("actors")
    if not isinstance(actors, dict):
        errors.append("actors must be an object")
        actors = {}
    builder = actors.get("builder")
    reviewer = actors.get("reviewer")
    if builder and reviewer and builder == reviewer:
        errors.append("Reviewer must be independent from Builder")

    baseline = state.get("baseline")
    change = state.get("change")
    validation = state.get("validation")
    findings = review.get("openFindings")

    if gates.get("G0_SCOPE") == "PASS":
        if not isinstance(baseline, dict):
            errors.append("G0_SCOPE PASS requires baseline object")
            baseline = {}
        for field in ("repositoryRoot", "baseBranch", "baseCommit"):
            if not _is_nonempty_string(baseline.get(field)):
                errors.append(f"G0_SCOPE PASS requires baseline.{field}")
        if not isinstance(baseline.get("allowedPaths"), list) or not baseline.get("allowedPaths"):
            errors.append("G0_SCOPE PASS requires at least one baseline.allowedPaths entry")
        if tier == "UNSET":
            errors.append("G0_SCOPE PASS requires a selected reviewPolicy.tier")
        if specialist_mode == "UNSET":
            errors.append("G0_SCOPE PASS requires a selected reviewPolicy.specialistMode")
        if not isinstance(budget_minutes, int) or isinstance(budget_minutes, bool) or budget_minutes < 1:
            errors.append("G0_SCOPE PASS requires a positive reviewPolicy.budgetMinutes")
        if not isinstance(max_broad_cycles, int) or isinstance(max_broad_cycles, bool) or max_broad_cycles < 1:
            errors.append("G0_SCOPE PASS requires reviewPolicy.maxBroadReviewCycles")

    if gates.get("G5_VALIDATION") == "PASS":
        if not isinstance(change, dict) or not _is_nonempty_string(change.get("currentSnapshot")):
            errors.append("G5_VALIDATION PASS requires change.currentSnapshot")
        if not isinstance(validation, list) or not validation:
            errors.append("G5_VALIDATION PASS requires fresh validation evidence")
        else:
            has_fresh_evidence = False
            for index, item in enumerate(validation, start=1):
                if not isinstance(item, dict):
                    errors.append(f"G5_VALIDATION evidence[{index}] must be an object")
                    continue
                if item.get("result") != "PASS" or item.get("exitCode") != 0:
                    errors.append(f"G5_VALIDATION evidence[{index}] must record PASS with exitCode 0")
                if item.get("afterLastEdit") is True:
                    has_fresh_evidence = True
                elif item.get("unaffectedByLaterEdit") is not True or not _is_nonempty_string(
                    item.get("unaffectedRationale")
                ):
                    errors.append(
                        f"G5_VALIDATION evidence[{index}] must be after the last edit or record "
                        "why a later edit cannot affect it"
                    )
                if not _is_nonempty_string(item.get("command")):
                    errors.append(f"G5_VALIDATION evidence[{index}] requires the exact command")
            if not has_fresh_evidence:
                errors.append("G5_VALIDATION PASS requires at least one check after the last edit")

    if gates.get("G6_REVIEW") == "PASS":
        current_snapshot = _get(change, "currentSnapshot")
        if review_type not in {"FULL", "DELTA"}:
            errors.append("G6_REVIEW PASS requires review.type FULL or DELTA")
        if review_type == "DELTA":
            if not _is_nonempty_string(base_approved_snapshot):
                errors.append("DELTA approval requires review.baseApprovedSnapshot")
            if not changed_criteria:
                errors.append("DELTA approval requires non-empty review.changedCriteria")
        if review.get("specVerdict") != "PASS":
            errors.append("G6_REVIEW PASS requires review.specVerdict PASS")
        if review.get("qualityVerdict") != "APPROVE":
            errors.append("G6_REVIEW PASS requires review.qualityVerdict APPROVE")
        if review.get("verdict") != "APPROVE":
            errors.append("G6_REVIEW PASS requires verdict APPROVE")
        if review.get("independent") is not True:
            errors.append("G6_REVIEW PASS requires an independent reviewer")
        if not reviewer or review.get("reviewer") != reviewer:
            errors.append("G6_REVIEW PASS requires review.reviewer to match actors.reviewer")
        if not _is_nonempty_string(current_snapshot) or review.get("reviewedSnapshot") != current_snapshot:
            errors.append("G6_REVIEW PASS requires review of the current snapshot")
        if not isinstance(findings, dict):
            errors.append("G6_REVIEW PASS requires review.openFindings")
        else:
            for severity in ("blocker", "major"):
                if findings.get(severity) != 0:
                    errors.append(f"G6_REVIEW PASS cannot have open {severity.upper()} findings")

    if gates.get("G7_HUMAN") == "PASS":
        if human.get("required") != "YES":
            errors.append("G7_HUMAN PASS requires humanApproval.required YES")
        if human.get("status") != "APPROVED" or not _is_nonempty_string(human.get("evidence")):
            errors.append("G7_HUMAN PASS requires APPROVED human approval with evidence")

    if status in SHIP_STATUSES:
        baseline = state.get("baseline")
        change = state.get("change")
        validation = state.get("validation")
        findings = review.get("openFindings")

        if not isinstance(baseline, dict):
            errors.append("ship-ready state requires baseline object")
            baseline = {}
        for field in ("repositoryRoot", "baseBranch", "baseCommit"):
            if not _is_nonempty_string(baseline.get(field)):
                errors.append(f"ship-ready state requires baseline.{field}")
        if not isinstance(baseline.get("allowedPaths"), list) or not baseline.get("allowedPaths"):
            errors.append("ship-ready state requires at least one baseline.allowedPaths entry")

        if not isinstance(change, dict):
            errors.append("ship-ready state requires change object")
            change = {}
        current_snapshot = change.get("currentSnapshot")
        reviewed_snapshot = review.get("reviewedSnapshot")
        if not _is_nonempty_string(current_snapshot):
            errors.append("ship-ready state requires change.currentSnapshot")
        if not _is_nonempty_string(reviewed_snapshot):
            errors.append("ship-ready state requires review.reviewedSnapshot")
        if current_snapshot != reviewed_snapshot:
            errors.append("review snapshot is stale: review.reviewedSnapshot must match change.currentSnapshot")

        if review.get("verdict") != "APPROVE":
            errors.append("only review verdict APPROVE permits READY_TO_SHIP or SHIPPED")
        if review.get("independent") is not True:
            errors.append("ship-ready state requires an independent review")
        if not reviewer or review.get("reviewer") != reviewer:
            errors.append("review.reviewer must match actors.reviewer")
        if not _is_nonempty_string(review.get("artifact")):
            errors.append("ship-ready state requires review.artifact")

        if not isinstance(findings, dict):
            errors.append("review.openFindings must be an object")
            findings = {}
        for severity in ("blocker", "major"):
            count = findings.get(severity)
            if count != 0:
                errors.append(f"open {severity.upper()} findings block shipping")

        if not isinstance(validation, list) or not validation:
            errors.append("ship-ready state requires fresh validation evidence")
        else:
            has_fresh_evidence = False
            for index, item in enumerate(validation, start=1):
                if not isinstance(item, dict):
                    errors.append(f"validation[{index}] must be an object")
                    continue
                if item.get("result") != "PASS" or item.get("exitCode") != 0:
                    errors.append(f"validation[{index}] must record PASS with exitCode 0")
                if item.get("afterLastEdit") is True:
                    has_fresh_evidence = True
                elif item.get("unaffectedByLaterEdit") is not True or not _is_nonempty_string(
                    item.get("unaffectedRationale")
                ):
                    errors.append(
                        f"validation[{index}] must be after the last edit or record why a later "
                        "edit cannot affect it"
                    )
                if not _is_nonempty_string(item.get("command")):
                    errors.append(f"validation[{index}] requires the exact command")
            if not has_fresh_evidence:
                errors.append("ship-ready state requires at least one check after the last edit")

        required_gate_states = {
            "G0_SCOPE": "PASS",
            "G1_RESEARCH": "PASS",
            "G2_DESIGN": {"PASS", "NOT_REQUIRED"},
            "G3_BUILD": "PASS",
            "G4_INTEGRATION": {"PASS", "NOT_REQUIRED"},
            "G5_VALIDATION": "PASS",
            "G6_REVIEW": "PASS",
            "G7_HUMAN": {"PASS", "NOT_REQUIRED"},
            "G8_SHIP_READY": "PASS",
        }
        for gate, expected in required_gate_states.items():
            actual = gates.get(gate)
            allowed = expected if isinstance(expected, set) else {expected}
            if actual not in allowed:
                errors.append(f"{gate} must be one of {sorted(allowed)} before shipping")

        if human.get("required") == "YES":
            if human.get("status") != "APPROVED" or not _is_nonempty_string(human.get("evidence")):
                errors.append("required human approval must be APPROVED with evidence")
        elif human.get("required") == "NO":
            if human.get("status") != "NOT_REQUIRED":
                errors.append("humanApproval.status must be NOT_REQUIRED when approval is not required")
        else:
            errors.append("ship-ready state requires humanApproval.required YES or NO")

        if status == "SHIPPED" and not _is_nonempty_string(state.get("shipEvidence")):
            errors.append("SHIPPED state requires shipEvidence")

    return errors


def validate_structure(root: Path) -> list[str]:
    """Validate the installed workflow file structure and canonical vocabulary."""
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    state_path = root / ".active" / "STATE.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot parse .active/STATE.json: {exc}")
        else:
            errors.extend(validate_state(state))
            errors.extend(validate_live_snapshot(root, state))

    retired_verdict = "APPROVE_WITH_FIXES"
    for path in root.rglob("*.md"):
        if any(part in {"archive", ".git"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read {path.relative_to(root)}: {exc}")
            continue
        if retired_verdict in text:
            errors.append(f"retired verdict {retired_verdict} remains in {path.relative_to(root)}")

    return errors


def _run_git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def compute_snapshot(root: Path, base_commit: str | None = None) -> str:
    """Compute a stable digest of delivery changes, excluding local .active evidence."""
    state_path = root / ".active" / "STATE.json"
    if base_commit is None:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        base_commit = _get(state.get("baseline"), "baseCommit")
    if not _is_nonempty_string(base_commit):
        raise RuntimeError("baseline.baseCommit is required before computing a snapshot")

    _run_git(root, "rev-parse", "--show-toplevel")
    diff = _run_git(
        root,
        "diff",
        "--binary",
        str(base_commit),
        "--",
        ".",
        ":(exclude).active/**",
    )
    untracked_raw = _run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    untracked = sorted(
        p.decode("utf-8", errors="surrogateescape")
        for p in untracked_raw.split(b"\0")
        if p and not p.replace(b"\\", b"/").startswith(b".active/")
    )

    digest = hashlib.sha256()
    digest.update(b"tracked-diff\0")
    digest.update(diff)
    for relative in untracked:
        path = root / relative
        digest.update(b"\0untracked\0")
        digest.update(relative.replace("\\", "/").encode("utf-8", errors="surrogateescape"))
        digest.update(b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
        else:
            digest.update(b"<non-file>")
    return f"sha256:{digest.hexdigest()}"


def resolve_repository_root(workflow_root: Path, state: dict[str, Any]) -> Path:
    """Resolve the delivery repository independently from the workflow home.

    Defaults to the workflow home (root install). When ``baseline.repositoryRoot`` is set,
    the workflow may live in a subdirectory of the delivery repository; a relative value is
    resolved against the workflow home.
    """
    configured = _get(state.get("baseline"), "repositoryRoot")
    if not _is_nonempty_string(configured):
        return workflow_root.resolve()
    candidate = Path(configured)
    if not candidate.is_absolute():
        candidate = workflow_root / candidate
    return candidate.resolve()


def validate_live_snapshot(workflow_root: Path, state: dict[str, Any]) -> list[str]:
    """Fail closed when recorded post-validation evidence does not match the live Git tree."""
    gates = state.get("gates") if isinstance(state.get("gates"), dict) else {}
    if state.get("status") not in SHIP_STATUSES and gates.get("G5_VALIDATION") != "PASS":
        return []

    recorded = _get(state.get("change"), "currentSnapshot")
    base_commit = _get(state.get("baseline"), "baseCommit")
    if not _is_nonempty_string(recorded) or not _is_nonempty_string(base_commit):
        return ["live delivery snapshot cannot be verified without recorded snapshot and base commit"]
    try:
        repository_root = resolve_repository_root(workflow_root, state)
        live = compute_snapshot(repository_root, base_commit)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        return [f"live delivery snapshot verification failed: {exc}"]
    if live != recorded:
        return [f"live delivery snapshot {live} does not match recorded {recorded}; validation/review is stale"]
    return []


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root(), help="workflow home containing .active and .agent")
    parser.add_argument("--snapshot", action="store_true", help="print current delivery snapshot")
    parser.add_argument("--base-commit", help="override baseline.baseCommit for --snapshot")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.snapshot:
        try:
            repository_root = root
            base_commit = args.base_commit
            state_path = root / ".active" / "STATE.json"
            if state_path.is_file():
                state = json.loads(state_path.read_text(encoding="utf-8"))
                repository_root = resolve_repository_root(root, state)
                if base_commit is None:
                    base_commit = _get(state.get("baseline"), "baseCommit")
            print(compute_snapshot(repository_root, base_commit))
        except (OSError, RuntimeError, json.JSONDecodeError) as exc:
            print(f"SNAPSHOT ERROR: {exc}", file=sys.stderr)
            return 2
        return 0

    errors = validate_structure(root)
    if errors:
        print(f"WORKFLOW INVALID ({len(errors)} issue{'s' if len(errors) != 1 else ''})")
        for error in errors:
            print(f"- {error}")
        return 1

    print("WORKFLOW VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
