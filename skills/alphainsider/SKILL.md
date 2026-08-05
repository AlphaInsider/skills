---
name: alphainsider
description: Navigate, use, debug, or document the AlphaInsider trading API, including strategies, subscriptions, normalized trading calculations, orders, positions, allocation rebalancing, bots, broker keys, webhooks, market data, timelines, billing, withdrawals, and WebSocket streams. Use for endpoint behavior, request examples, authentication rules, helper-managed defaults, thin REST requests, or WebSocket connections.
---

# AlphaInsider API

Use this skill when working with AlphaInsider REST or WebSocket integrations.

- REST base URL: `https://alphainsider.com/api`
- WebSocket URL: `wss://alphainsider.com/ws`
- Hosted docs: `https://api.alphainsider.com`
- Docs index: `https://api.alphainsider.com/llms.txt`; full-corpus fallback: `https://api.alphainsider.com/llms-full.txt`
- REST source of truth: `https://api.alphainsider.com/openapi.yaml`
- WebSocket source of truth: `https://api.alphainsider.com/asyncapi.yaml`

## Core Workflow

1. Start with `references/api-reference.md`, identify the API area, and read the matching focused reference.
2. When current behavior or an unlisted detail matters, use `llms.txt` to find the focused Markdown page, then verify REST details in OpenAPI or WebSocket details in AsyncAPI. Use `llms-full.txt` only as a fallback.
3. Construct endpoint paths, parameters, bodies, and channel names from the references; the Python scripts are generic transports, not an endpoint SDK.
4. For REST calls, use `scripts/alphainsider_request.py`; for WebSocket connections, use `scripts/alphainsider_stream.py`. Do not manually read or inject credentials.
5. Let the helpers own authentication and helper-managed default IDs. Use the deterministic calculation functions only for the normalized-value formulas they cover.

For a standalone Python integration, copy and import the request helper. Copy
the stream helper only when WebSocket events are required. Add small local
endpoint functions only for the integration's actual needs.

## Private Credential Boundary

- `ALPHAINSIDER_API_KEY` is a private AlphaInsider credential. Agents must never inspect, print, request, echo, or inline its value.
- Do not run commands intended to reveal the token, such as `env`, `printenv ALPHAINSIDER_API_KEY`, or opening `.env` for credential lookup.
- Do not manually populate `Authorization`, `token`, or `api_token` fields from environment variables or `.env`.
- Use `scripts/alphainsider_request.py` for REST calls. The helper reads only `ALPHAINSIDER_API_KEY`, `ALPHAINSIDER_STRATEGY_ID`, and `ALPHAINSIDER_BOT_ID` from the process environment or `.env` in the invoking directory, injects auth safely, and redacts credentials from dry runs, responses, and errors.
- Use `scripts/alphainsider_stream.py` for authenticated WebSocket subscriptions. It reads `ALPHAINSIDER_API_KEY` privately, never accepts it as a command-line argument, and redacts credentials from events and errors.
- The documented importable interfaces never return the API key or arbitrary environment contents. They still transmit the key to AlphaInsider as required; this boundary prevents accidental output exposure, not hostile same-process inspection.
- `ALPHAINSIDER_STRATEGY_ID` and `ALPHAINSIDER_BOT_ID` are helper-managed defaults, not secrets like the API key. A user may provide, request, and display explicit `strategy_id`, `bot_id`, or other non-secret configuration values.
- Never dump the process environment or complete `.env`. Use non-secret values only when the user provides them or explicitly asks for them.
- Broker keys and secrets passed to `newBot` or `updateBotBrokerKeys` are private credentials. Never print, log, commit, quote, or summarize them; send only the fields required by the selected broker.

If a required `strategy_id` or `bot_id` is not supplied by the user and the helper/API cannot resolve it from defaults, ask the user for that ID. Do not inspect `.env` to find it.

## Display Rule

AlphaInsider strategy performance, position, order, and trade values are normalized. Before showing strategy values, positions, orders, trades, or performance to a user, read `references/input-multiplier.md`.

- Strategy owners always have an `input_multiplier`; use it for owner positions, orders/trades, performance, and `newOrder` sizing.
- If an owner flow appears to lack `input_multiplier`, refresh the strategy subscription/calculation context before displaying values or sizing orders.
- Subscribers/non-owners use saved or calculated `input_multiplier` when available; if unavailable, label display values as percent derived from `strategy_value` or ask for `input_value` and `input_date`.
- Never silently treat a missing `input_multiplier` as `1`.
- API numeric values commonly arrive as strings; convert before math and preserve precision when sending normalized order values.
- `getMaxOrderSize` returns user-facing limits; do not apply `input_multiplier` to them. Use it before large, leveraged, or otherwise risky fixed orders.
- `newOrderWebhook` uses signal-style actions and no `input_multiplier` math. Alerts go fully in or out by default; `pyramiding` enables stepped entries.
- Open order responses from `getOrders`, `newOrder`, `newOrderAllocations`, `newOrderWebhook`, and `wsOrders` include `order_dependencies` as an array of prerequisite order IDs; `[]` means there are no outstanding prerequisites.

## Thin Helpers

Use `scripts/alphainsider_request.py` for REST calls from a project directory:

```bash
python scripts/alphainsider_request.py GET /getStrategyPerformance \
  --query start_date=2026-01-01T00:00:00Z

python scripts/alphainsider_request.py POST /newOrder \
  --json '{"stock_id":"SPY:ARCX","action":"buy","type":"market","total":"100"}'
```

It is also importable as `request(method, path, query=..., body=...)`. Use
`--output` for binary responses such as invoice PDFs.

Use `scripts/alphainsider_stream.py` with one or more reference-defined channels:

```bash
python scripts/alphainsider_stream.py \
  --channel "wsStrategyValue:<STRATEGY_ID>" \
  --channel "wsOrders:<STRATEGY_ID>"
```

The helpers own credential/default lookup. Do not read these values directly
from the environment or `.env`. Their public Python interfaces expose only
requests, streams, and deterministic calculations, not generic environment
readers. They deliberately do not model individual endpoints, choose channels,
retry requests, or implement trading policy.

## References

- Start with `references/api-reference.md` for the endpoint map.
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
- Use `references/trades.md` for positions, orders, user-facing max order size, fixed orders, allocation orders, and cancellations.
- Use `references/webhooks.md` for TradingView-style webhook orders, stepped entries with `pyramiding`, and webhook slippage.
- Use `references/bots.md` for bot lifecycle, private broker keys, full-replacement allocations, real broker values, performance, and activities.
- Use `references/websockets.md` for real-time subscriptions and channel payloads.
