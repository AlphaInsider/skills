import json

from scripts.market_data.cli import main


class FakeCoinbaseClient:
    def __init__(self):
        self.calls = []

    def list_products(self, *, limit=None, product_type=None):
        self.calls.append(("list_products", limit, product_type))
        return {"products": [{"product_id": "BTC-USD"}], "num_products": 1}

    def get_product(self, product_id):
        self.calls.append(("get_product", product_id))
        return {"product_id": product_id}

    def get_candles(self, product_id, granularity, start, end):
        self.calls.append(("get_candles", product_id, granularity, start, end))
        return {"candles": []}

    def get_market_trades(self, product_id, *, limit=None):
        self.calls.append(("get_market_trades", product_id, limit))
        return {"trades": []}

    def get_product_book(self, product_id, *, limit=None):
        self.calls.append(("get_product_book", product_id, limit))
        return {"pricebook": {"bids": [], "asks": []}}

    async def stream(self, channels, product_ids, *, heartbeats=True):
        self.calls.append(("stream", tuple(channels), tuple(product_ids)))
        for counter in range(10):
            yield {"channel": channels[0], "sequence": counter}


class FakeAlpacaClient:
    def __init__(self):
        self.calls = []

    def get_bars(self, symbols, timeframe="1Day", *, start=None, end=None, limit=None):
        self.calls.append(("get_bars", tuple(symbols), timeframe, limit))
        return {"SPY": [{"close": 100.0}]}

    def get_latest_quotes(self, symbols):
        self.calls.append(("get_latest_quotes", tuple(symbols)))
        return {"SPY": {"bid_price": 99.9}}

    def stream(self, symbols, channel, handler):
        self.calls.append(("stream", tuple(symbols), channel))
        handler({"event": 1})


def test_coinbase_products(capsys):
    client = FakeCoinbaseClient()
    assert main(["coinbase", "products", "--limit", "5"], coinbase_client=client) == 0
    assert client.calls == [("list_products", 5, None)]
    assert json.loads(capsys.readouterr().out)["num_products"] == 1


def test_coinbase_candles_defaults_window(capsys):
    client = FakeCoinbaseClient()
    assert main(["coinbase", "candles", "BTC-USD"], coinbase_client=client) == 0
    name, product_id, granularity, start, end = client.calls[0]
    assert (name, product_id, granularity) == ("get_candles", "BTC-USD", "ONE_HOUR")
    assert end - start == 300 * 3600  # 300 one-hour candles


def test_coinbase_stream_respects_limit(capsys):
    client = FakeCoinbaseClient()
    assert (
        main(
            ["coinbase", "stream", "BTC-USD", "--channel", "ticker", "--limit", "3"],
            coinbase_client=client,
        )
        == 0
    )
    assert capsys.readouterr().out.count('"sequence"') == 3


def test_alpaca_bars(capsys):
    client = FakeAlpacaClient()
    code = main(
        ["alpaca", "bars", "SPY", "--timeframe", "15Min", "--limit", "10"],
        alpaca_client=client,
    )
    assert code == 0
    assert client.calls == [("get_bars", ("SPY",), "15Min", 10)]
    assert json.loads(capsys.readouterr().out)["SPY"][0]["close"] == 100.0


def test_alpaca_quotes(capsys):
    client = FakeAlpacaClient()
    assert main(["alpaca", "quotes", "SPY"], alpaca_client=client) == 0
    assert json.loads(capsys.readouterr().out)["SPY"]["bid_price"] == 99.9


def test_alpaca_stream(capsys):
    client = FakeAlpacaClient()
    assert main(["alpaca", "stream", "SPY", "--channel", "trades"], alpaca_client=client) == 0
    assert client.calls == [("stream", ("SPY",), "trades")]


def test_alpaca_without_credentials_errors_cleanly(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ALPACA_KEY", raising=False)
    monkeypatch.delenv("ALPACA_SECRET", raising=False)
    assert main(["alpaca", "quotes", "SPY"]) == 1
    assert "ALPACA_KEY" in capsys.readouterr().err
