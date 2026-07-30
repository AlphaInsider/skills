"""Coinbase Advanced Trade *public* market data client.

Unauthenticated REST and WebSocket endpoints only: products, candles, market
trades, order books, and public stream channels. Coinbase accounts, orders,
and authenticated user channels are deliberately excluded — AlphaInsider is
the only order destination in this workspace.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, AsyncIterator, Callable, Iterable

import httpx

REST_BASE_URL = "https://api.coinbase.com/api/v3/brokerage/market"
WS_URL = "wss://advanced-trade-ws.coinbase.com"

PUBLIC_CHANNELS = frozenset(
    {"ticker", "ticker_batch", "candles", "market_trades", "level2", "status", "heartbeats"}
)

GRANULARITY_SECONDS = {
    "ONE_MINUTE": 60,
    "FIVE_MINUTE": 300,
    "FIFTEEN_MINUTE": 900,
    "THIRTY_MINUTE": 1800,
    "ONE_HOUR": 3600,
    "TWO_HOUR": 7200,
    "SIX_HOUR": 21600,
    "ONE_DAY": 86400,
}


class CoinbaseMarketDataError(Exception):
    """Coinbase public API returned an error response."""


def _unix_seconds(value: Any) -> str:
    if isinstance(value, datetime):
        return str(int(value.timestamp()))
    return str(int(value))


def _default_ws_connect(url: str):
    import websockets

    return websockets.connect(url)


class CoinbaseMarketDataClient:
    """List/get products, fetch candles/trades/books, and stream public channels."""

    def __init__(
        self,
        *,
        base_url: str = REST_BASE_URL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        ws_connect: Callable[[str], Any] | None = None,
    ):
        self._client = httpx.Client(base_url=base_url, timeout=timeout, transport=transport)
        self._ws_connect = ws_connect or _default_ws_connect

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CoinbaseMarketDataClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._client.get(
            path, params={k: v for k, v in (params or {}).items() if v is not None}
        )
        if response.status_code == 429:
            raise CoinbaseMarketDataError("rate limit reached; back off before retrying")
        if response.status_code >= 400:
            raise CoinbaseMarketDataError(
                f"HTTP {response.status_code} from {path}: {response.text}"
            )
        return response.json()

    # -- REST (public, no credentials) ----------------------------------------

    def list_products(
        self, *, limit: int | None = None, product_type: str | None = None
    ) -> dict[str, Any]:
        """All tradable products; optionally filter (e.g. product_type=SPOT)."""
        return self._get("/products", {"limit": limit, "product_type": product_type})

    def get_product(self, product_id: str) -> dict[str, Any]:
        """A single product, e.g. BTC-USD."""
        return self._get(f"/products/{product_id}")

    def get_candles(
        self, product_id: str, granularity: str, start: Any, end: Any
    ) -> dict[str, Any]:
        """OHLCV candles. ``start``/``end`` accept UNIX seconds or datetimes;
        Coinbase caps a request at 350 candles."""
        if granularity not in GRANULARITY_SECONDS:
            raise ValueError(
                f"granularity must be one of {sorted(GRANULARITY_SECONDS)}, got {granularity!r}"
            )
        return self._get(
            f"/products/{product_id}/candles",
            {
                "start": _unix_seconds(start),
                "end": _unix_seconds(end),
                "granularity": granularity,
            },
        )

    def get_market_trades(self, product_id: str, *, limit: int | None = None) -> dict[str, Any]:
        """Recent public trades (the product ticker endpoint)."""
        return self._get(f"/products/{product_id}/ticker", {"limit": limit})

    def get_product_book(self, product_id: str, *, limit: int | None = None) -> dict[str, Any]:
        """Public order book snapshot (bids/asks)."""
        return self._get("/product_book", {"product_id": product_id, "limit": limit})

    # -- WebSocket (public channels only) --------------------------------------

    async def stream(
        self,
        channels: Iterable[str],
        product_ids: Iterable[str],
        *,
        heartbeats: bool = True,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator of parsed messages from public channels
        (ticker, ticker_batch, candles, market_trades, level2, status).

        Subscribes to ``heartbeats`` by default so Coinbase keeps the
        connection open through quiet markets. Reconnection is the caller's
        responsibility (see scripts.strategy_runtime.StrategyRunner).
        """
        requested = list(channels)
        for channel in requested:
            if channel not in PUBLIC_CHANNELS:
                raise ValueError(
                    f"channel {channel!r} is not a public market-data channel; "
                    "authenticated Coinbase channels are excluded from this workspace"
                )
        if heartbeats and "heartbeats" not in requested:
            requested.append("heartbeats")
        product_ids = list(product_ids)
        async with self._ws_connect(WS_URL) as connection:
            # Coinbase requires one subscribe message per channel.
            for channel in requested:
                message: dict[str, Any] = {"type": "subscribe", "channel": channel}
                if channel != "heartbeats":
                    message["product_ids"] = product_ids
                await connection.send(json.dumps(message))
            async for raw in connection:
                yield json.loads(raw)
