# AlphaInsider Skills — Agent Guide

This repository publishes reusable AlphaInsider agent skills from `skills/`.

## Rules

- Keep each public skill self-contained except for the documented
  `strategy-creator` build-time dependency on `alphainsider`.
- Expose public skills only as `skills/<name>/SKILL.md`.
- Keep public skills and documentation agent-vendor agnostic; do not require
  vendor-specific metadata or behavior.
- Keep `SKILL.md` concise and route detailed material to one-level-deep
  `references/` files.
- Keep `skills/alphainsider/SKILL.md` and its `references/` aligned with the
  AlphaInsider API docs at `https://api.alphainsider.com`, including the
  current OpenAPI and AsyncAPI contracts.
- Put deterministic reusable code in `scripts/`; never place credentials,
  `.env`, user plans, or generated strategies in this repository.
- When a design decision changes the strategy interview, plan schema, or
  generated-workspace contract, update the skill references, catalog
  validation, and repository documentation in the same change.
- After the initial Strategy Creator `1.0.0` release, bump its shared SemVer
  for every subsequent change affecting `strategy-creator` before pushing to
  `master`. Follow `skills/strategy-creator/references/versioning.md` and keep
  its `current_version` aligned with the `contract_version` in
  `skills/strategy-creator/references/plan-template.md`.
- Preserve the AlphaInsider credential boundary: agents never inspect or print
  existing API keys or `.env` values. Strategy Creator may accept values the
  user deliberately pastes in chat and write them to the selected project's
  `.env` only through its non-echoing helper.
- Agents may create, edit, and run local tests under `tests/`. The directory is
  intentionally Git-ignored, so do not force-add its contents.
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
