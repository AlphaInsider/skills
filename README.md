# AlphaInsider Skills

## Overview

AlphaInsider Skills provides reusable AI agent skills for integrating with
AlphaInsider and building standalone automated paper-trading strategies. The
skills are designed for developers who want API guidance, credential-safe
tooling, or a structured workflow that turns a trading idea into a tested
project.

## Skills

- `alphainsider` documents the AlphaInsider API and includes reusable REST and
  WebSocket clients, normalized trading calculations, and authenticated request
  tooling.
- `strategy-creator` interviews the user, researches suitable data sources,
  maintains a confirmed strategy plan, and generates or updates one automated
  stock or cryptocurrency strategy.

## Install

Install only the AlphaInsider API skill:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Install Strategy Creator with its required AlphaInsider dependency:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider \
  --skill strategy-creator
```

## How it works

Use `alphainsider` when you need endpoint behavior, request examples, market
data guidance, or reusable clients for an existing application.

Use `strategy-creator` when you want a complete strategy project. It asks one
decision at a time and records the agreed design in `docs/plan.md`. After the
plan is confirmed, it builds the smallest project that implements it, including
strategy code, dependency configuration, documentation, and offline tests.

Generated strategies use AlphaInsider as their only paper-trading order
destination. They validate the configured asset class and instruments before
ordering, reconcile existing positions and orders, and keep decision logic
independently testable. Optional backtests are included only when the required
historical inputs can be reconstructed without future information.

Credentials remain in the generated project's `.env`. Credential-safe helpers
avoid displaying or recording secret values, and generated artifacts contain
only variable names and safe examples. Each generated README includes a short,
language-specific `Start` section with copy-paste setup, one-cycle, continuous,
and test commands.

Existing Strategy Creator projects can be updated or replaced. Replacement is
planned separately and requires explicit approval before attributable files are
removed. Offline verification mocks external services and never submits
AlphaInsider orders.

Detailed lifecycle, safety, and implementation rules remain in each skill's
`SKILL.md` and references.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
npm ci
python scripts/validate_catalog.py
pytest
npm run skills:list
```
