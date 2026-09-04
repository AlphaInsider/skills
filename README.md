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

Strategy Creator stores its source of truth in a persistent project's root
`plan.md`, with **Current status** first; former flat plans remain compatible.
The journey is **Define
Strategy**, optional **Backtest Strategy**, then **Implement Strategy on
AlphaInsider**. During Define, it inspects the actual native AI scheduler and
public AlphaInsider constraints and offers implementable timing choices.
Explicit session guidance takes priority. When it is absent, stocks use the
Strategy Creator fallback of US
regular hours; cryptocurrency is available 24/7. Scheduler and data-cutoff
limits still apply. It never fakes a faster cadence with a background loop.
Decisions use fixed code, scheduled AI, or both.

Backtesting is always offered. Feasibility is assessed only after selection.
Every run is a backtest with recorded future-information use, differences from
intended automation, a Valid, Superseded, or Failed disposition, and
recoverable source. Future-information use is warned before results and beside
affected measurements. Only Valid evidence for the current strategy advances
the outcome. Findings summaries embed or directly link two to four saved
data-derived visuals; a detailed report alone is insufficient.

Implementation safely obtains missing API access and selects a compatible or
new strategy. **Build, Configure, and Activate** authorizes reviewed work.
Order-free checks precede creation and activation. It never installs cron or
connects a broker. Creation is Complete only after the AlphaInsider strategy
validates and native automation is active.

Generated instructions support strategy runs and confirmed self-healing without
loading Strategy Creator. A shared lock prevents overlap. A run error ends
that run's order work: automation stays Active and Degraded/Retrying, and
the next trigger reconciles and retries. Unsafe, duplicate, missed, and same-run
retry orders are prohibited. Only the user, setup, update, or deletion pauses
automation. AlphaInsider uses simulated funds.
Errors only is the default notification choice. Users can also include
completed repairs, or completed repairs and warnings. Setup discovers
notification support without sending test messages. Delivery during operation
is best effort; failure never pauses trading or automation. Notification repair
runs only inside enabled, confirmed self-healing scope.

Explicit deletion inventories resources before selection. It never cancels
orders or liquidates positions.

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
