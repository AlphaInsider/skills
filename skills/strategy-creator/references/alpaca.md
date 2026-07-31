# Alpaca Equities Market Data

Use `AlpacaMarketDataClient` from this skill's `scripts/market_data/alpaca.py`.
It sends direct read-only REST requests with `httpx` and speaks Alpaca's stock
WebSocket protocol with `websockets`; it does not use an Alpaca SDK or trading
API. AlphaInsider remains the only paper-order destination. Generated
workspaces receive this module as `strategy/clients/alpaca.py`; import it from
there.

Official sources: [historical stock data](https://docs.alpaca.markets/docs/historical-stock-data-1),
[stock bars](https://docs.alpaca.markets/reference/stockbars), and
[real-time stock data](https://docs.alpaca.markets/us/docs/streaming-market-data).

## Configure the client

| Variable | Required | Meaning |
| --- | --- | --- |
| `ALPACA_KEY` | yes | Market-data API key ID |
| `ALPACA_SECRET` | yes | Market-data API secret |
| `ALPACA_FEED` | no | Defaults to `iex` |

The process environment wins; `.env` only fills missing values. Never print
the client, request headers, environment, or `.env`. Missing credentials raise
`MissingAlpacaCredentials`.

Free accounts are entitled to `iex` only; `sip` requires a paid market-data
subscription, and requests with an unentitled feed fail with HTTP 403.
Historical SIP data older than 15 minutes is available on free accounts, but
keep `iex` unless the user confirms a paid subscription.

```python
from strategy.clients.alpaca import AlpacaMarketDataClient

with AlpacaMarketDataClient(feed="iex") as client:
    bars = client.get_bars(["SPY", "MSFT"], "15Min", limit=200)
```

## REST methods

| Method | Direct endpoint | Result |
| --- | --- | --- |
| `get_bars(symbols, timeframe, …)` | `GET /v2/stocks/bars` | `{symbol: [bar, …]}` |
| `get_quotes(symbols, …)` | `GET /v2/stocks/quotes` | `{symbol: [quote, …]}` |
| `get_trades(symbols, …)` | `GET /v2/stocks/trades` | `{symbol: [trade, …]}` |
| `get_latest_quotes(symbols, …)` | `GET /v2/stocks/quotes/latest` | `{symbol: quote}` |
| `get_latest_trades(symbols, …)` | `GET /v2/stocks/trades/latest` | `{symbol: trade}` |
| `get_latest_bars(symbols, …)` | `GET /v2/stocks/bars/latest` | `{symbol: bar}` |

Historical bars accept `start`, `end`, `limit`, `sort`, `asof`, `currency`,
and `adjustment`. Historical quotes and trades accept the same controls except
`timeframe` and `adjustment`. `start` and `end` accept RFC 3339 strings or
`datetime`/`date` values. `sort` is `asc` or `desc`; `asof` is the
`YYYY-MM-DD` ticker mapping date used for renamed symbols.

Timeframes are `1`–`59Min`, `1`–`23Hour`, `1Day`, `1Week`, or
`1/2/3/4/6/12Month`. The client — and therefore the CLI — strips surrounding
whitespace and normalizes ASCII leading zeros and unit case; ` 015min `
becomes `15Min`. Shorthand such as `5T`, `1H`, and `1D` is rejected.
Adjustments are `raw`, `split`, `dividend`, or `all`.

Alpaca's historical `limit` is total across all symbols. Results are sorted by
symbol before timestamp, so a small limit can contain only the first symbol.
The client follows `next_page_token` until the requested total is collected.
Use bounded windows without a limit, or query symbols separately, when replay
coverage must be balanced.

Normalized dictionaries retain unknown wire fields. Bars expose `timestamp`,
OHLC, `volume`, `trade_count`, and `vwap`; quotes expose bid/ask price, size,
exchange, conditions, and tape; trades expose timestamp, price, size,
exchange, ID, conditions, and tape.

Historical methods accept `iex`, `sip`, `otc`, or `boats`. Latest methods also
accept `delayed_sip` and `overnight`. Live streams accept only `iex` or `sip`.
Do not silently fall back between feeds because that changes strategy inputs.

## One connection for multiple symbols

`stream_events(symbols, channels)` opens one authenticated stock connection
and sends one combined subscription containing every requested symbol for
every requested channel. Retained channels are `bars`, `updated_bars`,
`quotes`, `trades`, and `trading_statuses`; every yielded event includes its
`symbol` and normalized `channel`.

```python
import asyncio
from strategy.clients.alpaca import AlpacaMarketDataClient

async def watch():
    client = AlpacaMarketDataClient(feed="iex")
    async for event in client.stream_events(
        ["SPY", "MSFT"], ["bars", "updated_bars", "trading_statuses"]
    ):
        print(event["symbol"], event["channel"])

asyncio.run(watch())
```

Most users may have only one active Alpaca stock-data connection, and symbol
limits depend on the subscription. The client never opens extra sockets or
silently shards a request. Provider errors such as symbol-limit, connection-
limit, or slow-client failures surface as `AlpacaMarketDataError`; revise the
subscription deliberately. `StrategyRunner` owns bounded reconnect/backoff
and state restoration after disconnects.

Use `updated_bars` when late trades matter and `trading_statuses` to stop
decisions during halts. The blocking `stream(symbols, channels, handler)` uses
the same single connection and accepts sync or async handlers.

## CLI

```bash
python -m scripts.market_data alpaca bars SPY MSFT --timeframe 15Min --limit 200
python -m scripts.market_data alpaca historical-quotes SPY MSFT --limit 100
python -m scripts.market_data alpaca historical-trades SPY MSFT --limit 100
python -m scripts.market_data alpaca latest-quotes SPY MSFT
python -m scripts.market_data alpaca latest-trades SPY MSFT
python -m scripts.market_data alpaca latest-bars SPY MSFT
python -m scripts.market_data alpaca stream SPY MSFT \
  --channel bars --channel updated_bars --channel trading_statuses
```

Put `--feed` before the command to override the environment for one invocation.
`stream` subscribes to `bars` when no `--channel` is given. HTTP failures,
malformed responses, and WebSocket errors raise `AlpacaMarketDataError`; CLI
failures print `error:` and return status 1.

HTTP 429 raises `AlpacaMarketDataError`; apply bounded backoff and do not
tight-poll — for sub-minute cadence use the stream. All operations here are
read-only and safe to retry.

Snapshots, auctions, screeners, news, corporate actions, account data, assets,
calendars, clocks, positions, and orders are intentionally out of scope.
