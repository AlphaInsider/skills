# Alpaca Equities Market Data Reference

Client: `scripts.market_data.AlpacaMarketDataClient` (wraps `alpaca-py`
data-only clients). **Never** instantiate `TradingClient` or anything from
`alpaca.trading` — AlphaInsider is the only order destination.

## Authentication and environment

| Variable | Required | Notes |
| --- | --- | --- |
| `ALPACA_KEY` | yes | API key ID |
| `ALPACA_SECRET` | yes | API secret |
| `ALPACA_FEED` | no | `iex` (default) or `sip` |

Process environment wins over `.env`. Missing credentials raise
`MissingAlpacaCredentials` at construction time.

**Feed entitlement**: free accounts are entitled to `iex` (IEX exchange data
only). `sip` (consolidated tape) requires a paid market-data subscription —
requests with an unentitled feed fail with HTTP 403. Historical SIP data
older than 15 minutes is available on free accounts, but keep `iex` unless
the user confirms a paid subscription.

## Method → API map

Base URLs (handled by `alpaca-py`): REST `https://data.alpaca.markets`,
stream `wss://stream.data.alpaca.markets/v2/{feed}`.

| Method | Underlying API | Notes |
| --- | --- | --- |
| `get_bars(symbols, timeframe="1Day", start=, end=, limit=)` | `GET /v2/stocks/bars` via `StockHistoricalDataClient.get_stock_bars` | Returns `{symbol: [bar_dict, …]}` |
| `get_latest_quotes(symbols)` | `GET /v2/stocks/quotes/latest` via `get_stock_latest_quote` | Returns `{symbol: quote_dict}` |
| `stream(symbols, channel, handler)` | `StockDataStream.subscribe_bars/quotes/trades` | Blocking; `channel` ∈ `bars`/`quotes`/`trades` |

## Timeframes, timestamps, pagination

- `timeframe` strings: `<n>Min`, `<n>Hour`, `1Day`, `1Week`, `1Month`
  (e.g. `1Min`, `5Min`, `15Min`, `1Hour`, `1Day`). Invalid values raise
  `ValueError`.
- `start`/`end` accept ISO 8601 strings or `datetime` objects (UTC). Omitted
  `end` means "up to now"; recent SIP data (< 15 min) is excluded on free
  plans.
- `limit` caps the number of bars per symbol. `alpaca-py` transparently
  follows `next_page_token` pagination — no manual paging.
- Bar dict shape: `timestamp` (ISO 8601), `open`, `high`, `low`, `close`,
  `volume`, `vwap`, `trade_count`. Quote dict shape: `timestamp`,
  `bid_price`, `bid_size`, `ask_price`, `ask_size`.

## Streaming

`stream()` blocks the calling thread and invokes `handler(event)` per bar,
quote, or trade; events are `alpaca-py` models with the same fields as above.
Alpaca allows one concurrent data-stream connection per account — a second
connection gets `connection limit exceeded`. Reconnection/backoff belongs to
the caller (use `scripts.strategy_runtime.StrategyRunner`).

## Retry / rate limits

- REST: 200 requests/min on the free plan (HTTP 429 beyond). Back off and
  retry reads; do not tight-poll — for sub-minute cadence use the stream.
- Do not retry non-idempotent operations blindly (not applicable here; this
  module is read-only).

## Executable examples

```bash
python -m scripts.market_data alpaca bars SPY MSFT --timeframe 15Min --limit 10
python -m scripts.market_data alpaca quotes SPY
python -m scripts.market_data alpaca stream SPY --channel trades
```

```python
from scripts.market_data import AlpacaMarketDataClient

client = AlpacaMarketDataClient()
bars = client.get_bars(["SPY"], "1Day", limit=5)
quotes = client.get_latest_quotes(["SPY", "MSFT"])
client.stream(["SPY"], "bars", handler=print)   # blocks; Ctrl+C to stop
```

## Exclusions

Broker trading, account, and order APIs are out of scope. Never construct
`alpaca.trading.client.TradingClient`; paper orders go to AlphaInsider only.
