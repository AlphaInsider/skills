"""Inspect the direct Alpaca equities market-data integration.

Usage: ``python -m scripts.market_data alpaca <command>``. Commands need
``ALPACA_KEY`` / ``ALPACA_SECRET``.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .alpaca import (
    STOCK_STREAM_CHANNELS,
    AlpacaMarketDataClient,
    AlpacaMarketDataError,
    MissingAlpacaCredentials,
)


def _add_history_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("symbols", nargs="+")
    parser.add_argument("--start", help="inclusive RFC 3339 start")
    parser.add_argument("--end", help="inclusive RFC 3339 end")
    parser.add_argument("--limit", type=int, help="total across all symbols")
    parser.add_argument("--sort", choices=["asc", "desc"])
    parser.add_argument("--asof", help="YYYY-MM-DD ticker-symbol mapping date")
    parser.add_argument("--currency", help="ISO 4217 response currency")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="market-data alpaca", description="Inspect direct Alpaca equities market data"
    )
    parser.add_argument("--feed", help="overrides ALPACA_FEED for this command")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bars = subparsers.add_parser("bars", help="historical stock bars")
    _add_history_arguments(bars)
    bars.add_argument("--timeframe", default="1Day", help="e.g. 1Min, 15Min, 1Hour")
    bars.add_argument("--adjustment", choices=["raw", "split", "dividend", "all"])

    historical_quotes = subparsers.add_parser(
        "historical-quotes", help="historical bid/ask quotes"
    )
    _add_history_arguments(historical_quotes)

    historical_trades = subparsers.add_parser(
        "historical-trades", help="historical stock trades"
    )
    _add_history_arguments(historical_trades)

    for command in ("latest-quotes", "latest-trades", "latest-bars"):
        latest = subparsers.add_parser(command, help=command.replace("-", " "))
        latest.add_argument("symbols", nargs="+")
        latest.add_argument("--currency")

    stream = subparsers.add_parser("stream", help="live stock streams")
    stream.add_argument("symbols", nargs="+")
    stream.add_argument("--channel", action="append", choices=STOCK_STREAM_CHANNELS)

    return parser


def _print(result: Any) -> None:
    print(json.dumps(result, indent=2, default=str))


def _history_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "start": args.start,
        "end": args.end,
        "limit": args.limit,
        "sort": args.sort,
        "asof": args.asof,
        "currency": args.currency,
    }


def _run(args: argparse.Namespace, client: AlpacaMarketDataClient | None) -> int:
    client = client or AlpacaMarketDataClient(feed=args.feed)
    if args.command == "bars":
        _print(
            client.get_bars(
                args.symbols,
                args.timeframe,
                adjustment=args.adjustment,
                **_history_kwargs(args),
            )
        )
    elif args.command == "historical-quotes":
        _print(client.get_quotes(args.symbols, **_history_kwargs(args)))
    elif args.command == "historical-trades":
        _print(client.get_trades(args.symbols, **_history_kwargs(args)))
    elif args.command == "latest-quotes":
        _print(client.get_latest_quotes(args.symbols, currency=args.currency))
    elif args.command == "latest-trades":
        _print(client.get_latest_trades(args.symbols, currency=args.currency))
    elif args.command == "latest-bars":
        _print(client.get_latest_bars(args.symbols, currency=args.currency))
    elif args.command == "stream":
        client.stream(args.symbols, args.channel or ["bars"], _print)
    return 0


def main(
    argv: list[str] | None = None,
    *,
    client: AlpacaMarketDataClient | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    try:
        return _run(args, client)
    except (MissingAlpacaCredentials, AlpacaMarketDataError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
