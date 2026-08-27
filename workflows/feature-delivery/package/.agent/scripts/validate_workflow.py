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

    if state.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")

    status = state.get("status")
    risk = state.get("risk")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")
    if risk not in VALID_RISKS:
        errors.append(f"risk must be one of {sorted(VALID_RISKS)}")

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

    fix_cycles = state.get("fixCycles")
    max_fix_cycles = state.get("maxFixCycles")
    override_evidence = state.get("fixCycleOverrideEvidence")
    if not isinstance(fix_cycles, int) or fix_cycles < 0:
        errors.append("fixCycles must be a non-negative integer")
    if not isinstance(max_fix_cycles, int) or max_fix_cycles < 1:
        errors.append("maxFixCycles must be a positive integer")
    else:
        if max_fix_cycles > 2 and not _is_nonempty_string(override_evidence):
            errors.append("maxFixCycles above 2 requires fix-cycle override evidence")
        if (
            isinstance(fix_cycles, int)
            and fix_cycles > max_fix_cycles
            and status not in {"BLOCKED", "PAUSED", "CANCELLED"}
        ):
            errors.append(
                f"fix cycles exceeded authorized maximum of {max_fix_cycles}; "
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

    if gates.get("G5_VALIDATION") == "PASS":
        if not isinstance(change, dict) or not _is_nonempty_string(change.get("currentSnapshot")):
            errors.append("G5_VALIDATION PASS requires change.currentSnapshot")
        if not isinstance(validation, list) or not validation:
            errors.append("G5_VALIDATION PASS requires fresh validation evidence")
        else:
            for index, item in enumerate(validation, start=1):
                if not isinstance(item, dict):
                    errors.append(f"G5_VALIDATION evidence[{index}] must be an object")
                    continue
                if item.get("result") != "PASS" or item.get("exitCode") != 0:
                    errors.append(f"G5_VALIDATION evidence[{index}] must record PASS with exitCode 0")
                if item.get("afterLastEdit") is not True:
                    errors.append(f"G5_VALIDATION evidence[{index}] must be after the last edit")
                if not _is_nonempty_string(item.get("command")):
                    errors.append(f"G5_VALIDATION evidence[{index}] requires the exact command")

    if gates.get("G6_REVIEW") == "PASS":
        current_snapshot = _get(change, "currentSnapshot")
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
            for index, item in enumerate(validation, start=1):
                if not isinstance(item, dict):
                    errors.append(f"validation[{index}] must be an object")
                    continue
                if item.get("result") != "PASS" or item.get("exitCode") != 0:
                    errors.append(f"validation[{index}] must record PASS with exitCode 0")
                if item.get("afterLastEdit") is not True:
                    errors.append(f"validation[{index}] must be run after the last edit")
                if not _is_nonempty_string(item.get("command")):
                    errors.append(f"validation[{index}] requires the exact command")

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


def validate_live_snapshot(root: Path, state: dict[str, Any]) -> list[str]:
    """Fail closed when recorded post-validation evidence does not match the live Git tree."""
    gates = state.get("gates") if isinstance(state.get("gates"), dict) else {}
    if state.get("status") not in SHIP_STATUSES and gates.get("G5_VALIDATION") != "PASS":
        return []

    recorded = _get(state.get("change"), "currentSnapshot")
    base_commit = _get(state.get("baseline"), "baseCommit")
    if not _is_nonempty_string(recorded) or not _is_nonempty_string(base_commit):
        return ["live delivery snapshot cannot be verified without recorded snapshot and base commit"]
    try:
        live = compute_snapshot(root, base_commit)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        return [f"live delivery snapshot verification failed: {exc}"]
    if live != recorded:
        return [f"live delivery snapshot {live} does not match recorded {recorded}; validation/review is stale"]
    return []


def default_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root(), help="installed repository root")
    parser.add_argument("--snapshot", action="store_true", help="print current delivery snapshot")
    parser.add_argument("--base-commit", help="override baseline.baseCommit for --snapshot")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.snapshot:
        try:
            print(compute_snapshot(root, args.base_commit))
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
