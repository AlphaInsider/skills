# Input Multiplier And User-Facing Values

Use this reference before showing AlphaInsider strategy values, positions, orders, trades, or performance to users, and before converting user-entered quantities into `newOrder` requests.

## Contents

- [Core Model](#core-model)
- [Owner Vs Subscriber Context](#owner-vs-subscriber-context)
- [Getting A Multiplier](#getting-a-multiplier)
- [Related Endpoints](#related-endpoints)
- [Strategy Values And Performance](#strategy-values-and-performance)
- [Positions](#positions)
- [Orders](#orders)
- [New Orders](#new-orders)

## Core Model

AlphaInsider strategy fields such as `strategy_value`, position `amount`, position `total`, order `amount`, and order `total` are strategy-normalized values. They are not automatically user dollars or user share counts.

`input_multiplier` converts normalized strategy units into the user's displayed scale:

```text
user_value = normalized_strategy_value * input_multiplier
```

Each strategy/subscription can have its own multiplier. Strategy owners always have an owner `input_multiplier`; subscribers/non-owners may need a saved or calculated multiplier for their own display context. Do not reuse a multiplier across strategies, subscribers, or calculation dates. API numeric values commonly arrive as strings; parse them before doing math.

Prices are already market prices. Do not multiply or divide `price`, `bid`, `ask`, `last`, `stop_price`, slippage, fees, allocation percentages, or raw API responses unless this reference explicitly says to derive a display value.

## Owner Vs Subscriber Context

Strategy owners set the strategy's starting balance with `newStrategy.input_value` and can update it with `updateStrategy.input_value`. AlphaInsider uses that owner starting balance to establish the owner display calculation, so owner-managed positions, orders/trades, performance, and `newOrder` sizing should always use `input_multiplier`.

If an owner workflow appears to lack `input_multiplier`, do not fall back to percent display or assume `1`. Refresh the authenticated strategy subscription/calculation state, then use the owner multiplier before displaying USD/share values or converting user-entered order quantities.

Subscribers/non-owners use their saved calculation from `getStrategySubscriptions` when present. If they do not have a saved calculation, use `getStrategyCalculation` for a supplied `input_value` and `input_date`; use `updateStrategyCalculation` only when persisting that calculation for an authenticated subscription.

Missing-multiplier fallback is only for subscriber/non-owner display, or for workflows where the user explicitly provides normalized strategy units. It is not an owner-management fallback.

## Getting A Multiplier

For strategy owners, resolve the owner `input_multiplier` from the authenticated strategy calculation/subscription context and treat it as required.

For subscribers/non-owners, prefer `input_multiplier` from `getStrategySubscriptions` when the authenticated user is subscribed to the strategy.

Use `getStrategyCalculation` when the user provides an `input_value` and `input_date` and you need to calculate a multiplier for a point in strategy history:

```text
input_multiplier = input_value / strategy_value_at_input_date
```

Use `updateStrategyCalculation` to persist that calculation for an authenticated strategy subscription. Use `deleteStrategyCalculation` only when the user asks to remove the saved calculation.

If a subscriber/non-owner `input_multiplier` is missing, never assume it is `1`. Show percentage or normalized strategy-unit display values, or ask the user for an `input_value` and `input_date` before showing USD/share amounts. For owner flows, refresh the calculation context instead.

## Related Endpoints

- `getStrategySubscriptions`: preferred source for saved `input_multiplier`.
- `getStrategyCalculation`: calculate an `input_multiplier` for a supplied `input_value` and `input_date`.
- `updateStrategyCalculation`: persist the calculated `input_multiplier` for an authenticated subscription.
- `getStrategyValues`: returns normalized `strategy_value`.
- `getStrategyPerformance`: returns normalized performance points.
- `getPositions`: returns normalized position `amount` and `total`.
- `getOrders`: returns normalized open order `amount` and `total`.
- `newOrder`: accepts normalized `amount` or `total`.
- `wsStrategyValue`: streams normalized strategy value updates.
- `wsPositions`: streams normalized position updates.

## Strategy Values And Performance

Current displayed strategy value:

```text
display_value = strategy_value * input_multiplier
```

Performance charts use a baseline value. If the performance series includes the saved `input_date`, use the calculation's `strategy_value` at that date as the baseline for calculated user display. Otherwise use the first strategy value in the selected performance window.

Owners always display strategy performance with `input_multiplier`. Subscribers display dollar gain/loss when they have a saved or calculated multiplier:

```text
dollar_gain_loss = (current_strategy_value - baseline_strategy_value) * input_multiplier
```

Fallback performance display is only for subscribers/non-owners without a saved or calculated multiplier:

```text
percent_gain_loss = ((current_strategy_value - baseline_strategy_value) / baseline_strategy_value) * 100
```

For owner trade markers and timeline trade rows, display normalized trade amounts as user share/crypto amounts with `input_multiplier`. Subscribers use the same display when they have a saved or calculated multiplier:

```text
display_trade_amount = trade_amount * input_multiplier
```

For subscribers/non-owners without a multiplier, display the trade size as a percent of the strategy value at that time:

```text
trade_percent = ((trade_amount * trade_price) / trade_strategy_value) * 100
```

## Positions

Use bid prices for asset/long positions and ask prices for liability/short positions. If quotes are unavailable, fall back to the position's stored `price`.

```text
current_price = amount >= 0 ? bid : ask
position_percent = ((amount * current_price) / strategy_value) * 100
```

Owners always display position amount in user-visible shares/crypto units with `input_multiplier`. Subscribers use the same display when they have a saved or calculated multiplier:

```text
position_amount = amount * input_multiplier
```

Displayed market value can preserve the sign for exposure, or use absolute value for liability magnitude when that is clearer to the user:

```text
position_market_value = amount * current_price * input_multiplier
liability_market_value = abs(amount) * ask * input_multiplier
```

Position gain/loss amount uses normalized position value converted to user scale. Treat `avg_price` as the entry price when a client or integration names it that way; the REST position payload uses `price`.

```text
position_gain_loss_amount = ((amount * current_price) - (amount * avg_price_or_entry_price)) * input_multiplier
```

Position gain/loss percent does not use `input_multiplier`. It is based on normalized value change and should be sign-adjusted for liabilities:

```text
position_gain_loss_percent = (((amount * current_price) - position_total) / position_total) * 100
liability_gain_loss_percent = position_gain_loss_percent * -1
```

## Orders

Open order `amount` and `total` are normalized. Owners always display open orders with `input_multiplier`; subscribers use the same display when they have a saved or calculated multiplier:

```text
display_order_amount = order.amount * input_multiplier
display_order_total = order.total * input_multiplier
```

For subscribers/non-owners without a multiplier, show order size as a strategy percent. If the order has `total`, use it directly; otherwise derive total from `amount * order_price`.

```text
order_percent = (normalized_order_total / strategy_value) * 100
```

## New Orders

`newOrder` receives normalized strategy units. Owner-managed `newOrder` flows must resolve the owner `input_multiplier` before converting user-entered quantities. If the user enters share/crypto quantity or USD quantity in their displayed scale, divide by `input_multiplier` before sending the request.

For share/crypto quantity input:

```text
newOrder.amount = user_quantity / input_multiplier
```

For USD quantity input:

```text
newOrder.total = user_dollars / input_multiplier
```

Send exactly one of `amount` or `total` to `newOrder`. Keep `price` and `stop_price` as market prices; do not convert them with the multiplier.

For owner-managed trades, do not place a user-denominated `newOrder` until the owner multiplier is available. For subscribers/non-owners without a multiplier, do not convert user USD or user share/crypto quantities into `newOrder`; ask the user to set a calculation, or require the user to explicitly provide normalized strategy units.

`newOrderAllocations` uses target percentages and does not use `input_multiplier`.
