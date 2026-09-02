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

The built-in grill interview uses simple technical English, multiple-choice
questions, recommended answers, clear action blocks, and an explicit next
step. A project can be code-led, agent-led, or hybrid. Stock and cryptocurrency
projects remain strictly separate.

After the strategy is Agreed, the skill offers and recommends a credible
backtest. Results include suitable charts, a benchmark, metrics, assumptions,
and data limits. Performance is information, not a runtime success condition.
Poor results never cause automatic strategy changes.

After results are settled, the skill offers AlphaInsider paper forward testing.
API-key entry is chat-first, with direct `.env` editing as an alternative.
The **AI Agent** permission preset is recommended. New targets are recommended
while compatible owned public and private targets remain selectable. The
fallback paper starting balance is `$100,000`. The fallback maximum leverage is
`1×`, and the skill explains AlphaInsider's `2×` ceiling.

The implementation and order-free tests finish before a new AlphaInsider target
is created. The setup helper cannot submit or cancel orders. The project then
uses only the platform's native AI scheduler. It never installs a host cron,
service, or background runner.

Each automation occurrence runs one finite cycle. Scheduler **Run now** and a
chat normal run use the same order-capable path. A chat dry run blocks orders
and canonical state changes. One durable lock prevents overlap, and missed runs
do not catch up.

On a trading error, the strategy blocks orders and pauses future automation.
Enabled self-healing can repair only plan-preserving implementation problems.
It uses snapshots, order-free checks, rollback, and a maximum of 30 minutes
while progress continues. Profitability never triggers repair.

Healthy runs stay quiet. Optional notifications use clear Warning,
Self-Healed, and Error labels. Notification failure does not pause trading.

Updates preserve the agreed plan while affected decisions are reviewed and
tested. Explicit deletion inventories the scheduler, AlphaInsider target,
project data, history, secrets, and API-key revocation separately. Cleanup
never cancels orders or liquidates positions.

After successful automation, the handoff links to
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
