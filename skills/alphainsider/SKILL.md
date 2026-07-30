---
name: alphainsider
description: Build, debug, or document integrations with the AlphaInsider trading API, including strategies, subscriptions, orders, positions, allocation rebalancing, bots, webhooks, market data, timelines, billing, withdrawals, and WebSocket streams. Use when Codex needs AlphaInsider endpoint behavior, request examples, authentication rules, helper-managed defaults, the request helper, or reusable REST and WebSocket clients.
---

# AlphaInsider API

Use this skill when working with AlphaInsider REST or WebSocket integrations.

- REST base URL: `https://alphainsider.com/api`
- WebSocket URL: `wss://alphainsider.com/ws`
- Source docs used for this skill: `https://api.alphainsider.com/llms.txt`, `https://api.alphainsider.com/openapi.yaml`, and `https://api.alphainsider.com/asyncapi.yaml`

## Core Workflow

1. Identify the API area and read the matching file in `references/`.
2. For authenticated REST calls, use `scripts/alphainsider_request.py`; do not manually read or inject credentials.
3. Let the helper add the authorization token and any helper-managed default IDs.
4. Check `success` before using `response`; errors use `{ "success": false, "response": "<message>" }`.

For a standalone Python integration, reuse `scripts/runtime/`. Its REST and
WebSocket clients are the canonical runtime source for `$strategy-creator`;
do not duplicate them in another skill.

## Private Credential Boundary

- `ALPHAINSIDER_API_KEY` is a private AlphaInsider credential. Agents must never inspect, print, request, echo, or inline its value.
- Do not run commands intended to reveal the token, such as `env`, `printenv ALPHAINSIDER_API_KEY`, or opening `.env` for credential lookup.
- Do not manually populate `Authorization`, `token`, or `api_token` fields from environment variables or `.env`.
- Use `scripts/alphainsider_request.py` for authenticated REST calls. The helper may read `ALPHAINSIDER_API_KEY`, `ALPHAINSIDER_STRATEGY_ID`, and `ALPHAINSIDER_BOT_ID` from the process environment or `.env` in the invoking directory, inject auth safely, and redact token fields in dry-run output.
- `ALPHAINSIDER_STRATEGY_ID` and `ALPHAINSIDER_BOT_ID` are helper-managed defaults, not secrets like the API key. A user may still provide explicit `strategy_id` or `bot_id` values in a request.

If a required `strategy_id` or `bot_id` is not supplied by the user and the helper/API cannot resolve it from defaults, ask the user for that ID. Do not inspect `.env` to find it.

## Display Rule

AlphaInsider strategy performance, position, order, and trade values are normalized. Before showing strategy values, positions, orders, trades, or performance to a user, read `references/input-multiplier.md`.

- Strategy owners always have an `input_multiplier`; use it for owner positions, orders/trades, performance, and `newOrder` sizing.
- If an owner flow appears to lack `input_multiplier`, refresh the strategy subscription/calculation context before displaying values or sizing orders.
- Subscribers/non-owners use saved or calculated `input_multiplier` when available; if unavailable, label display values as percent derived from `strategy_value` or ask for `input_value` and `input_date`.
- Never silently treat a missing `input_multiplier` as `1`.
- API numeric values commonly arrive as strings; convert before math.
- Open order responses from `getOrders`, `newOrder`, `newOrderAllocations`, `newOrderWebhook`, and `wsOrders` include `order_dependencies` as an array of prerequisite order IDs; `[]` means there are no outstanding prerequisites.

## Request Helper

Use `scripts/alphainsider_request.py` for quick REST calls from a project directory:

```bash
python scripts/alphainsider_request.py GET /getStrategyPerformance \
  --query start_date=2026-01-01T00:00:00Z

python scripts/alphainsider_request.py POST /newOrder \
  --json '{"stock_id":"SPY:ARCX","action":"buy","type":"market","total":"100"}'
```

The helper owns credential/default lookup. Do not read these values directly from the environment or `.env`; run the helper and let it inject auth plus default strategy or bot IDs only for endpoints documented as accepting those IDs.

## References

- Start with `references/api-reference.md` for the endpoint map.
- Use `references/runtime-client.md` for the reusable REST/WebSocket package.
- Use `references/limits.md` for account tiers, endpoint caps, withdrawal minimums, and 429 handling.
- Use `references/input-multiplier.md` for normalized strategy values, position/order display, performance display, and `newOrder` amount/total conversion.
- Use `references/authentication.md` for token verification.
- Use `references/users.md` for profile and notification endpoints.
- Use `references/strategies.md` for strategy discovery, creation, updates, values, and performance.
- Use `references/subscriptions.md` for strategy subscriptions, calculations, account tiers, and account subscription changes.
- Use `references/payments.md` for invoices and payment sources.
- Use `references/withdrawals.md` for balances, payouts, payout fees, income, and Stripe account links.
- Use `references/timelines.md` for posts, previews, likes, and timeline reads.
- Use `references/stocks.md` for stock lookup, search, price history, and exchange status.
- Use `references/trades.md` for positions, orders, max order size, fixed orders, allocation orders, and cancellations.
- Use `references/webhooks.md` for TradingView-style webhook orders.
- Use `references/bots.md` for bot lifecycle, broker keys, allocations, performance, and activities.
- Use `references/websockets.md` for real-time subscriptions and channel payloads.
