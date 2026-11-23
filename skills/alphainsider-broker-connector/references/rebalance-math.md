# Rebalance Math

How AlphaInsider bots size a broker account across strategy allocations. Use it
as the model of where the account should be; fill in gaps with the
[broker facts](broker-contract.md) you research.

- Compute in your own throwaway code with decimal arithmetic (for example Python
  `Decimal` from strings), never mentally or with binary floats.
- Strategy values and positions are normalized. These formulas use only ratios
  of normalized values within the same strategy, so no `input_multiplier`
  conversion applies. Broker values, quotes, and percentages are real values.
- Each example is independent; `D` is `Decimal`.

## Inputs

| Symbol | Meaning | Source |
| --- | --- | --- |
| `p_i` | allocation weight saved at the last baseline | `connection.db` |
| `V0_i` | strategy value saved at the last baseline | `connection.db` |
| `V_i` | current strategy value | `getStrategyValues` |
| `a_ik` | signed normalized position amount of symbol `k` in strategy `i`, excluding cash | `getPositions` |
| `L` | bot leverage, a whole number from 1 to `L_max` | `plan.md` |
| `value` | real broker account value (equity) | broker |
| `capacity` | most gross position value the account can carry | broker |
| `fee`, `slippage` | per-side fee rate and slippage reserve rate | `plan.md` |

## Leverage

Every AlphaInsider strategy is a 2x margin account, so each strategy sizes its
positions against `2 * V_i`. A bot with leverage `L` gives each allocation a
sleeve holding `L / 2` times its strategy's exposure.

```text
L_max = floor(capacity / value)    # the account's maximum leverage
1 <= L <= L_max                    # whole number
```

- `L = 1`: cash account; each sleeve holds half its strategy's exposure, so a
  strategy at 1x leaves half its sleeve in cash.
- `L = 2`: matches AlphaInsider's 2x strategies; sleeves mirror them 1:1.
- `L > 2`: more leverage; a 2x strategy at `L = 10` is 10x.
- Sleeve gains and losses are `L / 2` times the strategy's. Recommend
  `L = min(2, L_max)` and explain this when the user chooses.
- Price moves can take an existing strategy above 2x exposure. In that case
  use its current gross exposure in [the target calculation](#2-exposure-per-symbol).
  Check the resulting orders against the broker's current limits.

`capacity` includes current positions and uses overnight, not intraday, limits:
current gross position value plus the broker's reported remaining buying power,
or equity times the account type's documented maximum leverage. On perpetual
futures, a market's own maximum leverage can lower it when targets concentrate
in that market. Re-read it every run; if `L` exceeds the current `L_max`, the
cap in [section 3](#3-broker-buying-power) scales every sleeve down, so warn the
user and propose a lower `L`.

## 1. Drift weights

Each allocation's weight follows its strategy's performance since the baseline.
Weights never return to the original targets on their own. Between rebalances
each sleeve holds a fixed `L / 2` copy of its strategy's positions, so these
weights equal each sleeve's actual share of the account. At `L != 2`, a
rebalance also adjusts sleeves whose strategies did not trade, restoring their
leverage.

```text
cash      = max(1 - sum(p), 0)
adj_i     = max(p_i * (1 + L / 2 * (V_i / V0_i - 1)), 0)    # 0 if V_i <= 0 or V0_i <= 0
w_i       = adj_i / (cash + sum(adj))                        # 0 if the denominator is 0
```

A new allocation without a baseline uses `V0_i = V_i`. Display current weights
rounded to `0.0001`; keep full precision in calculations.

```python
# example: drift
from decimal import Decimal as D, localcontext
with localcontext() as context:
    context.prec = 34
    p, V0, V, L = [D('0.6'), D('0.3')], [D('1'), D('1')], [D('1.1'), D('0.9')], D('2')
    cash = max(D('1') - sum(p), D('0'))
    adj = [max(pi * (1 + L / 2 * (v / v0 - 1)), D('0')) for pi, v, v0 in zip(p, V, V0)]
    w = [a / (cash + sum(adj)) for a in adj]
    weights = [x.quantize(D('0.0001')) for x in w]
# Expected weights: [Decimal('0.6408'), Decimal('0.2621')]; with L = 4: 0.6792, 0.2264
```

## 2. Exposure per symbol

Each strategy's positions become units per dollar of buying power, then sum
across strategies. Overlapping strategies net into one target per symbol.

```text
gross_i = sum_k(abs(a_ik) * price_ik)        # bid for longs, ask for shorts
sbp_i   = max(2 * V_i, gross_i)              # strategy buying power
f_k     = sum_i(w_i * a_ik / sbp_i)
```

Positions that cannot be traded (see [section 5](#5-execution-guidance)) stay in
`gross_i`, so their share of the allocation remains in cash.
Skip zero-weight allocations. If an active allocation's inputs are missing or
its buying power cannot be determined, pause before placing orders.

## 3. Broker buying power

```text
B = min(value * L, capacity) * (1 - 4 * fee - 2 * slippage)
```

With `L <= L_max`, `B = value * L * (1 - 4 * fee - 2 * slippage)`; the cap only
protects the account when capacity falls. The reserve leaves room for fees on both sides and for slippage, so orders fit
the account. Deposits and withdrawals change `value` and flow into every
allocation at the next rebalance.

## 4. Targets and orders

```text
T_k     = f_k * B              # signed target units; negative is short
delta_k = T_k - held_k         # held_k: signed broker units now
```

- Every held symbol without a target gets `T_k = 0` and closes, including
  holdings unrelated to the strategies.
- When `T_k` and `held_k` have opposite signs, close the position first, then
  open the new side.
- Order types: `close`, `sell_long`, or `buy_short` decrease exposure;
  `buy_long` or `sell_short` increase it.
- Estimate order cost at `ask * (1 + slippage)` for buys and
  `bid * (1 - slippage)` for sells.

```python
# example: targets
from decimal import Decimal as D, localcontext
with localcontext() as context:
    context.prec = 34
    value, capacity, L, fee, slippage = D('10000'), D('20000'), D('2'), D('0'), D('0.005')
    B = min(value * L, capacity) * (1 - 4 * fee - 2 * slippage)
    # Strategy A: w 0.5, V 2, long AAPL 0.005 at bid 200 (50% long), cash 1.
    f_aapl = D('0.5') * D('0.005') / max(2 * D('2'), D('0.005') * D('200'))
    # Strategy B: w 0.25, V 1, short TSLA -0.002 at ask 250 (50% short), cash 1.5.
    f_tsla = D('0.25') * D('-0.002') / max(2 * D('1'), D('0.002') * D('250'))
    t_aapl, t_tsla = f_aapl * B, f_tsla * B
    # Broker holds 5 AAPL, 3 TSLA, 10 MSFT.
    orders = [('buy_long', 'AAPL', t_aapl - 5), ('close', 'TSLA', D('3')),
              ('sell_short', 'TSLA', abs(t_tsla)), ('close', 'MSFT', D('10'))]
    # Same strategies in a cash account (capacity 10,000, L 1):
    t_aapl_cash = f_aapl * min(value * 1, D('10000')) * (1 - 4 * fee - 2 * slippage)
# Expected B: 19800; t_aapl: 12.375 (2,475 at 200 = 0.5 * 0.5 * 10,000 * 0.99)
# Expected t_tsla: -4.95; orders: buy 7.375 AAPL, close 3 TSLA, short 4.95 TSLA, close 10 MSFT
# Expected t_aapl_cash: 6.1875 (half of t_aapl)
```

## 5. Execution guidance

Adapt these to the broker's real limits; they are not fixed formulas.

- Skip increase and partial-decrease orders below
  `max(broker minimum order, 0.0001 * value)`; always allow closes.
- Split orders above the broker's maximum order size.
- Place all decreases first, then re-read capacity and place increases. If the
  broker limits buying power per batch, place increases in batches.
- Leave exposure the account cannot hold in cash and report it after the run:
  - symbols the broker does not carry or that cannot be mapped
  - shorts in an account that cannot short
  - fractional remainders on whole-unit brokers (round targets toward zero)
  - orders below the broker minimum

## Baselines

- After a successful rebalance, read strategy values again, recompute `w_i`
  from the previous baseline with them, then save `p_i = w_i` and `V0_i = V_i`
  for every allocation. This records the values at that moment, as AlphaInsider
  does. If `V_i <= 0`, clear `V0_i`.
- After a failed run, keep the previous baseline.
- An allocation or leverage change replaces every `p_i` with the new targets,
  sets `V0_i = V_i`, and triggers a rebalance. Unchanged allocations keep their
  current drifted weight.
- Targets are fractions in `0.0001` increments with `sum(p) <= 1`. Convert dollar
  targets with `round(dollars / value, 4)`.
