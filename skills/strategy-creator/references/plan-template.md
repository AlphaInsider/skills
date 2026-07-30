---
status: interviewing
---

# Strategy Plan

<!--
Copy this template to docs/plan.md on the first confirmed interview
answer. Fill sections as answers arrive; leave unanswered sections as
"_not yet decided_". Lifecycle: status is one of
interviewing | confirmed | implemented.
-->

## Primary market data provider

_not yet decided_ <!-- exactly one: alpaca | coinbase -->

## Universe

_not yet decided_
<!-- provider symbols/product IDs AND AlphaInsider stock_ids, e.g.
- Alpaca SPY  → AlphaInsider SPY:ARCX
- Coinbase BTC-USD → AlphaInsider BTC:COINBASE -->

## Signals and decision logic

_not yet decided_ <!-- deterministic rules or LLM engine (model + prompt contract) -->

## Data cadence

_not yet decided_ <!-- polling interval + timeframe, or WebSocket channels;
extra signal sources only if explicitly confirmed -->

## Order style and sizing

_not yet decided_ <!-- discrete new_order vs rebalance_allocations; sizes/percents; leverage ≤ 2.0 -->

## Risk constraints

_not yet decided_ <!-- max position, stops, drawdown kill-switch, open-order handling -->

## Schedule

_not yet decided_ <!-- market hours / 24-7 / custom window -->

## Backtesting

_not yet decided_
<!-- Record exactly one resolved outcome:
- unavailable: why the strategy cannot be historically replayed (do not ask
  the user about backtesting; this does not block the strategy)
- available: user declined
- available: user accepted, with the historical window and the evaluation
  timing derived from the confirmed holding period or exit logic
-->

## Confirmation

- [ ] User explicitly confirmed the complete plan (set `status: confirmed`)
