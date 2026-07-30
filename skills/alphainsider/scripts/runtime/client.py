"""Thin client for the AlphaInsider paper-trading REST API.

AlphaInsider is the only order destination in this workspace and every order is
a paper order. Strategy values, position/order ``amount`` and ``total`` fields
are strategy-normalized — convert with the input-multiplier helpers below
before showing values to users or sizing user-denominated orders. See
``references/trades.md`` and ``references/input-multiplier.md``.
"""

from __future__ import annotations

import os
from decimal import Decimal
from typing import Any

import httpx
from dotenv import find_dotenv, load_dotenv

BASE_URL = "https://alphainsider.com/api"


def load_env() -> None:
    """Load working-directory `.env` values without overriding the process."""
    load_dotenv(find_dotenv(usecwd=True))


class AlphaInsiderError(Exception):
    """AlphaInsider returned ``success: false`` or an unusable response."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AlphaInsiderRateLimitError(AlphaInsiderError):
    """HTTP 429 — stop the current burst; retry later only if safe to repeat."""


def to_normalized(user_value: Any, input_multiplier: Any) -> Decimal:
    """Convert a user-denominated quantity (USD or shares/crypto) into
    normalized strategy units for ``newOrder`` ``amount``/``total``."""
    multiplier = Decimal(str(input_multiplier))
    if multiplier <= 0:
        raise ValueError("input_multiplier must be positive")
    return Decimal(str(user_value)) / multiplier


def to_display(normalized_value: Any, input_multiplier: Any) -> Decimal:
    """Convert a normalized strategy value into the user's displayed scale."""
    return Decimal(str(normalized_value)) * Decimal(str(input_multiplier))


class AlphaInsiderClient:
    """Importable client covering validation, strategy values/performance,
    positions, open orders, sizing, paper orders, allocation rebalancing, and
    cancellation."""

    def __init__(
        self,
        api_key: str | None = None,
        strategy_id: str | None = None,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ):
        load_env()
        self.api_key = api_key or os.environ.get("ALPHAINSIDER_API_KEY")
        self.strategy_id = strategy_id or os.environ.get("ALPHAINSIDER_STRATEGY_ID")
        if not self.api_key:
            raise AlphaInsiderError("ALPHAINSIDER_API_KEY is not set (environment or .env)")
        self._client = httpx.Client(base_url=base_url, timeout=timeout, transport=transport)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AlphaInsiderClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def _resolve_strategy_id(self, strategy_id: str | None) -> str:
        resolved = strategy_id or self.strategy_id
        if not resolved:
            raise AlphaInsiderError(
                "strategy_id is required (pass it or set ALPHAINSIDER_STRATEGY_ID)"
            )
        return resolved

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        authenticated: bool = True,
    ) -> Any:
        headers = {}
        if authenticated:
            # The token is the entire header value; AlphaInsider rejects "Bearer".
            headers["Authorization"] = self.api_key
        response = self._client.request(method, path, params=params, json=json, headers=headers)
        if response.status_code == 429:
            raise AlphaInsiderRateLimitError("Rate limit reached.", status_code=429)
        try:
            payload = response.json()
        except ValueError:
            raise AlphaInsiderError(
                f"non-JSON response from {path} (HTTP {response.status_code})",
                status_code=response.status_code,
            )
        if not payload.get("success"):
            raise AlphaInsiderError(str(payload.get("response")), status_code=response.status_code)
        return payload["response"]

    # -- validation ----------------------------------------------------------

    def verify_token(self, token: str | None = None) -> dict[str, Any]:
        """Validate an API token. The token travels in the JSON body, not the
        Authorization header."""
        return self._request(
            "POST", "/verifyToken", json={"token": token or self.api_key}, authenticated=False
        )

    def validate_strategy(self, strategy_id: str | None = None) -> dict[str, Any]:
        """Confirm the configured strategy exists and return it."""
        return self.get_strategy(strategy_id)

    # -- strategy management ------------------------------------------------

    def get_strategy(self, strategy_id: str | None = None) -> dict[str, Any]:
        """Return the configured strategy."""
        resolved = self._resolve_strategy_id(strategy_id)
        strategies = self._request("GET", "/getStrategies", params={"strategy_id[]": resolved})
        for strategy in strategies:
            if strategy.get("strategy_id") == resolved:
                return strategy
        raise AlphaInsiderError(f"strategy {resolved} not found")

    def update_strategy(
        self,
        name: str,
        input_value: Any,
        *,
        description: str | None = None,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Update the configured strategy's metadata and owner input value."""
        body: dict[str, Any] = {
            "strategy_id": self._resolve_strategy_id(strategy_id),
            "name": name,
            "input_value": str(input_value),
        }
        if description is not None:
            body["description"] = description
        return self._request("POST", "/updateStrategy", json=body)

    def update_strategy_price(
        self, price: Any, strategy_id: str | None = None
    ) -> dict[str, Any]:
        """Update the configured strategy's monthly subscription price."""
        return self._request(
            "POST",
            "/updateStrategyPrice",
            json={
                "strategy_id": self._resolve_strategy_id(strategy_id),
                "price": str(price),
            },
        )

    # -- strategy values and performance --------------------------------------

    def get_strategy_values(self, strategy_id: str | None = None) -> list[dict[str, Any]]:
        """Current normalized strategy value(s)."""
        resolved = self._resolve_strategy_id(strategy_id)
        return self._request("GET", "/getStrategyValues", params={"strategy_id[]": resolved})

    def get_strategy_performance(
        self,
        start_date: str,
        *,
        end_date: str | None = None,
        frequency: int | None = None,
        interval: str | None = None,
        strategy_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Normalized performance points between ``start_date`` and ``end_date``."""
        params: dict[str, Any] = {
            "strategy_id": self._resolve_strategy_id(strategy_id),
            "start_date": start_date,
        }
        if end_date is not None:
            params["end_date"] = end_date
        if frequency is not None:
            params["frequency"] = frequency
        if interval is not None:
            params["interval"] = interval
        return self._request("GET", "/getStrategyPerformance", params=params)

    # -- subscription calculations and account limits -----------------------

    def get_strategy_subscriptions(
        self, strategy_id: str | None = None
    ) -> list[dict[str, Any]]:
        """Return subscription/calculation context for the configured strategy."""
        resolved = self._resolve_strategy_id(strategy_id)
        return self._request(
            "GET", "/getStrategySubscriptions", params={"strategy_id[]": resolved}
        )

    def get_input_multiplier(self, strategy_id: str | None = None) -> Decimal:
        """Resolve the saved ``input_multiplier`` for the authenticated
        subscription. Never assume a missing multiplier is 1."""
        resolved = self._resolve_strategy_id(strategy_id)
        subscriptions = self.get_strategy_subscriptions(resolved)
        for subscription in subscriptions:
            if subscription.get("strategy_id") == resolved and subscription.get("input_multiplier"):
                return Decimal(str(subscription["input_multiplier"]))
        raise AlphaInsiderError(
            f"no saved input_multiplier for strategy {resolved}; refresh the strategy "
            "calculation before displaying values or sizing user-denominated orders"
        )

    def get_strategy_calculation(
        self,
        input_value: Any,
        input_date: str,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Calculate an input multiplier without persisting it."""
        return self._request(
            "GET",
            "/getStrategyCalculation",
            params={
                "strategy_id": self._resolve_strategy_id(strategy_id),
                "input_value": str(input_value),
                "input_date": input_date,
            },
        )

    def update_strategy_calculation(
        self,
        input_value: Any,
        input_date: str,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Persist relative calculation inputs for the configured strategy."""
        return self._request(
            "POST",
            "/updateStrategyCalculation",
            json={
                "strategy_id": self._resolve_strategy_id(strategy_id),
                "input_value": str(input_value),
                "input_date": input_date,
            },
        )

    def delete_strategy_calculation(self, strategy_id: str | None = None) -> Any:
        """Delete the saved relative calculation for the configured strategy."""
        return self._request(
            "POST",
            "/deleteStrategyCalculation",
            json={"strategy_id": self._resolve_strategy_id(strategy_id)},
        )

    def get_account_subscription(self) -> dict[str, Any]:
        """Return the authenticated account's active limits and tier."""
        return self._request("GET", "/getAccountSubscription")

    # -- positions and open orders ---------------------------------------------

    def get_positions(self, strategy_id: str | None = None) -> list[dict[str, Any]]:
        """Current positions; ``amount``/``total`` are normalized."""
        return self._request(
            "GET", "/getPositions", params={"strategy_id": self._resolve_strategy_id(strategy_id)}
        )

    def get_orders(self, strategy_id: str | None = None) -> list[dict[str, Any]]:
        """Open orders; each includes ``order_dependencies`` (``[]`` = none)."""
        return self._request(
            "GET", "/getOrders", params={"strategy_id": self._resolve_strategy_id(strategy_id)}
        )

    def get_max_order_size(self, stock_id: str, strategy_id: str | None = None) -> dict[str, Any]:
        """Buying/selling power for ``stock_id``, already factoring slippage and fees."""
        return self._request(
            "GET",
            "/getMaxOrderSize",
            params={
                "strategy_id": self._resolve_strategy_id(strategy_id),
                "stock_id": stock_id,
            },
        )

    # -- order management -------------------------------------------------------

    def new_order(
        self,
        stock_id: str,
        action: str,
        order_type: str = "market",
        *,
        amount: Any | None = None,
        total: Any | None = None,
        price: Any | None = None,
        stop_price: Any | None = None,
        order_dependencies: list[str] | None = None,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Submit a paper order. ``amount``/``total`` are normalized strategy
        units — pass exactly one of them (divide user quantities by the
        ``input_multiplier`` first)."""
        if (amount is None) == (total is None):
            raise ValueError("pass exactly one of amount or total")
        body: dict[str, Any] = {
            "strategy_id": self._resolve_strategy_id(strategy_id),
            "stock_id": stock_id,
            "action": action,
            "type": order_type,
        }
        if amount is not None:
            body["amount"] = str(amount)
        if total is not None:
            body["total"] = str(total)
        if price is not None:
            body["price"] = str(price)
        if stop_price is not None:
            body["stop_price"] = str(stop_price)
        if order_dependencies is not None:
            body["order_dependencies"] = list(order_dependencies)
        return self._request("POST", "/newOrder", json=body)

    def rebalance_allocations(
        self,
        allocations: list[dict[str, Any]],
        *,
        slippage: float | None = None,
        strategy_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Create market orders moving the strategy toward target percentage
        allocations (fractions of equity, total leverage <= 2). Percentages do
        not use the input multiplier."""
        body: dict[str, Any] = {
            "strategy_id": self._resolve_strategy_id(strategy_id),
            "allocations": allocations,
        }
        if slippage is not None:
            body["slippage"] = slippage
        return self._request("POST", "/newOrderAllocations", json=body)

    def cancel_order(self, order_id: str, strategy_id: str | None = None) -> Any:
        """Cancel (delete) one open order."""
        return self._request(
            "POST",
            "/deleteOrder",
            json={
                "strategy_id": self._resolve_strategy_id(strategy_id),
                "order_id": order_id,
            },
        )

    def new_order_webhook(
        self,
        stock_id: str,
        action: str,
        *,
        leverage: float | None = None,
        pyramiding: int | None = None,
        slippage: float | None = None,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Submit a signal-style paper order with the token in ``api_token``."""
        body: dict[str, Any] = {
            "strategy_id": self._resolve_strategy_id(strategy_id),
            "stock_id": stock_id,
            "action": action,
            "api_token": self.api_key,
        }
        if leverage is not None:
            body["leverage"] = leverage
        if pyramiding is not None:
            body["pyramiding"] = pyramiding
        if slippage is not None:
            body["slippage"] = slippage
        return self._request(
            "POST", "/newOrderWebhook", json=body, authenticated=False
        )

    # -- timelines ----------------------------------------------------------

    def get_timelines(self, timeline_ids: list[str]) -> list[dict[str, Any]]:
        """Return timeline events by ID."""
        return self._request("GET", "/getTimelines", params={"timeline_id[]": timeline_ids})

    def get_strategy_timelines(
        self,
        *,
        limit: int,
        timeline_types: list[str] | None = None,
        is_notification: bool | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        offset_id: str | None = None,
        strategy_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return paginated events for the configured strategy."""
        params: dict[str, Any] = {
            "strategy_id[]": self._resolve_strategy_id(strategy_id),
            "limit": limit,
        }
        if timeline_types:
            params["type[]"] = timeline_types
        if is_notification is not None:
            params["is_notification"] = is_notification
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if offset_id is not None:
            params["offset_id"] = offset_id
        return self._request("GET", "/getStrategyTimelines", params=params)

    def new_post(
        self,
        *,
        description: str | None = None,
        url: str | None = None,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Create a post on the configured strategy's timeline."""
        return self._request(
            "POST",
            "/newPost",
            json=self._post_body(description, url, strategy_id),
        )

    def preview_post(
        self,
        *,
        description: str | None = None,
        url: str | None = None,
        strategy_id: str | None = None,
    ) -> dict[str, Any]:
        """Preview a strategy timeline post without publishing it."""
        return self._request(
            "POST",
            "/previewPost",
            json=self._post_body(description, url, strategy_id),
        )

    def _post_body(
        self,
        description: str | None,
        url: str | None,
        strategy_id: str | None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"strategy_id": self._resolve_strategy_id(strategy_id)}
        if description is not None:
            body["description"] = description
        if url is not None:
            body["url"] = url
        return body

    def delete_post(self, timeline_id: str) -> Any:
        """Delete a timeline post."""
        return self._request("POST", "/deletePost", json={"timeline_id": timeline_id})

    def like_timeline(self, timeline_id: str) -> Any:
        """Like a timeline event."""
        return self._request("POST", "/like", json={"timeline_id": timeline_id})

    def unlike_timeline(self, timeline_id: str) -> Any:
        """Remove a like from a timeline event."""
        return self._request("POST", "/unlike", json={"timeline_id": timeline_id})

    # -- AlphaInsider asset directory --------------------------------------

    def get_stocks(self, stock_ids: list[str]) -> list[dict[str, Any]]:
        """Return stock/crypto metadata for one or more AlphaInsider IDs."""
        return self._request("GET", "/getStocks", params={"stock_id[]": stock_ids})

    def search_stocks(
        self,
        search: str,
        *,
        security_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Search AlphaInsider's stock and cryptocurrency directory."""
        body: dict[str, Any] = {"search": search}
        if security_type is not None:
            body["type"] = security_type
        if limit is not None:
            body["limit"] = limit
        return self._request("POST", "/searchStocks", json=body)

    def get_stock_price_history(
        self,
        stock_id: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Return AlphaInsider bid/ask/last history for an asset."""
        params: dict[str, Any] = {"stock_id": stock_id}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if limit is not None:
            params["limit"] = limit
        return self._request("GET", "/getStockPriceHistory", params=params)

    def get_exchange_status(self) -> dict[str, Any]:
        """Return AlphaInsider stock and cryptocurrency exchange status."""
        return self._request("GET", "/getExchangeStatus")
