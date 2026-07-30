# Coinbase Public Crypto Market Data Reference

Client: `scripts.market_data.CoinbaseMarketDataClient`. Uses only the
**unauthenticated public** Coinbase Advanced Trade market-data endpoints — no
credentials, ever.

## Authentication and environment

None. Public REST and public WebSocket channels require no API keys. If a
task appears to need Coinbase accounts, orders, portfolios, or the
authenticated `user`/`futures_balance_summary` channels, stop: those are
excluded from this workspace (AlphaInsider is the only order destination).

## Method → endpoint map

REST base URL: `https://api.coinbase.com/api/v3/brokerage/market`.
WebSocket URL: `wss://advanced-trade-ws.coinbase.com`.

| Method | Endpoint | Notes |
| --- | --- | --- |
| `list_products(limit=, product_type=)` | `GET /products` | `product_type` ∈ `SPOT`/`FUTURE`; response `{products: […], num_products}` |
| `get_product(product_id)` | `GET /products/{product_id}` | e.g. `BTC-USD` |
| `get_candles(product_id, granularity, start, end)` | `GET /products/{product_id}/candles` | see below |
| `get_market_trades(product_id, limit=)` | `GET /products/{product_id}/ticker` | recent public trades + best bid/ask |
| `get_product_book(product_id, limit=)` | `GET /product_book` | `{pricebook: {bids, asks, time}}` |
| `stream(channels, product_ids, heartbeats=True)` | WebSocket subscribe | async generator of parsed messages |

REST methods return the parsed JSON body verbatim.

## Products, granularities, timestamps, pagination

- Product IDs are `BASE-QUOTE` strings: `BTC-USD`, `ETH-USD`, …
- Candle `granularity` ∈ `ONE_MINUTE`, `FIVE_MINUTE`, `FIFTEEN_MINUTE`,
  `THIRTY_MINUTE`, `ONE_HOUR`, `TWO_HOUR`, `SIX_HOUR`, `ONE_DAY`.
- Candle `start`/`end` are **UNIX seconds** (the client also accepts
  `datetime`). Max **350 candles per request** — page by shifting the
  start/end window; there is no page token.
- Candles arrive newest-first as
  `{start, low, high, open, close, volume}` with string numbers.
- `list_products` paginates with `limit`/`offset`; trades use `limit`.
- Public REST responses are served from a cache on Coinbase's side (roughly
  per-second freshness) — do not tight-poll expecting tick-level updates;
  use the WebSocket for real-time data.

## WebSocket behavior

- Public channels: `ticker`, `ticker_batch`, `candles`, `market_trades`,
  `level2` (order-book updates: snapshot then l2 updates), `status`,
  `heartbeats`. Authenticated channels are rejected by the client.
- One subscribe message per channel:
  `{"type": "subscribe", "channel": "<name>", "product_ids": […]}`.
- **Heartbeats**: Coinbase disconnects quiet connections; `stream()`
  subscribes to `heartbeats` by default (once per second, global — no
  product IDs) to keep the connection open through quiet markets. Filter
  heartbeat messages out of strategy logic (`message["channel"] == "heartbeats"`).
- The generator ends if Coinbase closes the connection; reconnection/backoff
  belongs to the caller (use `scripts.strategy_runtime.StrategyRunner`).

## Retry / rate limits

Public REST: ~10 requests/sec per IP; HTTP 429 raises
`CoinbaseMarketDataError` — back off before retrying (all endpoints here are
idempotent reads). WebSocket: 750 messages/sec per IP inbound, which
subscribe-only usage never approaches.

## Executable examples

```bash
python -m scripts.market_data coinbase products --limit 5
python -m scripts.market_data coinbase product BTC-USD
python -m scripts.market_data coinbase candles BTC-USD --granularity ONE_HOUR
python -m scripts.market_data coinbase trades BTC-USD --limit 5
python -m scripts.market_data coinbase book BTC-USD --limit 10
python -m scripts.market_data coinbase stream BTC-USD ETH-USD --channel ticker --limit 5
```

```python
import asyncio
from scripts.market_data import CoinbaseMarketDataClient

client = CoinbaseMarketDataClient()
candles = client.get_candles("BTC-USD", "ONE_HOUR", start=1753600000, end=1753686400)

async def watch():
    async for message in client.stream(["ticker"], ["BTC-USD"]):
        if message.get("channel") != "heartbeats":
            print(message)

asyncio.run(watch())
```

## Exclusions

Coinbase accounts, orders, fills, portfolios, converts, payment methods, and
authenticated WebSocket channels are out of scope. The client raises
`ValueError` for non-public channels.
