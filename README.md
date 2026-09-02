# AlphaInsider Skills

## Overview

Reusable, vendor-neutral skills for AlphaInsider API work and automated
AlphaInsider strategy projects.

## Skills

- `alphainsider` routes an explicit request to a published specialist.
- `alphainsider-api` provides current REST, WebSocket, authentication, sizing,
  and order guidance.
- `alphainsider-strategy-creator` creates and maintains plan-driven strategies,
  backtests, implementations, and native AI automation.

## Install

Install the optional router:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider
```

Invoke it with `/alphainsider`, “use the alphainsider skill,” “route this with
alphainsider,” or “which AlphaInsider skill.”

Install the API specialist:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-api
```

Install Strategy Creator with the API specialist:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-api \
  --skill alphainsider-strategy-creator
```

Strategy Creator remains self-contained when `alphainsider-api` is absent.

## How it works

Strategy Creator selects a persistent project and maintains its root `plan.md`
as the strategy agreement and current status. The interview settles the
strategy first, offers a credible backtest, and then separately offers to set
up the strategy on AlphaInsider. Strategy decisions can use fixed code, the
scheduled AI, or both.

If AlphaInsider setup is accepted, safe API-key access is the first action. The
skill then discovers compatible owned AlphaInsider strategies or plans a new
one. It builds and passes order-free checks before creating a strategy or
activating the platform's native AI scheduler. It never installs cron or
connects a broker.

The generated plan and scheduled-run instructions let scheduled agents perform
strategy runs and agreed self-healing without loading Strategy Creator. A
shared lock prevents overlap. A run error pauses new orders and future
scheduled runs until a verified repair or user-directed recovery succeeds.
Healthy runs stay quiet; poor performance alone is not an error. AlphaInsider
uses simulated funds; the skill never submits live-broker orders.
Errors only is the default notification choice. Users can also include
completed repairs, or completed repairs and warnings.

Explicit deletion inventories the project, schedule, AlphaInsider strategy,
history, and secrets before asking what to remove. It never cancels orders or
liquidates positions.

After successful setup, the handoff links to
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
The skill does not request broker credentials or create that connection.

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
