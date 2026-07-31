"""Direct, read-only Alpaca equities market-data client.

The implementation uses Alpaca REST and WebSocket protocols directly. It does
not import a vendor SDK or any trading API, and it never submits broker orders.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
import re
from datetime import date, datetime
from typing import Any, AsyncIterator, Callable, Iterable

import httpx
from dotenv import find_dotenv, load_dotenv

REST_BASE_URL = "https://data.alpaca.markets"
STOCK_WS_BASE_URL = "wss://stream.data.alpaca.markets/v2"

_TIMEFRAME_PATTERN = re.compile(r"([0-9]+)(min|hour|day|week|month)", re.IGNORECASE)
_TIMEFRAME_VALUES = {
    "min": range(1, 60),
    "hour": range(1, 24),
    "day": {1},
    "week": {1},
    "month": {1, 2, 3, 4, 6, 12},
}
_TIMEFRAME_UNITS = {
    "min": "Min",
    "hour": "Hour",
    "day": "Day",
    "week": "Week",
    "month": "Month",
}
_HISTORICAL_FEEDS = {"iex", "otc", "sip", "boats"}
_LATEST_FEEDS = _HISTORICAL_FEEDS | {"delayed_sip", "overnight"}
STOCK_STREAM_CHANNELS = (
    "bars",
    "updated_bars",
    "quotes",
    "trades",
    "trading_statuses",
)

_BAR_FIELDS = {
    "t": "timestamp",
    "o": "open",
    "h": "high",
    "l": "low",
    "c": "close",
    "v": "volume",
    "n": "trade_count",
    "vw": "vwap",
}
_QUOTE_FIELDS = {
    "t": "timestamp",
    "ax": "ask_exchange",
    "ap": "ask_price",
    "as": "ask_size",
    "bx": "bid_exchange",
    "bp": "bid_price",
    "bs": "bid_size",
    "c": "conditions",
    "z": "tape",
}
_TRADE_FIELDS = {
    "t": "timestamp",
    "p": "price",
    "s": "size",
    "x": "exchange",
    "i": "id",
    "c": "conditions",
    "z": "tape",
}
_STATUS_FIELDS = {
    "t": "timestamp",
    "sc": "status_code",
    "sm": "status_message",
    "rc": "reason_code",
    "rm": "reason_message",
    "z": "tape",
}
_EVENT_CHANNELS = {
    "b": ("bars", _BAR_FIELDS),
    "u": ("updated_bars", _BAR_FIELDS),
    "q": ("quotes", _QUOTE_FIELDS),
    "t": ("trades", _TRADE_FIELDS),
    "s": ("trading_statuses", _STATUS_FIELDS),
}
_SUBSCRIPTION_KEYS = {
    "bars": "bars",
    "updated_bars": "updatedBars",
    "quotes": "quotes",
    "trades": "trades",
    "trading_statuses": "statuses",
}


def load_env() -> None:
    """Load working-directory ``.env`` values without overriding the process."""
    load_dotenv(find_dotenv(usecwd=True))


class MissingAlpacaCredentials(Exception):
    """``ALPACA_KEY`` / ``ALPACA_SECRET`` are not configured."""


class AlpacaMarketDataError(Exception):
    """Alpaca returned an invalid or unsuccessful market-data response."""


def _default_ws_connect(url: str):
    import websockets

    return websockets.connect(url)


def _symbols(values: Iterable[str] | str) -> list[str]:
    symbols = [values] if isinstance(values, str) else list(values)
    if not symbols or any(not isinstance(symbol, str) or not symbol.strip() for symbol in symbols):
        raise ValueError("at least one non-empty Alpaca symbol is required")
    return symbols


def _wire_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, bool):
        return str(value).lower()
    return value


def _validate_choice(value: str | None, choices: set[str], label: str) -> str | None:
    if value is not None and value not in choices:
        raise ValueError(f"{label} must be one of {sorted(choices)}, got {value!r}")
    return value


def _normalize_timeframe(value: str) -> str:
    match = _TIMEFRAME_PATTERN.fullmatch(value.strip())
    if match is not None:
        amount = int(match.group(1))
        unit = match.group(2).lower()
        if amount in _TIMEFRAME_VALUES[unit]:
            return f"{amount}{_TIMEFRAME_UNITS[unit]}"
    raise ValueError(
        f"invalid timeframe {value!r}; use 1-59Min, 1-23Hour, 1Day, "
        "1Week, or 1/2/3/4/6/12Month"
    )


def _normalize_fields(payload: dict[str, Any], fields: dict[str, str]) -> dict[str, Any]:
    return {fields.get(key, key): value for key, value in payload.items()}


def _decode_ws_message(raw: Any) -> list[dict[str, Any]]:
    try:
        payload = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AlpacaMarketDataError("Alpaca WebSocket returned malformed JSON") from exc
    messages = payload if isinstance(payload, list) else [payload]
    if not all(isinstance(message, dict) for message in messages):
        raise AlpacaMarketDataError("Alpaca WebSocket returned a non-object message")
    return messages


class AlpacaMarketDataClient:
    """Direct Alpaca historical, latest, and streaming stock-data client."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        *,
        feed: str | None = None,
        base_url: str = REST_BASE_URL,
        stock_ws_base_url: str = STOCK_WS_BASE_URL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        ws_connect: Callable[[str], Any] | None = None,
    ):
        load_env()
        self.api_key = api_key or os.environ.get("ALPACA_KEY")
        self.api_secret = api_secret or os.environ.get("ALPACA_SECRET")
        if not self.api_key or not self.api_secret:
            raise MissingAlpacaCredentials(
                "set ALPACA_KEY and ALPACA_SECRET in the environment or .env"
            )
        self.feed = (feed or os.environ.get("ALPACA_FEED") or "iex").lower()
        _validate_choice(self.feed, _LATEST_FEEDS, "feed")
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.api_secret,
                "Accept": "application/json",
            },
            timeout=timeout,
            transport=transport,
        )
        self._stock_ws_base_url = stock_ws_base_url.rstrip("/")
        self._ws_connect = ws_connect or _default_ws_connect

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AlpacaMarketDataClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._client.get(
            path,
            params={
                key: _wire_value(value)
                for key, value in (params or {}).items()
                if value is not None
            },
        )
        if response.status_code == 429:
            raise AlpacaMarketDataError("rate limit reached; back off before retrying")
        if response.status_code >= 400:
            raise AlpacaMarketDataError(
                f"HTTP {response.status_code} from {path}: {response.text}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise AlpacaMarketDataError(
                f"Alpaca returned non-JSON data from {path}"
            ) from exc
        if not isinstance(payload, dict):
            raise AlpacaMarketDataError(f"Alpaca returned a non-object response from {path}")
        return payload

    def _symbol_pages(
        self,
        path: str,
        data_key: str,
        params: dict[str, Any],
        *,
        limit: int | None,
        page_size: int = 10_000,
        normalize: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:
        collected: dict[str, list[dict[str, Any]]] = {}
        page_token = params.pop("page_token", None)
        seen_tokens: set[str] = set()
        total = 0
        while True:
            current_limit = page_size if limit is None else min(page_size, limit - total)
            if current_limit < 1:
                break
            response = self._get(
                path,
                {**params, "limit": current_limit, "page_token": page_token},
            )
            page = response.get(data_key, {})
            if not isinstance(page, dict):
                raise AlpacaMarketDataError(f"Alpaca response omitted object field {data_key!r}")
            for symbol, items in page.items():
                collected.setdefault(symbol, []).extend(normalize(item) for item in items)
            total += sum(len(items) for items in page.values())
            page_token = response.get("next_page_token")
            if not page_token:
                break
            if page_token in seen_tokens:
                raise AlpacaMarketDataError(f"Alpaca repeated a {data_key} pagination token")
            seen_tokens.add(page_token)
        return collected

    def _historical_params(
        self,
        symbols: Iterable[str] | str,
        *,
        start: Any | None,
        end: Any | None,
        sort: str | None,
        asof: str | None,
        currency: str | None,
    ) -> dict[str, Any]:
        _validate_choice(self.feed, _HISTORICAL_FEEDS, "historical feed")
        _validate_choice(sort, {"asc", "desc"}, "sort")
        return {
            "symbols": ",".join(_symbols(symbols)),
            "start": start,
            "end": end,
            "sort": sort,
            "asof": asof,
            "currency": currency,
            "feed": self.feed,
        }

    def get_bars(
        self,
        symbols: Iterable[str] | str,
        timeframe: str = "1Day",
        *,
        start: Any | None = None,
        end: Any | None = None,
        limit: int | None = None,
        adjustment: str | None = None,
        sort: str | None = None,
        asof: str | None = None,
        currency: str | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        """Historical bars. ``limit`` is total across all requested symbols."""
        timeframe = _normalize_timeframe(timeframe)
        _validate_choice(adjustment, {"raw", "split", "dividend", "all"}, "adjustment")
        params = self._historical_params(
            symbols,
            start=start,
            end=end,
            sort=sort,
            asof=asof,
            currency=currency,
        )
        params.update({"timeframe": timeframe, "adjustment": adjustment})
        return self._symbol_pages(
            "/v2/stocks/bars",
            "bars",
            params,
            limit=limit,
            normalize=lambda item: _normalize_fields(item, _BAR_FIELDS),
        )

    def get_quotes(
        self,
        symbols: Iterable[str] | str,
        *,
        start: Any | None = None,
        end: Any | None = None,
        limit: int | None = None,
        sort: str | None = None,
        asof: str | None = None,
        currency: str | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        """Historical bid/ask quotes grouped by symbol."""
        params = self._historical_params(
            symbols,
            start=start,
            end=end,
            sort=sort,
            asof=asof,
            currency=currency,
        )
        return self._symbol_pages(
            "/v2/stocks/quotes",
            "quotes",
            params,
            limit=limit,
            normalize=lambda item: _normalize_fields(item, _QUOTE_FIELDS),
        )

    def get_trades(
        self,
        symbols: Iterable[str] | str,
        *,
        start: Any | None = None,
        end: Any | None = None,
        limit: int | None = None,
        sort: str | None = None,
        asof: str | None = None,
        currency: str | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        """Historical prints grouped by symbol."""
        params = self._historical_params(
            symbols,
            start=start,
            end=end,
            sort=sort,
            asof=asof,
            currency=currency,
        )
        return self._symbol_pages(
            "/v2/stocks/trades",
            "trades",
            params,
            limit=limit,
            normalize=lambda item: _normalize_fields(item, _TRADE_FIELDS),
        )

    def _latest(
        self,
        path: str,
        data_key: str,
        symbols: Iterable[str] | str,
        fields: dict[str, str],
        currency: str | None,
    ) -> dict[str, dict[str, Any]]:
        response = self._get(
            path,
            {
                "symbols": ",".join(_symbols(symbols)),
                "feed": _validate_choice(self.feed, _LATEST_FEEDS, "latest feed"),
                "currency": currency,
            },
        )
        data = response.get(data_key, {})
        if not isinstance(data, dict):
            raise AlpacaMarketDataError(f"Alpaca response omitted object field {data_key!r}")
        return {symbol: _normalize_fields(item, fields) for symbol, item in data.items()}

    def get_latest_quotes(
        self, symbols: Iterable[str] | str, *, currency: str | None = None
    ) -> dict[str, dict[str, Any]]:
        return self._latest(
            "/v2/stocks/quotes/latest", "quotes", symbols, _QUOTE_FIELDS, currency
        )

    def get_latest_trades(
        self, symbols: Iterable[str] | str, *, currency: str | None = None
    ) -> dict[str, dict[str, Any]]:
        return self._latest(
            "/v2/stocks/trades/latest", "trades", symbols, _TRADE_FIELDS, currency
        )

    def get_latest_bars(
        self, symbols: Iterable[str] | str, *, currency: str | None = None
    ) -> dict[str, dict[str, Any]]:
        return self._latest(
            "/v2/stocks/bars/latest", "bars", symbols, _BAR_FIELDS, currency
        )

    @staticmethod
    def _require_ws_success(messages: list[dict[str, Any]], expected: str) -> None:
        for message in messages:
            if message.get("T") == "error":
                raise AlpacaMarketDataError(
                    f"Alpaca WebSocket error {message.get('code')}: {message.get('msg')}"
                )
            if message.get("T") == "success" and message.get("msg") == expected:
                return
        raise AlpacaMarketDataError(
            f"Alpaca WebSocket did not confirm {expected!r}: {messages}"
        )

    async def stream_events(
        self,
        symbols: Iterable[str] | str,
        channels: Iterable[str] | str,
    ) -> AsyncIterator[dict[str, Any]]:
        """Yield all requested symbols from one authenticated stock connection."""
        requested = [channels] if isinstance(channels, str) else list(channels)
        requested = list(dict.fromkeys(requested))
        if not requested:
            raise ValueError("at least one Alpaca stream channel is required")
        unknown = [channel for channel in requested if channel not in STOCK_STREAM_CHANNELS]
        if unknown:
            raise ValueError(
                f"channels must be chosen from {STOCK_STREAM_CHANNELS}; got {unknown}"
            )
        if self.feed not in {"iex", "sip"}:
            raise ValueError("Alpaca stock streaming supports only the iex and sip feeds")

        requested_symbols = _symbols(symbols)
        subscription: dict[str, Any] = {"action": "subscribe"}
        for channel in requested:
            subscription[_SUBSCRIPTION_KEYS[channel]] = requested_symbols

        connection_context = self._ws_connect(f"{self._stock_ws_base_url}/{self.feed}")
        async with connection_context as connection:
            connected = _decode_ws_message(await connection.recv())
            self._require_ws_success(connected, "connected")
            await connection.send(
                json.dumps(
                    {"action": "auth", "key": self.api_key, "secret": self.api_secret}
                )
            )
            authenticated = _decode_ws_message(await connection.recv())
            self._require_ws_success(authenticated, "authenticated")
            await connection.send(json.dumps(subscription))
            async for raw in connection:
                for event in _decode_ws_message(raw):
                    if event.get("T") == "error":
                        raise AlpacaMarketDataError(
                            f"Alpaca WebSocket error {event.get('code')}: {event.get('msg')}"
                        )
                    channel_info = _EVENT_CHANNELS.get(event.get("T"))
                    if channel_info is None:
                        continue
                    channel, fields = channel_info
                    if channel not in requested:
                        continue
                    normalized = _normalize_fields(
                        {key: value for key, value in event.items() if key not in {"T", "S"}},
                        fields,
                    )
                    normalized["channel"] = channel
                    if "S" in event:
                        normalized["symbol"] = event["S"]
                    yield normalized

    def stream(
        self,
        symbols: Iterable[str] | str,
        channels: Iterable[str] | str,
        handler: Callable[[dict[str, Any]], Any],
    ) -> None:
        """Blocking wrapper around :meth:`stream_events`."""

        async def consume() -> None:
            async for event in self.stream_events(symbols, channels):
                result = handler(event)
                if inspect.isawaitable(result):
                    await result

        asyncio.run(consume())
