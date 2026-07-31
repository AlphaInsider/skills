# Coinbase Public Crypto Market Data

Use `CoinbaseMarketDataClient` from this skill's
`scripts/market_data/coinbase.py`. It sends direct public Advanced Trade REST
requests with `httpx` and speaks the public WebSocket protocol with
`websockets`; it does not use a Coinbase SDK. No Coinbase API key is read or
required. Generated workspaces receive this module as
`strategy/clients/coinbase.py`; import it from there.

Official sources: [public REST overview](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/rest-api),
[public products](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/list-public-products),
[candles](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles),
[market trades](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-market-trades),
[WebSocket overview](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-overview),
and [channels](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-channels).

## Configure the client

There are no environment variables or credentials. REST uses
`https://api.coinbase.com/api/v3/brokerage/market`; WebSocket uses
`wss://advanced-trade-ws.coinbase.com`.

```python
from strategy.clients.coinbase import CoinbaseMarketDataClient

with CoinbaseMarketDataClient() as client:
    product = client.get_product("BTC-USD")
```

The wrapper intentionally excludes Coinbase accounts, portfolios, balances,
orders, fills, conversions, and authenticated `user` or
`futures_balance_summary` streams. AlphaInsider remains the only paper-order
destination.

## Complete public REST surface

| Method | Direct endpoint | Result |
| --- | --- | --- |
| `get_server_time()` | `GET /api/v3/brokerage/time` | Coinbase epoch and ISO time |
| `list_products(…)` | `GET /products` | Product page and cursors |
| `iter_products(…)` | repeated `GET /products` | Product dictionaries across pages |
| `get_product(product_id)` | `GET /products/{product_id}` | One product |
| `get_candles(product_id, granularity, start, end, limit=)` | `GET /products/{product_id}/candles` | One candle page |
| `get_market_trades(product_id, limit=, start=, end=)` | `GET /products/{product_id}/ticker` | Trades and best bid/ask |
| `get_product_book(product_id, limit=, aggregation_price_increment=)` | `GET /product_book` | Bid/ask snapshot |

REST responses are returned verbatim as parsed JSON. Numeric market values are
normally strings; convert them with `Decimal` before strategy calculations.

## Product discovery and pagination

Product IDs use `BASE-QUOTE`, for example `BTC-USD` and `ETH-USD`. Record the
exact Coinbase product ID and matching AlphaInsider `stock_id`; never infer one
from the other at runtime.

`list_products()` exposes every documented public query field:

- `limit`, `offset`, and `cursor`;
- `product_type` and `product_ids`;
- `contract_expiry_type`, `expiring_contract_status`, and
  `futures_underlying_type`;
- `get_all_products`, `expired`, and `user_country_code`;
- `products_sort_order`.

For crypto strategy creation, normally filter `product_type="SPOT"` or the
explicitly selected `FUTURE`. Do not silently add equities or product-group
records merely because the public endpoint can return them.

Use `iter_products()` for complete discovery. It follows
`pagination.next_cursor` (and the older top-level `next_cursor` form), drops
duplicate product IDs across page boundaries, removes the initial `offset`
after the first page, and raises if Coinbase repeats a cursor.

```python
products = list(client.iter_products(product_type="SPOT", limit=100))
```

## Candles, trades, books, and time

Candle granularities are `ONE_MINUTE`, `FIVE_MINUTE`, `FIFTEEN_MINUTE`,
`THIRTY_MINUTE`, `ONE_HOUR`, `TWO_HOUR`, `FOUR_HOUR`, `SIX_HOUR`, and
`ONE_DAY`. `start` and `end` accept UNIX seconds or timezone-aware `datetime`
values. Naive datetimes are rejected so the host timezone cannot alter a
replay window.

Coinbase returns at most 350 candle buckets per request; `limit` must be 1–350.
Candles are newest-first with `start`, `low`, `high`, `open`, `close`, and
`volume`. A longer replay must make adjacent requests, de-duplicate on candle
`start`, sort chronologically, and assert that expected bucket boundaries are
present before running decisions.

`get_market_trades()` accepts optional `start` and `end` UNIX timestamps in
addition to `limit`, making trade-driven signal replay possible. Validate the
returned trade times and ordering rather than assuming the endpoint filled the
entire requested interval.

`get_product_book()` accepts `aggregation_price_increment`, the minimum price
interval used to combine levels. Record it in the plan because changing
aggregation changes an order-book signal.

Use `get_server_time()` to measure clock skew. Do not substitute server time
for an event's own timestamp.

## Public WebSocket channels

`stream()` is an async generator for all public channels:

- `ticker` and `ticker_batch`;
- `candles` (five-minute live buckets);
- `market_trades`;
- `level2`;
- `status`;
- `heartbeats`.

```python
import asyncio
from strategy.clients.coinbase import CoinbaseMarketDataClient

async def watch():
    client = CoinbaseMarketDataClient()
    async for message in client.stream(
        ["ticker", "market_trades"], ["BTC-USD", "ETH-USD"]
    ):
        if message.get("channel") != "heartbeats":
            print(message)

asyncio.run(watch())
```

The client opens one socket for the full product list, sends one subscribe
message per channel with every requested product ID, and adds one `heartbeats`
subscription by default. Every yielded market event retains its `product_id`.
The client never silently shards products across more sockets; if throughput
or provider limits require splitting, make that an explicit strategy decision.
Heartbeats keep quiet subscriptions open and contain a `heartbeat_counter`.
Set `heartbeats=False` only when the caller deliberately owns connection
liveness.

Every message on the socket carries `sequence_num`, one monotonic counter for
the whole connection — heartbeats and subscription acknowledgements consume
numbers too. With the default `validate_sequence=True`,
`CoinbaseSequenceTracker` validates that connection counter and raises:

- `CoinbaseSequenceGapError` when a number jumps, indicating dropped data;
- `CoinbaseOutOfOrderError` for a duplicate or lower number.

Heartbeat continuity is additionally validated with `heartbeat_counter`.
Incoming `l2_data` envelopes are exposed as the requested `level2` channel.
This fail-closed behavior prevents decisions on silently incomplete feeds.
After either error, use `StrategyRunner` for bounded reconnect/backoff and
resynchronize before trading: reconnect `level2` to receive its guaranteed
snapshot/update stream, refresh ticker/trades with `get_market_trades()`,
refresh candles with `get_candles()`, or refresh product status with
`get_product()`. Disabling sequence validation must be an explicit plan
decision with a documented reason.

Coinbase documents that feed servers can still drop or reorder data despite
TCP. The `level2` channel is the documented delivery-guaranteed choice for a
synchronized book. `new_quantity` is the resulting size at a level, not a
delta; zero removes the level.

The async generator ends if Coinbase closes the socket. Reconnection and
state restoration belong to `StrategyRunner`. Do not tight-loop reconnects or
subscriptions; follow current [WebSocket limits](https://docs.cdp.coinbase.com/coinbase-business/advanced-trade-apis/websocket/websocket-rate-limits).

## CLI

```bash
# REST
python -m scripts.market_data coinbase time
python -m scripts.market_data coinbase products --product-type SPOT --limit 100
python -m scripts.market_data coinbase products --product-type SPOT --all-pages
python -m scripts.market_data coinbase product BTC-USD
python -m scripts.market_data coinbase candles BTC-USD \
  --granularity FOUR_HOUR --start 1782777600 --end 1783382400 --limit 42
python -m scripts.market_data coinbase trades BTC-USD \
  --start 1782777600 --end 1782777900 --limit 100
python -m scripts.market_data coinbase book BTC-USD \
  --limit 50 --aggregation-price-increment 0.10

# Repeat --channel to share one WebSocket connection
python -m scripts.market_data coinbase stream BTC-USD ETH-USD \
  --channel ticker --channel market_trades --limit 20
```

Product discovery also exposes `--offset`, `--cursor`, `--product-id`,
`--contract-expiry-type`, `--expiring-contract-status`, `--get-all-products`,
`--products-sort-order`, `--futures-underlying-type`, `--user-country-code`,
and `--expired`. Use `--no-heartbeats` or `--no-sequence-validation` only for
deliberate diagnostics.

CLI defaults: `stream` subscribes to `ticker` when no `--channel` is given;
`candles` defaults to `--granularity ONE_HOUR` with a 300-bucket lookback
ending now; `trades` defaults to `--limit 10`.

## Errors and operating rules

HTTP 429 raises `CoinbaseMarketDataError`; apply bounded backoff and use the
provider's current response headers instead of hard-coding an assumed request
rate. Other HTTP failures and malformed REST/WebSocket responses raise the
same base error. All REST operations are idempotent reads.

Public responses are cached by Coinbase and are not a tick feed. Use REST for
discovery, snapshots, and replay; use WebSocket for live signals. Generated
tests must mock both transports. Network smoke tests remain read-only and
opt-in with `RUN_SMOKE_TESTS=1`.
