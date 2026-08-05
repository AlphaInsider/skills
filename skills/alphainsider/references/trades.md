# Trades Endpoints

REST base URL: `https://alphainsider.com/api`.

Positions, open orders, max order sizing, fixed orders, allocation orders, and order deletion.

Read `input-multiplier.md` before displaying positions or orders, calculating user-facing order size, or converting user-entered quantities into `newOrder`.

## getPositions - GET `/getPositions`

Get strategy positions.

Note: Position `amount` and `total` values are strategy-normalized. Owners use `input_multiplier` for USD/share display; subscriber/non-owner percent fallback is documented in `input-multiplier.md`.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id` | Yes | string | Strategy ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].position_id` | string | Strategy position identifier. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].price` | string | Price or execution price, depending on context. |
| `response[].amount` | string | Amount. |
| `response[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].symbol` | string | Ticker or asset symbol. |
| `response[].name` | string | Display name. |
| `response[].sector` | string | Sector or asset category. |
| `response[].security` | string | Security type, such as stock or cryptocurrency. |
| `response[].exchange` | string | Exchange code. |
| `response[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].peg` | string | Peg or quote currency. |
| `response[].provider` | string | External provider or data provider. |
| `response[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].fee` | string | Fee value. |
| `response[].links` | object | External research and market-data links. |
| `response[].stock_status` | string | Current stock status. |
| `response[].bid` | string | Current bid price. |
| `response[].ask` | string | Current ask price. |
| `response[].last` | string | Last traded price. |

Example request:

```http
GET /getPositions?strategy_id=<STRATEGY_ID>
```

## getOrders - GET `/getOrders`

Get strategy orders.

Note: Open order `amount` and `total` values are strategy-normalized. Owners use `input_multiplier` for user-visible amount and total; subscriber/non-owner percent display is documented in `input-multiplier.md`.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id` | Yes | string | Strategy ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].order_id` | string | Order identifier. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].action` | string | Order or signal action. |
| `response[].stop_price` | null or value | Stop trigger price. |
| `response[].price` | string | Price or execution price, depending on context. |
| `response[].amount` | string | Amount. |
| `response[].total` | null or value | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].symbol` | string | Ticker or asset symbol. |
| `response[].name` | string | Display name. |
| `response[].sector` | string | Sector or asset category. |
| `response[].security` | string | Security type, such as stock or cryptocurrency. |
| `response[].exchange` | string | Exchange code. |
| `response[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].peg` | string | Peg or quote currency. |
| `response[].provider` | string | External provider or data provider. |
| `response[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].fee` | string | Fee value. |
| `response[].links` | object | External research and market-data links. |
| `response[].stock_status` | string | Current stock status. |
| `response[].bid` | string | Current bid price. |
| `response[].ask` | string | Current ask price. |
| `response[].last` | string | Last traded price. |
| `response[].order_dependencies` | array of string | Order IDs this order is waiting on; `[]` means the order has no outstanding dependencies. |

Example request:

```http
GET /getOrders?strategy_id=<STRATEGY_ID>
Authorization: <API_TOKEN>
```

## getMaxOrderSize - GET `/getMaxOrderSize`

Get max order size. Be sure to leave room for slippage and fee when calculating max buying/selling power.

Note: Use this before large, leveraged, or otherwise user-risky fixed orders because it factors available buying/selling power, slippage, and fees. The returned limits are user-facing; do not apply `input_multiplier` to them.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id` | Yes | string | Strategy ID. |
| query | `stock_id` | Yes | string | Stock ID. `"stock:exchange"` or `"stock_id"` |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Max order size payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response.remaining_assets_amount` | string | Remaining asset buying/selling capacity. |
| `response.remaining_liabilities_amount` | string | Remaining liability capacity. |
| `response.buying_power_total` | string | Total buying power available for the requested order. |
| `response.selling_power_total` | string | Total selling power available for the requested order. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.fee` | string | Fee value. |

Example request:

```http
GET /getMaxOrderSize?strategy_id=<STRATEGY_ID>&stock_id=SPY:ARCX
Authorization: <API_TOKEN>
```

## newOrder - POST `/newOrder`

Create a new open order. Must pass `amount` or `total` not both. For TradingView or webhook integrations with percentage based order actions, see [newOrderWebhook](https://api.alphainsider.com/resources/webhooks/neworderwebhook) or [newOrderAllocations](https://api.alphainsider.com/resources/trades/neworderallocations).

Note: Send exactly one of `amount` or `total`. Owner-managed trades must resolve the owner `input_multiplier` before converting user-entered quantities. If the user entered share/crypto or USD quantity, divide by `input_multiplier` before sending `newOrder.amount` or `newOrder.total`; see `input-multiplier.md`. Subscriber/non-owner missing-multiplier fallback is display-only unless the user explicitly provides normalized strategy units. Use `newOrderAllocations` for percentage allocation rebalances.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `stock_id` | Yes | string | Stock ID. `"stock:exchange"` or `"stock_id"` |
| body | `action` | Yes | string: `buy`, `sell` | Order action. |
| body | `type` | Yes | string: `market`, `limit`, `stop_market`, `stop_limit`, `oco` | Type of order. |
| body | `amount` | No | string (double(30,15)) | Normalized order amount. If the user entered share/crypto quantity, send `user_quantity / input_multiplier`. For `newOrder`, send only one of `amount` or `total`. |
| body | `total` | No | string (double(30,15)) | Normalized cash allocated to the order. If the user entered USD quantity, send `user_dollars / input_multiplier`. For `newOrder`, send only one of `amount` or `total`. |
| body | `price` | No | string (double(30,15)) | Price to make trade at. |
| body | `stop_price` | No | string (double(30,15)) | Price to trigger order. |
| body | `order_dependencies` | No | array of string | An array of order IDs to wait for before this order can be executed. |

Responses from `newOrder`, `getOrders`, `newOrderAllocations`, and `wsOrders` include `order_dependencies` as an array of prerequisite order IDs. Orders with no prerequisites return `[]`. `newOrderAllocations` does not accept `order_dependencies` in the request, but increase orders created by allocation rebalances may depend on reduce orders.

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.order_id` | string | Order identifier. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.type` | string | Type or category for this object. |
| `response.action` | string | Order or signal action. |
| `response.stop_price` | null or value | Stop trigger price. |
| `response.price` | string | Price or execution price, depending on context. |
| `response.amount` | string | Amount. |
| `response.total` | null or value | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response.created_at` | string | Creation timestamp. |
| `response.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response.figi_composite` | null or value | Composite FIGI identifier when available. |
| `response.symbol` | string | Ticker or asset symbol. |
| `response.name` | string | Display name. |
| `response.sector` | string | Sector or asset category. |
| `response.security` | string | Security type, such as stock or cryptocurrency. |
| `response.exchange` | string | Exchange code. |
| `response.stock` | string | Stock symbol as stored by AlphaInsider. |
| `response.peg` | string | Peg or quote currency. |
| `response.provider` | string | External provider or data provider. |
| `response.slippage` | string | Slippage value or configured slippage fraction. |
| `response.fee` | string | Fee value. |
| `response.links` | object | External research and market-data links. |
| `response.stock_status` | string | Current stock status. |
| `response.bid` | string | Current bid price. |
| `response.ask` | string | Current ask price. |
| `response.last` | string | Last traded price. |
| `response.order_dependencies` | array of string | Order IDs this order is waiting on; `[]` means the order has no outstanding dependencies. |

Example request:

```http
POST /newOrder
Authorization: <API_TOKEN>
Content-Type: application/json

{"stock_id":"SPY:ARCX","action":"buy","type":"market","total":"100","strategy_id":"<STRATEGY_ID>"}
```

## newOrderAllocations - POST `/newOrderAllocations`

Create new orders based on percentage allocations.

Note: Creates market orders to move a strategy toward target percentage allocations. Do not send `order_dependencies` in this request. Allocation-generated increase orders may depend on reduce orders, so inspect each returned `order_dependencies` array before assuming the order can execute immediately.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `allocations` | Yes | array of object | An array of positions the strategy should be allocated to. |
| body | `allocations[].stock_id` | No | string | Stock ID. `"stock:exchange"` or `"stock_id"` |
| body | `allocations[].action` | No | string: `buy`, `long`, `sell`, `short`, `close`, `flat` | Order actions. Action "buy" is the same as "long", "sell" is the same as "short", "close" is the same as "flat". When using "close" or "flat", the percent is set to 0—ignoring any percent passed. |
| body | `allocations[].percent` | No | number (0..2; increments of `0.0001`) | The final position size, expressed as a positive decimal fraction of your equity (e.g., TSLA long 1.5 for a 150% long position in TSLA). Values must be positive decimals ranging from 0 to 2, with the sum of all allocations not exceeding the maximum leverage of 2 (or 200%). |
| body | `slippage` | No | number (0..2; increments of `0.001`; default `0.002`) | Slippage represents the percentage offset from the current bid/ask price when placing a limit order. This adjustment helps ensure that orders are more likely to fill by accounting for potential price movements. **Please note that the allocations may not sum precisely to 100%.** The following calculation illustrates our approach to determining a conservative buffer for potential fees and slippage: * `MaxOrderTotal = BuyingPower * 2` This calculates the maximum possible order total, representing a full position reversal (e.g., from maximum long to maximum short, or vice versa). * `ConservativeFeeTotal = MaxOrderTotal * (fee * 2)` This accounts for the buying power reduction due to fees, as fees are deducted from collateral. (Stock Fees: 0%, Crypto Fees: 0.25%). * `ConservativeSlippageTotal = MaxOrderTotal * Slippage` This reserves funds for the worst-case scenario of order fills impacted by slippage. * `FinalBuyingPower = BuyingPower - ConservativeFeeTotal - ConservativeSlippageTotal` The adjusted buying power after these reductions. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].order_id` | string | Order identifier. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].action` | string | Order or signal action. |
| `response[].stop_price` | null or value | Stop trigger price. |
| `response[].price` | null or value | Price or execution price, depending on context. |
| `response[].amount` | null or value | Amount. |
| `response[].total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].figi_composite` | string | Composite FIGI identifier when available. |
| `response[].symbol` | string | Ticker or asset symbol. |
| `response[].name` | string | Display name. |
| `response[].sector` | string | Sector or asset category. |
| `response[].security` | string | Security type, such as stock or cryptocurrency. |
| `response[].exchange` | string | Exchange code. |
| `response[].stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].peg` | string | Peg or quote currency. |
| `response[].provider` | string | External provider or data provider. |
| `response[].slippage` | string | Slippage value or configured slippage fraction. |
| `response[].fee` | string | Fee value. |
| `response[].links` | object | External research and market-data links. |
| `response[].stock_status` | string | Current stock status. |
| `response[].bid` | string | Current bid price. |
| `response[].ask` | string | Current ask price. |
| `response[].last` | string | Last traded price. |
| `response[].order_dependencies` | array of string | Order IDs this order is waiting on; `[]` means the order has no outstanding dependencies. |

Example request:

```http
POST /newOrderAllocations
Authorization: <API_TOKEN>
Content-Type: application/json

{"allocations":[{"stock_id":"SPY:ARCX","action":"buy","percent":0.8}],"slippage":0.003,"strategy_id":"<STRATEGY_ID>"}
```

## deleteOrder - POST `/deleteOrder`

Delete existing order.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `order_id` | Yes | string | Order ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example request:

```http
POST /deleteOrder
Authorization: <API_TOKEN>
Content-Type: application/json

{"order_id":"order_123","strategy_id":"<STRATEGY_ID>"}
```
