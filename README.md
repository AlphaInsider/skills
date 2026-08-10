# AlphaInsider Skills

## Overview

AlphaInsider Skills provides reusable AI agent skills for integrating with
AlphaInsider and building standalone automated paper-trading strategies. The
skills combine API guidance and credential-safe tooling with a workflow that
turns a trading idea into a tested project.

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

Use `strategy-creator` to record decisions in `docs/plan.md`. It
plans market, behavior, execution, risk, and resources before AlphaInsider
forward-test setup and backtesting. A confirmed plan builds code,
dependencies, documentation, and offline tests and is the sole approval for
creating its planned remote target.

Generated strategies use AlphaInsider as their only paper-trading order
destination and prefer it for supported current market data. They validate
instruments, reconcile positions and orders, and keep decision logic testable.
Backtests require credible external history and are unavailable without it.
User-run one-cycle and continuous commands may submit paper orders without a
second prompt; Strategy Creator never starts them automatically.

Credentials remain in the generated project's `.env`. Strategy Creator
verifies its required API-key permissions, discovers owned strategies when no
ID is configured, creates only plan-confirmed remote strategies, and syncs the
confirmed description. Users should add credentials directly; agent-assisted
entry warns that pasted values are visible and uses a non-echoing helper. Each
generated README includes a short, language-specific `Start` section with
setup, run, and test commands.

Blocked AlphaInsider setup can be recorded as deferred without blocking
backtest planning or a complete local build with mocked external interactions.
Deferred plans make no remote calls, keep operational commands unavailable,
and remain confirmed until target setup is completed and the full plan is
reconfirmed.

Existing Strategy Creator projects can be updated or replaced. Replacement is
planned separately and requires explicit approval before attributable files are
removed. Offline verification mocks external services and never submits
AlphaInsider orders.

Strategy Creator plans share `contract_version`. A read-only check reports a
newer canonical release with
`npx skills@latest update alphainsider strategy-creator`, but it is never
installed automatically. The installed index routes older projects through
applicable `references/versions/vN.md` increments and combines them into one
approval-gated upgrade.

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
