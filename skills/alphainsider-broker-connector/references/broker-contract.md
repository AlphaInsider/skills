# Broker Contract

Facts the agent must establish about the user's broker and account before the
[rebalance math](rebalance-math.md) can size real orders. Research the broker's
current official documentation and the user's actual account; do not rely on
memory for rules that change.

- Record each fact in `connection.md` under broker facts, with its source and
  date. Mark unknowns and how the connection handles them.
- Recheck facts when the broker rejects an order, behavior changes, or a fact is
  more than a few months old.
- Present the access options you find and let the user choose the direction
  before setting up [credentials](credentials.md).

## Access

- Official API availability, account eligibility, and required approvals.
- Authentication type: API key, OAuth with refresh tokens, or website/app login
  only.
- How sessions are refreshed, how long they last, and what triggers MFA.
- Without an official API: whether the runtime can drive the user's logged-in
  browser session, and the broker's terms for automated access.
- Rate limits and maintenance windows.

## Account

- Accounts the access reaches: main, sub-accounts, and paper or sandbox
  accounts, and whether new sub-accounts can be opened. The user chooses one;
  research the facts below for that account.
- Account type: cash, margin, or portfolio margin; taxable or retirement. Tell
  the user that rebalancing a taxable account realizes gains and losses.
- Current minimum balances and trading restrictions for the account type,
  researched from current rules rather than assumed.
- How to read account value (equity), cash, and positions with signed
  quantities.
- Buying power semantics and the account's maximum leverage, used to derive
  `capacity` and `L_max` (see [leverage](rebalance-math.md#leverage)).
- Short selling availability and borrow limits.
- Settlement timing and limits on trading unsettled funds in cash accounts.
- Sub-accounts: stocks and cryptocurrency must be in separate accounts. If they
  cannot be separated, the user chooses one asset type; holdings of the other
  type count in the account value and close like any unrelated holding. Warn the
  user before confirming scope.

## Instruments

- Supported asset type matches the connection's strategies (stocks or
  cryptocurrency).
- Symbol lookup used to map AlphaInsider stocks; match on `symbol`, `exchange`,
  `security`, and `figi_composite` where available.
- Fractional quantity support, lot size, tick size, and quantity precision.
- Minimum and maximum order size.

## Market data

- Use AlphaInsider quotes (`bid`, `ask`, `last`) and exchange status through the
  [API skill](https://api.alphainsider.com/skill.md).
- Broker quotes are optional; note when they differ materially.
- Trading hours and extended-hours support at the broker.

## Orders

- Supported order types and time-in-force values.
- How to place, cancel, and cancel all open orders.
- How to read order status, fills, and partial fills, and how to tell an accepted
  order from an executed one.
- Any per-batch or initial buying power limit that affects increase orders.
- Per-market leverage settings that must be raised before increasing exposure,
  as on some perpetual futures exchanges.

## Costs

- Commissions and fees per side; use them as `fee` in the
  [reserve](rebalance-math.md#3-broker-buying-power).
- Typical slippage for the account's instruments; use it to choose the
  `slippage` reserve (AlphaInsider bots default to `0.005`).
