import json

import pytest

from runtime.stream import AlphaInsiderStream, strategy_channels


class FakeSocket:
    def __init__(self, messages):
        self.messages = iter(messages)
        self.sent = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return None

    async def send(self, message):
        self.sent.append(message)

    async def recv(self):
        return next(self.messages)


@pytest.mark.asyncio
async def test_stream_subscribes_to_configured_strategy_without_exposing_token():
    socket = FakeSocket(
        [
            json.dumps(
                [
                    {
                        "event": "wsStrategyValue",
                        "channel": "wsStrategyValue:strat_1",
                        "response": {"strategy_id": "strat_1", "strategy_value": "1.01"},
                    }
                ]
            )
        ]
    )
    stream = AlphaInsiderStream(
        api_key="secret-token",
        strategy_id="strat_1",
        connect=lambda url: socket,
    )

    events = stream.events()
    event = await anext(events)
    await events.aclose()

    subscription = json.loads(socket.sent[0])
    assert subscription == {
        "event": "subscribe",
        "payload": {
            "channels": strategy_channels("strat_1"),
            "token": "secret-token",
        },
    }
    assert "secret-token" not in json.dumps(event)
    assert event["channel"] == "wsStrategyValue:strat_1"


def test_default_strategy_channels_cover_live_management():
    assert strategy_channels("strat_1") == [
        "wsStrategyValue:strat_1",
        "wsOrders:strat_1",
        "wsPositions:strat_1",
        "wsTimelines:strat_1",
    ]
