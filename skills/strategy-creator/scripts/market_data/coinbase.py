"""Coinbase Advanced Trade unauthenticated market-data client.

Only public REST endpoints and public WebSocket channels are implemented.
Coinbase account, portfolio, order, and authenticated user APIs are excluded;
AlphaInsider remains the only order destination in generated workspaces.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, AsyncIterator, Callable, Iterable, Iterator

import httpx

REST_BASE_URL = "https://api.coinbase.com/api/v3/brokerage/market"
WS_URL = "wss://advanced-trade-ws.coinbase.com"

PUBLIC_CHANNELS = frozenset(
    {
        "ticker",
        "ticker_batch",
        "candles",
        "market_trades",
        "level2",
        "status",
        "heartbeats",
    }
)
_INCOMING_CHANNELS = {"l2_data": "level2"}

GRANULARITY_SECONDS = {
    "ONE_MINUTE": 60,
    "FIVE_MINUTE": 300,
    "FIFTEEN_MINUTE": 900,
    "THIRTY_MINUTE": 1800,
    "ONE_HOUR": 3600,
    "TWO_HOUR": 7200,
    "FOUR_HOUR": 14400,
    "SIX_HOUR": 21600,
    "ONE_DAY": 86400,
}


class CoinbaseMarketDataError(Exception):
    """Coinbase public API returned an error response."""


class CoinbaseSequenceError(CoinbaseMarketDataError):
    """A WebSocket feed sequence is incomplete or out of order."""


class CoinbaseSequenceGapError(CoinbaseSequenceError):
    """One or more WebSocket messages were dropped."""


class CoinbaseOutOfOrderError(CoinbaseSequenceError):
    """A duplicate or out-of-order WebSocket message was received."""


def _unix_seconds(value: Any) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("datetime values must include a timezone")
        return str(int(value.timestamp()))
    return str(int(value))


def _product_ids(values: Iterable[str] | str) -> list[str]:
    product_ids = [values] if isinstance(values, str) else list(values)
    if not product_ids or any(
        not isinstance(product_id, str) or not product_id.strip()
        for product_id in product_ids
    ):
        raise ValueError("at least one non-empty Coinbase product ID is required")
    return product_ids


class CoinbaseSequenceTracker:
    """Validate the single per-connection Coinbase ``sequence_num`` counter."""

    def __init__(self) -> None:
        self._last: int | None = None
        self._last_heartbeat: int | None = None

    def observe(self, message: dict[str, Any]) -> None:
        # ``sequence_num`` is one monotonic counter for the whole connection;
        # every message — including heartbeats and subscription
        # acknowledgements — consumes one number.
        sequence = message.get("sequence_num")
        if sequence is not None:
            try:
                sequence = int(sequence)
            except (TypeError, ValueError) as exc:
                raise CoinbaseSequenceError(
                    f"invalid Coinbase sequence_num {sequence!r}"
                ) from exc
            self._validate(self._last, sequence, "the connection")
            self._last = sequence

        if message.get("channel") == "heartbeats":
            self._observe_heartbeat(message)

    def _observe_heartbeat(self, message: dict[str, Any]) -> None:
        for event in message.get("events", []):
            if not isinstance(event, dict) or "heartbeat_counter" not in event:
                continue
            value = event["heartbeat_counter"]
            try:
                heartbeat = int(value)
            except (TypeError, ValueError) as exc:
                raise CoinbaseSequenceError(
                    f"invalid Coinbase heartbeat_counter {value!r}"
                ) from exc
            self._validate(self._last_heartbeat, heartbeat, "heartbeats")
            self._last_heartbeat = heartbeat

    @staticmethod
    def _validate(previous: int | None, current: int, scope: str) -> None:
        if previous is not None and current > previous + 1:
            raise CoinbaseSequenceGapError(
                f"Coinbase sequence jumped from {previous} to {current} for {scope}; "
                "refresh state before trading"
            )
        if previous is not None and current <= previous:
            raise CoinbaseOutOfOrderError(
                f"Coinbase sequence moved from {previous} to {current} for {scope}; "
                "refresh state before trading"
            )


def _default_ws_connect(url: str):
    import websockets

    return websockets.connect(url)


class CoinbaseMarketDataClient:
    """Complete public Coinbase market-data REST and WebSocket surface."""

    def __init__(
        self,
        *,
        base_url: str = REST_BASE_URL,
        ws_url: str = WS_URL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        ws_connect: Callable[[str], Any] | None = None,
    ):
        self._client = httpx.Client(base_url=base_url, timeout=timeout, transport=transport)
        self._ws_url = ws_url
        self._ws_connect = ws_connect or _default_ws_connect

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CoinbaseMarketDataClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._client.get(
            path, params={key: value for key, value in (params or {}).items() if value is not None}
        )
        if response.status_code == 429:
            raise CoinbaseMarketDataError("rate limit reached; back off before retrying")
        if response.status_code >= 400:
            raise CoinbaseMarketDataError(
                f"HTTP {response.status_code} from {path}: {response.text}"
            )
        try:
            return response.json()
        except ValueError as exc:
            raise CoinbaseMarketDataError(
                f"Coinbase returned non-JSON data from {path}"
            ) from exc

    # -- REST (public, no credentials) -------------------------------------

    def get_server_time(self) -> dict[str, Any]:
        """Coinbase epoch and ISO server time for clock-skew checks."""
        # Resolves against the ``…/market`` base URL to /api/v3/brokerage/time.
        return self._get("../time")

    def list_products(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        product_type: str | None = None,
        product_ids: Iterable[str] | str | None = None,
        contract_expiry_type: str | None = None,
        expiring_contract_status: str | None = None,
        get_all_products: bool | None = None,
        products_sort_order: str | None = None,
        cursor: str | None = None,
        futures_underlying_type: str | None = None,
        user_country_code: str | None = None,
        expired: bool | None = None,
    ) -> dict[str, Any]:
        """List products with every public endpoint filter and page control."""
        requested_ids = None if product_ids is None else _product_ids(product_ids)
        return self._get(
            "/products",
            {
                "limit": limit,
                "offset": offset,
                "product_type": product_type,
                "product_ids": requested_ids,
                "contract_expiry_type": contract_expiry_type,
                "expiring_contract_status": expiring_contract_status,
                "get_all_products": get_all_products,
                "products_sort_order": products_sort_order,
                "cursor": cursor,
                "futures_underlying_type": futures_underlying_type,
                "user_country_code": user_country_code,
                "expired": expired,
            },
        )

    def iter_products(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Yield products across ``next_cursor`` pages without duplicates."""
        cursor = filters.pop("cursor", None)
        seen_cursors: set[str] = set()
        seen_products: set[str] = set()
        while True:
            response = self.list_products(cursor=cursor, **filters)
            for product in response.get("products", []):
                product_id = product.get("product_id")
                if product_id is None or product_id not in seen_products:
                    if product_id is not None:
                        seen_products.add(product_id)
                    yield product
            pagination = response.get("pagination")
            cursor = response.get("next_cursor")
            if cursor is None and isinstance(pagination, dict):
                cursor = pagination.get("next_cursor")
            if not cursor:
                return
            if cursor in seen_cursors:
                raise CoinbaseMarketDataError("Coinbase repeated a product pagination cursor")
            seen_cursors.add(cursor)
            filters.pop("offset", None)

    def get_product(self, product_id: str) -> dict[str, Any]:
        """Get one public product such as ``BTC-USD``."""
        return self._get(f"/products/{_product_ids(product_id)[0]}")

    def get_candles(
        self,
        product_id: str,
        granularity: str,
        start: Any,
        end: Any,
        *,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Get one page of OHLCV candles; Coinbase caps pages at 350."""
        if granularity not in GRANULARITY_SECONDS:
            raise ValueError(
                f"granularity must be one of {sorted(GRANULARITY_SECONDS)}, "
                f"got {granularity!r}"
            )
        if limit is not None and not 1 <= limit <= 350:
            raise ValueError("candle limit must be between 1 and 350")
        return self._get(
            f"/products/{_product_ids(product_id)[0]}/candles",
            {
                "start": _unix_seconds(start),
                "end": _unix_seconds(end),
                "granularity": granularity,
                "limit": limit,
            },
        )

    def get_market_trades(
        self,
        product_id: str,
        *,
        limit: int | None = None,
        start: Any | None = None,
        end: Any | None = None,
    ) -> dict[str, Any]:
        """Get public trades and best bid/ask, optionally for a replay window."""
        return self._get(
            f"/products/{_product_ids(product_id)[0]}/ticker",
            {
                "limit": limit,
                "start": None if start is None else _unix_seconds(start),
                "end": None if end is None else _unix_seconds(end),
            },
        )

    def get_product_book(
        self,
        product_id: str,
        *,
        limit: int | None = None,
        aggregation_price_increment: str | None = None,
    ) -> dict[str, Any]:
        """Get a public bid/ask snapshot, optionally aggregated by price."""
        return self._get(
            "/product_book",
            {
                "product_id": _product_ids(product_id)[0],
                "limit": limit,
                "aggregation_price_increment": aggregation_price_increment,
            },
        )

    # -- WebSocket (public channels only) ----------------------------------

    async def stream(
        self,
        channels: Iterable[str] | str,
        product_ids: Iterable[str] | str,
        *,
        heartbeats: bool = True,
        validate_sequence: bool = True,
    ) -> AsyncIterator[dict[str, Any]]:
        """Yield all requested products over one public market-data connection.

        Subscribe to ``ticker``, ``ticker_batch``, ``candles``,
        ``market_trades``, ``level2``, ``status``, and/or ``heartbeats``.
        Reconnection and REST resynchronization remain the caller's job.
        """
        requested = [channels] if isinstance(channels, str) else list(channels)
        requested = list(dict.fromkeys(requested))
        for channel in requested:
            if channel not in PUBLIC_CHANNELS:
                raise ValueError(
                    f"channel {channel!r} is not a public market-data channel; "
                    "authenticated Coinbase channels are excluded"
                )
        if not requested:
            raise ValueError("at least one Coinbase stream channel is required")
        if heartbeats and "heartbeats" not in requested:
            requested.append("heartbeats")

        data_channels = [channel for channel in requested if channel != "heartbeats"]
        requested_products = _product_ids(product_ids) if data_channels else []
        tracker = CoinbaseSequenceTracker()

        async with self._ws_connect(self._ws_url) as connection:
            for channel in requested:
                message: dict[str, Any] = {"type": "subscribe", "channel": channel}
                if channel != "heartbeats":
                    message["product_ids"] = requested_products
                await connection.send(json.dumps(message))

            async for raw in connection:
                try:
                    message = json.loads(raw)
                except (TypeError, json.JSONDecodeError) as exc:
                    raise CoinbaseMarketDataError(
                        "Coinbase WebSocket returned malformed JSON"
                    ) from exc
                if not isinstance(message, dict):
                    raise CoinbaseMarketDataError(
                        "Coinbase WebSocket returned a non-object message"
                    )
                if message.get("type") == "error" or message.get("channel") == "error":
                    detail = message.get("message") or message.get("error") or message
                    raise CoinbaseMarketDataError(f"Coinbase WebSocket error: {detail}")
                channel = message.get("channel")
                normalized_channel = _INCOMING_CHANNELS.get(channel, channel)
                if normalized_channel != channel:
                    message = {**message, "channel": normalized_channel}
                if validate_sequence:
                    tracker.observe(message)
                if message.get("channel") not in requested:
                    continue
                yield message
