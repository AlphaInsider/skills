# AlphaInsider Skills

## Overview

AlphaInsider Skills provides reusable AI agent skills for integrating with
AlphaInsider and building standalone automated paper-trading strategies. The
skills are designed for developers who want API guidance, credential-safe
tooling, or a structured workflow that turns a trading idea into a tested
project.

## Skills

- `alphainsider` documents the AlphaInsider API and includes thin REST and
  WebSocket helpers plus deterministic normalized-value calculations.
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
data guidance, or credential-safe generic API transports.

Use `strategy-creator` when you want a complete strategy project. It asks one
decision at a time and records the agreed design in `docs/plan.md`. After the
plan is confirmed, it builds the smallest project that implements it, including
strategy code, dependency configuration, documentation, and offline tests.

Generated strategies use AlphaInsider as their only paper-trading order
destination and prefer it for supported current market data. They validate
instruments, reconcile positions and orders, and keep decision logic testable.
Backtests require credible external history and are unavailable without it.

Credentials remain in the generated project's `.env`. Strategy Creator lists
and verifies its required API-key permissions without exposing the key. If no
strategy ID is configured, it discovers owned strategies or approval-gates a
new remote strategy after plan confirmation, safely stores its ID, and syncs
the confirmed description. Users are advised to add credentials directly;
optional agent-assisted entry warns that pasted values are visible and uses a
non-echoing helper. Generated artifacts contain only safe examples. Each
generated README includes a short, language-specific `Start` section with
copy-paste setup, one-cycle, continuous, and test commands.

Existing Strategy Creator projects can be updated or replaced. Replacement is
planned separately and requires explicit approval before attributable files are
removed. Offline verification mocks external services and never submits
AlphaInsider orders.

Strategy Creator plans carry the skill's shared `contract_version`. On every
invocation, a read-only check compares the installed version with the canonical
repository. A newer release is reported with
`npx skills@latest update alphainsider strategy-creator`, but is never installed
automatically. Project upgrades use only the installed contract and remain
approval-gated.

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
