# Stocks Endpoints

REST base URL: `https://alphainsider.com/api`.

Stock and cryptocurrency lookup, price history, search, and exchange status.

`stock_id` accepts either an internal AlphaInsider stock ID or `SYMBOL:EXCHANGE` such as `SPY:ARCX`.

## getStocks - GET `/getStocks`

Get stock information.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| query | `stock_id[]` | Yes | array of string (max 100) | One or more stock IDs. Use an internal ID or `SYMBOL:EXCHANGE`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
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

Example request:

```http
GET /getStocks?stock_id[]=SPY:ARCX
```

## getAllStocks - GET `/getAllStocks`

Get all stock information. *Limited to 20 requests per hour.*

Note: The docs mark this endpoint as limited to 20 requests per hour; prefer `searchStocks` for lookup flows.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| - | - | - | - | No inputs. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
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

Example request:

```http
GET /getAllStocks
```

## getStockPriceHistory - GET `/getStockPriceHistory`

Get stock price history.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| query | `stock_id` | Yes | string | Stock ID. `"stock:exchange"` or `"stock_id"` |
| query | `start_date` | No | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |
| query | `limit` | No | number | Number of results to return. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].stock_price_id` | string | Stock price id. |
| `response[].stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].bid` | string | Current bid price. |
| `response[].ask` | string | Current ask price. |
| `response[].last` | string | Last traded price. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getStockPriceHistory?stock_id=SPY:ARCX&start_date=2026-01-01T00:00:00Z
```

## searchStocks - POST `/searchStocks`

Search stocks.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| body | `search` | Yes | string | Term to search for. |
| body | `type` | No | string: `stock`, `cryptocurrency` | Type or category for this object. |
| body | `limit` | No | number | Number of results to return. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
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

Example request:

```http
POST /searchStocks
Content-Type: application/json

{"search":"SPY","type":"stock","limit":5}
```

## getExchangeStatus - GET `/getExchangeStatus`

Get exchange status.

Note: Use this to observe current exchange status, but do not treat a status
string by itself as permission to place a stock order. The local OpenAPI
snapshot does not enumerate the response values or map them to accepted stock
order sessions. Its `extended-hours` example is illustrative, not an
eligibility rule. Check the current `llms.txt` index for session guidance, then
the focused exchange-status and selected order-operation pages for an explicit
mapping. If they do not provide one, stock-session eligibility remains
unresolved.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| - | - | - | - | No inputs. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.stock` | string | Stock symbol as stored by AlphaInsider. |
| `response.cryptocurrency` | string | Cryptocurrency. |

Example request:

```http
GET /getExchangeStatus
```
