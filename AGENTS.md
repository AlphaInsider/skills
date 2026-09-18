# AlphaInsider Skills — Agent Guide

This repository publishes reusable AlphaInsider agent skills from `skills/`.

## Published skills

- [AlphaInsider router](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider/SKILL.md)
- [Strategy Creator](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider-strategy-creator/SKILL.md)
- [AlphaInsider API](https://api.alphainsider.com/skill.md)

For web-loaded files, resolve relative links against each fetched file's URL,
retaining the same Git ref (`master` above, or the selected release).
Human-facing documentation links to skill folders; agent-facing source links
use raw `SKILL.md` URLs. Keep installed package references relative.

## Rules

- Keep each public skill self-contained. `alphainsider` is the optional
  explicit router to published specialists; specialists stay self-contained.
  API behavior comes from the hosted `alphainsider-api` skill at
  `https://api.alphainsider.com/skill.md`, including for Strategy Creator.
  Do not prefer an older installed GitHub copy.
- Expose public skills only as `skills/<name>/SKILL.md`.
- Keep public skills and documentation agent-vendor agnostic; do not require
  vendor-specific metadata or behavior.
- Keep `SKILL.md` concise and route detailed material to one-level-deep
  `references/` files.
- The API skill and endpoint references are maintained in Mintlify; do not
  recreate a local API skill or copy its endpoint catalog into this repository.
- Before finalizing API-dependent guidance changes, read the hosted skill, the live
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
  generated-workspace contract, update the skill references and repository
  documentation in the same change.
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
pytest
npx skills@latest add . --list
```
