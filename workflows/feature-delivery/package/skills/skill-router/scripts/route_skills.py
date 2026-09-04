#!/usr/bin/env python
"""Rank every installed Hermes skill against a natural-language request."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from rebuild_skill_catalog import build_catalog, default_skills_root, write_catalog

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "based", "by", "can", "do", "for",
    "from", "give", "help", "how", "i", "in", "is", "it", "me", "my", "need", "of", "on",
    "or", "please", "should", "skill", "skills", "that", "the", "this", "to", "use", "user",
    "want", "what", "when", "which", "with", "workflow", "you",
}
SYNONYMS: dict[str, tuple[str, ...]] = {
    "website": ("web", "browser", "frontend", "page", "ui"),
    "webpage": ("web", "browser", "page", "frontend"),
    "ui": ("interface", "visual", "frontend", "screen"),
    "ux": ("usability", "experience", "interface"),
    "bug": ("debug", "error", "failure", "issue"),
    "broken": ("debug", "failure", "error"),
    "research": ("investigate", "evidence", "sources", "validate"),
    "idea": ("founder", "validate", "problem", "startup"),
    "document": ("docx", "pdf", "file", "report"),
    "spreadsheet": ("excel", "xlsx", "csv", "table"),
    "slides": ("presentation", "powerpoint", "pptx", "deck"),
    "video": ("motion", "frames", "media", "recording"),
    "image": ("visual", "picture", "screenshot", "media"),
    "screen": ("interface", "ui", "visual", "rendered"),
    "review": ("audit", "critique", "inspect", "evaluation"),
    "build": ("create", "implement", "generate", "develop"),
    "create": ("build", "generate", "author", "produce"),
    "send": ("message", "email", "delivery", "outbound"),
    "privacy": ("identity", "removal", "broker", "security"),
    "slow": ("performance", "diagnostics", "cpu", "memory", "disk"),
    "repo": ("repository", "github", "codebase"),
    "pr": ("pull", "request", "github", "diff"),
    "mobile": ("phone", "android", "ios", "touch", "pwa"),
    "dashboard": ("analytics", "kpi", "metrics", "admin"),
}
FIELD_WEIGHTS = {
    "name": 6.0,
    "description": 2.2,
    "tags": 3.4,
    "triggers": 4.5,
    "category": 1.8,
    "related": 0.8,
    "prerequisites": 0.5,
}


def stem(token: str) -> str:
    if len(token) > 5 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 5 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 4 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def tokens(value: Any) -> list[str]:
    found = []
    for token in TOKEN_RE.findall(str(value).casefold().replace("-", " ")):
        token = stem(token)
        if token and token not in STOPWORDS and len(token) > 1:
            found.append(token)
    return found


def normalized_phrase(value: str) -> str:
    return " ".join(TOKEN_RE.findall(value.casefold().replace("-", " ")))


def query_terms(query: str) -> dict[str, float]:
    terms: dict[str, float] = {}
    for token in tokens(query):
        terms[token] = max(terms.get(token, 0.0), 1.0)
        for synonym in SYNONYMS.get(token, ()):
            synonym = stem(synonym)
            terms[synonym] = max(terms.get(synonym, 0.0), 0.38)
    return terms


def field_texts(skill: dict[str, Any]) -> dict[str, str]:
    return {
        "name": skill["name"],
        "description": skill["description"],
        "tags": " ".join(skill.get("tags", [])),
        "triggers": " ".join(skill.get("trigger_phrases", [])),
        "category": skill.get("category", ""),
        "related": " ".join(skill.get("related_skills", [])),
        "prerequisites": " ".join(skill.get("prerequisites", [])),
    }


def load_overrides(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"never_default": [], "phrase_boosts": []}
    return json.loads(path.read_text(encoding="utf-8"))


def latest_skill_mtime(skills_root: Path) -> float:
    mtimes = []
    for path in skills_root.rglob("SKILL.md"):
        try:
            mtimes.append(path.stat().st_mtime)
        except OSError:
            continue
    return max(mtimes, default=0.0)


def ensure_catalog(skills_root: Path, json_path: Path, markdown_path: Path, force: bool = False) -> tuple[dict[str, Any], bool]:
    stale = force or not json_path.exists() or json_path.stat().st_mtime < latest_skill_mtime(skills_root)
    if stale:
        catalog = build_catalog(skills_root)
        write_catalog(catalog, json_path, markdown_path)
        return catalog, True
    return json.loads(json_path.read_text(encoding="utf-8")), False


def rank_skills(query: str, catalog: dict[str, Any], overrides: dict[str, Any], top: int = 8) -> list[dict[str, Any]]:
    skills = catalog.get("skills", [])
    q_terms = query_terms(query)
    if not q_terms:
        return []

    documents: list[dict[str, Counter[str]]] = []
    document_frequency: Counter[str] = Counter()
    for skill in skills:
        fields = {name: Counter(tokens(text)) for name, text in field_texts(skill).items()}
        documents.append(fields)
        present = set().union(*(counter.keys() for counter in fields.values()))
        document_frequency.update(present)

    count = max(len(skills), 1)
    idf = {term: math.log((count + 1) / (df + 1)) + 1.0 for term, df in document_frequency.items()}
    query_phrase = normalized_phrase(query)
    query_lower = query.casefold()

    explicitly_named: set[str] = set()
    mentioned_names: set[str] = set()
    for skill in skills:
        name = skill["name"]
        normalized_name = normalized_phrase(name)
        direct_patterns = (
            f"/skill {name.casefold()}",
            f"use {name.casefold()} skill",
            f"load {name.casefold()} skill",
            f"skill {name.casefold()}",
        )
        if any(pattern in query_lower for pattern in direct_patterns):
            explicitly_named.add(name)
        elif len(normalized_name.split()) > 1 and normalized_name in query_phrase:
            mentioned_names.add(name)

    override_scores: dict[str, float] = Counter()
    override_reasons: dict[str, list[str]] = {}
    for rule in overrides.get("phrase_boosts", []):
        for phrase in rule.get("phrases", []):
            if normalized_phrase(phrase) in query_phrase:
                for name, boost in rule.get("skills", {}).items():
                    override_scores[name] += float(boost)
                    override_reasons.setdefault(name, []).append(f"phrase: {phrase}")
                break

    never_default = set(overrides.get("never_default", []))
    results: list[dict[str, Any]] = []
    for skill, fields in zip(skills, documents):
        score = 0.0
        matched_fields: dict[str, list[str]] = {}
        for field, counter in fields.items():
            field_matches = []
            for term, query_weight in q_terms.items():
                tf = counter.get(term, 0)
                if tf:
                    score += query_weight * idf.get(term, 1.0) * FIELD_WEIGHTS[field] * (1.0 + math.log(tf))
                    if query_weight >= 0.99:
                        field_matches.append(term)
            if field_matches:
                matched_fields[field] = sorted(set(field_matches))

        name = skill["name"]
        normalized_name = normalized_phrase(name)
        if name in explicitly_named:
            score += 60.0
        elif name in mentioned_names:
            score += 12.0

        if name not in explicitly_named:
            # Query bigrams appearing in descriptions help distinguish phases and artifacts.
            query_tokens = normalized_phrase(query).split()
            description_phrase = normalized_phrase(skill["description"])
            for left, right in zip(query_tokens, query_tokens[1:]):
                if f"{left} {right}" in description_phrase:
                    score += 2.5

        for trigger in skill.get("trigger_phrases", []):
            trigger_phrase = normalized_phrase(trigger)
            if trigger_phrase and trigger_phrase in query_phrase:
                score += 20.0
                override_reasons.setdefault(name, []).append(f"trigger: {trigger}")

        score += override_scores.get(name, 0.0)

        if (name in never_default or skill.get("retired_or_negative_default")) and name not in explicitly_named:
            score -= 100.0
        if skill.get("disable_model_invocation") and name not in explicitly_named:
            score -= 25.0

        if score <= 0.0:
            continue

        reasons = []
        if name in explicitly_named:
            reasons.append("explicit skill name")
        elif name in mentioned_names:
            reasons.append("skill-name phrase")
        reasons.extend(override_reasons.get(name, []))
        for field in ("name", "triggers", "tags", "description", "category"):
            if field in matched_fields:
                reasons.append(f"{field}: {', '.join(matched_fields[field][:5])}")

        results.append({
            "name": name,
            "score": round(score, 2),
            "category": skill.get("category", ""),
            "description": skill["description"],
            "path": skill["path"],
            "reasons": reasons[:8],
            "retired_or_negative_default": skill.get("retired_or_negative_default", False) or name in never_default,
        })

    results.sort(key=lambda item: (-item["score"], item["name"]))
    return results[: max(1, top)]


def render_markdown(query: str, candidates: list[dict[str, Any]], catalog_count: int, refreshed: bool) -> str:
    lines = [
        f"Query: {query}",
        f"Catalog: {catalog_count} skill(s){' (refreshed)' if refreshed else ''}",
        "",
        "| Rank | Skill | Score | Category | Why it matched |",
        "|---:|---|---:|---|---|",
    ]
    for index, candidate in enumerate(candidates, 1):
        reason = "; ".join(candidate["reasons"]) or "lexical context"
        lines.append(
            f"| {index} | `{candidate['name']}` | {candidate['score']:.2f} | "
            f"{candidate['category']} | {reason.replace('|', '/')} |"
        )
    if not candidates:
        lines.append("| — | No candidate | — | — | Use `skills_list` and a direct tool fallback. |")
    lines.extend([
        "",
        "Shortlist only: load plausible candidates with `skill_view` before choosing the route.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Natural-language user request to route.")
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--skills-root", type=Path, default=default_skills_root())
    skill_dir = Path(__file__).resolve().parents[1]
    parser.add_argument("--catalog", type=Path, default=skill_dir / "references" / "skill-catalog.json")
    parser.add_argument("--markdown-catalog", type=Path, default=skill_dir / "references" / "skill-catalog.md")
    parser.add_argument("--overrides", type=Path, default=skill_dir / "references" / "routing-overrides.json")
    args = parser.parse_args()

    catalog, refreshed = ensure_catalog(args.skills_root.resolve(), args.catalog, args.markdown_catalog, args.rebuild)
    overrides = load_overrides(args.overrides)
    candidates = rank_skills(args.query, catalog, overrides, args.top)

    if args.as_json:
        print(json.dumps({
            "query": args.query,
            "catalog_count": catalog.get("skill_count", len(catalog.get("skills", []))),
            "catalog_refreshed": refreshed,
            "candidates": candidates,
        }, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(args.query, candidates, catalog.get("skill_count", len(catalog.get("skills", []))), refreshed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
