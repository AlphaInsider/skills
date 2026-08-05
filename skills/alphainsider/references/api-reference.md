# AlphaInsider API Reference

Source material: AlphaInsider `llms.txt`, focused Markdown pages, OpenAPI, AsyncAPI, agent guides, and limits documentation. For current REST schemas use `https://api.alphainsider.com/openapi.yaml`; for current WebSocket schemas use `https://api.alphainsider.com/asyncapi.yaml`.

## Base URLs

- REST: `https://alphainsider.com/api`
- WebSocket: `wss://alphainsider.com/ws`

## Authentication

Protected REST endpoints use this wire format:

```http
Authorization: <api-token>
```

Do not add a `Bearer` prefix. `verifyToken` uses a body field named `token`; `newOrderWebhook` uses a body field named `api_token`.

## Response Shape

Successful REST responses use `{ "success": true, "response": <data> }`. Failed responses use `{ "success": false, "response": "<message>" }`. Always inspect `success` first.

## Display Values

Read `input-multiplier.md` before displaying strategy values, positions, orders, trades, or performance to users. AlphaInsider returns normalized strategy values; user-facing USD or share/crypto amounts require `input_multiplier`.

Bot broker values and `getMaxOrderSize` limits are already user-facing; do not apply `input_multiplier` to them. Webhook signal actions and percentage allocations also do not use multiplier math.

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
