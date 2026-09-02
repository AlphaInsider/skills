# Backtesting

This file owns the check for whether a reliable backtest is possible, backtest
design, execution, and results. Read **Can this strategy be backtested
reliably?** after strategy agreement and before asking whether to backtest.
Read the remaining sections only after the user accepts a backtest. A backtest
never authorizes a strategy change or submits an AlphaInsider order.

## Can this strategy be backtested reliably?

Confirm that each decision can be recreated from information available at that
time. Require:

- historical signal inputs with usable timestamps;
- the assets that were eligible on each past date for dynamic selection;
- assets that later stopped trading or failed, when they were eligible;
- the applicable market calendar and decision timing;
- credible assumptions for prices, fees, execution delay, order fills, and the
  estimated price difference before a fill (slippage); and
- no use of later revisions, members added to an index later, or only assets
  that still exist today.

For an agent-led decision, determine whether the historical prompt context and
permitted evidence can be recreated. Record model or reasoning differences. Do
not claim that a fixed code backtest exactly represents decisions made by the
scheduled AI.

Research current provider documentation. Use AlphaInsider price history only
when it covers the dates and level of detail the plan needs. Use a credible
external source when required. If no reliable backtest is possible, mark the
backtest unavailable and explain why. Return that result to the interview; it
owns the next transition.

## Plan the backtest

Ask only about choices that can change the test:

- test dates and any final test period kept separate until the strategy is set;
- simulated starting value and maximum leverage;
- decision and execution timestamps;
- order-fill, fee, slippage, delay, and missing-data assumptions;
- an appropriate comparison investment (benchmark); and
- results that will make the test easy to understand.

Performance goals can guide interpretation but are never a completion or
strategy-run health requirement. Define correctness checks for strategy logic
and data timing. Do not tune rules, thresholds, the test window, or the
benchmark after seeing results unless the user explicitly returns the strategy
plan to Draft and agrees to a revision.

## Build and run

Reuse the production decision logic or a shared pure decision module. Keep the
backtest entry point unable to call AlphaInsider ordering endpoints. Mock all
external trading actions.

Process historical data in chronological order. Persist:

- source and dataset identity;
- data retrieval and cutoff times;
- code revision or content fingerprint;
- assumptions and known differences from scheduled strategy runs;
- exact command and random seed when applicable; and
- results and generated artifact paths.

Use a simple portfolio backtest only when the fill and accounting assumptions
are credible. A signal-quality analysis is better than false portfolio
precision.

## Present results

Lead with a plain conclusion that says whether the backtest followed the agreed
strategy. Refer to the complete design as the strategy, not as a rule. State
that results do not guarantee future performance.

Show the main comparison in a compact, valid Markdown table with a header and
separator row. Do not emit empty chart placeholders, broken tables, or
excessive blank lines. Define each standard financial term the first time it
appears. Include, when applicable:

- equity curve with the benchmark;
- drawdown chart, where drawdown is the fall from a prior high;
- returns by period;
- total and annualized return for a suitable window;
- maximum drawdown, volatility, and a risk-adjusted return measure;
- trade count, win rate, trading frequency or turnover, fees, and time invested
  or exposure; and
- important assumptions and data limits.

Embed charts only when the interface can render them. Otherwise, provide named
links to the chart files. End with a direct link to the detailed report.

State whether the backtest followed `plan.md`. Separate that finding from
profitability. Poor returns do not mean the backtest failed.

Record the results in `plan.md` and store detailed reports under `backtest/`.
Set **Highest completed outcome** to Backtest after a valid backtest. Return the
results to `interview.md`, which owns the result decision and next transition.
