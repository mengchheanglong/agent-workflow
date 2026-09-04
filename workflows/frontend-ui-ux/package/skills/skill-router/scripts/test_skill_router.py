#!/usr/bin/env python
"""Smoke-test high-value routing decisions against the live skill catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from route_skills import ensure_catalog, load_overrides, rank_skills  # noqa: E402
from rebuild_skill_catalog import default_skills_root  # noqa: E402

CASES = [
    ("Polish this UI component and make the interaction details feel intentional", "emil-design-eng"),
    ("Add subtle micro-interactions and animation to this existing menu", "animate"),
    ("Build a polished browser dashboard prototype from real design references", "web-design-engineer"),
    ("Build a high converting landing page with SEO and one CTA", "landing-page-design"),
    ("Analyze this reference video and produce a detailed design motion superprompt", "video-to-superprompt"),
    ("Create a cinematic Awwwards-quality scroll storytelling portfolio", "build-awwwards-quality-sites"),
    ("Review the UI changes in this pull request and catch regressions", "interface-review"),
    ("Fix spacing grouping alignment and responsive layout problems", "better-layout"),
    ("Make this generic AI UI look distinctive and match this vibe", "tastemaker"),
    ("Critique this rendered interface screenshot across visual dimensions", "critique-screen"),
    ("Apply Gestalt proximity and Fitts law to this interface", "perception-laws"),
    ("Extract obligations and deadlines from this contract PDF", "document-to-action-items"),
    ("Debug this login form server action that does not submit", "web-form-flow-debugging"),
    ("Research whether this startup problem is real before building", "external-validation-research"),
    ("Create an Excel workbook with formulas and charts", "xlsx"),
    ("The Windows machine is slow and disk usage is stuck at 100 percent", "windows-system-diagnostics"),
    ("Create a stakeholder product requirements document from these meeting notes", "stakeholder-product-requirements"),
    ("Send this email and verify that it was delivered", "outbound-communication-operations"),
    ("Build a file-first second brain for this project", "project-second-brain"),
    ("Configure the Hermes gateway and tools", "hermes-agent"),
]


def main() -> int:
    skill_dir = SCRIPT_DIR.parent
    refs = skill_dir / "references"
    catalog, refreshed = ensure_catalog(
        default_skills_root(),
        refs / "skill-catalog.json",
        refs / "skill-catalog.md",
    )
    overrides = load_overrides(refs / "routing-overrides.json")
    installed = {skill["name"] for skill in catalog.get("skills", [])}

    failures = []
    for query, expected in CASES:
        candidates = rank_skills(query, catalog, overrides, top=5)
        actual = candidates[0]["name"] if candidates else None
        if expected not in installed:
            failures.append({"query": query, "expected": expected, "actual": actual, "reason": "expected skill is not installed"})
        elif actual != expected:
            failures.append({
                "query": query,
                "expected": expected,
                "actual": actual,
                "top3": [candidate["name"] for candidate in candidates[:3]],
            })

    unknown_overrides = sorted({
        name
        for rule in overrides.get("phrase_boosts", [])
        for name in rule.get("skills", {})
        if name not in installed
    })
    if unknown_overrides:
        failures.append({"reason": "routing overrides reference missing skills", "skills": unknown_overrides})

    result = {
        "catalog_count": catalog.get("skill_count", len(installed)),
        "catalog_refreshed": refreshed,
        "cases": len(CASES),
        "passed": len(CASES) - sum(1 for failure in failures if "query" in failure),
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
