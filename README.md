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

The [access check](skills/alphainsider-strategy-creator/references/workflow-contracts.md#check-platform-and-automation-access)
verifies execution and persistent file access before project work. Use the host
application's native AI scheduler unless unsupported or the user explicitly requests
external scheduling.

Strategy Creator guides **Define strategy → Backtest → Implement** using
ranked workflow outlines: number only operations that require sequence; use
bullets and sub-bullets for other notes, ranked by importance. Question rounds
present options on consecutive lines, with recommendations. After strategy definition
and backtesting, a summary and standalone next-step question let users backtest, implement on
AlphaInsider, revise, or stop. Required user actions get their own turn; questions
resume after completion. Questions and guardrails reflect actual AI scheduling,
AlphaInsider, and data limits. Backtest planning starts with feasibility and
useful alternatives; users can skip after reviewing limitations. Results include
charts and visuals when possible.

The project's root `plan.md` records decisions, progress, resources, open questions,
workspace/runner binding and access evidence, and the next action. Its flexible
outline supports later chats. Secrets stay in project `.env`; users may paste
new API keys for the non-echoing helper or edit `.env` themselves. Agents never
inspect existing secret values.
Before requesting a key, create missing `.env` and `.env.example` files with an
empty `ALPHAINSIDER_API_KEY=` entry.

Implementation recommends a new public AlphaInsider strategy and offers compatible
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

New schedules activate automatically during setup for the next run, without
another prompt. Access is rechecked for the actual task, alongside agent-controlled
pause/resume, using configuration and documentation; no prior scheduled run is
required. Explicit user pauses or concrete setup failures keep automation
inactive. Local checks and backtests never submit AlphaInsider orders.

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
