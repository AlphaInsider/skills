#!/usr/bin/env python3
"""Validate the public AlphaInsider skill catalog."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
EXPECTED_SKILLS = {"alphainsider", "strategy-creator"}
EXPECTED_ALPHA_SCRIPTS = {
    "alphainsider_request.py",
    "alphainsider_stream.py",
}
EXPECTED_ALPHA_REFERENCES = {
    "api-reference.md",
    "authentication.md",
    "bots.md",
    "input-multiplier.md",
    "limits.md",
    "payments.md",
    "stocks.md",
    "strategies.md",
    "subscriptions.md",
    "timelines.md",
    "trades.md",
    "users.md",
    "webhooks.md",
    "websockets.md",
    "withdrawals.md",
}
EXPECTED_STRATEGY_REFERENCES = {"interview.md", "plan-template.md"}
EXPECTED_STRATEGY_SCRIPTS = {"set_env_value.py"}
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
    "- Automatic pause or shutdown conditions and logging:",
    "- Tests to run and expected results:",
}
REMOVED_PLAN_FIELDS = {
    "- Why the strategy could work:",
    "- When results will be reviewed:",
    "- What would show the strategy is working:",
    "- What would show the strategy needs changes or should stop:",
    "- User confirmation:",
    "- Confirmation time:",
}
REMOVED_INTERVIEW_QUESTIONS = {
    "Why do you think this trading idea could work?",
    "After how much time or how many trades should we review the results?",
    "What results would tell you the strategy is working?",
    "What loss or behavior would make you change or stop it?",
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
REQUIRED_CREDENTIAL_GUIDANCE = {
    "`scripts/set_env_value.py`",
    "`scripts/alphainsider_request.py`",
    "`scripts/alphainsider_stream.py`",
    "Recommend that the user add the values to `.env` themselves",
    "they may paste the values in chat",
    "the value is visible to the agent",
    "non-echoing prompt",
    "Never pass a credential in a command argument",
    "Do not open `.env` before or after the update",
    "approval to update only those names",
    "use the sibling request helper",
}
REQUIRED_ALPHA_CREDENTIAL_GUIDANCE = {
    "never return the API key or arbitrary environment contents",
    "not secrets like the API key",
    "Never dump the process environment or complete `.env`",
    "prevents accidental output exposure, not hostile same-process inspection",
}
REQUIRED_STARTUP_GUIDANCE = {
    "a short `## Start` section",
    "ordered, copy-paste commands",
    "dependency installation and `.env` preparation",
    "one decision cycle and continuous operation equally",
    "Match the selected language",
    "`source .venv/bin/activate` immediately before the execution commands",
    "the project's exact package-manager and runtime commands",
}
README_MAX_WORDS = 450
REQUIRED_README_SECTIONS = {
    "# AlphaInsider Skills",
    "## Overview",
    "## Skills",
    "## Install",
    "## How it works",
    "## Development",
}
REQUIRED_README_OVERVIEW_GUIDANCE = {
    "`alphainsider`",
    "`strategy-creator`",
    "npx skills@latest add",
    "`docs/plan.md`",
    "paper-trading",
    "Credentials remain",
    "offline tests",
    "language-specific `Start` section",
    "explicit approval",
    "never submits AlphaInsider orders",
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

    strategy = SKILLS_DIR / "strategy-creator"
    actual_strategy_refs = {
        path.name for path in (strategy / "references").glob("*.md")
    }
    if actual_strategy_refs != EXPECTED_STRATEGY_REFERENCES:
        errors.append(
            "strategy-creator references must be exactly "
            f"{sorted(EXPECTED_STRATEGY_REFERENCES)}"
        )

    strategy_scripts = {
        path.relative_to(strategy / "scripts").as_posix()
        for path in (strategy / "scripts").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if strategy_scripts != EXPECTED_STRATEGY_SCRIPTS:
        errors.append(
            "strategy-creator scripts must be exactly "
            f"{sorted(EXPECTED_STRATEGY_SCRIPTS)}"
        )

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
        obsolete_fields = {
            field for field in REMOVED_PLAN_FIELDS if field in plan_text
        }
        if obsolete_fields:
            errors.append(
                "strategy plan template contains removed evaluation fields "
                f"{sorted(obsolete_fields)}"
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
    obsolete_questions = {
        question
        for question in REMOVED_INTERVIEW_QUESTIONS
        if question in interview_text
    }
    if obsolete_questions:
        errors.append(
            "strategy interview contains removed evaluation questions "
            f"{sorted(obsolete_questions)}"
        )
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

    missing_credential_guidance = {
        guidance
        for guidance in REQUIRED_CREDENTIAL_GUIDANCE
        if guidance not in manual_text
    }
    if missing_credential_guidance:
        errors.append(
            "strategy-creator is missing credential setup guidance "
            f"{sorted(missing_credential_guidance)}"
        )

    missing_startup_guidance = {
        guidance
        for guidance in REQUIRED_STARTUP_GUIDANCE
        if guidance not in manual_text
    }
    if missing_startup_guidance:
        errors.append(
            "strategy-creator is missing generated README startup guidance "
            f"{sorted(missing_startup_guidance)}"
        )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized_readme = " ".join(readme_text.split())
    missing_readme_sections = REQUIRED_README_SECTIONS - set(
        readme_text.splitlines()
    )
    if missing_readme_sections:
        errors.append(
            "README is missing sections " f"{sorted(missing_readme_sections)}"
        )

    readme_word_count = len(readme_text.split())
    if readme_word_count > README_MAX_WORDS:
        errors.append(
            f"README must not exceed {README_MAX_WORDS} words; "
            f"found {readme_word_count}"
        )

    missing_readme_overview_guidance = {
        guidance
        for guidance in REQUIRED_README_OVERVIEW_GUIDANCE
        if guidance not in normalized_readme
    }
    if missing_readme_overview_guidance:
        errors.append(
            "README is missing high-level guidance "
            f"{sorted(missing_readme_overview_guidance)}"
        )

    alphainsider = SKILLS_DIR / "alphainsider"
    alphainsider_text = (alphainsider / "SKILL.md").read_text(encoding="utf-8")
    missing_alpha_credential_guidance = {
        guidance
        for guidance in REQUIRED_ALPHA_CREDENTIAL_GUIDANCE
        if guidance not in " ".join(alphainsider_text.split())
    }
    if missing_alpha_credential_guidance:
        errors.append(
            "alphainsider is missing credential boundary guidance "
            f"{sorted(missing_alpha_credential_guidance)}"
        )

    alpha_scripts = {
        path.relative_to(alphainsider / "scripts").as_posix()
        for path in (alphainsider / "scripts").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if alpha_scripts != EXPECTED_ALPHA_SCRIPTS:
        errors.append(
            "alphainsider scripts must be exactly "
            f"{sorted(EXPECTED_ALPHA_SCRIPTS)}"
        )

    alpha_references = {
        path.name for path in (alphainsider / "references").glob("*.md")
    }
    if alpha_references != EXPECTED_ALPHA_REFERENCES:
        errors.append(
            "alphainsider references must be exactly "
            f"{sorted(EXPECTED_ALPHA_REFERENCES)}"
        )

    helper_markers = {
        "scripts/alphainsider_request.py",
        "scripts/alphainsider_stream.py",
        "stream_events(",
    }
    references_with_helper_guidance = {
        path.name
        for path in (alphainsider / "references").glob("*.md")
        if any(marker in path.read_text(encoding="utf-8") for marker in helper_markers)
    }
    if references_with_helper_guidance:
        errors.append(
            "alphainsider references must contain API information only; "
            "helper guidance found in "
            f"{sorted(references_with_helper_guidance)}"
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
