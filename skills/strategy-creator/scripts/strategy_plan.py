"""Detect the strategy-plan lifecycle state from ``docs/plan.md``.

States: ``interviewing`` (plan missing or draft), ``confirmed`` (user approved
the full plan; implement it), ``implemented`` (strategy built; handle prompts
normally). Run ``python -m scripts.strategy_plan`` to see the state and the
next action.
"""

from __future__ import annotations

import argparse
from pathlib import Path

PLAN_PATH = Path("docs/plan.md")
STATES = ("interviewing", "confirmed", "implemented")

NEXT_ACTION = {
    "interviewing": "Begin or resume the strategy interview with $strategy-creator.",
    "confirmed": "Implement the confirmed plan with $strategy-creator.",
    "implemented": "Strategy is implemented; handle prompts normally.",
}


def _frontmatter_status(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if key.strip() == "status":
            return value.strip().lower()
    return None


def read_plan_status(path: str | Path = PLAN_PATH) -> str:
    """Missing plan, or a draft without a valid ``status`` in its frontmatter,
    is ``interviewing``."""
    path = Path(path)
    if not path.exists():
        return "interviewing"
    status = _frontmatter_status(path.read_text())
    return status if status in STATES else "interviewing"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="strategy-plan", description=__doc__)
    parser.add_argument("--path", default=PLAN_PATH, help="plan file (default: %(default)s)")
    args = parser.parse_args(argv)
    status = read_plan_status(args.path)
    print(f"plan state: {status}")
    print(f"next: {NEXT_ACTION[status]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
