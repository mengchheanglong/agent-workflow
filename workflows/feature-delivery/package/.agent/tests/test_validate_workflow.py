import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_workflow.py"
spec = importlib.util.spec_from_file_location("validate_workflow", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load validator at {SCRIPT}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def idle_state():
    return {
        "schemaVersion": 1,
        "feature": {"name": None, "slug": None},
        "status": "IDLE",
        "risk": "UNASSESSED",
        "workflowPath": [],
        "actors": {
            "router": None,
            "researcher": None,
            "architect": None,
            "builder": None,
            "integrator": None,
            "reviewer": None,
        },
        "baseline": {
            "repositoryRoot": None,
            "baseBranch": None,
            "baseCommit": None,
            "preExistingChanges": [],
            "allowedPaths": [],
        },
        "change": {"currentSnapshot": None, "changedFiles": []},
        "gates": {f"G{i}_{name}": "NOT_RUN" for i, name in enumerate([
            "SCOPE", "RESEARCH", "DESIGN", "BUILD", "INTEGRATION",
            "VALIDATION", "REVIEW", "HUMAN", "SHIP_READY",
        ])},
        "gateEvidence": {f"G{i}_{name}": [] for i, name in enumerate([
            "SCOPE", "RESEARCH", "DESIGN", "BUILD", "INTEGRATION",
            "VALIDATION", "REVIEW", "HUMAN", "SHIP_READY",
        ])},
        "validation": [],
        "review": {
            "artifact": ".active/REVIEW.md",
            "reviewedSnapshot": None,
            "reviewer": None,
            "independent": False,
            "specVerdict": "NOT_REVIEWED",
            "qualityVerdict": "NOT_REVIEWED",
            "verdict": "NOT_REVIEWED",
            "openFindings": {"blocker": 0, "major": 0, "minor": 0, "nit": 0},
        },
        "humanApproval": {"required": "UNKNOWN", "status": "NOT_REQUESTED", "evidence": None},
        "shipEvidence": None,
        "fixCycles": 0,
        "maxFixCycles": 2,
        "fixCycleOverrideEvidence": None,
        "nextAction": "Initialize one feature.",
    }


def ready_state():
    state = idle_state()
    state.update({
        "feature": {"name": "Example", "slug": "example"},
        "status": "READY_TO_SHIP",
        "risk": "LOW",
        "workflowPath": ["SCOPE", "RESEARCH", "BUILD", "VALIDATE", "REVIEW", "READY_TO_SHIP"],
        "actors": {
            "router": "agent-router",
            "researcher": "agent-researcher",
            "architect": None,
            "builder": "agent-builder",
            "integrator": None,
            "reviewer": "agent-reviewer",
        },
        "baseline": {
            "repositoryRoot": ".",
            "baseBranch": "main",
            "baseCommit": "abc123",
            "preExistingChanges": [],
            "allowedPaths": ["src/**", "tests/**"],
        },
        "change": {"currentSnapshot": "sha256:current", "changedFiles": ["src/example.py", "tests/test_example.py"]},
        "validation": [{"command": "pytest", "result": "PASS", "exitCode": 0, "afterLastEdit": True}],
        "review": {
            "artifact": ".active/REVIEW.md",
            "reviewedSnapshot": "sha256:current",
            "reviewer": "agent-reviewer",
            "independent": True,
            "specVerdict": "PASS",
            "qualityVerdict": "APPROVE",
            "verdict": "APPROVE",
            "openFindings": {"blocker": 0, "major": 0, "minor": 0, "nit": 0},
        },
        "humanApproval": {"required": "NO", "status": "NOT_REQUIRED", "evidence": None},
        "nextAction": "Ship or hand back the approved change.",
    })
    state["gates"].update({
        "G0_SCOPE": "PASS",
        "G1_RESEARCH": "PASS",
        "G2_DESIGN": "NOT_REQUIRED",
        "G3_BUILD": "PASS",
        "G4_INTEGRATION": "NOT_REQUIRED",
        "G5_VALIDATION": "PASS",
        "G6_REVIEW": "PASS",
        "G7_HUMAN": "NOT_REQUIRED",
        "G8_SHIP_READY": "PASS",
    })
    state["gateEvidence"] = {gate: [f"evidence for {gate}"] for gate in state["gates"]}
    return state


class StateValidationTests(unittest.TestCase):
    def test_idle_state_is_valid(self):
        self.assertEqual([], validator.validate_state(idle_state()))

    def test_ready_state_is_valid(self):
        self.assertEqual([], validator.validate_state(ready_state()))

    def test_completed_gate_requires_evidence_reference_or_rationale(self):
        state = ready_state()
        state["gateEvidence"]["G1_RESEARCH"] = []
        errors = validator.validate_state(state)
        self.assertTrue(any("G1_RESEARCH" in error and "evidence" in error.lower() for error in errors), errors)

    def test_active_state_requires_gate_evidence_map(self):
        state = ready_state()
        state.pop("gateEvidence")
        errors = validator.validate_state(state)
        self.assertTrue(any("gateEvidence" in error for error in errors), errors)

    def test_only_approve_can_ship(self):
        state = ready_state()
        state["review"]["verdict"] = "CHANGES_REQUESTED"
        errors = validator.validate_state(state)
        self.assertTrue(any("APPROVE" in error for error in errors), errors)

    def test_review_gate_requires_spec_compliance_pass(self):
        state = ready_state()
        state["review"]["specVerdict"] = "FAIL"
        errors = validator.validate_state(state)
        self.assertTrue(any("specVerdict PASS" in error for error in errors), errors)

    def test_review_gate_requires_quality_approve(self):
        state = ready_state()
        state["review"]["qualityVerdict"] = "CHANGES_REQUESTED"
        errors = validator.validate_state(state)
        self.assertTrue(any("qualityVerdict APPROVE" in error for error in errors), errors)

    def test_stale_review_snapshot_blocks_shipping(self):
        state = ready_state()
        state["review"]["reviewedSnapshot"] = "sha256:old"
        errors = validator.validate_state(state)
        self.assertTrue(any("snapshot" in error.lower() for error in errors), errors)

    def test_open_major_blocks_shipping(self):
        state = ready_state()
        state["review"]["openFindings"]["major"] = 1
        errors = validator.validate_state(state)
        self.assertTrue(any("MAJOR" in error for error in errors), errors)

    def test_high_risk_requires_human_approval(self):
        state = ready_state()
        state["risk"] = "HIGH"
        state["humanApproval"] = {"required": "YES", "status": "NOT_REQUESTED", "evidence": None}
        state["gates"]["G7_HUMAN"] = "FAIL"
        errors = validator.validate_state(state)
        self.assertTrue(any("human approval" in error.lower() for error in errors), errors)

    def test_reviewer_must_be_independent(self):
        state = ready_state()
        state["actors"]["reviewer"] = state["actors"]["builder"]
        state["review"]["reviewer"] = state["actors"]["builder"]
        errors = validator.validate_state(state)
        self.assertTrue(any("independent" in error.lower() for error in errors), errors)

    def test_validation_must_be_after_last_edit(self):
        state = ready_state()
        state["validation"][0]["afterLastEdit"] = False
        errors = validator.validate_state(state)
        self.assertTrue(any("last edit" in error.lower() for error in errors), errors)

    def test_fix_loop_is_bounded(self):
        state = ready_state()
        state["status"] = "FIX"
        state["fixCycles"] = 3
        state["review"]["verdict"] = "CHANGES_REQUESTED"
        state["gates"]["G6_REVIEW"] = "FAIL"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        errors = validator.validate_state(state)
        self.assertTrue(any("fix cycles" in error.lower() for error in errors), errors)

    def test_human_evidence_can_authorize_additional_fix_cycle(self):
        state = ready_state()
        state["status"] = "FIX"
        state["fixCycles"] = 3
        state["maxFixCycles"] = 3
        state["fixCycleOverrideEvidence"] = "DEC-003 approved by product owner"
        state["review"]["verdict"] = "CHANGES_REQUESTED"
        state["gates"]["G6_REVIEW"] = "FAIL"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        errors = validator.validate_state(state)
        self.assertFalse(any("fix cycles" in error.lower() for error in errors), errors)

    def test_fix_loop_cannot_be_bypassed_by_advancing_status(self):
        state = ready_state()
        state["status"] = "VALIDATE"
        state["fixCycles"] = 3
        state["gates"]["G6_REVIEW"] = "FAIL"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        errors = validator.validate_state(state)
        self.assertTrue(any("fix cycles" in error.lower() for error in errors), errors)

    def test_scope_pass_requires_baseline_and_allowed_paths(self):
        state = idle_state()
        state["feature"] = {"name": "Example", "slug": "example"}
        state["status"] = "RESEARCH"
        state["risk"] = "LOW"
        state["gates"]["G0_SCOPE"] = "PASS"
        errors = validator.validate_state(state)
        self.assertTrue(any("baseline.baseCommit" in error for error in errors), errors)
        self.assertTrue(any("allowedPaths" in error for error in errors), errors)

    def test_validation_pass_requires_fresh_evidence_and_snapshot(self):
        state = ready_state()
        state["status"] = "REVIEW"
        state["gates"]["G6_REVIEW"] = "NOT_RUN"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        state["change"]["currentSnapshot"] = None
        state["validation"] = []
        errors = validator.validate_state(state)
        self.assertTrue(any("G5_VALIDATION" in error and "evidence" in error for error in errors), errors)
        self.assertTrue(any("currentSnapshot" in error for error in errors), errors)

    def test_review_pass_requires_current_independent_approve(self):
        state = ready_state()
        state["status"] = "HUMAN_CHECKPOINT"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        state["review"]["verdict"] = "CHANGES_REQUESTED"
        errors = validator.validate_state(state)
        self.assertTrue(any("G6_REVIEW" in error and "APPROVE" in error for error in errors), errors)

    def test_human_gate_pass_requires_approval_evidence(self):
        state = ready_state()
        state["status"] = "HUMAN_CHECKPOINT"
        state["risk"] = "HIGH"
        state["gates"]["G7_HUMAN"] = "PASS"
        state["gates"]["G8_SHIP_READY"] = "NOT_RUN"
        state["humanApproval"] = {"required": "YES", "status": "APPROVED", "evidence": None}
        errors = validator.validate_state(state)
        self.assertTrue(any("G7_HUMAN" in error and "evidence" in error for error in errors), errors)


class SnapshotTests(unittest.TestCase):
    def test_snapshot_changes_with_source_but_not_active_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "workflow@example.test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Workflow Test"], check=True)
            (root / "src.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "src.txt"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)
            base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

            (root / "src.txt").write_text("changed\n", encoding="utf-8")
            first = validator.compute_snapshot(root, base)

            (root / ".active").mkdir()
            (root / ".active" / "STATE.md").write_text("evidence one\n", encoding="utf-8")
            second = validator.compute_snapshot(root, base)
            self.assertEqual(first, second)

            (root / "src.txt").write_text("changed again\n", encoding="utf-8")
            third = validator.compute_snapshot(root, base)
            self.assertNotEqual(second, third)

    def test_ship_ready_live_snapshot_must_match_recorded_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "workflow@example.test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Workflow Test"], check=True)
            (root / "src.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "src.txt"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True)
            base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            (root / "src.txt").write_text("changed\n", encoding="utf-8")

            state = ready_state()
            state["baseline"]["baseCommit"] = base
            state["change"]["currentSnapshot"] = "sha256:fabricated"
            state["review"]["reviewedSnapshot"] = "sha256:fabricated"
            errors = validator.validate_live_snapshot(root, state)
            self.assertTrue(any("live delivery snapshot" in error.lower() for error in errors), errors)

            real = validator.compute_snapshot(root, base)
            state["change"]["currentSnapshot"] = real
            state["review"]["reviewedSnapshot"] = real
            self.assertEqual([], validator.validate_live_snapshot(root, state))


class StructureValidationTests(unittest.TestCase):
    def test_validator_and_tests_are_required_install_files(self):
        self.assertIn(".agent/scripts/validate_workflow.py", validator.REQUIRED_FILES)
        self.assertIn(".agent/tests/test_validate_workflow.py", validator.REQUIRED_FILES)

    def test_missing_required_files_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = validator.validate_structure(Path(tmp))
        self.assertTrue(any("AGENTS.md" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
