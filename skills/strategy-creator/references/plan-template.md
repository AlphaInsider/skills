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
<!-- Record provider symbols/product IDs and an AlphaInsider metadata snapshot
for every instrument: stock_id, security, peg, fee, slippage, and retrieved_at
in UTC. Every instrument's security must equal the provider class: stock for
alpaca, cryptocurrency for coinbase. Record invalid or missing fee/slippage as
0 with a warning, e.g.
- Alpaca SPY → AlphaInsider SPY:ARCX; peg USD; fee 0; slippage 0.002;
  retrieved_at 2026-07-31T12:00:00Z
- Coinbase BTC-USD → AlphaInsider BTC:COINBASE; peg USD; fee 0.0025;
  slippage 0.002; retrieved_at 2026-07-31T12:00:00Z -->

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
- for an accepted USD portfolio replay: positive default starting value in
  USD; optional `--initial-value` override; the frozen per-asset fee/slippage
  snapshot and any zero-default warnings; signal-close execution; and the
  required mark-to-market and hypothetical-liquidation results
- for an accepted non-USD replay: signal-only, with portfolio valuation marked
  unavailable
-->

## Confirmation

- [ ] User explicitly confirmed the complete plan (set `status: confirmed`)
