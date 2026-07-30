#!/usr/bin/env python3
"""Validate the public AlphaInsider skill catalog."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EXPECTED_SKILLS = {"alphainsider", "strategy-creator"}
EXPECTED_ALPHA_RUNTIME = {"__init__.py", "client.py", "stream.py"}
EXPECTED_STRATEGY_RUNTIME = {
    "__init__.py",
    "checkpoint.py",
    "reconcile.py",
    "runner.py",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"{path}: invalid frontmatter line {line!r}")
        fields[key.strip()] = value.strip()
    return fields


def validate() -> list[str]:
    errors: list[str] = []
    discovered = {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}
    if discovered != EXPECTED_SKILLS:
        errors.append(
            f"expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(discovered)}"
        )

    all_skill_files = list(ROOT.rglob("SKILL.md"))
    if len(all_skill_files) != len(EXPECTED_SKILLS):
        errors.append(f"expected exactly two SKILL.md files, found {len(all_skill_files)}")

    for name in sorted(EXPECTED_SKILLS):
        skill_dir = SKILLS_DIR / name
        skill_md = skill_dir / "SKILL.md"
        metadata = skill_dir / "agents" / "openai.yaml"
        if not skill_md.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        try:
            fields = frontmatter(skill_md)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: frontmatter must contain only name and description")
        if fields.get("name") != name:
            errors.append(f"{name}: frontmatter name does not match directory")
        if len(fields.get("description", "")) < 40:
            errors.append(f"{name}: description is too short")
        if not metadata.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")

    strategy = SKILLS_DIR / "strategy-creator"
    forbidden = list((strategy / "scripts").rglob("*alphainsider*"))
    forbidden += list((strategy / "references").glob("*alphainsider*"))
    if forbidden:
        errors.append("strategy-creator must not duplicate AlphaInsider resources")

    required_strategy_refs = {"plan-template.md", "alpaca.md", "coinbase.md"}
    actual_strategy_refs = {
        path.name for path in (strategy / "references").glob("*.md")
    }
    if actual_strategy_refs != required_strategy_refs:
        errors.append(
            "strategy-creator references must be exactly "
            f"{sorted(required_strategy_refs)}"
        )

    alpha_runtime = {
        path.name
        for path in (SKILLS_DIR / "alphainsider" / "scripts" / "runtime").glob("*.py")
    }
    if alpha_runtime != EXPECTED_ALPHA_RUNTIME:
        errors.append(
            "alphainsider runtime files must be exactly "
            f"{sorted(EXPECTED_ALPHA_RUNTIME)}"
        )

    strategy_runtime = {
        path.name for path in (strategy / "scripts" / "strategy_runtime").glob("*.py")
    }
    if strategy_runtime != EXPECTED_STRATEGY_RUNTIME:
        errors.append(
            "strategy runtime files must be exactly "
            f"{sorted(EXPECTED_STRATEGY_RUNTIME)}"
        )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("validated skills: alphainsider, strategy-creator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
