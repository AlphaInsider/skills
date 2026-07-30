"""Alpaca equities market data client (data APIs only).

This module must never instantiate an Alpaca trading client or submit broker
orders — AlphaInsider is the only order destination in this workspace.

Credentials: ``ALPACA_KEY`` / ``ALPACA_SECRET`` from the environment first,
then ``.env``. Optional ``ALPACA_FEED`` selects ``iex`` (default, free tier)
or ``sip`` (paid entitlement).
"""

from __future__ import annotations

import os
import re
from typing import Any, Callable, Iterable

from dotenv import find_dotenv, load_dotenv

_TIMEFRAME_PATTERN = re.compile(r"^(\d+)(Min|Hour|Day|Week|Month)$")
_STREAM_CHANNELS = ("bars", "quotes", "trades")


def load_env() -> None:
    """Load working-directory `.env` values without overriding the process."""
    load_dotenv(find_dotenv(usecwd=True))


class MissingAlpacaCredentials(Exception):
    """ALPACA_KEY / ALPACA_SECRET are not configured."""


def _parse_timeframe(timeframe: str):
    from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

    match = _TIMEFRAME_PATTERN.match(timeframe)
    if not match:
        raise ValueError(
            f"invalid timeframe {timeframe!r}; use e.g. 1Min, 5Min, 1Hour, 1Day, 1Week, 1Month"
        )
    amount, unit = int(match.group(1)), match.group(2)
    units = {
        "Min": TimeFrameUnit.Minute,
        "Hour": TimeFrameUnit.Hour,
        "Day": TimeFrameUnit.Day,
        "Week": TimeFrameUnit.Week,
        "Month": TimeFrameUnit.Month,
    }
    return TimeFrame(amount, units[unit])


def _bar_to_dict(bar: Any) -> dict[str, Any]:
    return {
        "timestamp": bar.timestamp.isoformat(),
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume,
        "vwap": getattr(bar, "vwap", None),
        "trade_count": getattr(bar, "trade_count", None),
    }


def _quote_to_dict(quote: Any) -> dict[str, Any]:
    return {
        "timestamp": quote.timestamp.isoformat(),
        "bid_price": quote.bid_price,
        "bid_size": quote.bid_size,
        "ask_price": quote.ask_price,
        "ask_size": quote.ask_size,
    }


def _default_historical_client(api_key: str, api_secret: str):
    from alpaca.data.historical import StockHistoricalDataClient

    return StockHistoricalDataClient(api_key, api_secret)


def _default_stream(api_key: str, api_secret: str, feed: str):
    from alpaca.data.enums import DataFeed
    from alpaca.data.live import StockDataStream

    return StockDataStream(api_key, api_secret, feed=DataFeed(feed))


class AlpacaMarketDataClient:
    """Recent/historical stock bars, latest quotes, and live data streams."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        *,
        feed: str | None = None,
        historical_client: Any | None = None,
        stream_factory: Callable[[str, str, str], Any] | None = None,
    ):
        load_env()
        self.api_key = api_key or os.environ.get("ALPACA_KEY")
        self.api_secret = api_secret or os.environ.get("ALPACA_SECRET")
        if not self.api_key or not self.api_secret:
            raise MissingAlpacaCredentials(
                "set ALPACA_KEY and ALPACA_SECRET in the environment or .env"
            )
        self.feed = (feed or os.environ.get("ALPACA_FEED") or "iex").lower()
        self._historical = historical_client
        self._stream_factory = stream_factory or _default_stream

    @property
    def historical(self) -> Any:
        if self._historical is None:
            self._historical = _default_historical_client(self.api_key, self.api_secret)
        return self._historical

    def get_bars(
        self,
        symbols: Iterable[str],
        timeframe: str = "1Day",
        *,
        start: Any | None = None,
        end: Any | None = None,
        limit: int | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        """Bars per symbol, newest window controlled by start/end/limit.
        ``timeframe`` examples: ``1Min``, ``15Min``, ``1Hour``, ``1Day``."""
        from alpaca.data.requests import StockBarsRequest

        request = StockBarsRequest(
            symbol_or_symbols=list(symbols),
            timeframe=_parse_timeframe(timeframe),
            start=start,
            end=end,
            limit=limit,
            feed=self.feed,
        )
        bars = self.historical.get_stock_bars(request)
        return {symbol: [_bar_to_dict(bar) for bar in items] for symbol, items in bars.data.items()}

    def get_latest_quotes(self, symbols: Iterable[str]) -> dict[str, dict[str, Any]]:
        """Latest NBBO quote per symbol."""
        from alpaca.data.requests import StockLatestQuoteRequest

        request = StockLatestQuoteRequest(symbol_or_symbols=list(symbols), feed=self.feed)
        quotes = self.historical.get_stock_latest_quote(request)
        return {symbol: _quote_to_dict(quote) for symbol, quote in quotes.items()}

    def stream(
        self,
        symbols: Iterable[str],
        channel: str,
        handler: Callable[[Any], Any],
    ) -> None:
        """Blocking live stream of ``bars``, ``quotes``, or ``trades``;
        ``handler`` is called with each event. Stop with Ctrl+C."""
        if channel not in _STREAM_CHANNELS:
            raise ValueError(f"channel must be one of {_STREAM_CHANNELS}, got {channel!r}")
        stream = self._stream_factory(self.api_key, self.api_secret, self.feed)

        async def _on_event(event: Any) -> None:
            handler(event)

        subscribe = {
            "bars": stream.subscribe_bars,
            "quotes": stream.subscribe_quotes,
            "trades": stream.subscribe_trades,
        }[channel]
        subscribe(_on_event, *list(symbols))
        stream.run()
