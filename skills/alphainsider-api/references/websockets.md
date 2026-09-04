# WebSocket API

WebSocket URL: `wss://alphainsider.com/ws`.

Send `ping` about every 30 seconds; the server responds with `pong`. Send one `subscribe` message with the full desired channel list because a new subscribe request overwrites previous subscriptions. After a recoverable connection or server error, reconnect and re-subscribe with that complete list. Treat missing credentials, invalid channel configuration, and authentication failures as terminal.

Contract note: several current AsyncAPI server-message schemas define only an
envelope or selected enum fields while their examples contain the detailed
response objects listed below. Treat example-only fields as illustrative, not
required schema guarantees, and handle missing or additive fields safely.

WebSocket strategy, position, order, and timeline payloads carry normalized strategy values. Read `input-multiplier.md` before displaying live strategy values, positions, orders, trades, or performance changes to users.

## Channel Summary

| Channel | Cadence | Description |
| --- | --- | --- |
| `wsStockPrice:<stock_id>` | ~1 second | Live bid, ask, and last price for a stock or crypto asset. |
| `wsStrategyValue:<strategy_id>` | ~5 seconds | Normalized strategy value updates; convert before displaying USD values. |
| `wsOrders:<strategy_id>` | Instant | Open order updates. |
| `wsPositions:<strategy_id>` | Instant | Strategy position updates. |
| `wsTimelines:<strategy_id>` | Instant | New strategy timeline events. |
| `wsBotStatus:<bot_id>` | Instant | Bot status changes. |
| `wsBotAllocations:<bot_id>` | Instant | Bot allocation changes. |
| `wsBotActivities:<bot_id>` | Instant | New bot activities. |

## Message Contents

- [`ping`](#ping---ping) — Ping
- [`pingResponse`](#pingresponse---ping-response) — Ping Response
- [`subscribe`](#subscribe---subscribe) — Subscribe
- [`subscribeResponse`](#subscriberesponse---subscribe-response) — Subscribe Response
- [`error`](#error---error-response) — Error Response
- [`wsStockPrice`](#wsstockprice---stock-price) — Stock Price
- [`wsStrategyValue`](#wsstrategyvalue---strategy-value) — Strategy Value
- [`wsOrders`](#wsorders---orders) — Orders
- [`wsPositions`](#wspositions---positions) — Positions
- [`wsTimelines`](#wstimelines---timelines) — Timelines
- [`wsBotStatus`](#wsbotstatus---bot-status) — Bot Status
- [`wsBotAllocations`](#wsbotallocations---bot-allocations) — Bot Allocations
- [`wsBotActivities`](#wsbotactivities---bot-activities) — Bot Activities

## ping - Ping

Client heartbeat message to keep the connection alive. We recommend sending a ping every 30 seconds.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| message | `ping` | Yes | string | Client heartbeat message. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `payload` | string | Message payload. |

Example:

```text
ping
```

## pingResponse - Ping Response

Server heartbeat response to a client ping.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `payload` | string | Message payload. |

Example:

```text
pong
```

## subscribe - Subscribe

Client request to subscribe to one or more channels. A new subscribe request overwrites all previous subscriptions.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| payload | `event` | Yes | `subscribe` | Subscribe event name. |
| payload | `payload.channels` | Yes | array of strings | Full set of channels to subscribe to. |
| payload | `payload.token` | Yes | string | AlphaInsider API token supplied by a secure WebSocket client/runtime. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `event` | string | WebSocket event name. |
| `payload` | object | Payload. |
| `payload.channels` | array of string | Channels. |
| `payload.token` | string | Token supplied by the WebSocket client/runtime. |

Example:

```json
{
  "event": "subscribe",
  "payload": {
    "channels": [
      "wsStockPrice:<STOCK_ID>",
      "wsStrategyValue:<STRATEGY_ID>",
      "wsOrders:<STRATEGY_ID>",
      "wsPositions:<STRATEGY_ID>",
      "wsTimelines:<STRATEGY_ID>",
      "wsBotStatus:<BOT_ID>",
      "wsBotAllocations:<BOT_ID>",
      "wsBotActivities:<BOT_ID>"
    ],
    "token": "<supplied-by-secure-client>"
  }
}
```

## subscribeResponse - Subscribe Response

Server confirmation of successful subscription.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```json
[
  {
    "event": "subscribe",
    "channel": "wsStockPrice:64diisPJwIqt99jyjoIGT",
    "response": "Subscribed to channel."
  }
]
```

## error - Error Response

Server error response, which may include a specific channel. Reconnect and re-subscribe with the complete channel list after recoverable errors. Do not retry an authentication failure without corrected credentials.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name when the error applies to a specific channel. |
| `[].response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```json
[
  {
    "event": "error",
    "response": "Request failed."
  },
  {
    "event": "error",
    "response": "Authentication failed."
  },
  {
    "event": "error",
    "channel": "wsStockPrice:64diisPJwIqt99jyjoIGT",
    "response": "Failed to subscribe to channel."
  },
  {
    "event": "error",
    "channel": "wsStockPrice:64diisPJwIqt99jyjoIGT",
    "response": "Channel closed."
  }
]
```

## wsStockPrice - Stock Price

Real-time stock price update (every 1 second). You can use either the internal stock ID or `"stock:exchange"` format (e.g. `"AAPL:XNAS"`). To lookup available stock_ids use the [/searchstocks](https://api.alphainsider.com/resources/stocks/searchstocks) or [/getallstocks](https://api.alphainsider.com/resources/stocks/getallstocks) endpoints.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `[].response.bid` | string | Current bid price. |
| `[].response.ask` | string | Current ask price. |
| `[].response.last` | string | Last traded price. |

Example:

```json
[
  {
    "event": "wsStockPrice",
    "channel": "wsStockPrice:yv4fbstPFFxgngHWPwnNq",
    "response": {
      "stock_id": "yv4fbstPFFxgngHWPwnNq",
      "bid": "675.59",
      "ask": "675.59",
      "last": "675.18"
    }
  }
]
```

## wsStrategyValue - Strategy Value

Real-time strategy value update (every 5 seconds).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response.strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |

Example:

```json
[
  {
    "event": "wsStrategyValue",
    "channel": "wsStrategyValue:IMgszSAVzapxSQCbYZC--",
    "response": {
      "strategy_id": "IMgszSAVzapxSQCbYZC--",
      "strategy_value": "0.99998930000000000"
    }
  }
]
```

## wsOrders - Orders

Updates for open orders (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response[].order_id` | string | Order identifier. |
| `[].response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response[].type` | string | Type or category for this object. |
| `[].response[].action` | string | Order or signal action. |
| `[].response[].stop_price` | null or value | Stop trigger price. |
| `[].response[].price` | null or value | Price or execution price, depending on context. |
| `[].response[].amount` | string | Amount. |
| `[].response[].total` | null or value | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `[].response[].created_at` | string | Creation timestamp. |
| `[].response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `[].response[].figi_composite` | string | Composite FIGI identifier when available. |
| `[].response[].symbol` | string | Ticker or asset symbol. |
| `[].response[].name` | string | Display name. |
| `[].response[].sector` | string | Sector or asset category. |
| `[].response[].security` | string | Security type, such as stock or cryptocurrency. |
| `[].response[].exchange` | string | Exchange code. |
| `[].response[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `[].response[].peg` | string | Peg or quote currency. |
| `[].response[].provider` | string | External provider or data provider. |
| `[].response[].slippage` | string | Slippage value or configured slippage fraction. |
| `[].response[].fee` | string | Fee value. |
| `[].response[].links` | object | External research and market-data links. |
| `[].response[].stock_status` | string | Current stock status. |
| `[].response[].bid` | string | Current bid price. |
| `[].response[].ask` | string | Current ask price. |
| `[].response[].last` | string | Last traded price. |
| `[].response[].order_dependencies` | array of string | Order IDs this order is waiting on; `[]` means the order has no outstanding dependencies. |

Example:

```json
[
  {
    "event": "wsOrders",
    "channel": "wsOrders:IMgszSAVzapxSQCbYZC--",
    "response": [
      {
        "order_id": "i9wtRL8_CsiT9krl1Zp_e",
        "strategy_id": "IMgszSAVzapxSQCbYZC--",
        "type": "market",
        "action": "buy",
        "stop_price": null,
        "price": null,
        "amount": "0.000010000000000",
        "total": null,
        "created_at": "2026-04-08T13:46:23.606Z",
        "stock_id": "yv4fbstPFFxgngHWPwnNq",
        "figi_composite": "BBG000BDTBL9",
        "symbol": "SPY",
        "name": "State Street SPDR S&P 500 ETF Trust",
        "sector": "Exchange Traded Fund",
        "security": "stock",
        "exchange": "ARCX",
        "stock": "SPY",
        "peg": "USD",
        "provider": "polygon",
        "slippage": "0.000000000000000",
        "fee": "0.000000000000000",
        "links": {},
        "stock_status": "active",
        "bid": "675.53",
        "ask": "675.53",
        "last": "675.18",
        "order_dependencies": []
      }
    ]
  }
]
```

## wsPositions - Positions

Updates for strategy positions (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response[].position_id` | string | Strategy position identifier. |
| `[].response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response[].type` | string | Type or category for this object. |
| `[].response[].price` | string | Price or execution price, depending on context. |
| `[].response[].amount` | string | Amount. |
| `[].response[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `[].response[].updated_at` | string | Last update timestamp. |
| `[].response[].created_at` | string | Creation timestamp. |
| `[].response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `[].response[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `[].response[].symbol` | string | Ticker or asset symbol. |
| `[].response[].name` | string | Display name. |
| `[].response[].sector` | string | Sector or asset category. |
| `[].response[].security` | string | Security type, such as stock or cryptocurrency. |
| `[].response[].exchange` | string | Exchange code. |
| `[].response[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `[].response[].peg` | string | Peg or quote currency. |
| `[].response[].provider` | string | External provider or data provider. |
| `[].response[].slippage` | string | Slippage value or configured slippage fraction. |
| `[].response[].fee` | string | Fee value. |
| `[].response[].links` | object | External research and market-data links. |
| `[].response[].stock_status` | string | Current stock status. |
| `[].response[].bid` | string | Current bid price. |
| `[].response[].ask` | string | Current ask price. |
| `[].response[].last` | string | Last traded price. |

Example:

```json
[
  {
    "event": "wsPositions",
    "channel": "wsPositions:IMgszSAVzapxSQCbYZC--",
    "response": [
      {
        "position_id": "biwu829fLOSI2enaRVuIx",
        "strategy_id": "IMgszSAVzapxSQCbYZC--",
        "type": "asset",
        "price": "1.000000000000000",
        "amount": "0.993242800000000",
        "total": "0.993242800000000",
        "updated_at": "2026-04-08T13:46:24.908Z",
        "created_at": "2026-04-08T13:46:24.908Z",
        "stock_id": "ubfhvYUsgvMIuJPwr76My",
        "figi_composite": null,
        "symbol": "USD",
        "name": "US Dollar",
        "sector": "Unallocated",
        "security": "",
        "exchange": "ALPHAINSIDER",
        "stock": "USD",
        "peg": "USD",
        "provider": "alphainsider",
        "slippage": "0.000000000000000",
        "fee": "0.000000000000000",
        "links": {},
        "stock_status": "active",
        "bid": "1.00",
        "ask": "1.00",
        "last": "1.00"
      },
      {
        "position_id": "mfx507iaGBpuNkgYi_Oob",
        "strategy_id": "IMgszSAVzapxSQCbYZC--",
        "type": "asset",
        "price": "675.720000000000000",
        "amount": "0.000010000000000",
        "total": "0.006757200000000",
        "updated_at": "2026-04-08T13:46:24.908Z",
        "created_at": "2026-04-08T13:46:24.908Z",
        "stock_id": "yv4fbstPFFxgngHWPwnNq",
        "figi_composite": "BBG000BDTBL9",
        "symbol": "SPY",
        "name": "State Street SPDR S&P 500 ETF Trust",
        "sector": "Exchange Traded Fund",
        "security": "stock",
        "exchange": "ARCX",
        "stock": "SPY",
        "peg": "USD",
        "provider": "polygon",
        "slippage": "0.000000000000000",
        "fee": "0.000000000000000",
        "links": {},
        "stock_status": "active",
        "bid": "675.73",
        "ask": "675.73",
        "last": "675.19"
      }
    ]
  }
]
```

## wsTimelines - Timelines

New strategy timeline events (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response.timeline_id` | string | Timeline event identifier. |
| `[].response.created_at` | string | Creation timestamp. |
| `[].response.strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response.name` | string | Display name. |
| `[].response.user_id` | string | AlphaInsider user identifier. |
| `[].response.likes` | string | Like count. |
| `[].response.liked` | boolean | Whether the authenticated user liked the event. |
| `[].response.type` | string | Type or category for this object. |
| `[].response.data` | object | Timeline event-specific payload. |
| `[].response.data.history_id` | string | Trade history identifier. |
| `[].response.data.action` | string | Order or signal action. |
| `[].response.data.price` | string | Price or execution price, depending on context. |
| `[].response.data.amount` | string | Amount. |
| `[].response.data.fee_total` | string | Total fee for a trade event. |
| `[].response.data.total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `[].response.data.new_holdings` | string | Holdings after the trade event. |
| `[].response.data.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `[].response.data.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `[].response.data.figi_composite` | string | Composite FIGI identifier when available. |
| `[].response.data.symbol` | string | Ticker or asset symbol. |
| `[].response.data.name` | string | Display name. |
| `[].response.data.sector` | string | Sector or asset category. |
| `[].response.data.security` | string | Security type, such as stock or cryptocurrency. |
| `[].response.data.exchange` | string | Exchange code. |
| `[].response.data.stock` | string | Stock symbol as stored by AlphaInsider. |
| `[].response.data.peg` | string | Peg or quote currency. |
| `[].response.data.provider` | string | External provider or data provider. |
| `[].response.data.slippage` | string | Slippage value or configured slippage fraction. |
| `[].response.data.fee` | string | Fee value. |
| `[].response.data.links` | object | External research and market-data links. |
| `[].response.data.stock_status` | string | Current stock status. |

Example:

```json
[
  {
    "event": "wsTimelines",
    "channel": "wsTimelines:IMgszSAVzapxSQCbYZC--",
    "response": {
      "timeline_id": "1",
      "created_at": "2026-04-08T13:46:24.908Z",
      "strategy_id": "IMgszSAVzapxSQCbYZC--",
      "name": "test stocks",
      "user_id": "user_1",
      "likes": "0",
      "liked": false,
      "type": "trade",
      "data": {
        "history_id": "hdyS4tHfSXV3fOVaDNRPV",
        "action": "buy",
        "price": "675.720000000000000",
        "amount": "0.000010000000000",
        "fee_total": "0.000000000000000",
        "total": "0.006757200000000",
        "new_holdings": "0.000010000000000",
        "strategy_value": "1.000000000000000",
        "stock_id": "yv4fbstPFFxgngHWPwnNq",
        "figi_composite": "BBG000BDTBL9",
        "symbol": "SPY",
        "name": "State Street SPDR S&P 500 ETF Trust",
        "sector": "Exchange Traded Fund",
        "security": "stock",
        "exchange": "ARCX",
        "stock": "SPY",
        "peg": "USD",
        "provider": "polygon",
        "slippage": "0.000000000000000",
        "fee": "0.000000000000000",
        "links": {},
        "stock_status": "active"
      }
    }
  }
]
```

## wsBotStatus - Bot Status

Bot status changes (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response.bot_id` | string | AlphaInsider bot identifier. |
| `[].response.status` | string | Current status. |

Example:

```json
[
  {
    "event": "wsBotStatus",
    "channel": "wsBotStatus:FSGV8HoplnWqotw5upiyV",
    "response": {
      "bot_id": "FSGV8HoplnWqotw5upiyV",
      "status": "on"
    }
  }
]
```

## wsBotAllocations - Bot Allocations

Bot allocation changes (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response[].bot_allocation_id` | string | Bot allocation identifier. |
| `[].response[].bot_id` | string | AlphaInsider bot identifier. |
| `[].response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response[].percent` | string | Portfolio allocation fraction. |
| `[].response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `[].response[].positions` | array of object | Nested position records. |
| `[].response[].positions[].position_id` | string | Strategy position identifier. |
| `[].response[].positions[].strategy_id` | string | AlphaInsider strategy identifier. |
| `[].response[].positions[].type` | string | Type or category for this object. |
| `[].response[].positions[].price` | string | Price or execution price, depending on context. |
| `[].response[].positions[].amount` | string | Amount. |
| `[].response[].positions[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `[].response[].positions[].updated_at` | string | Last update timestamp. |
| `[].response[].positions[].created_at` | string | Creation timestamp. |
| `[].response[].positions[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `[].response[].positions[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `[].response[].positions[].symbol` | string | Ticker or asset symbol. |
| `[].response[].positions[].name` | string | Display name. |
| `[].response[].positions[].sector` | string | Sector or asset category. |
| `[].response[].positions[].security` | string | Security type, such as stock or cryptocurrency. |
| `[].response[].positions[].exchange` | string | Exchange code. |
| `[].response[].positions[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `[].response[].positions[].peg` | string | Peg or quote currency. |
| `[].response[].positions[].provider` | string | External provider or data provider. |
| `[].response[].positions[].slippage` | string | Slippage value or configured slippage fraction. |
| `[].response[].positions[].fee` | string | Fee value. |
| `[].response[].positions[].links` | object | External research and market-data links. |
| `[].response[].positions[].stock_status` | string | Current stock status. |
| `[].response[].positions[].bid` | string | Current bid price. |
| `[].response[].positions[].ask` | string | Current ask price. |
| `[].response[].positions[].last` | string | Last traded price. |
| `[].response[].updated_at` | string | Last update timestamp. |
| `[].response[].created_at` | string | Creation timestamp. |

Example:

```json
[
  {
    "event": "wsBotAllocations",
    "channel": "wsBotAllocations:FSGV8HoplnWqotw5upiyV",
    "response": [
      {
        "bot_allocation_id": "FLyLk7XLHW31SXZSMq1uS",
        "bot_id": "FSGV8HoplnWqotw5upiyV",
        "strategy_id": "IMgszSAVzapxSQCbYZC--",
        "percent": "0.8000000480005932873330314362685522793061722242886922082356937931",
        "strategy_value": "0.9999877",
        "positions": [
          {
            "position_id": "biwu829fLOSI2enaRVuIx",
            "strategy_id": "IMgszSAVzapxSQCbYZC--",
            "type": "asset",
            "price": "1.000000000000000",
            "amount": "0.993242800000000",
            "total": "0.993242800000000",
            "updated_at": "2026-04-08T13:46:24.908Z",
            "created_at": "2026-04-08T13:46:24.908Z",
            "stock_id": "ubfhvYUsgvMIuJPwr76My",
            "figi_composite": null,
            "symbol": "USD",
            "name": "US Dollar",
            "sector": "Unallocated",
            "security": "",
            "exchange": "ALPHAINSIDER",
            "stock": "USD",
            "peg": "USD",
            "provider": "alphainsider",
            "slippage": "0.000000000000000",
            "fee": "0.000000000000000",
            "links": {},
            "stock_status": "active",
            "bid": "1.00",
            "ask": "1.00",
            "last": "1.00"
          },
          {
            "position_id": "mfx507iaGBpuNkgYi_Oob",
            "strategy_id": "IMgszSAVzapxSQCbYZC--",
            "type": "asset",
            "price": "675.720000000000000",
            "amount": "0.000010000000000",
            "total": "0.006757200000000",
            "updated_at": "2026-04-08T13:46:24.908Z",
            "created_at": "2026-04-08T13:46:24.908Z",
            "stock_id": "yv4fbstPFFxgngHWPwnNq",
            "figi_composite": "BBG000BDTBL9",
            "symbol": "SPY",
            "name": "State Street SPDR S&P 500 ETF Trust",
            "sector": "Exchange Traded Fund",
            "security": "stock",
            "exchange": "ARCX",
            "stock": "SPY",
            "peg": "USD",
            "provider": "polygon",
            "slippage": "0.000000000000000",
            "fee": "0.000000000000000",
            "links": {},
            "stock_status": "active",
            "bid": "674.49",
            "ask": "674.53",
            "last": "674.2"
          }
        ],
        "updated_at": "2026-04-08T13:57:12.784Z",
        "created_at": "2026-04-08T13:57:12.784Z"
      }
    ]
  }
]
```

## wsBotActivities - Bot Activities

New bot activities (instant).

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| server | - | - | - | This message is sent by the server. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `[].event` | string | WebSocket event name. |
| `[].channel` | string | WebSocket channel name. |
| `[].response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `[].response.bot_activity_id` | string | Bot activity identifier. |
| `[].response.bot_id` | string | AlphaInsider bot identifier. |
| `[].response.type` | string | Type or category for this object. |
| `[].response.message` | string | Activity or status message. |
| `[].response.created_at` | string | Creation timestamp. |

Example:

```json
[
  {
    "event": "wsBotActivities",
    "channel": "wsBotActivities:FSGV8HoplnWqotw5upiyV",
    "response": {
      "bot_activity_id": "2h0-0OBMXOcl5wjkoGjKf",
      "bot_id": "FSGV8HoplnWqotw5upiyV",
      "type": "start",
      "message": "Bot started.",
      "created_at": "2026-04-08T13:51:31.553Z"
    }
  }
]
```
