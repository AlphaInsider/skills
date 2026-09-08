# AlphaInsider Skills

## Overview

Vendor-neutral skills for AlphaInsider API work and strategy automation.

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

Install both specialists:

```bash
npx skills@latest add https://github.com/AlphaInsider/skills \
  --skill alphainsider-api \
  --skill alphainsider-strategy-creator
```

`alphainsider-api` is optional.

## How it works

Strategy Creator guides **Define strategy → Backtest → Implement** using
question rounds with options and recommendations. Required user actions get
their own turn; questions resume after completion. The agent chooses relevant
questions and guardrails for the strategy, considering actual AI scheduling,
AlphaInsider, and data limits. Backtest feasibility comes first; users can
choose the closest useful test or skip it after reviewing limitations. Results
include charts and visuals when possible.

A dedicated persistent project's root `plan.md` records high-level decisions,
progress, open questions, resources, and the next action. Its outline is
flexible so later chats can resume or update the work without a fixed field
schema. Secrets stay in project `.env`; users may paste a new API key in chat
for the non-echoing helper or edit `.env` themselves. Agents never inspect
existing secret values.

Implementation recommends a new AlphaInsider strategy and offers compatible
owned strategies. Users choose self-healing and notification settings. Trading
decisions can use code, scheduled AI judgment, or both. The skill generates
project-specific code and a runbook; AlphaInsider strategies use simulated funds.

Each scheduled agent runs the program command and evaluates expected outcomes.
Shared exclusivity prevents overlapping runs. On an error, execution blocks
new orders and pauses the scheduler. Enabled self-healing may repair any
implementation issue that preserves the plan's decisions and needs no human
input or new authority. A dry run without orders verifies the fix before a
suitable immediate rerun or resumption for the next scheduled run. Unresolved
or interrupted recovery stays paused for the user. Notifications explain the
issue, automation state, and next step through the selected events and channels.

New schedules are enabled automatically during setup for the next scheduled
run, without another activation prompt. Project access and agent-controlled
pause/resume are checked through platform configuration and documentation;
no prior scheduled run is required. Explicit user pauses or concrete setup
failures leave automation inactive. Local checks and backtests never submit
AlphaInsider orders.

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
