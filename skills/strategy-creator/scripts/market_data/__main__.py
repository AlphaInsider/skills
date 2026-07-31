"""Dispatch ``python -m scripts.market_data <provider> <command>`` to the
selected provider's standalone CLI without importing the other provider."""

import sys


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    provider, rest = (argv[0], argv[1:]) if argv else (None, [])
    if provider == "alpaca":
        from .alpaca_cli import main as provider_main
    elif provider == "coinbase":
        from .coinbase_cli import main as provider_main
    else:
        print(
            "usage: python -m scripts.market_data {alpaca,coinbase} <command> …",
            file=sys.stderr,
        )
        return 2
    return provider_main(rest)


raise SystemExit(main())
