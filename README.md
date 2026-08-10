# AlphaInsider Skills

## Overview

Agent skills for AlphaInsider API integration and automated
paper-trading strategy projects.

## Skills

- `alphainsider` documents the AlphaInsider API and includes REST and
  WebSocket helpers plus deterministic normalized-value calculations.
- `strategy-creator` interviews the user, researches data sources,
  maintains a confirmed strategy plan, and generates or updates one automated
  stock or cryptocurrency strategy.

## Install

Install the AlphaInsider API skill:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Install Strategy Creator with its AlphaInsider dependency:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider \
  --skill strategy-creator
```

## How it works

Use `alphainsider` when you need endpoint behavior, request examples, market
data guidance, or credential-safe generic API transports.

Use `strategy-creator` to record decisions in `docs/plan.md`. It
plans market, behavior, execution, risk, and resources, then optional
background operation, before AlphaInsider forward-test setup and backtesting.
A confirmed plan builds code, dependencies, documentation, and offline tests
and is the sole approval for every exact planned implementation or update
action, including target creation, overwrites, replacements, synchronization,
and background installation.

Generated strategies use AlphaInsider as their only paper-trading order
destination and prefer it for supported current market data. They validate
instruments, reconcile positions and orders, and keep decision logic testable.
Backtests require credible external history and are unavailable without it.
User-run one-cycle and continuous commands may submit paper orders without a
second prompt; Strategy Creator never starts them automatically.

Background operation uses one user-level systemd, launchd, or tmux setup.
Native definitions install inactive; generated instructions cover management
and logs.

Credentials remain in project `.env` files. Users edit them by default. Chat
entry is a less-secure agent-only fallback: values may appear in tool metadata
or process listings but are never printed. Generated READMEs omit the helper
and include a language-specific `Start` section.
Strategy Creator verifies its required API-key permissions, discovers owned
strategies, and syncs the confirmed description.

Blocked AlphaInsider setup can be recorded as deferred without blocking
backtest planning or a complete local build with mocked external interactions.
Deferred plans make no remote calls, keep operational commands unavailable,
and remain confirmed until target setup is completed and the full plan is
reconfirmed.

Existing Strategy Creator projects can be updated or replaced. Replacement is
planned separately; its final confirmation authorizes exact attributable
removal and promotion without another approval. Offline verification mocks
external services and never submits AlphaInsider orders.

Strategy Creator plans share `contract_version`. A read-only check reports a
newer canonical release with
`npx skills@latest update alphainsider strategy-creator`, but it is never
installed automatically. The installed index routes older projects through
applicable `references/versions/vN.md` increments and combines them into one
final-confirmation upgrade.

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
