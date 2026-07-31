"""Lazy provider facade: importing one provider's symbols never imports the
other provider's module. Generated workspaces do not use this package; they
receive the self-contained provider file as ``strategy/clients/<provider>.py``.
"""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "AlpacaMarketDataClient": "alpaca",
    "AlpacaMarketDataError": "alpaca",
    "MissingAlpacaCredentials": "alpaca",
    "CoinbaseMarketDataClient": "coinbase",
    "CoinbaseMarketDataError": "coinbase",
    "CoinbaseOutOfOrderError": "coinbase",
    "CoinbaseSequenceError": "coinbase",
    "CoinbaseSequenceGapError": "coinbase",
    "CoinbaseSequenceTracker": "coinbase",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str) -> Any:
    try:
        submodule = _EXPORTS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    return getattr(import_module(f".{submodule}", __name__), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
