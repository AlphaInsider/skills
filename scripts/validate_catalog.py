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
EXPECTED_STRATEGY_REFERENCES = {"interview.md", "plan-template.md"}
EXPECTED_PLAN_STATES = {"draft", "confirmed", "implemented"}
REQUIRED_PLAN_SECTIONS = {
    "# Strategy Plan",
    "## Objective",
    "## AlphaInsider target",
    "## Strategy behavior",
    "## Data and resources",
    "## Execution and risk",
    "## Backtesting",
    "## Implementation",
    "## Confirmation",
}
REQUIRED_PLAIN_LANGUAGE_PLAN_FIELDS = {
    "- Goal:",
    "- Why the strategy could work:",
    "- When results will be reviewed:",
    "- What would show the strategy is working:",
    "- What would show the strategy needs changes or should stop:",
    "- Automatic pause or shutdown conditions and logging:",
    "- Tests to run and expected results:",
}
FORBIDDEN_USER_FACING_PHRASES = {
    "acceptance criteria",
    "evaluation horizon",
    "success and failure criteria",
    "success criteria",
    "success criterion",
    "success or failure criteria",
}
REQUIRED_REPLACEMENT_GUIDANCE = {
    "every section heading from the current plan template",
    "update the existing plan",
    "replace the trading strategy with a new one",
    "`docs/replacement-plan.md`",
    "does not authorize deletion, plan promotion, or implementation",
    "Show the exact proposed deletion paths",
    "separate explicit approval",
    "Never recursively delete the project root",
    "Never delete `.env`",
    "If the user declines",
    "replace `docs/plan.md` with `docs/replacement-plan.md`",
}
REQUIRED_README_REPLACEMENT_GUIDANCE = {
    "recognizes the folder as an existing project",
    "`docs/replacement-plan.md`",
    "separate explicit approval",
    "never recursively deletes the project root",
    "never deletes `.env`",
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
    actual_strategy_refs = {
        path.name for path in (strategy / "references").glob("*.md")
    }
    if actual_strategy_refs != EXPECTED_STRATEGY_REFERENCES:
        errors.append(
            "strategy-creator references must be exactly "
            f"{sorted(EXPECTED_STRATEGY_REFERENCES)}"
        )

    strategy_scripts = [
        path
        for path in (strategy / "scripts").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]
    if strategy_scripts:
        errors.append("strategy-creator must not contain scripts")

    plan_template = strategy / "references" / "plan-template.md"
    if plan_template.is_file():
        plan_text = plan_template.read_text(encoding="utf-8")
        try:
            plan_fields = frontmatter(plan_template)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if plan_fields != {"status": "draft"}:
                errors.append("strategy plan template must start in draft status")
        missing_sections = REQUIRED_PLAN_SECTIONS - set(plan_text.splitlines())
        if missing_sections:
            errors.append(
                "strategy plan template is missing sections "
                f"{sorted(missing_sections)}"
            )
        plan_lines = {line.partition(" _")[0] for line in plan_text.splitlines()}
        missing_fields = REQUIRED_PLAIN_LANGUAGE_PLAN_FIELDS - plan_lines
        if missing_fields:
            errors.append(
                "strategy plan template is missing plain-language fields "
                f"{sorted(missing_fields)}"
            )

        interview_path = strategy / "references" / "interview.md"
        if interview_path.is_file():
            interview_text = interview_path.read_text(encoding="utf-8")
            user_facing_text = f"{interview_text}\n{plan_text}".lower()
            found_phrases = {
                phrase
                for phrase in FORBIDDEN_USER_FACING_PHRASES
                if phrase in user_facing_text
            }
            if found_phrases:
                errors.append(
                    "strategy interview or plan uses replaced planning jargon "
                    f"{sorted(found_phrases)}"
                )

    strategy_text = (strategy / "SKILL.md").read_text(encoding="utf-8")
    missing_states = {
        state for state in EXPECTED_PLAN_STATES if f"`{state}`" not in strategy_text
    }
    if missing_states:
        errors.append(
            "strategy-creator is missing plan states " f"{sorted(missing_states)}"
        )

    interview_text = (
        strategy / "references" / "interview.md"
    ).read_text(encoding="utf-8")
    manual_text = " ".join(f"{strategy_text}\n{interview_text}".split())
    missing_replacement_guidance = {
        guidance
        for guidance in REQUIRED_REPLACEMENT_GUIDANCE
        if guidance not in manual_text
    }
    if missing_replacement_guidance:
        errors.append(
            "strategy-creator is missing replacement guidance "
            f"{sorted(missing_replacement_guidance)}"
        )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme_text.split())
    missing_readme_guidance = {
        guidance
        for guidance in REQUIRED_README_REPLACEMENT_GUIDANCE
        if guidance not in normalized_readme
    }
    if missing_readme_guidance:
        errors.append(
            "README is missing strategy replacement guidance "
            f"{sorted(missing_readme_guidance)}"
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
