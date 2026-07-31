"""Inspect the direct Coinbase public crypto market-data integration.

Usage: ``python -m scripts.market_data coinbase <command>``. Commands need
no credentials.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from typing import Any

from .coinbase import (
    GRANULARITY_SECONDS,
    PUBLIC_CHANNELS,
    CoinbaseMarketDataClient,
    CoinbaseMarketDataError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="market-data coinbase",
        description="Inspect direct Coinbase public market data",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("time", help="Coinbase server time")

    products = subparsers.add_parser("products", help="list and filter products")
    products.add_argument("--limit", type=int)
    products.add_argument("--offset", type=int)
    products.add_argument("--product-type")
    products.add_argument("--product-id", action="append", dest="product_ids")
    products.add_argument("--contract-expiry-type")
    products.add_argument("--expiring-contract-status")
    products.add_argument("--get-all-products", action="store_true", default=None)
    products.add_argument("--products-sort-order")
    products.add_argument("--cursor")
    products.add_argument("--futures-underlying-type")
    products.add_argument("--user-country-code")
    products.add_argument("--expired", action="store_true", default=None)
    products.add_argument("--all-pages", action="store_true")

    product = subparsers.add_parser("product", help="one product")
    product.add_argument("product_id", help="e.g. BTC-USD")

    candles = subparsers.add_parser("candles", help="OHLCV candles")
    candles.add_argument("product_id")
    candles.add_argument("--granularity", default="ONE_HOUR", choices=sorted(GRANULARITY_SECONDS))
    candles.add_argument("--start", type=int, help="UNIX seconds (default: 300 candles back)")
    candles.add_argument("--end", type=int, help="UNIX seconds (default: now)")
    candles.add_argument("--limit", type=int)

    trades = subparsers.add_parser("trades", help="public market trades")
    trades.add_argument("product_id")
    trades.add_argument("--limit", type=int, default=10)
    trades.add_argument("--start", type=int)
    trades.add_argument("--end", type=int)

    book = subparsers.add_parser("book", help="public order book")
    book.add_argument("product_id")
    book.add_argument("--limit", type=int)
    book.add_argument("--aggregation-price-increment")

    stream = subparsers.add_parser("stream", help="public WebSocket channels")
    stream.add_argument("product_ids", nargs="+")
    stream.add_argument(
        "--channel",
        action="append",
        choices=sorted(PUBLIC_CHANNELS - {"heartbeats"}),
    )
    stream.add_argument("--no-heartbeats", action="store_false", dest="heartbeats")
    stream.add_argument(
        "--no-sequence-validation", action="store_false", dest="validate_sequence"
    )
    stream.add_argument("--limit", type=int, help="stop after N messages")
    stream.set_defaults(heartbeats=True, validate_sequence=True)

    return parser


def _print(result: Any) -> None:
    print(json.dumps(result, indent=2, default=str))


def _product_filters(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "limit": args.limit,
        "offset": args.offset,
        "product_type": args.product_type,
        "product_ids": args.product_ids,
        "contract_expiry_type": args.contract_expiry_type,
        "expiring_contract_status": args.expiring_contract_status,
        "get_all_products": args.get_all_products,
        "products_sort_order": args.products_sort_order,
        "cursor": args.cursor,
        "futures_underlying_type": args.futures_underlying_type,
        "user_country_code": args.user_country_code,
        "expired": args.expired,
    }


def _run(args: argparse.Namespace, client: CoinbaseMarketDataClient | None) -> int:
    client = client or CoinbaseMarketDataClient()
    if args.command == "time":
        _print(client.get_server_time())
    elif args.command == "products":
        filters = _product_filters(args)
        if args.all_pages:
            _print(list(client.iter_products(**filters)))
        else:
            _print(client.list_products(**filters))
    elif args.command == "product":
        _print(client.get_product(args.product_id))
    elif args.command == "candles":
        end = args.end if args.end is not None else int(time.time())
        start = (
            args.start
            if args.start is not None
            else end - 300 * GRANULARITY_SECONDS[args.granularity]
        )
        _print(
            client.get_candles(
                args.product_id,
                args.granularity,
                start,
                end,
                limit=args.limit,
            )
        )
    elif args.command == "trades":
        _print(
            client.get_market_trades(
                args.product_id,
                limit=args.limit,
                start=args.start,
                end=args.end,
            )
        )
    elif args.command == "book":
        _print(
            client.get_product_book(
                args.product_id,
                limit=args.limit,
                aggregation_price_increment=args.aggregation_price_increment,
            )
        )
    elif args.command == "stream":

        async def consume() -> None:
            count = 0
            async for message in client.stream(
                args.channel or ["ticker"],
                args.product_ids,
                heartbeats=args.heartbeats,
                validate_sequence=args.validate_sequence,
            ):
                _print(message)
                count += 1
                if args.limit is not None and count >= args.limit:
                    break

        asyncio.run(consume())
    return 0


def main(
    argv: list[str] | None = None,
    *,
    client: CoinbaseMarketDataClient | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    try:
        return _run(args, client)
    except (CoinbaseMarketDataError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
