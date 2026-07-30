import json
from decimal import Decimal

import httpx
import pytest

from runtime import (
    AlphaInsiderClient,
    AlphaInsiderError,
    AlphaInsiderRateLimitError,
    to_display,
    to_normalized,
)
from tests.alphainsider.conftest import envelope


def test_auth_header_is_verbatim_token(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "test-token"
        assert "Bearer" not in request.headers["Authorization"]
        return envelope([])

    make_alpha_client(handler).get_positions()


def test_missing_api_key_raises(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ALPHAINSIDER_API_KEY", raising=False)
    with pytest.raises(AlphaInsiderError, match="ALPHAINSIDER_API_KEY"):
        AlphaInsiderClient()


def test_verify_token_sends_token_in_body_without_auth_header(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/verifyToken")
        assert "Authorization" not in request.headers
        assert json.loads(request.content) == {"token": "test-token"}
        return envelope({"token_id": "tok_1", "user_id": "user_1"})

    assert make_alpha_client(handler).verify_token()["token_id"] == "tok_1"


def test_validate_strategy_found(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["strategy_id[]"] == "strat_1"
        return envelope([{"strategy_id": "strat_1", "name": "Test"}])

    assert make_alpha_client(handler).validate_strategy()["name"] == "Test"


def test_validate_strategy_missing_raises(make_alpha_client):
    client = make_alpha_client(lambda request: envelope([]))
    with pytest.raises(AlphaInsiderError, match="strat_1 not found"):
        client.validate_strategy()


def test_get_strategy_values(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/getStrategyValues")
        return envelope([{"strategy_id": "strat_1", "strategy_value": "10250.5"}])

    values = make_alpha_client(handler).get_strategy_values()
    assert values[0]["strategy_value"] == "10250.5"


def test_get_strategy_performance_params(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        params = request.url.params
        assert params["strategy_id"] == "strat_1"
        assert params["start_date"] == "2026-01-01T00:00:00Z"
        assert params["interval"] == "day"
        assert "end_date" not in params
        return envelope([{"strategy_value": "10100"}])

    make_alpha_client(handler).get_strategy_performance(
        "2026-01-01T00:00:00Z", interval="day"
    )


def test_get_orders_passes_through_order_dependencies(make_alpha_client):
    orders = [{"order_id": "o1", "order_dependencies": ["o0"]}]
    result = make_alpha_client(lambda request: envelope(orders)).get_orders()
    assert result[0]["order_dependencies"] == ["o0"]


def test_get_max_order_size(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["stock_id"] == "SPY:ARCX"
        return envelope({"buying_power_total": "5000", "selling_power_total": "5000"})

    result = make_alpha_client(handler).get_max_order_size("SPY:ARCX")
    assert result["buying_power_total"] == "5000"


def test_new_order_requires_exactly_one_of_amount_or_total(make_alpha_client):
    client = make_alpha_client(lambda request: envelope({}))
    with pytest.raises(ValueError, match="exactly one"):
        client.new_order("SPY:ARCX", "buy", amount="1", total="100")
    with pytest.raises(ValueError, match="exactly one"):
        client.new_order("SPY:ARCX", "buy")


def test_new_order_body(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body == {
            "strategy_id": "strat_1",
            "stock_id": "SPY:ARCX",
            "action": "buy",
            "type": "limit",
            "total": "100.5",
            "price": "500.25",
            "order_dependencies": ["o0"],
        }
        return envelope({"order_id": "o1", "order_dependencies": ["o0"]})

    order = make_alpha_client(handler).new_order(
        "SPY:ARCX",
        "buy",
        "limit",
        total="100.5",
        price="500.25",
        order_dependencies=["o0"],
    )
    assert order["order_id"] == "o1"


def test_rebalance_allocations_body(make_alpha_client):
    allocations = [{"stock_id": "SPY:ARCX", "action": "buy", "percent": 0.8}]

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["strategy_id"] == "strat_1"
        assert body["allocations"] == allocations
        assert body["slippage"] == 0.003
        return envelope([{"order_id": "o1", "order_dependencies": []}])

    result = make_alpha_client(handler).rebalance_allocations(allocations, slippage=0.003)
    assert result[0]["order_id"] == "o1"


def test_cancel_order_body(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content) == {"strategy_id": "strat_1", "order_id": "o1"}
        return envelope("deleted")

    assert make_alpha_client(handler).cancel_order("o1") == "deleted"


def test_error_envelope_raises_with_message(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"success": False, "response": "Invalid strategy."})

    with pytest.raises(AlphaInsiderError, match="Invalid strategy."):
        make_alpha_client(handler).get_positions()


def test_rate_limit_raises_dedicated_error(make_alpha_client):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"success": False, "response": "Rate limit reached."})

    with pytest.raises(AlphaInsiderRateLimitError):
        make_alpha_client(handler).get_orders()


def test_missing_strategy_id_raises(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ALPHAINSIDER_STRATEGY_ID", raising=False)
    client = AlphaInsiderClient(api_key="test-token")
    with pytest.raises(AlphaInsiderError, match="strategy_id is required"):
        client.get_positions()


def test_get_input_multiplier_from_subscription(make_alpha_client):
    subscriptions = [{"strategy_id": "strat_1", "input_multiplier": "12.5"}]
    client = make_alpha_client(lambda request: envelope(subscriptions))
    assert client.get_input_multiplier() == Decimal("12.5")


def test_missing_input_multiplier_never_defaults_to_one(make_alpha_client):
    client = make_alpha_client(lambda request: envelope([{"strategy_id": "strat_1"}]))
    with pytest.raises(AlphaInsiderError, match="input_multiplier"):
        client.get_input_multiplier()


def test_normalization_helpers_round_trip():
    multiplier = Decimal("12.5")
    normalized = to_normalized("100", multiplier)  # user dollars -> strategy units
    assert normalized == Decimal("8")
    assert to_display(normalized, multiplier) == Decimal("100")
    with pytest.raises(ValueError):
        to_normalized("100", 0)


def test_update_strategy_and_price(make_alpha_client):
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.url.path, json.loads(request.content)))
        return envelope({"strategy_id": "strat_1"})

    client = make_alpha_client(handler)
    client.update_strategy("Momentum", "10000", description="Daily momentum")
    client.update_strategy_price("15")

    assert requests == [
        (
            "/api/updateStrategy",
            {
                "strategy_id": "strat_1",
                "name": "Momentum",
                "input_value": "10000",
                "description": "Daily momentum",
            },
        ),
        ("/api/updateStrategyPrice", {"strategy_id": "strat_1", "price": "15"}),
    ]


def test_strategy_subscriptions_calculations_and_account_limits(make_alpha_client):
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path, dict(request.url.params)))
        if request.url.path.endswith("/getStrategySubscriptions"):
            return envelope([{"strategy_id": "strat_1", "input_multiplier": "10"}])
        if request.url.path.endswith("/getStrategyCalculation"):
            return envelope({"strategy_id": "strat_1", "input_multiplier": "10"})
        return envelope({"limits": {"new_order": 50}})

    client = make_alpha_client(handler)
    assert client.get_strategy_subscriptions()[0]["input_multiplier"] == "10"
    assert client.get_strategy_calculation("10000", "2026-01-01T00:00:00Z")[
        "input_multiplier"
    ] == "10"
    assert client.get_account_subscription()["limits"]["new_order"] == 50

    assert requests[0][2]["strategy_id[]"] == "strat_1"
    assert requests[1][2] == {
        "strategy_id": "strat_1",
        "input_value": "10000",
        "input_date": "2026-01-01T00:00:00Z",
    }


def test_update_and_delete_strategy_calculation(make_alpha_client):
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append((request.url.path, json.loads(request.content)))
        return envelope({"strategy_id": "strat_1"})

    client = make_alpha_client(handler)
    client.update_strategy_calculation("10000", "2026-01-01T00:00:00Z")
    client.delete_strategy_calculation()

    assert requests == [
        (
            "/api/updateStrategyCalculation",
            {
                "strategy_id": "strat_1",
                "input_value": "10000",
                "input_date": "2026-01-01T00:00:00Z",
            },
        ),
        ("/api/deleteStrategyCalculation", {"strategy_id": "strat_1"}),
    ]


def test_strategy_timelines_and_posts(make_alpha_client):
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else None
        requests.append((request.method, request.url.path, request.url.params, body))
        if request.method == "GET":
            return envelope([{"timeline_id": "timeline_1", "type": "trade"}])
        return envelope({"timeline_id": "timeline_1"})

    client = make_alpha_client(handler)
    client.get_strategy_timelines(limit=20, timeline_types=["trade", "post"])
    client.new_post(description="Update", url="https://example.com")
    client.preview_post(url="https://example.com")
    client.delete_post("timeline_1")
    client.like_timeline("timeline_1")
    client.unlike_timeline("timeline_1")

    params = requests[0][2]
    assert params.get_list("strategy_id[]") == ["strat_1"]
    assert params.get_list("type[]") == ["trade", "post"]
    assert params["limit"] == "20"
    assert requests[1][3] == {
        "strategy_id": "strat_1",
        "description": "Update",
        "url": "https://example.com",
    }
    assert [request[1] for request in requests[3:]] == [
        "/api/deletePost",
        "/api/like",
        "/api/unlike",
    ]


def test_stock_discovery_and_webhook_order(make_alpha_client):
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else None
        requests.append((request.method, request.url.path, request.headers, body))
        if request.url.path.endswith("/newOrderWebhook"):
            return envelope({"order_id": "o1", "order_dependencies": []})
        return envelope([{"stock_id": "SPY:ARCX"}])

    client = make_alpha_client(handler)
    assert client.search_stocks("SPY", security_type="stock", limit=5)[0]["stock_id"] == "SPY:ARCX"
    order = client.new_order_webhook(
        "SPY:ARCX", "long", leverage=1.5, pyramiding=3, slippage=0.003
    )

    assert requests[0][3] == {"search": "SPY", "type": "stock", "limit": 5}
    assert "Authorization" not in requests[1][2]
    assert requests[1][3] == {
        "strategy_id": "strat_1",
        "stock_id": "SPY:ARCX",
        "action": "long",
        "leverage": 1.5,
        "pyramiding": 3,
        "slippage": 0.003,
        "api_token": "test-token",
    }
