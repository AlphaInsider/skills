# AlphaInsider Skills — Agent Guide

This repository publishes reusable AlphaInsider agent skills from `skills/`.

## Rules

- Keep each public skill self-contained. `alphainsider` is the optional
  explicit router to published specialists; specialists stay self-contained.
  When `alphainsider-api` and `alphainsider-strategy-creator` are both
  installed, Strategy Creator should read `alphainsider-api` for API behavior.
- Expose public skills only as `skills/<name>/SKILL.md`.
- Keep public skills and documentation agent-vendor agnostic; do not require
  vendor-specific metadata or behavior.
- Keep `SKILL.md` concise and route detailed material to one-level-deep
  `references/` files.
- Keep `skills/alphainsider-api/SKILL.md` and its `references/` aligned with the
  AlphaInsider API docs at `https://api.alphainsider.com`, including the
  current OpenAPI and AsyncAPI contracts.
- Before finalizing any change under `skills/alphainsider-api/`, read the live
  `https://api.alphainsider.com/llms.txt` index and the relevant focused
  Markdown pages, then verify REST operations against
  `https://api.alphainsider.com/openapi.yaml` and WebSocket messages against
  `https://api.alphainsider.com/asyncapi.yaml`. Compare operation and message
  inventories, methods, paths, fields, requiredness, types, enums, defaults,
  authentication placement, channel names, examples, and documented side
  effects. Reconcile every discrepancy in the same change and report which
  live sources were checked.
- Put deterministic reusable code in `scripts/`; never place credentials,
  `.env`, user plans, or generated strategies in this repository.
- When a design decision changes the strategy interview, plan schema, or
  generated-workspace contract, update the skill references, catalog
  validation, and repository documentation in the same change.
- Preserve the AlphaInsider credential boundary: agents never inspect or print
  existing API keys or `.env` values. Public strategy IDs may be shown.
  Strategy Creator may accept values the user deliberately pastes in chat and
  write them to the selected project's `.env` only through its non-echoing
  helper.
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
