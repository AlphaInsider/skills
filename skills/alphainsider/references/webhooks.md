# Webhooks Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

TradingView-style webhook order signals.

## newOrderWebhook - POST `/newOrderWebhook`

New order from webhook. [Tutorial setup](https://alphainsider.com/resources#trading-view). Note, you can only go fully in or out of a position.

Note: This endpoint sends the token in the JSON body as `api_token`; do not send an `Authorization` header. Webhook signals can only go fully in or out of a position.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `stock_id` | Yes | string | Stock ID. `"stock:exchange"` or `"stock_id"` |
| body | `action` | Yes | string: `buy`, `long`, `sell`, `short`, `close`, `flat` | Order actions. Action "buy" is the same as "long", "sell" is the same as "short", "close" is the same as "flat". It is recommended for TradingView webhooks to use the **{{strategy.market_position}}** to get all strategy actions. [See TradingView strategy alert guide for full list of automated actions](https://www.tradingview.com/support/solutions/43000481368-strategy-alerts/). |
| body | `leverage` | No | number (0..2; default `1`) | Leverage to trade at. Defaults to 1 if not set. |
| body | `api_token` | Yes | string (JWT) | AlphaInsider API token used by webhook calls in the request body. |

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
| `response.price` | null or value | Price or execution price, depending on context. |
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

Example:

```bash
python scripts/alphainsider_request.py POST /newOrderWebhook \
  --json '{"stock_id":"SPY:ARCX","action":"buy","leverage":1}'
```
