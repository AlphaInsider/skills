import json
from datetime import datetime, timezone

import httpx
import pytest

from scripts.market_data.coinbase import (
    WS_URL,
    CoinbaseMarketDataClient,
    CoinbaseMarketDataError,
)


def make_client(handler=None, **kwargs):
    transport = httpx.MockTransport(handler) if handler else None
    return CoinbaseMarketDataClient(transport=transport, **kwargs)


def test_list_products():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/brokerage/market/products"
        assert request.url.params["limit"] == "2"
        return httpx.Response(
            200, json={"products": [{"product_id": "BTC-USD"}], "num_products": 1}
        )

    payload = make_client(handler).list_products(limit=2)
    assert payload["products"][0]["product_id"] == "BTC-USD"


def test_get_product():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/products/BTC-USD")
        return httpx.Response(200, json={"product_id": "BTC-USD", "price": "50000"})

    assert make_client(handler).get_product("BTC-USD")["price"] == "50000"


def test_get_candles_converts_timestamps_and_validates_granularity():
    start = datetime(2026, 7, 28, tzinfo=timezone.utc)

    def handler(request: httpx.Request) -> httpx.Response:
        params = request.url.params
        assert request.url.path.endswith("/products/BTC-USD/candles")
        assert params["granularity"] == "ONE_HOUR"
        assert params["start"] == str(int(start.timestamp()))
        assert params["end"] == "1753747200"
        return httpx.Response(200, json={"candles": [{"open": "50000", "close": "50100"}]})

    payload = make_client(handler).get_candles("BTC-USD", "ONE_HOUR", start, 1753747200)
    assert payload["candles"][0]["close"] == "50100"

    with pytest.raises(ValueError, match="granularity"):
        make_client().get_candles("BTC-USD", "HOURLY", 0, 1)


def test_get_market_trades():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/products/BTC-USD/ticker")
        assert request.url.params["limit"] == "5"
        return httpx.Response(200, json={"trades": [{"trade_id": "t1"}]})

    assert make_client(handler).get_market_trades("BTC-USD", limit=5)["trades"][0]["trade_id"] == "t1"


def test_get_product_book():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/product_book")
        assert request.url.params["product_id"] == "BTC-USD"
        return httpx.Response(200, json={"pricebook": {"bids": [], "asks": []}})

    assert "pricebook" in make_client(handler).get_product_book("BTC-USD")


def test_http_error_raises():
    handler = lambda request: httpx.Response(404, json={"error": "NOT_FOUND"})
    with pytest.raises(CoinbaseMarketDataError, match="404"):
        make_client(handler).get_product("NOPE-USD")


def test_rate_limit_raises():
    handler = lambda request: httpx.Response(429, text="slow down")
    with pytest.raises(CoinbaseMarketDataError, match="rate limit"):
        make_client(handler).list_products()


class FakeWebSocket:
    def __init__(self, messages):
        self.sent = []
        self._messages = list(messages)

    async def send(self, message):
        self.sent.append(json.loads(message))

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._messages:
            raise StopAsyncIteration
        return self._messages.pop(0)


class FakeConnect:
    def __init__(self, websocket):
        self.websocket = websocket
        self.url = None

    def __call__(self, url):
        self.url = url
        return self

    async def __aenter__(self):
        return self.websocket

    async def __aexit__(self, *exc):
        return False


async def collect(stream):
    return [message async for message in stream]


async def test_stream_subscribes_and_yields_messages():
    ticker = {"channel": "ticker", "events": [{"tickers": [{"price": "50000"}]}]}
    heartbeat = {"channel": "heartbeats", "events": [{"heartbeat_counter": "1"}]}
    websocket = FakeWebSocket([json.dumps(ticker), json.dumps(heartbeat)])
    connect = FakeConnect(websocket)
    client = CoinbaseMarketDataClient(ws_connect=connect)

    messages = await collect(client.stream(["ticker"], ["BTC-USD"]))

    assert connect.url == WS_URL
    assert websocket.sent == [
        {"type": "subscribe", "channel": "ticker", "product_ids": ["BTC-USD"]},
        {"type": "subscribe", "channel": "heartbeats"},
    ]
    assert messages == [ticker, heartbeat]


async def test_stream_can_disable_heartbeats():
    websocket = FakeWebSocket([])
    client = CoinbaseMarketDataClient(ws_connect=FakeConnect(websocket))
    await collect(client.stream(["level2"], ["ETH-USD"], heartbeats=False))
    assert websocket.sent == [
        {"type": "subscribe", "channel": "level2", "product_ids": ["ETH-USD"]}
    ]


async def test_stream_rejects_authenticated_channels():
    client = CoinbaseMarketDataClient(ws_connect=FakeConnect(FakeWebSocket([])))
    with pytest.raises(ValueError, match="not a public"):
        await collect(client.stream(["user"], ["BTC-USD"]))
