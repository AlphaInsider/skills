# AlphaInsider Skills

## Overview

Reusable, vendor-neutral skills for AlphaInsider API work and automated
paper-trading strategy projects.

## Skills

- `alphainsider` routes an explicit request to a published specialist.
- `alphainsider-api` provides current REST, WebSocket, authentication, sizing,
  and order guidance.
- `alphainsider-strategy-creator` interviews the user, maintains a strategy
  agreement, builds and backtests the project, and configures native AI
  automation.

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

Strategy Creator selects the safest persistent workspace without asking for a
path. Each strategy gets one dedicated project with a root `plan.md`,
`strategy/`, `backtest/`, `runtime/`, and `tests/`. The plan separately records
the current phase, Draft or Agreed plan state, highest completed outcome, and
automation state. Another chat or scheduled agent can resume from its current
status.

The grill interview uses simple technical English, multiple-choice questions,
recommendations, clear actions, and an explicit next step. Each choice covers
only its current decision. Later optional work is
introduced separately without internal stage names. Projects can be code-led,
agent-led, or hybrid. Stock and cryptocurrency projects remain separate.

After the strategy is Agreed, the skill offers and recommends a credible
backtest. Results include suitable charts, a benchmark, metrics, assumptions,
and data limits. Performance is information, not a runtime success condition.
Poor results never cause automatic strategy changes.

After backtest results, the skill recommends AlphaInsider paper forward testing.
It verifies scheduled secret storage, then makes a missing API key the first
user action. Chat entry and the **AI Agent** permission preset are recommended;
direct `.env` editing is an alternative. It checks discovery permissions first
and final permissions after implementation design. The verified account
supplies target choices. It recommends a new public target with a `$100,000`
starting scale; existing targets keep their settings and history. Leverage
defaults to `1×` within AlphaInsider's `2×` limit.

The implementation and order-free tests finish before a new AlphaInsider target
is created. The setup helper cannot submit or cancel orders. The project then
uses only the platform's native AI scheduler. It never installs a host cron,
service, or background runner. The generated plan and runbook are sufficient
for normal runs and agreed self-healing without the installed skill.

Stopped setup pauses automation, preserves resources, and records its resume
point.

Each automation occurrence runs one finite cycle. Scheduler **Run now** and a
chat normal run use the same order-capable path. A chat dry run blocks orders
and canonical state changes. One durable lock prevents overlap, and missed runs
do not catch up.

Generated projects use one shared AlphaInsider compatibility check for every
order-capable path, including verification that stock orders occur only during
regular market hours.

A true run error blocks orders and pauses automation. Only successful
self-healing or verified user-directed recovery resumes it. Repair uses
snapshots, order-free checks, rollback, and at most 30 minutes while progress
continues. Profitability never triggers repair.

Healthy runs stay quiet. Optional notifications ask for event policy and
supported channels. Essential notifications send Error and Self-Healed events;
Expanded also sends Warnings. A notification-only failure does not pause.

Updates preserve the agreed plan while affected decisions are reviewed and
tested. Explicit deletion inventories the scheduler, AlphaInsider target,
project data, history, secrets, and API-key revocation separately. Cleanup
never cancels orders or liquidates positions.

Earlier endings use matching headings. Automated success recommends optional
broker connection through
[AlphaInsider broker automation resources](https://alphainsider.com/resources#automating-trades).
The skill never handles broker credentials or creates a broker connection.

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
