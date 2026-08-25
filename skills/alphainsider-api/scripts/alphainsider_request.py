#!/usr/bin/env python3
"""Thin executable and importable wrapper for the AlphaInsider REST API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any


BASE_URL = "https://alphainsider.com/api"

__all__ = [
    "AlphaInsiderRequestError",
    "calculate_input_multiplier",
    "percent_change",
    "position_exposure_percent",
    "position_gain_loss_amount",
    "position_gain_loss_percent",
    "request",
    "to_display",
    "to_normalized",
]

_CONFIGURED_NAMES = {
    "ALPHAINSIDER_API_KEY",
    "ALPHAINSIDER_STRATEGY_ID",
    "ALPHAINSIDER_BOT_ID",
}
_REDACTED = "<redacted>"

STRATEGY_ARRAY_QUERY_PATHS = {
    "/getStrategies",
    "/getStrategyValues",
    "/getRecommendedStrategies",
    "/getStrategySubscriptions",
    "/getStrategyTimelines",
}

STRATEGY_QUERY_PATHS = {
    "/getStrategyPerformance",
    "/getStrategyCalculation",
    "/getPositions",
    "/getOrders",
    "/getMaxOrderSize",
}

STRATEGY_BODY_PATHS = {
    "/updateStrategy",
    "/updateStrategyPrice",
    "/deleteStrategy",
    "/newStrategySubscription",
    "/deleteStrategySubscription",
    "/updateStrategySubscriptionNotifications",
    "/updateStrategyCalculation",
    "/deleteStrategyCalculation",
    "/newPost",
    "/previewPost",
    "/newOrder",
    "/newOrderAllocations",
    "/deleteOrder",
    "/newOrderWebhook",
}

BOT_ARRAY_QUERY_PATHS = {
    "/getBots",
    "/getBotAllocations",
}

BOT_QUERY_PATHS = {
    "/getBotInfo",
    "/getBotPerformance",
    "/getBotActivities",
}

BOT_BODY_PATHS = {
    "/updateBotSettings",
    "/updateBotBrokerKeys",
    "/updateBotNotifications",
    "/deleteBot",
    "/startBot",
    "/stopBot",
    "/resetBot",
    "/resetBotPerformance",
    "/updateBotAllocations",
}

BODY_TOKEN_PATHS = {
    "/newOrderWebhook": "api_token",
}


class AlphaInsiderRequestError(Exception):
    """The request failed or AlphaInsider returned an unusable response."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _decimal(value: Any, name: str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc


def _positive_multiplier(value: Any) -> Decimal:
    multiplier = _decimal(value, "input_multiplier")
    if multiplier <= 0:
        raise ValueError("input_multiplier must be positive")
    return multiplier


def calculate_input_multiplier(input_value: Any, baseline_strategy_value: Any) -> Decimal:
    """Calculate ``input_value / baseline_strategy_value`` precisely."""
    baseline = _decimal(baseline_strategy_value, "baseline_strategy_value")
    if baseline == 0:
        raise ValueError("baseline_strategy_value cannot be zero")
    multiplier = _decimal(input_value, "input_value") / baseline
    if multiplier <= 0:
        raise ValueError("calculated input_multiplier must be positive")
    return multiplier


def to_display(normalized_value: Any, input_multiplier: Any) -> Decimal:
    """Convert a normalized strategy value to the user's displayed scale."""
    return _decimal(normalized_value, "normalized_value") * _positive_multiplier(
        input_multiplier
    )


def to_normalized(display_value: Any, input_multiplier: Any) -> Decimal:
    """Convert a user-visible value to normalized strategy units."""
    return _decimal(display_value, "display_value") / _positive_multiplier(
        input_multiplier
    )


def percent_change(current_value: Any, baseline_value: Any) -> Decimal:
    """Calculate percentage change from a nonzero baseline."""
    current = _decimal(current_value, "current_value")
    baseline = _decimal(baseline_value, "baseline_value")
    if baseline == 0:
        raise ValueError("baseline_value cannot be zero")
    return ((current - baseline) / baseline) * Decimal("100")


def position_exposure_percent(
    amount: Any,
    strategy_value: Any,
    *,
    bid: Any | None = None,
    ask: Any | None = None,
    price: Any | None = None,
) -> Decimal:
    """Calculate signed position exposure using bid for longs and ask for shorts."""
    position_amount = _decimal(amount, "amount")
    total_strategy_value = _decimal(strategy_value, "strategy_value")
    if total_strategy_value == 0:
        raise ValueError("strategy_value cannot be zero")

    quote = bid if position_amount >= 0 else ask
    if quote is None:
        quote = price
    if quote is None:
        raise ValueError("a current bid/ask or fallback price is required")
    current_price = _decimal(quote, "current_price")
    return (
        (position_amount * current_price) / total_strategy_value
    ) * Decimal("100")


def position_gain_loss_amount(
    amount: Any,
    current_price: Any,
    entry_price: Any,
    input_multiplier: Any,
) -> Decimal:
    """Calculate user-scaled position gain or loss."""
    position_amount = _decimal(amount, "amount")
    current = _decimal(current_price, "current_price")
    entry = _decimal(entry_price, "entry_price")
    return position_amount * (current - entry) * _positive_multiplier(input_multiplier)


def position_gain_loss_percent(
    amount: Any,
    current_price: Any,
    position_total: Any,
) -> Decimal:
    """Calculate position gain/loss percent with liability sign adjustment."""
    position_amount = _decimal(amount, "amount")
    current = _decimal(current_price, "current_price")
    total = _decimal(position_total, "position_total")
    if total == 0:
        raise ValueError("position_total cannot be zero")
    result = (((position_amount * current) - total) / total) * Decimal("100")
    return result * Decimal("-1") if position_amount < 0 else result


def _configured_value(name: str, cwd: str) -> str | None:
    """Read one recognized AlphaInsider setting without exposing other values."""
    if name not in _CONFIGURED_NAMES:
        raise ValueError(f"unsupported AlphaInsider setting: {name}")

    environment_value = os.environ.get(name)
    if environment_value:
        return environment_value

    path = os.path.join(cwd, ".env")
    if not os.path.isfile(path):
        return None

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key == name:
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] == '"':
                    try:
                        decoded = json.loads(value)
                    except json.JSONDecodeError:
                        decoded = value[1:-1]
                    if isinstance(decoded, str):
                        value = decoded
                elif len(value) >= 2 and value[0] == value[-1] == "'":
                    value = value[1:-1]
                return value or None
    return None


def parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected key=value")
    key, parsed_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("key cannot be empty")
    return key, parsed_value


def normalize_path(path: str) -> str:
    return path if path.startswith("/") else f"/{path}"


def _query_items(
    query: Mapping[str, Any] | Sequence[tuple[str, Any]] | None,
) -> list[tuple[str, str]]:
    if query is None:
        return []
    source = query.items() if isinstance(query, Mapping) else query
    items: list[tuple[str, str]] = []
    for key, value in source:
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            items.extend((str(key), str(item)) for item in value)
        else:
            items.append((str(key), str(value)))
    return items


def _has_query_key(query: Sequence[tuple[str, str]], *names: str) -> bool:
    wanted = set(names)
    return any(key in wanted for key, _ in query)


def _body_has_key(body: object, name: str) -> bool:
    return isinstance(body, dict) and name in body


def _apply_defaults(
    path: str,
    query: list[tuple[str, str]],
    body: object,
    api_key: str | None,
    strategy_id: str | None,
    bot_id: str | None,
) -> object:
    """Apply private token and configured ID defaults without replacing inputs."""
    if path in BODY_TOKEN_PATHS:
        field = BODY_TOKEN_PATHS[path]
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise AlphaInsiderRequestError(f"{path} requires a JSON object body")
        if field not in body:
            if not api_key:
                raise AlphaInsiderRequestError(
                    f"ALPHAINSIDER_API_KEY is required for {path}"
                )
            body[field] = api_key

    if strategy_id:
        if path in STRATEGY_ARRAY_QUERY_PATHS and not _has_query_key(
            query, "strategy_id[]", "strategy_id"
        ):
            query.append(("strategy_id[]", strategy_id))
        elif path in STRATEGY_QUERY_PATHS and not _has_query_key(
            query, "strategy_id", "strategy_id[]"
        ):
            query.append(("strategy_id", strategy_id))
        elif path in STRATEGY_BODY_PATHS and not _body_has_key(body, "strategy_id"):
            if body is None:
                body = {}
            if isinstance(body, dict):
                body["strategy_id"] = strategy_id

    if bot_id:
        if path in BOT_ARRAY_QUERY_PATHS and not _has_query_key(
            query, "bot_id[]", "bot_id"
        ):
            query.append(("bot_id[]", bot_id))
        elif path in BOT_QUERY_PATHS and not _has_query_key(
            query, "bot_id", "bot_id[]"
        ):
            query.append(("bot_id", bot_id))
        elif path in BOT_BODY_PATHS and not _body_has_key(body, "bot_id"):
            if body is None:
                body = {}
            if isinstance(body, dict):
                body["bot_id"] = bot_id

    return body


def _build_request(
    method: str,
    path: str,
    *,
    query: Mapping[str, Any] | Sequence[tuple[str, Any]] | None = None,
    body: object = None,
    base_url: str = BASE_URL,
) -> tuple[urllib.request.Request, object, tuple[str, ...]]:
    cwd = os.getcwd()
    api_key = _configured_value("ALPHAINSIDER_API_KEY", cwd)
    strategy_id = _configured_value("ALPHAINSIDER_STRATEGY_ID", cwd)
    bot_id = _configured_value("ALPHAINSIDER_BOT_ID", cwd)

    normalized_path = normalize_path(path)
    query_items = _query_items(query)
    prepared_body = dict(body) if isinstance(body, dict) else body
    prepared_body = _apply_defaults(
        normalized_path,
        query_items,
        prepared_body,
        api_key,
        strategy_id,
        bot_id,
    )

    url = f"{base_url.rstrip('/')}{normalized_path}"
    if query_items:
        url = f"{url}?{urllib.parse.urlencode(query_items)}"

    headers = {"Accept": "application/json"}
    data = None
    if prepared_body is not None:
        data = json.dumps(prepared_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key and normalized_path not in BODY_TOKEN_PATHS:
        headers["Authorization"] = api_key

    secrets = _credential_values(prepared_body)
    secrets.extend(
        value for key, value in query_items if _is_credential_key(key) and value
    )
    if api_key:
        secrets.append(api_key)

    return (
        urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method.upper(),
        ),
        prepared_body,
        tuple(dict.fromkeys(secrets)),
    )


def _is_credential_key(key: object) -> bool:
    normalized = str(key).lower().removesuffix("[]").replace("-", "_")
    return normalized in {
        "accesskey",
        "accesstoken",
        "apikey",
        "authorization",
        "password",
        "refresh_token",
        "secret",
        "secretkey",
        "token",
    } or normalized.endswith(("_key", "_password", "_secret", "_token"))


def _credential_values(value: object) -> list[str]:
    secrets: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if _is_credential_key(key) and isinstance(item, str) and item:
                secrets.append(item)
            else:
                secrets.extend(_credential_values(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            secrets.extend(_credential_values(item))
    return secrets


def _redact(value: object, secrets: Sequence[str] = ()) -> object:
    if isinstance(value, dict):
        return {
            key: _REDACTED
            if _is_credential_key(key)
            else _redact(item, secrets)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item, secrets) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact(item, secrets) for item in value)
    if isinstance(value, str):
        for secret in sorted(set(secrets), key=len, reverse=True):
            if secret:
                value = value.replace(secret, _REDACTED)
        return value
    if isinstance(value, bytes):
        for secret in sorted(set(secrets), key=len, reverse=True):
            if secret:
                value = value.replace(secret.encode(), _REDACTED.encode())
        return value
    return value


def _api_error(
    payload: bytes,
    content_type: str,
    status_code: int,
    secrets: Sequence[str],
) -> str:
    if "json" in content_type.lower():
        try:
            decoded = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
        else:
            if isinstance(decoded, dict) and decoded.get("response") is not None:
                return str(_redact(decoded["response"], secrets))
    return f"HTTP {status_code}"


def request(
    method: str,
    path: str,
    *,
    query: Mapping[str, Any] | Sequence[tuple[str, Any]] | None = None,
    body: object = None,
    base_url: str = BASE_URL,
    timeout: float = 30.0,
) -> Any:
    """Send one AlphaInsider request and return its ``response`` value or bytes."""
    prepared, _, secrets = _build_request(
        method,
        path,
        query=query,
        body=body,
        base_url=base_url,
    )
    try:
        with urllib.request.urlopen(prepared, timeout=timeout) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "")
            status_code = response.getcode()
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        content_type = exc.headers.get("Content-Type", "")
        raise AlphaInsiderRequestError(
            _api_error(payload, content_type, exc.code, secrets),
            status_code=exc.code,
        ) from None
    except urllib.error.URLError as exc:
        reason = _redact(str(exc.reason), secrets)
        raise AlphaInsiderRequestError(f"request failed: {reason}") from None

    if "json" not in content_type.lower():
        return _redact(payload, secrets)
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AlphaInsiderRequestError(
            "invalid JSON response", status_code=status_code
        ) from exc
    if not isinstance(decoded, dict):
        raise AlphaInsiderRequestError(
            "invalid AlphaInsider response envelope", status_code=status_code
        )
    if not decoded.get("success"):
        raise AlphaInsiderRequestError(
            str(_redact(decoded.get("response", "Request failed."), secrets)),
            status_code=status_code,
        )
    if "response" not in decoded:
        raise AlphaInsiderRequestError(
            "AlphaInsider response is missing response data", status_code=status_code
        )
    return _redact(decoded["response"], secrets)


def _print_dry_run(
    prepared: urllib.request.Request,
    body: object,
    secrets: Sequence[str],
) -> None:
    print(
        json.dumps(
            {
                "method": prepared.get_method(),
                "url": _redact(prepared.full_url, secrets),
                "headers": _redact(dict(prepared.header_items()), secrets),
                "body": _redact(body, secrets),
            },
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Make a request to the AlphaInsider REST API."
    )
    parser.add_argument("method", help="HTTP method, such as GET or POST.")
    parser.add_argument("path", help="API path, such as /getStrategies.")
    parser.add_argument(
        "--query",
        action="append",
        type=parse_key_value,
        help="Query parameter as key=value. Repeat as needed.",
    )
    parser.add_argument("--json", help="JSON request body.")
    parser.add_argument(
        "--base-url", default=BASE_URL, help=f"Base URL. Defaults to {BASE_URL}."
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0, help="Request timeout in seconds."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the request without sending it."
    )
    parser.add_argument("--output", help="Write a binary response to this path.")
    args = parser.parse_args()

    try:
        body = json.loads(args.json) if args.json else None
    except json.JSONDecodeError as exc:
        print(f"invalid --json: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        try:
            prepared, prepared_body, secrets = _build_request(
                args.method,
                args.path,
                query=args.query,
                body=body,
                base_url=args.base_url,
            )
        except AlphaInsiderRequestError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        _print_dry_run(prepared, prepared_body, secrets)
        return 0

    try:
        response = request(
            args.method,
            args.path,
            query=args.query,
            body=body,
            base_url=args.base_url,
            timeout=args.timeout,
        )
    except AlphaInsiderRequestError as exc:
        print(
            json.dumps({"success": False, "response": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return 1

    if isinstance(response, bytes):
        if not args.output:
            print("binary response requires --output", file=sys.stderr)
            return 2
        with open(args.output, "wb") as handle:
            handle.write(response)
        return 0

    print(json.dumps({"success": True, "response": response}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
