# AlphaInsider Skills — Agent Guide

This repository publishes reusable AlphaInsider agent skills from `skills/`.

## Rules

- Keep each public skill self-contained except for the documented
  `strategy-creator` build-time dependency on `alphainsider`.
- Expose public skills only as `skills/<name>/SKILL.md`.
- Keep `SKILL.md` concise and route detailed material to one-level-deep
  `references/` files.
- Put deterministic reusable code in `scripts/`; never place credentials,
  `.env`, user plans, or generated strategies in this repository.
- Preserve the AlphaInsider credential boundary: agents never inspect or print
  API keys or `.env` values.
- Tests must not submit AlphaInsider paper orders. Network smoke tests are
  read-only and opt-in.

## Verification

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm ci
python scripts/validate_catalog.py
pytest
npm run skills:list
```
