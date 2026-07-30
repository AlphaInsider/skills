"""Thin AlphaInsider WebSocket client for the configured paper strategy."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import AsyncIterator, Callable
from typing import Any

from websockets import connect as websocket_connect

from .client import AlphaInsiderError, load_env

WEBSOCKET_URL = "wss://alphainsider.com/ws"


class AlphaInsiderStreamError(AlphaInsiderError):
    """AlphaInsider rejected a subscription or returned an invalid event."""


def strategy_channels(strategy_id: str) -> list[str]:
    """Channels used to monitor one paper strategy."""
    return [
        f"wsStrategyValue:{strategy_id}",
        f"wsOrders:{strategy_id}",
        f"wsPositions:{strategy_id}",
        f"wsTimelines:{strategy_id}",
    ]


class AlphaInsiderStream:
    """Subscribe to live strategy, order, position, and timeline events."""

    def __init__(
        self,
        api_key: str | None = None,
        strategy_id: str | None = None,
        *,
        websocket_url: str = WEBSOCKET_URL,
        ping_interval: float = 30.0,
        connect: Callable[[str], Any] = websocket_connect,
    ):
        load_env()
        self.api_key = api_key or os.environ.get("ALPHAINSIDER_API_KEY")
        self.strategy_id = strategy_id or os.environ.get("ALPHAINSIDER_STRATEGY_ID")
        if not self.api_key:
            raise AlphaInsiderStreamError(
                "ALPHAINSIDER_API_KEY is not set (environment or .env)"
            )
        self.websocket_url = websocket_url
        self.ping_interval = ping_interval
        self._connect = connect

    def _channels(self, channels: list[str] | None) -> list[str]:
        if channels:
            return channels
        if not self.strategy_id:
            raise AlphaInsiderStreamError(
                "strategy_id is required for default channels "
                "(pass it or set ALPHAINSIDER_STRATEGY_ID)"
            )
        return strategy_channels(self.strategy_id)

    async def events(self, channels: list[str] | None = None) -> AsyncIterator[dict[str, Any]]:
        """Yield events from one connection.

        The caller owns reconnect/backoff after connection failures or an
        AlphaInsider ``error`` event.
        """
        subscription = {
            "event": "subscribe",
            "payload": {"channels": self._channels(channels), "token": self.api_key},
        }
        async with self._connect(self.websocket_url) as socket:
            await socket.send(json.dumps(subscription))
            while True:
                try:
                    raw = await asyncio.wait_for(socket.recv(), timeout=self.ping_interval)
                except TimeoutError:
                    await socket.send("ping")
                    continue
                if raw == "pong":
                    continue
                try:
                    payload = json.loads(raw)
                except (TypeError, json.JSONDecodeError) as exc:
                    raise AlphaInsiderStreamError("invalid WebSocket JSON payload") from exc
                for event in payload if isinstance(payload, list) else [payload]:
                    if not isinstance(event, dict):
                        raise AlphaInsiderStreamError("invalid WebSocket event payload")
                    if event.get("event") == "error":
                        raise AlphaInsiderStreamError(str(event.get("response", "stream error")))
                    yield event
