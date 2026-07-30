"""Market-data CLI for inspecting either provider before writing strategy code.

Usage: ``python -m scripts.market_data <provider> <command>`` (or
``market-data`` when installed). Coinbase commands need no credentials;
Alpaca commands need ``ALPACA_KEY`` / ``ALPACA_SECRET``.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from typing import Any

from .alpaca import AlpacaMarketDataClient, MissingAlpacaCredentials
from .coinbase import (
    GRANULARITY_SECONDS,
    CoinbaseMarketDataClient,
    CoinbaseMarketDataError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="market-data", description="Inspect market data")
    provider = parser.add_subparsers(dest="provider", required=True)

    alpaca = provider.add_parser("alpaca", help="Alpaca equities market data")
    alpaca_sub = alpaca.add_subparsers(dest="command", required=True)

    bars = alpaca_sub.add_parser("bars", help="recent/historical stock bars")
    bars.add_argument("symbols", nargs="+")
    bars.add_argument("--timeframe", default="1Day", help="e.g. 1Min, 15Min, 1Hour, 1Day")
    bars.add_argument("--start", help="ISO 8601 start")
    bars.add_argument("--end", help="ISO 8601 end")
    bars.add_argument("--limit", type=int)

    quotes = alpaca_sub.add_parser("quotes", help="latest quotes")
    quotes.add_argument("symbols", nargs="+")

    alpaca_stream = alpaca_sub.add_parser("stream", help="live bars/quotes/trades (Ctrl+C to stop)")
    alpaca_stream.add_argument("symbols", nargs="+")
    alpaca_stream.add_argument("--channel", default="bars", choices=["bars", "quotes", "trades"])

    coinbase = provider.add_parser("coinbase", help="Coinbase public crypto market data")
    coinbase_sub = coinbase.add_subparsers(dest="command", required=True)

    products = coinbase_sub.add_parser("products", help="list products")
    products.add_argument("--limit", type=int)
    products.add_argument("--product-type", choices=["SPOT", "FUTURE"])

    product = coinbase_sub.add_parser("product", help="one product")
    product.add_argument("product_id", help="e.g. BTC-USD")

    candles = coinbase_sub.add_parser("candles", help="OHLCV candles")
    candles.add_argument("product_id")
    candles.add_argument("--granularity", default="ONE_HOUR", choices=sorted(GRANULARITY_SECONDS))
    candles.add_argument("--start", type=int, help="UNIX seconds (default: 300 candles back)")
    candles.add_argument("--end", type=int, help="UNIX seconds (default: now)")

    trades = coinbase_sub.add_parser("trades", help="recent market trades")
    trades.add_argument("product_id")
    trades.add_argument("--limit", type=int, default=10)

    book = coinbase_sub.add_parser("book", help="public order book")
    book.add_argument("product_id")
    book.add_argument("--limit", type=int)

    cb_stream = coinbase_sub.add_parser("stream", help="public WebSocket channels")
    cb_stream.add_argument("product_ids", nargs="+")
    cb_stream.add_argument(
        "--channel",
        default="ticker",
        choices=["ticker", "ticker_batch", "candles", "market_trades", "level2", "status"],
    )
    cb_stream.add_argument("--limit", type=int, help="stop after N messages (default: run forever)")

    return parser


def _print(result: Any) -> None:
    print(json.dumps(result, indent=2, default=str))


def _run_alpaca(args: argparse.Namespace, client: AlpacaMarketDataClient | None) -> int:
    client = client or AlpacaMarketDataClient()
    if args.command == "bars":
        _print(
            client.get_bars(
                args.symbols,
                args.timeframe,
                start=args.start,
                end=args.end,
                limit=args.limit,
            )
        )
    elif args.command == "quotes":
        _print(client.get_latest_quotes(args.symbols))
    elif args.command == "stream":
        client.stream(args.symbols, args.channel, lambda event: _print(event))
    return 0


def _run_coinbase(args: argparse.Namespace, client: CoinbaseMarketDataClient | None) -> int:
    client = client or CoinbaseMarketDataClient()
    if args.command == "products":
        _print(client.list_products(limit=args.limit, product_type=args.product_type))
    elif args.command == "product":
        _print(client.get_product(args.product_id))
    elif args.command == "candles":
        end = args.end if args.end is not None else int(time.time())
        start = (
            args.start
            if args.start is not None
            else end - 300 * GRANULARITY_SECONDS[args.granularity]
        )
        _print(client.get_candles(args.product_id, args.granularity, start, end))
    elif args.command == "trades":
        _print(client.get_market_trades(args.product_id, limit=args.limit))
    elif args.command == "book":
        _print(client.get_product_book(args.product_id, limit=args.limit))
    elif args.command == "stream":

        async def _consume() -> None:
            count = 0
            async for message in client.stream([args.channel], args.product_ids):
                _print(message)
                count += 1
                if args.limit is not None and count >= args.limit:
                    break

        asyncio.run(_consume())
    return 0


def main(
    argv: list[str] | None = None,
    *,
    alpaca_client: AlpacaMarketDataClient | None = None,
    coinbase_client: CoinbaseMarketDataClient | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.provider == "alpaca":
            return _run_alpaca(args, alpaca_client)
        return _run_coinbase(args, coinbase_client)
    except (MissingAlpacaCredentials, CoinbaseMarketDataError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
