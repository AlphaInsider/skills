# AlphaInsider Skills

## Overview

Skills for AlphaInsider API integration and paper-trading strategy projects.

## Skills

- `alphainsider-api` documents the AlphaInsider API and includes REST and
  WebSocket helpers plus normalized-value calculations.
- `alphainsider-strategy-creator` interviews the user, researches data sources,
  maintains a confirmed strategy plan, and generates or updates one automated
  stock or cryptocurrency strategy.

## Install

Install AlphaInsider:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-api
```

Install Strategy Creator and AlphaInsider:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-api \
  --skill alphainsider-strategy-creator
```

Strategy Creator does not require `alphainsider-api`.

## How it works

Use `alphainsider-strategy-creator` to maintain `docs/plan.md`. It plans Objective, Market
and instruments, Strategy behavior, Data and resources, Execution and risk,
Backtesting, and Implementation before Operation and scheduling and final
AlphaInsider target setup. Confirmation builds offline tests and is the sole
approval for every exact planned implementation or update action.

Strategies use AlphaInsider as their only paper-trading order
destination and prefer it for supported current market data. Backtests require
credible external history. User-run commands may submit orders without a
second prompt; offline verification never submits AlphaInsider orders.

Operation and scheduling distinguishes a single run, a persistent process, and
a recurring finite cycle across foreground, a background process using
user-level systemd or launchd or Windows Task Scheduler, or an agent
scheduler.
Managed resources default active on a first-session ready target.

Credentials remain in project `.env` files; agent-only chat entry is never
printed. Generated READMEs omit the helper and include a
language-specific `Start` section. Strategy Creator verifies its required
API-key permissions, discovers owned strategies, and syncs the confirmed
description. AlphaInsider's **AI Agent** preset selects the full bundle.

Local-only plans allow a mocked local build but make no remote calls or
operation resources and remain confirmed until target setup and
reconfirmation.

Existing Strategy Creator projects can be updated or replaced. Replacement is
planned separately and confirmed once for attributable cleanup, promotion, and
implementation without another approval. A local-only replacement leaves the
current strategy untouched.

An implemented strategy can also be retired through one confirmed
`docs/plan.md`. Strategy Creator first disables and removes only its
attributable operation resources, then lets the user retain and detach or
delete any exactly verified owned AlphaInsider target. It preserves `.env`,
`.gitignore`, historical data, unrelated files, and a retired audit plan.
Deletion warns about live state and undocumented cascades but never cancels
orders, liquidates positions, or submits a trade.

Strategy Creator plans share `contract_version`. A read-only check reports a
newer canonical release with
`npx skills@latest update alphainsider-api alphainsider-strategy-creator`, but it is never
installed automatically. The installed index routes older projects through
`references/versions/vN.md` into one final-confirmation upgrade.

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
