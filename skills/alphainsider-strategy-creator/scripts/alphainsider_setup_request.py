#!/usr/bin/env python3
"""Agent-only AlphaInsider REST wrapper that hides ALPHAINSIDER_API_KEY."""

from __future__ import annotations

if __name__ != "__main__":
    raise RuntimeError(
        "alphainsider_setup_request.py is CLI-only; run it from the strategy "
        "project root"
    )

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


BASE_URL = "https://alphainsider.com/api"
_PRINTABLE_CONFIG = "ALPHAINSIDER_STRATEGY_ID"
_READABLE_NAMES = frozenset({"ALPHAINSIDER_API_KEY", _PRINTABLE_CONFIG})
_REDACTED = "<redacted>"


class _SetupRequestError(ValueError):
    """The setup request cannot be built or sent safely."""


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        self.exit(
            2,
            "error: invalid arguments; pass METHOD PATH or "
            "--print-config ALPHAINSIDER_STRATEGY_ID\n",
        )


def _configured_value(name: str, cwd: str) -> str | None:
    if name not in _READABLE_NAMES:
        raise _SetupRequestError(f"unsupported AlphaInsider setting: {name}")

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
            if key.strip() != name:
                continue
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


def _parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected key=value")
    key, parsed_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("key cannot be empty")
    return key, parsed_value


def _normalize_path(path: str) -> str:
    return path if path.startswith("/") else f"/{path}"


def _query_items(query: list[tuple[str, str]] | None) -> list[tuple[str, str]]:
    return list(query or ())


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


def _redact(value: object, secrets: tuple[str, ...]) -> object:
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


def _collect_secrets(
    api_key: str | None,
    query_items: list[tuple[str, str]],
    body: object,
) -> tuple[str, ...]:
    secrets = _credential_values(body)
    secrets.extend(
        value for key, value in query_items if _is_credential_key(key) and value
    )
    if api_key:
        secrets.append(api_key)
    return tuple(dict.fromkeys(secrets))


def _build_request(
    method: str,
    path: str,
    *,
    query: list[tuple[str, str]] | None,
    body: object,
    base_url: str,
    api_key: str | None,
) -> tuple[urllib.request.Request, object, tuple[str, ...]]:
    normalized_path = _normalize_path(path)
    query_items = _query_items(query)
    prepared_body = dict(body) if isinstance(body, dict) else body
    url = f"{base_url.rstrip('/')}{normalized_path}"
    if query_items:
        url = f"{url}?{urllib.parse.urlencode(query_items)}"

    headers = {"Accept": "application/json"}
    data = None
    if prepared_body is not None:
        data = json.dumps(prepared_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = api_key

    return (
        urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method.upper(),
        ),
        prepared_body,
        _collect_secrets(api_key, query_items, prepared_body),
    )


def _api_error(
    payload: bytes,
    content_type: str,
    status_code: int,
    secrets: tuple[str, ...],
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


def _send_request(
    prepared: urllib.request.Request,
    secrets: tuple[str, ...],
    timeout: float,
) -> Any:
    try:
        with urllib.request.urlopen(prepared, timeout=timeout) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "")
            status_code = response.getcode()
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        content_type = exc.headers.get("Content-Type", "")
        raise _SetupRequestError(
            _api_error(payload, content_type, exc.code, secrets)
        ) from None
    except urllib.error.URLError as exc:
        reason = _redact(str(exc.reason), secrets)
        raise _SetupRequestError(f"request failed: {reason}") from None

    if "json" not in content_type.lower():
        raise _SetupRequestError("binary responses are not supported")
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _SetupRequestError("invalid JSON response") from exc
    if not isinstance(decoded, dict):
        raise _SetupRequestError("invalid AlphaInsider response envelope")
    if not decoded.get("success"):
        raise _SetupRequestError(
            str(_redact(decoded.get("response", "Request failed."), secrets))
        )
    if "response" not in decoded:
        raise _SetupRequestError("AlphaInsider response is missing response data")
    return _redact(decoded["response"], secrets)


def _print_dry_run(
    prepared: urllib.request.Request,
    body: object,
    secrets: tuple[str, ...],
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


def _print_config(name: str) -> int:
    if name != _PRINTABLE_CONFIG:
        print(
            "error: --print-config accepts only ALPHAINSIDER_STRATEGY_ID",
            file=sys.stderr,
        )
        return 2
    value = _configured_value(name, os.getcwd())
    if not value:
        print(f"error: {name} is not configured", file=sys.stderr)
        return 1
    print(value)
    return 0


def _main(argv: list[str] | None = None) -> int:
    parser = _SafeArgumentParser(
        description="Agent-only AlphaInsider REST request that hides the API key."
    )
    parser.add_argument("method", nargs="?", help="HTTP method, such as GET or POST.")
    parser.add_argument("path", nargs="?", help="API path, such as /verifyToken.")
    parser.add_argument(
        "--print-config",
        metavar="NAME",
        help="Print one public configured name. Only ALPHAINSIDER_STRATEGY_ID.",
    )
    parser.add_argument(
        "--query",
        action="append",
        type=_parse_key_value,
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
    args = parser.parse_args(argv)

    if args.print_config:
        if args.method is not None or args.path is not None or args.dry_run:
            parser.error("a config lookup does not accept METHOD PATH or --dry-run")
        try:
            return _print_config(args.print_config)
        except (_SetupRequestError, OSError, UnicodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.method is None or args.path is None:
        parser.error("a request requires METHOD PATH")

    try:
        body = json.loads(args.json) if args.json else None
    except json.JSONDecodeError as exc:
        print(f"invalid --json: {exc}", file=sys.stderr)
        return 2

    api_key = _configured_value("ALPHAINSIDER_API_KEY", os.getcwd())
    try:
        prepared, prepared_body, secrets = _build_request(
            args.method,
            args.path,
            query=args.query,
            body=body,
            base_url=args.base_url,
            api_key=api_key,
        )
    except _SetupRequestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        _print_dry_run(prepared, prepared_body, secrets)
        return 0

    try:
        response = _send_request(prepared, secrets, args.timeout)
    except _SetupRequestError as exc:
        print(
            json.dumps({"success": False, "response": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return 1

    print(json.dumps({"success": True, "response": response}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
