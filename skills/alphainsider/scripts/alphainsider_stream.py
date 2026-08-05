#!/usr/bin/env python3
"""Thin executable and importable wrapper for AlphaInsider WebSocket events."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from collections.abc import AsyncIterator, Sequence
from typing import Any

from websockets import connect as _websocket_connect

from alphainsider_request import _configured_value, _redact


WEBSOCKET_URL = "wss://alphainsider.com/ws"

__all__ = ["AlphaInsiderStreamError", "stream_events"]


class AlphaInsiderStreamError(Exception):
    """AlphaInsider rejected a subscription or returned an invalid event."""


async def stream_events(
    channels: Sequence[str],
    *,
    websocket_url: str = WEBSOCKET_URL,
    ping_interval: float = 30.0,
) -> AsyncIterator[dict[str, Any]]:
    """Yield events for the complete caller-provided AlphaInsider channel list."""
    selected_channels = [channel for channel in channels if channel]
    if not selected_channels:
        raise AlphaInsiderStreamError("at least one channel is required")

    api_key = _configured_value("ALPHAINSIDER_API_KEY", os.getcwd())
    if not api_key:
        raise AlphaInsiderStreamError(
            "ALPHAINSIDER_API_KEY is not set (environment or .env)"
        )

    subscription = {
        "event": "subscribe",
        "payload": {"channels": selected_channels, "token": api_key},
    }
    try:
        async with _websocket_connect(websocket_url) as socket:
            await socket.send(json.dumps(subscription))
            while True:
                try:
                    raw = await asyncio.wait_for(socket.recv(), timeout=ping_interval)
                except TimeoutError:
                    await socket.send("ping")
                    continue
                if raw == "pong":
                    continue
                try:
                    payload = json.loads(raw)
                except (TypeError, json.JSONDecodeError) as exc:
                    raise AlphaInsiderStreamError(
                        "invalid WebSocket JSON payload"
                    ) from exc
                for event in payload if isinstance(payload, list) else [payload]:
                    if not isinstance(event, dict):
                        raise AlphaInsiderStreamError(
                            "invalid WebSocket event payload"
                        )
                    event = _redact(event, (api_key,))
                    if event.get("event") == "error":
                        raise AlphaInsiderStreamError(
                            str(event.get("response", "stream error"))
                        )
                    yield event
    except AlphaInsiderStreamError:
        raise
    except Exception as exc:
        message = _redact(str(exc), (api_key,))
        raise AlphaInsiderStreamError(f"WebSocket failed: {message}") from None


async def _run(args: argparse.Namespace) -> None:
    async for event in stream_events(
        args.channel,
        websocket_url=args.websocket_url,
        ping_interval=args.ping_interval,
    ):
        print(json.dumps(event, separators=(",", ":")), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stream events from AlphaInsider WebSocket channels."
    )
    parser.add_argument(
        "--channel",
        action="append",
        required=True,
        help="Channel name from the WebSocket reference. Repeat as needed.",
    )
    parser.add_argument(
        "--websocket-url",
        default=WEBSOCKET_URL,
        help=f"WebSocket URL. Defaults to {WEBSOCKET_URL}.",
    )
    parser.add_argument(
        "--ping-interval",
        type=float,
        default=30.0,
        help="Seconds of inactivity before sending ping.",
    )
    args = parser.parse_args()

    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        return 0
    except AlphaInsiderStreamError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
