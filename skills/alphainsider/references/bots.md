# Bots Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Bot lifecycle, broker keys, settings, notifications, performance, allocations, and activities.

Supported bot brokers are `alpaca`, `binance`, `bitfinex`, and `hyperliquid`.

The request helper can supply a default bot ID for endpoints that accept `bot_id` when the user has not supplied an explicit ID.

## getBots - GET `/getBots`

Get user bots.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id[]` | No | array of string | One or more bot IDs. Repeat this query parameter for multiple bots. |

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

Example:

```bash
python scripts/alphainsider_request.py GET /getBots
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

Example:

```bash
python scripts/alphainsider_request.py GET /getBotInfo
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

Example:

```bash
python scripts/alphainsider_request.py POST /newBot \
  --json '{"broker":"alpaca","broker_keys":{"live":false,"alpaca_key":"<key>","alpaca_secret":"<secret>"}}'
```

## updateBotSettings - POST `/updateBotSettings`

Update bot settings.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `leverage` | No | number (2..50) | The maximum leverage strategies can use to place orders. |
| body | `slippage` | No | number (0..0.05) | The maximum percent from current price orders can be filled. |
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

Example:

```bash
python scripts/alphainsider_request.py POST /updateBotSettings \
  --json '{"leverage":2,"slippage":0.005,"rebalance_on_start":true}'
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

Example:

```bash
python scripts/alphainsider_request.py POST /updateBotBrokerKeys \
  --json '{"broker_keys":{"live":false,"alpaca_key":"<key>","alpaca_secret":"<secret>"}}'
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

Example:

```bash
python scripts/alphainsider_request.py POST /updateBotNotifications \
  --json '{"notifications":["start","stop","error"]}'
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

Example:

```bash
python scripts/alphainsider_request.py POST /deleteBot
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

Example:

```bash
python scripts/alphainsider_request.py POST /startBot \
  --json '{"rebalance_on_start":true}'
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

Example:

```bash
python scripts/alphainsider_request.py POST /stopBot \
  --json '{"close_on_stop":false}'
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

Example:

```bash
python scripts/alphainsider_request.py POST /resetBot
```

## getBotPerformance - GET `/getBotPerformance`

Get bot performance data.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id` | Yes | string | Bot ID. |
| query | `frequency` | No | number (default `1`) | The number of intervals per tick. |
| query | `interval` | No | string: `hour`, `day`, `week` | The timeframe per tick. |
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

Example:

```bash
python scripts/alphainsider_request.py GET /getBotPerformance \
  --query "start_date=2026-01-01T00:00:00Z" \
  --query "interval=day"
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

Example:

```bash
python scripts/alphainsider_request.py POST /resetBotPerformance
```

## getBotAllocations - GET `/getBotAllocations`

Get bot allocations.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id[]` | Yes | array of string | One or more bot IDs. Repeat this query parameter for multiple bots. |

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

Example:

```bash
python scripts/alphainsider_request.py GET /getBotAllocations
```

## updateBotAllocations - POST `/updateBotAllocations`

Update bot allocations.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bot_id` | Yes | string | Bot ID. |
| body | `allocations` | Yes | array of object | Array of allocations. |
| body | `allocations[].strategy_id` | Yes | string | Strategy ID. |
| body | `allocations[].percent` | Yes | number (0..1) | Percent of portfolio in this strategy. |

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

Example:

```bash
python scripts/alphainsider_request.py POST /updateBotAllocations \
  --json '{"allocations":[{"strategy_id":"<STRATEGY_ID>","percent":0.5}]}'
```

## getBotActivities - GET `/getBotActivities`

Get bot activities.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `bot_id` | Yes | string | Bot ID. |
| query | `bot_activity_id[]` | No | array of string | Array of bot activity IDs. Leave empty to get all bot activities. |
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

Example:

```bash
python scripts/alphainsider_request.py GET /getBotActivities \
  --query "limit=20"
```
