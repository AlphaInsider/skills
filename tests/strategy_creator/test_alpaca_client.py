import asyncio
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.market_data.alpaca import AlpacaMarketDataClient, MissingAlpacaCredentials


class FakeHistoricalClient:
    def __init__(self, bars_by_symbol=None, quotes_by_symbol=None):
        self.bars_by_symbol = bars_by_symbol or {}
        self.quotes_by_symbol = quotes_by_symbol or {}
        self.requests = []

    def get_stock_bars(self, request):
        self.requests.append(request)
        return SimpleNamespace(data=self.bars_by_symbol)

    def get_stock_latest_quote(self, request):
        self.requests.append(request)
        return self.quotes_by_symbol


class FakeStream:
    def __init__(self, events):
        self.events = events
        self.subscriptions = []
        self._handler = None

    def subscribe_bars(self, handler, *symbols):
        self.subscriptions.append(("bars", symbols))
        self._handler = handler

    def subscribe_quotes(self, handler, *symbols):
        self.subscriptions.append(("quotes", symbols))
        self._handler = handler

    def subscribe_trades(self, handler, *symbols):
        self.subscriptions.append(("trades", symbols))
        self._handler = handler

    def run(self):
        for event in self.events:
            asyncio.run(self._handler(event))


def make_client(**kwargs):
    return AlpacaMarketDataClient(api_key="key", api_secret="secret", **kwargs)


def fake_bar(close=100.0):
    return SimpleNamespace(
        timestamp=datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc),
        open=99.0,
        high=101.0,
        low=98.5,
        close=close,
        volume=1_000_000,
        vwap=99.9,
        trade_count=5000,
    )


def test_missing_credentials_raise(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ALPACA_KEY", raising=False)
    monkeypatch.delenv("ALPACA_SECRET", raising=False)
    with pytest.raises(MissingAlpacaCredentials):
        AlpacaMarketDataClient()


def test_credentials_from_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ALPACA_KEY", "env-key")
    monkeypatch.setenv("ALPACA_SECRET", "env-secret")
    monkeypatch.setenv("ALPACA_FEED", "SIP")
    client = AlpacaMarketDataClient()
    assert client.api_key == "env-key"
    assert client.feed == "sip"


def test_dotenv_fallback_does_not_override_env(monkeypatch, tmp_path):
    (tmp_path / ".env").write_text("ALPACA_KEY=dotenv-key\nALPACA_SECRET=dotenv-secret\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ALPACA_KEY", "env-key")
    monkeypatch.delenv("ALPACA_SECRET", raising=False)
    client = AlpacaMarketDataClient()
    assert client.api_key == "env-key"  # environment wins
    assert client.api_secret == "dotenv-secret"  # .env fills the gap


def test_get_bars_converts_and_builds_request():
    fake = FakeHistoricalClient(bars_by_symbol={"SPY": [fake_bar()]})
    client = make_client(historical_client=fake)
    bars = client.get_bars(["SPY"], "15Min", limit=5)

    assert list(bars) == ["SPY"]
    bar = bars["SPY"][0]
    assert bar["close"] == 100.0
    assert bar["timestamp"] == "2026-07-28T20:00:00+00:00"

    request = fake.requests[0]
    assert request.symbol_or_symbols == ["SPY"]
    assert request.limit == 5
    assert request.timeframe.amount == 15
    assert str(request.feed.value) == "iex"


def test_invalid_timeframe_raises():
    client = make_client(historical_client=FakeHistoricalClient())
    with pytest.raises(ValueError, match="invalid timeframe"):
        client.get_bars(["SPY"], "2Fortnight")


def test_get_latest_quotes_converts():
    quote = SimpleNamespace(
        timestamp=datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc),
        bid_price=99.9,
        bid_size=2,
        ask_price=100.1,
        ask_size=3,
    )
    client = make_client(historical_client=FakeHistoricalClient(quotes_by_symbol={"SPY": quote}))
    quotes = client.get_latest_quotes(["SPY"])
    assert quotes["SPY"]["bid_price"] == 99.9
    assert quotes["SPY"]["ask_price"] == 100.1


def test_stream_dispatches_events_to_handler():
    events = ["bar1", "bar2"]
    stream = FakeStream(events)
    client = make_client(stream_factory=lambda key, secret, feed: stream)

    received = []
    client.stream(["SPY", "MSFT"], "bars", received.append)

    assert stream.subscriptions == [("bars", ("SPY", "MSFT"))]
    assert received == events


def test_stream_rejects_unknown_channel():
    client = make_client(stream_factory=lambda key, secret, feed: FakeStream([]))
    with pytest.raises(ValueError, match="channel"):
        client.stream(["SPY"], "orders", print)


def test_module_never_touches_alpaca_trading():
    source = (
        Path(__file__).resolve().parents[2]
        / "skills"
        / "strategy-creator"
        / "scripts"
        / "market_data"
        / "alpaca.py"
    ).read_text()
    assert "TradingClient" not in source
    assert "alpaca.trading" not in source
