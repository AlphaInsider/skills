# Backtesting

This file owns historical feasibility, replay design, execution, and results.
Read **Feasibility** after strategy agreement and before asking whether to
backtest. Read the remaining sections only after the user accepts a backtest.
A backtest never authorizes a strategy change or submits an AlphaInsider order.

## Feasibility

Confirm that each decision can be reconstructed as it was known at the time.
Require:

- historical signal inputs with usable timestamps;
- the historical instrument universe for dynamic selection;
- delisted and failed instruments when they were eligible;
- the applicable market calendar and decision timing;
- a credible price, fee, slippage, latency, and fill model; and
- no use of future revisions, future constituents, or today's survivors.

For an agent-led decision, determine whether the historical prompt context and
permitted evidence can be reconstructed. Record model or reasoning differences.
Do not pretend a deterministic replay is exact when the live agent has
discretion.

Research current provider documentation. Use AlphaInsider price history only
when its actual coverage and granularity fit the plan. Use a credible external
source when required. If no defensible replay exists, mark the backtest
unavailable and explain why. Return that result to the interview; it owns the
next transition.

## Plan the replay

Ask only material choices:

- test dates and any out-of-sample period;
- starting paper value and maximum leverage;
- decision and execution timestamps;
- fill, fee, slippage, delay, and missing-data assumptions;
- an appropriate passive benchmark; and
- results that will make the test easy to understand.

Performance goals can guide interpretation but are never a completion or
runtime-health requirement. Define correctness checks for strategy logic and
data timing. Do not tune rules, thresholds, the test window, or the benchmark
after seeing results unless the user explicitly returns the strategy plan to
Draft and agrees to a revision.

## Build and run

Reuse the production decision logic or a shared pure decision module. Keep the
backtest entry point unable to call AlphaInsider ordering endpoints. Mock all
external trading actions.

Replay in chronological order. Persist:

- source and dataset identity;
- data retrieval and as-of times;
- code revision or content fingerprint;
- assumptions and known differences from forward operation;
- exact command and random seed when applicable; and
- results and generated artifact paths.

Use a simple portfolio replay only when the fill and accounting assumptions
are credible. A signal-quality analysis is better than false portfolio
precision.

## Present results

Show an easy-to-read summary and, when applicable:

- equity curve with the benchmark;
- drawdown chart, where drawdown is the fall from a prior high;
- returns by period;
- total and annualized return for a suitable window;
- maximum drawdown, volatility, and a risk-adjusted measure;
- trade count, win rate, turnover, fees, and exposure; and
- important assumptions and data limits.

State whether the implementation followed `plan.md`. Separate that finding
from profitability. Poor returns do not mean the implementation failed.

Record the results in `plan.md` and store detailed reports under `backtest/`.
Set **Highest completed outcome** to Backtest after a valid replay. Return the
results to `interview.md`, which owns the result decision and next transition.
