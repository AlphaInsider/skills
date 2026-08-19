#!/usr/bin/env python3
"""Silently check the canonical Strategy Creator version for an update."""

from __future__ import annotations

import re
from http.client import HTTPException
from pathlib import Path
from urllib.request import Request, urlopen


VERSION_REFERENCE = (
    Path(__file__).resolve().parents[1] / "references" / "versioning.md"
)
REMOTE_VERSION_URL = (
    "https://raw.githubusercontent.com/AlphaInsider/skills/master/"
    "skills/alphainsider-strategy-creator/references/versioning.md"
)
UPDATE_COMMAND = "npx skills@latest update alphainsider-api alphainsider-strategy-creator"
TIMEOUT_SECONDS = 3
MAX_RESPONSE_BYTES = 64 * 1024
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)


class UpdateCheckError(ValueError):
    """The local or remote version document cannot be safely interpreted."""


def parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_PATTERN.fullmatch(value)
    if match is None:
        raise UpdateCheckError("invalid semantic version")
    return tuple(int(part) for part in match.groups())


def version_from_reference(text: str) -> str:
    match = FRONTMATTER_PATTERN.match(text)
    if match is None:
        raise UpdateCheckError("missing version frontmatter")

    versions = []
    for line in match.group("body").splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() == "current_version":
            versions.append(value.strip())

    if len(versions) != 1:
        raise UpdateCheckError("expected one current_version")
    parse_semver(versions[0])
    return versions[0]


def fetch_remote_reference() -> str:
    request = Request(
        REMOTE_VERSION_URL,
        headers={"User-Agent": "AlphaInsider-Strategy-Creator-Version-Check"},
    )
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        if response.geturl() != REMOTE_VERSION_URL:
            raise UpdateCheckError("unexpected redirect")
        payload = response.read(MAX_RESPONSE_BYTES + 1)

    if len(payload) > MAX_RESPONSE_BYTES:
        raise UpdateCheckError("version reference is too large")
    return payload.decode("utf-8")


def update_notice(installed: str, available: str) -> str | None:
    if parse_semver(available) <= parse_semver(installed):
        return None
    return (
        f"Strategy Creator {available} is available (installed: {installed}).\n"
        "To update both required AlphaInsider skills, run:\n"
        f"{UPDATE_COMMAND}\n"
        "Then invoke Strategy Creator again."
    )


def check_for_update() -> str | None:
    installed = version_from_reference(VERSION_REFERENCE.read_text(encoding="utf-8"))
    available = version_from_reference(fetch_remote_reference())
    return update_notice(installed, available)


def main() -> int:
    try:
        notice = check_for_update()
    except (OSError, HTTPException, UnicodeError, UpdateCheckError):
        return 0
    if notice is not None:
        print(notice)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
