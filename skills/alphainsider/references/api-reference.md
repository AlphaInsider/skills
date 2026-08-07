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

Follow the link for the exact operation or WebSocket message. Read only that
section plus the domain guidance before its first endpoint section.

| Group | Reference | Endpoints |
| --- | --- | --- |
| Authentication | [`authentication.md`](authentication.md) | [`verifyToken`](authentication.md#verifytoken---post-verifytoken) |
| Users | [`users.md`](users.md) | [`getUsers`](users.md#getusers---get-getusers), [`getUserInfo`](users.md#getuserinfo---get-getuserinfo), [`updateUserInfo`](users.md#updateuserinfo---post-updateuserinfo), [`updateUserNotifications`](users.md#updateusernotifications---post-updateusernotifications) |
| Strategies | [`strategies.md`](strategies.md) | [`getStrategies`](strategies.md#getstrategies---get-getstrategies), [`getStrategyValues`](strategies.md#getstrategyvalues---get-getstrategyvalues), [`getUserStrategies`](strategies.md#getuserstrategies---get-getuserstrategies), [`getStrategyPerformance`](strategies.md#getstrategyperformance---get-getstrategyperformance), [`getRecommendedStrategies`](strategies.md#getrecommendedstrategies---get-getrecommendedstrategies), [`searchStrategies`](strategies.md#searchstrategies---post-searchstrategies), [`newStrategy`](strategies.md#newstrategy---post-newstrategy), [`updateStrategy`](strategies.md#updatestrategy---post-updatestrategy), [`updateStrategyPrice`](strategies.md#updatestrategyprice---post-updatestrategyprice), [`deleteStrategy`](strategies.md#deletestrategy---post-deletestrategy) |
| Subscriptions | [`subscriptions.md`](subscriptions.md) | [`getStrategySubscriptions`](subscriptions.md#getstrategysubscriptions---get-getstrategysubscriptions), [`newStrategySubscription`](subscriptions.md#newstrategysubscription---post-newstrategysubscription), [`deleteStrategySubscription`](subscriptions.md#deletestrategysubscription---post-deletestrategysubscription), [`updateStrategySubscriptionNotifications`](subscriptions.md#updatestrategysubscriptionnotifications---post-updatestrategysubscriptionnotifications), [`getStrategyCalculation`](subscriptions.md#getstrategycalculation---get-getstrategycalculation), [`updateStrategyCalculation`](subscriptions.md#updatestrategycalculation---post-updatestrategycalculation), [`deleteStrategyCalculation`](subscriptions.md#deletestrategycalculation---post-deletestrategycalculation), [`getAccountTiers`](subscriptions.md#getaccounttiers---get-getaccounttiers), [`getAccountSubscription`](subscriptions.md#getaccountsubscription---get-getaccountsubscription), [`updateAccountSubscription`](subscriptions.md#updateaccountsubscription---post-updateaccountsubscription) |
| Payments | [`payments.md`](payments.md) | [`getPaymentSources`](payments.md#getpaymentsources---get-getpaymentsources), [`getUpcomingInvoice`](payments.md#getupcominginvoice---get-getupcominginvoice), [`getInvoices`](payments.md#getinvoices---get-getinvoices), [`getInvoicePdf`](payments.md#getinvoicepdf---get-getinvoicepdf), [`retryInvoice`](payments.md#retryinvoice---post-retryinvoice), [`getUpcomingInvoiceItems`](payments.md#getupcominginvoiceitems---get-getupcominginvoiceitems), [`getInvoiceItems`](payments.md#getinvoiceitems---get-getinvoiceitems) |
| Withdrawals | [`withdrawals.md`](withdrawals.md) | [`getUserBalance`](withdrawals.md#getuserbalance---get-getuserbalance), [`getPayouts`](withdrawals.md#getpayouts---get-getpayouts), [`newPayout`](withdrawals.md#newpayout---post-newpayout), [`getPayoutFees`](withdrawals.md#getpayoutfees---get-getpayoutfees), [`getIncome`](withdrawals.md#getincome---get-getincome), [`getStripeAccountLink`](withdrawals.md#getstripeaccountlink---get-getstripeaccountlink) |
| Timelines | [`timelines.md`](timelines.md) | [`getTimelines`](timelines.md#gettimelines---get-gettimelines), [`getStrategyTimelines`](timelines.md#getstrategytimelines---get-getstrategytimelines), [`newPost`](timelines.md#newpost---post-newpost), [`previewPost`](timelines.md#previewpost---post-previewpost), [`deletePost`](timelines.md#deletepost---post-deletepost), [`like`](timelines.md#like---post-like), [`unlike`](timelines.md#unlike---post-unlike) |
| Stocks | [`stocks.md`](stocks.md) | [`getStocks`](stocks.md#getstocks---get-getstocks), [`getAllStocks`](stocks.md#getallstocks---get-getallstocks), [`getStockPriceHistory`](stocks.md#getstockpricehistory---get-getstockpricehistory), [`searchStocks`](stocks.md#searchstocks---post-searchstocks), [`getExchangeStatus`](stocks.md#getexchangestatus---get-getexchangestatus) |
| Trades | [`trades.md`](trades.md) | [`getPositions`](trades.md#getpositions---get-getpositions), [`getOrders`](trades.md#getorders---get-getorders), [`getMaxOrderSize`](trades.md#getmaxordersize---get-getmaxordersize), [`newOrder`](trades.md#neworder---post-neworder), [`newOrderAllocations`](trades.md#neworderallocations---post-neworderallocations), [`deleteOrder`](trades.md#deleteorder---post-deleteorder) |
| Webhooks | [`webhooks.md`](webhooks.md) | [`newOrderWebhook`](webhooks.md#neworderwebhook---post-neworderwebhook) |
| Bots | [`bots.md`](bots.md) | [`getBots`](bots.md#getbots---get-getbots), [`getBotInfo`](bots.md#getbotinfo---get-getbotinfo), [`newBot`](bots.md#newbot---post-newbot), [`updateBotSettings`](bots.md#updatebotsettings---post-updatebotsettings), [`updateBotBrokerKeys`](bots.md#updatebotbrokerkeys---post-updatebotbrokerkeys), [`updateBotNotifications`](bots.md#updatebotnotifications---post-updatebotnotifications), [`deleteBot`](bots.md#deletebot---post-deletebot), [`startBot`](bots.md#startbot---post-startbot), [`stopBot`](bots.md#stopbot---post-stopbot), [`resetBot`](bots.md#resetbot---post-resetbot), [`getBotPerformance`](bots.md#getbotperformance---get-getbotperformance), [`resetBotPerformance`](bots.md#resetbotperformance---post-resetbotperformance), [`getBotAllocations`](bots.md#getbotallocations---get-getbotallocations), [`updateBotAllocations`](bots.md#updatebotallocations---post-updatebotallocations), [`getBotActivities`](bots.md#getbotactivities---get-getbotactivities) |
| Limits | `limits.md` | `new_order`, `new_post`, `like`, `getAllStocks`, account tier limits, withdrawal minimums, 429 handling |
| Input Multiplier | `input-multiplier.md` | Display and order-conversion rules for `getStrategySubscriptions`, `getStrategyCalculation`, `updateStrategyCalculation`, `getStrategyValues`, `getStrategyPerformance`, `getPositions`, `getOrders`, `newOrder`, `wsStrategyValue`, `wsPositions`, and timeline trade data |
| WebSockets | [`websockets.md`](websockets.md) | [`ping`](websockets.md#ping---ping), [`pingResponse`](websockets.md#pingresponse---ping-response), [`subscribe`](websockets.md#subscribe---subscribe), [`subscribeResponse`](websockets.md#subscriberesponse---subscribe-response), [`error`](websockets.md#error---error-response), [`wsStockPrice`](websockets.md#wsstockprice---stock-price), [`wsStrategyValue`](websockets.md#wsstrategyvalue---strategy-value), [`wsOrders`](websockets.md#wsorders---orders), [`wsPositions`](websockets.md#wspositions---positions), [`wsTimelines`](websockets.md#wstimelines---timelines), [`wsBotStatus`](websockets.md#wsbotstatus---bot-status), [`wsBotAllocations`](websockets.md#wsbotallocations---bot-allocations), [`wsBotActivities`](websockets.md#wsbotactivities---bot-activities) |

## Stock Identifiers

`stock_id` accepts either an internal AlphaInsider stock ID or `SYMBOL:EXCHANGE`, such as `SPY:ARCX`, `AAPL:XNAS`, or `ETH-USD:COINBASE`.

Prefer `searchStocks` for discovery. Use `getAllStocks` sparingly because the docs mark it as limited to 20 requests per hour.
