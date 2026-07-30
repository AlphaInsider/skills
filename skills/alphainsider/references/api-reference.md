# AlphaInsider API Reference

Source material: AlphaInsider `llms.txt`, OpenAPI, AsyncAPI, and limits documentation.

## Base URLs

- REST: `https://alphainsider.com/api`
- WebSocket: `wss://alphainsider.com/ws`

## Authentication

Protected REST endpoints use this wire format:

```http
Authorization: <api-token>
```

Do not add a `Bearer` prefix. `verifyToken` uses a body field named `token`; `newOrderWebhook` uses a body field named `api_token`.

Agents should not manually read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should not manually populate `Authorization`, `token`, or `api_token`. Use `scripts/alphainsider_request.py` for REST calls so the helper can inject credentials privately.

## Request Helper Configuration

- `ALPHAINSIDER_API_KEY`: private token used by `scripts/alphainsider_request.py` for authenticated requests.
- `ALPHAINSIDER_STRATEGY_ID`: optional helper default for endpoints that accept `strategy_id` or `strategy_id[]`.
- `ALPHAINSIDER_BOT_ID`: optional helper default for endpoints that accept `bot_id` or `bot_id[]`.

## Response Shape

Successful REST responses use `{ "success": true, "response": <data> }`. Failed responses use `{ "success": false, "response": "<message>" }`. Always inspect `success` first.

## Display Values

Read `input-multiplier.md` before displaying strategy values, positions, orders, trades, or performance to users. AlphaInsider returns normalized strategy values; user-facing USD or share/crypto amounts require `input_multiplier`.

## Endpoint Groups

| Group | Reference | Endpoints |
| --- | --- | --- |
| Authentication | `authentication.md` | `verifyToken` |
| Users | `users.md` | `getUsers`, `getUserInfo`, `updateUserInfo`, `updateUserNotifications` |
| Strategies | `strategies.md` | `getStrategies`, `getStrategyValues`, `getUserStrategies`, `getStrategyPerformance`, `getRecommendedStrategies`, `searchStrategies`, `newStrategy`, `updateStrategy`, `updateStrategyPrice`, `deleteStrategy` |
| Subscriptions | `subscriptions.md` | `getStrategySubscriptions`, `newStrategySubscription`, `deleteStrategySubscription`, `updateStrategySubscriptionNotifications`, `getStrategyCalculation`, `updateStrategyCalculation`, `deleteStrategyCalculation`, `getAccountTiers`, `getAccountSubscription`, `updateAccountSubscription` |
| Payments | `payments.md` | `getPaymentSources`, `getUpcomingInvoice`, `getInvoices`, `getInvoicePdf`, `retryInvoice`, `getUpcomingInvoiceItems`, `getInvoiceItems` |
| Withdrawals | `withdrawals.md` | `getUserBalance`, `getPayouts`, `newPayout`, `getPayoutFees`, `getIncome`, `getStripeAccountLink` |
| Timelines | `timelines.md` | `getTimelines`, `getStrategyTimelines`, `newPost`, `previewPost`, `deletePost`, `like`, `unlike` |
| Stocks | `stocks.md` | `getStocks`, `getAllStocks`, `getStockPriceHistory`, `searchStocks`, `getExchangeStatus` |
| Trades | `trades.md` | `getPositions`, `getOrders`, `getMaxOrderSize`, `newOrder`, `newOrderAllocations`, `deleteOrder` |
| Webhooks | `webhooks.md` | `newOrderWebhook` |
| Bots | `bots.md` | `getBots`, `getBotInfo`, `newBot`, `updateBotSettings`, `updateBotBrokerKeys`, `updateBotNotifications`, `deleteBot`, `startBot`, `stopBot`, `resetBot`, `getBotPerformance`, `resetBotPerformance`, `getBotAllocations`, `updateBotAllocations`, `getBotActivities` |
| Limits | `limits.md` | `new_order`, `new_post`, `like`, `getAllStocks`, account tier limits, withdrawal minimums, 429 handling |
| Input Multiplier | `input-multiplier.md` | Display and order-conversion rules for `getStrategySubscriptions`, `getStrategyCalculation`, `updateStrategyCalculation`, `getStrategyValues`, `getStrategyPerformance`, `getPositions`, `getOrders`, `newOrder`, `wsStrategyValue`, `wsPositions`, and timeline trade data |
| WebSockets | `websockets.md` | `ping`, `pingResponse`, `subscribe`, `subscribeResponse`, `error`, `wsStockPrice`, `wsStrategyValue`, `wsOrders`, `wsPositions`, `wsTimelines`, `wsBotStatus`, `wsBotAllocations`, `wsBotActivities` |

## Stock Identifiers

`stock_id` accepts either an internal AlphaInsider stock ID or `SYMBOL:EXCHANGE`, such as `SPY:ARCX`, `AAPL:XNAS`, or `ETH-USD:COINBASE`.

Prefer `searchStocks` for discovery. Use `getAllStocks` sparingly because the docs mark it as limited to 20 requests per hour.
