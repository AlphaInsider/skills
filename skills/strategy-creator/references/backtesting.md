# Portfolio-Valued Backtesting

Read this file in full when a user accepts backtesting for a historically
reconstructable strategy. Generate the simulator inside the strategy workspace;
do not add a generic simulator to this skill.

## Plan the replay

- Permit portfolio valuation only when every selected asset has `peg: USD`.
  A replayable non-USD strategy may keep signal-only analytics, but must state
  that portfolio valuation is unavailable.
- During universe discovery, resolve each AlphaInsider `stock_id` with the
  sibling skill's read-only `getStocks` workflow. Record `security`, `peg`,
  `fee`, `slippage`, and the UTC retrieval time in `docs/plan.md`.
- Parse `fee` and `slippage` as nonnegative decimal fractions. Record an
  invalid or missing value as zero and attach a prominent warning to both the
  plan and every backtest result that uses it.
- After the user accepts a USD portfolio replay and selects its window, ask for
  a positive default starting value in USD. Ask only one decision per turn.

## Expose the command

Keep optional `--start` and `--end`, defaulting to the confirmed window. Add
optional `--initial-value`, defaulting to the confirmed starting value. Reject
non-finite or non-positive values, or a start later than the end. Treat both
bounds as inclusive UTC and use `Decimal`; round only for display.

## Simulate the portfolio

Start the requested window entirely in cash with no positions. Historical
bars before `--start` may warm indicators, but they must not create trades or
affect portfolio value. Replay production decision logic chronologically and
expose no bars after the decision timestamp.

Use the signal bar's close as the unadjusted execution reference. Apply the
snapshotted AlphaInsider costs to every executed quantity:

```text
buy_fill  = close * (1 + slippage)
sell_fill = close * (1 - slippage)
fee_total = abs(quantity * fill_price) * fee
```

Do not cap a slippage-adjusted fill to the candle high or low. Track the
resulting cash, signed quantity, and average cost per asset. Deduct fees on
entries, reductions, closes, and reversals. Treat a reversal as one signed
quantity change and calculate realized P&L for the closed portion before
establishing the new average cost.

Preserve the confirmed order semantics:

- Scale fixed normalized `amount` and `total` values by an input multiplier
  equal to `initial_value / 1`, where `1` is the normalized starting value.
- Apply allocation targets to current pre-trade equity.
- Apply signal actions at the confirmed leverage; when pyramiding is enabled,
  step exposure by `leverage / pyramiding`, cap repeated same-direction alerts
  at full leverage, and start an opposite alert at the first step on that side.
- For a batch rebalance, calculate targets from one pre-trade equity snapshot,
  process reductions before increases, and otherwise retain stable plan order.

Enforce the confirmed position, leverage, drawdown, kill-switch, and
buying-power constraints. Reject an unaffordable or otherwise invalid order,
leave the portfolio unchanged for that order, record the reason, and continue.
Stop the replay and report portfolio depletion if equity reaches zero or less.

Make no AlphaInsider calls during replay. Use only the frozen plan metadata and
do not alter live paper-order slippage. Do not model dividends, corporate
actions, borrow or financing costs, taxes, or costs absent from the snapshot.
State these omissions and optimistic same-bar-close execution in every result.

## Report results

Retain signal counts, directional hit rate, forward returns, timestamped
records, and unevaluable trailing signals. Add:

- starting value;
- ending mark-to-market equity at the final close, with dollar and percent P&L;
- hypothetical liquidation equity after adverse slippage and fees at the
  final close, with dollar and percent P&L;
- realized and unrealized P&L;
- fees and slippage impact from executed fills, with hypothetical liquidation
  costs identified separately;
- rejected orders, portfolio-depletion status, cost-default warnings, and
  modeling limitations.

Present mark-to-market and liquidation results equally; do not label either as
the headline result. Calculate hypothetical liquidation without mutating the
portfolio or adding a synthetic trade to the timestamped record. Calculate
gross realized and unrealized P&L from slippage-adjusted fills, report fees
separately, and reconcile `realized + unrealized - fees` to mark-to-market P&L.
Slippage is embedded in fills; never subtract its reported impact again.

## Test generated code

Add offline cases for profitable and losing longs and shorts, closes and
reversals, normalized-size scaling, the selected allocation or signal sizing,
fees and slippage, rejected orders, open-position valuation, zeroed missing
costs and warnings, portfolio depletion, date bounds, and initial-value CLI
defaults and overrides. Tests must make no AlphaInsider calls and submit no
paper orders.
