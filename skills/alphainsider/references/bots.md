# Bots Endpoints

REST base URL: `https://alphainsider.com/api`.

Bot lifecycle, broker keys, settings, notifications, performance, allocations, and activities.

Supported bot brokers are `alpaca`, `binance`, `bitfinex`, and `hyperliquid`. Broker keys are private credentials: never print, log, commit, quote, or summarize them, and send only the key fields required by the selected broker.

Workflow rules:

- Create the bot, set the complete desired allocation list, configure optional settings/notifications, then start it and confirm status. Use reset or delete operations only when the user explicitly requests them.
- `updateBotAllocations` replaces the full allocation set; it is not a patch. Read current allocations before changing one entry, keep the sum at or below `1.0`, and leave any remainder as broker cash.
- Bot leverage is separate from allocation percent. Do not use leverage to make allocation sums exceed `1.0`.
- `getBotInfo.broker_details`, `getBotPerformance.response[].portfolio_value`, broker cash, and broker positions are real broker values. Never apply `input_multiplier` to them.
- `getBotAllocations.response[].positions` contains normalized strategy positions. For high-level target exposure, multiply the real broker portfolio value by the allocation percent and let AlphaInsider compute broker orders.
- Use `updateBotBrokerKeys` to rotate credentials or switch paper/live mode, and confirm `getBotInfo.response.broker_status` before starting or restarting. To change broker type, create a new bot.
- Bot statuses include `on`, `scheduled_rebalance`, `rebalancing`, `scheduled_close`, `closing`, `stopping`, and `off`. Confirm status before assuming a lifecycle action completed.

## getBots - GET `/getBots`

Get user bots.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id[]` | No | array of string (max 100) | One or more bot IDs. Repeat this query parameter for multiple bots. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].bot_id` | string | AlphaInsider bot identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].leverage` | string | Requested leverage. |
| `response[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response[].close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response[].broker` | string | Broker used by the bot. |
| `response[].type` | string | Type or category for this object. |
| `response[].live` | boolean | Whether the broker account is live rather than paper. |
| `response[].account_id` | string | Broker account identifier. |
| `response[].status` | string | Current status. |
| `response[].notifications` | array | Enabled notification types. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getBots?bot_id[]=<BOT_ID>
Authorization: <API_TOKEN>
```

## getBotInfo - GET `/getBotInfo`

Get bot info.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id` | Yes | string | Bot ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.broker_status` | string | Broker connection status. |
| `response.broker_details` | object | Broker account details returned by the broker integration. |
| `response.broker_details.margin_type` | string | Broker margin type. |
| `response.broker_details.value` | string | Broker account value. |
| `response.broker_details.buying_power` | string | Broker buying power. |
| `response.broker_details.min_total` | string | Minimum order total for the broker account. |
| `response.broker_details.max_leverage` | string | Maximum broker leverage. |
| `response.broker_details.initial_buying_power_percent` | string | Initial buying-power percentage reserved for bot execution. |
| `response.broker_details.positions` | array of object | Nested position records. |
| `response.broker_details.positions[].broker_stock_id` | string | Broker-specific symbol or stock identifier. |
| `response.broker_details.positions[].amount` | string | Amount. |
| `response.broker_details.positions[].bid` | string | Current bid price. |
| `response.broker_details.positions[].ask` | string | Current ask price. |

Example request:

```http
GET /getBotInfo?bot_id=<BOT_ID>
Authorization: <API_TOKEN>
```

## newBot - POST `/newBot`

Create new bot.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `broker` | Yes | string: `alpaca`, `binance`, `bitfinex`, `hyperliquid` | Bot broker. |
| body | `broker_keys` | Yes | object | Broker keys. |
| body | `broker_keys.live` | No | boolean | Live or paper account. |
| body | `broker_keys.bitfinex_key` | No | string | Bitfinex key. |
| body | `broker_keys.bitfinex_secret` | No | string | Bitfinex secret. |
| body | `broker_keys.binance_key` | No | string | Binance key. |
| body | `broker_keys.binance_secret` | No | string | Binance secret. |
| body | `broker_keys.alpaca_key` | No | string | Alpaca key. |
| body | `broker_keys.alpaca_secret` | No | string | Alpaca secret. |
| body | `broker_keys.hyperliquid_key` | No | string | Hyperliquid key. |
| body | `broker_keys.hyperliquid_secret` | No | string | Hyperliquid secret. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /newBot
Authorization: <API_TOKEN>
Content-Type: application/json

{"broker":"alpaca","broker_keys":{"live":false,"alpaca_key":"<key>","alpaca_secret":"<secret>"}}
```

## updateBotSettings - POST `/updateBotSettings`

Update bot settings.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `leverage` | No | number (2..50; increments of `1`) | The maximum leverage strategies can use to place orders. |
| body | `slippage` | No | number (0..0.05; increments of `0.001`) | The maximum percent from current price orders can be filled. |
| body | `rebalance_on_start` | No | boolean | Rebalance on start. |
| body | `close_on_stop` | No | boolean | Close on stop. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateBotSettings
Authorization: <API_TOKEN>
Content-Type: application/json

{"leverage":2,"slippage":0.005,"rebalance_on_start":true,"bot_id":"<BOT_ID>"}
```

## updateBotBrokerKeys - POST `/updateBotBrokerKeys`

Update bot broker keys.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `broker_keys` | Yes | object | Broker keys. |
| body | `broker_keys.live` | No | boolean | Live or paper account. |
| body | `broker_keys.bitfinex_key` | No | string | Bitfinex key. |
| body | `broker_keys.bitfinex_secret` | No | string | Bitfinex secret. |
| body | `broker_keys.binance_key` | No | string | Binance key. |
| body | `broker_keys.binance_secret` | No | string | Binance secret. |
| body | `broker_keys.alpaca_key` | No | string | Alpaca key. |
| body | `broker_keys.alpaca_secret` | No | string | Alpaca secret. |
| body | `broker_keys.hyperliquid_key` | No | string | Hyperliquid key. |
| body | `broker_keys.hyperliquid_secret` | No | string | Hyperliquid secret. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateBotBrokerKeys
Authorization: <API_TOKEN>
Content-Type: application/json

{"broker_keys":{"live":false,"alpaca_key":"<key>","alpaca_secret":"<secret>"},"bot_id":"<BOT_ID>"}
```

## updateBotNotifications - POST `/updateBotNotifications`

Update bot notifications.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `notifications` | Yes | array of string | Which notification types to receive. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateBotNotifications
Authorization: <API_TOKEN>
Content-Type: application/json

{"notifications":["start","stop","error"],"bot_id":"<BOT_ID>"}
```

## deleteBot - POST `/deleteBot`

Delete bot.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example request:

```http
POST /deleteBot
Authorization: <API_TOKEN>
Content-Type: application/json

{"bot_id":"<BOT_ID>"}
```

## startBot - POST `/startBot`

Start bot.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `rebalance_on_start` | No | boolean | Rebalance on start. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /startBot
Authorization: <API_TOKEN>
Content-Type: application/json

{"rebalance_on_start":true,"bot_id":"<BOT_ID>"}
```

## stopBot - POST `/stopBot`

Stop bot.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `close_on_stop` | No | boolean | Close on stop. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /stopBot
Authorization: <API_TOKEN>
Content-Type: application/json

{"close_on_stop":false,"bot_id":"<BOT_ID>"}
```

## resetBot - POST `/resetBot`

Reset bot.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.bot_id` | string | AlphaInsider bot identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.leverage` | string | Requested leverage. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.rebalance_on_start` | boolean | Whether the bot rebalances when started. |
| `response.close_on_stop` | boolean | Whether the bot closes positions when stopped. |
| `response.broker` | string | Broker used by the bot. |
| `response.type` | string | Type or category for this object. |
| `response.live` | boolean | Whether the broker account is live rather than paper. |
| `response.account_id` | string | Broker account identifier. |
| `response.status` | string | Current status. |
| `response.notifications` | array | Enabled notification types. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /resetBot
Authorization: <API_TOKEN>
Content-Type: application/json

{"bot_id":"<BOT_ID>"}
```

## getBotPerformance - GET `/getBotPerformance`

Get bot performance data.

Note: `portfolio_value` is a real broker value. Do not apply `input_multiplier`.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id` | Yes | string | Bot ID. |
| query | `frequency` | No | number (default `1`) | The number of intervals per tick. |
| query | `interval` | No | string: `hour`, `day`, `week` (default `hour`) | The timeframe per tick. |
| query | `start_date` | Yes | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].bot_id` | string | AlphaInsider bot identifier. |
| `response[].portfolio_value` | string | Portfolio value. |
| `response[].activity` | string | Trade activity label for a performance interval. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getBotPerformance?bot_id=<BOT_ID>&start_date=2026-01-01T00:00:00Z&interval=day
Authorization: <API_TOKEN>
```

## resetBotPerformance - POST `/resetBotPerformance`

Resets the bot performance graph.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example request:

```http
POST /resetBotPerformance
Authorization: <API_TOKEN>
Content-Type: application/json

{"bot_id":"<BOT_ID>"}
```

## getBotAllocations - GET `/getBotAllocations`

Get bot allocations.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id[]` | Yes | array of string (max 100) | One or more bot IDs. Repeat this query parameter for multiple bots. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].bot_allocation_id` | string | Bot allocation identifier. |
| `response[].bot_id` | string | AlphaInsider bot identifier. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].percent` | string | Portfolio allocation fraction. |
| `response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].positions` | array of object | Nested position records. |
| `response[].positions[].position_id` | string | Strategy position identifier. |
| `response[].positions[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].positions[].type` | string | Type or category for this object. |
| `response[].positions[].price` | string | Price or execution price, depending on context. |
| `response[].positions[].amount` | string | Amount. |
| `response[].positions[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].positions[].updated_at` | string | Last update timestamp. |
| `response[].positions[].created_at` | string | Creation timestamp. |
| `response[].positions[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].positions[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].positions[].symbol` | string | Ticker or asset symbol. |
| `response[].positions[].name` | string | Display name. |
| `response[].positions[].sector` | string | Sector or asset category. |
| `response[].positions[].security` | string | Security type, such as stock or cryptocurrency. |
| `response[].positions[].exchange` | string | Exchange code. |
| `response[].positions[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].positions[].peg` | string | Peg or quote currency. |
| `response[].positions[].provider` | string | External provider or data provider. |
| `response[].positions[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].positions[].fee` | string | Fee value. |
| `response[].positions[].links` | object | External research and market-data links. |
| `response[].positions[].stock_status` | string | Current stock status. |
| `response[].positions[].bid` | string | Current bid price. |
| `response[].positions[].ask` | string | Current ask price. |
| `response[].positions[].last` | string | Last traded price. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getBotAllocations?bot_id[]=<BOT_ID>
Authorization: <API_TOKEN>
```

## updateBotAllocations - POST `/updateBotAllocations`

Update bot allocations.

Note: This endpoint replaces the full allocation set. Submit every allocation that should remain, keep the sum at or below `1.0`, and treat the unallocated remainder as broker cash.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `allocations` | Yes | array of object (max 100) | Complete desired allocation list. This replaces the existing set. |
| body | `allocations[].strategy_id` | Yes | string | Strategy ID. |
| body | `allocations[].percent` | Yes | number (0..1; increments of `0.0001`) | Fraction of the broker portfolio assigned to this strategy. Keep the allocation sum at or below `1.0`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].bot_allocation_id` | string | Bot allocation identifier. |
| `response[].bot_id` | string | AlphaInsider bot identifier. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].percent` | string | Portfolio allocation fraction. |
| `response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].positions` | array of object | Nested position records. |
| `response[].positions[].position_id` | string | Strategy position identifier. |
| `response[].positions[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].positions[].type` | string | Type or category for this object. |
| `response[].positions[].price` | string | Price or execution price, depending on context. |
| `response[].positions[].amount` | string | Amount. |
| `response[].positions[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].positions[].updated_at` | string | Last update timestamp. |
| `response[].positions[].created_at` | string | Creation timestamp. |
| `response[].positions[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].positions[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].positions[].symbol` | string | Ticker or asset symbol. |
| `response[].positions[].name` | string | Display name. |
| `response[].positions[].sector` | string | Sector or asset category. |
| `response[].positions[].security` | string | Security type, such as stock or cryptocurrency. |
| `response[].positions[].exchange` | string | Exchange code. |
| `response[].positions[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].positions[].peg` | string | Peg or quote currency. |
| `response[].positions[].provider` | string | External provider or data provider. |
| `response[].positions[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].positions[].fee` | string | Fee value. |
| `response[].positions[].links` | object | External research and market-data links. |
| `response[].positions[].stock_status` | string | Current stock status. |
| `response[].positions[].bid` | string | Current bid price. |
| `response[].positions[].ask` | string | Current ask price. |
| `response[].positions[].last` | string | Last traded price. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateBotAllocations
Authorization: <API_TOKEN>
Content-Type: application/json

{"allocations":[{"strategy_id":"<STRATEGY_ID>","percent":0.5}],"bot_id":"<BOT_ID>"}
```

## getBotActivities - GET `/getBotActivities`

Get bot activities.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id` | Yes | string | Bot ID. |
| query | `bot_activity_id[]` | No | array of string (max 100) | Array of bot activity IDs. Leave empty to get all bot activities. |
| query | `type[]` | No | array of string | Array of activity types to filter by. |
| query | `start_date` | No | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |
| query | `limit` | No | number | Number of results to return. |
| query | `offset_id` | No | string | Offet by ID. Used for pagination. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].bot_activity_id` | string | Bot activity identifier. |
| `response[].bot_id` | string | AlphaInsider bot identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].message` | string | Activity or status message. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getBotActivities?bot_id=<BOT_ID>&limit=20
Authorization: <API_TOKEN>
```
