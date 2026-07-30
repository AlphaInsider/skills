"""Atomic tracking of the last processed market event.

The generated strategy marks each market event (bar timestamp, trade ID, …)
after acting on it. On restart or stream replay, ``is_new`` rejects the event
that was already processed, preventing duplicate paper-order submissions.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


class EventCheckpoint:
    """Persist the last processed event ID with an atomic file replacement."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._last: str | None = None
        if self.path.exists():
            self._last = json.loads(self.path.read_text()).get("last_event_id")

    @property
    def last_event_id(self) -> str | None:
        return self._last

    def is_new(self, event_id: str) -> bool:
        """Return whether ``event_id`` differs from the processed event."""
        return event_id != self._last

    def mark(self, event_id: str) -> None:
        """Atomically record ``event_id`` as processed."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=self.path.parent, prefix=self.path.name, suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as handle:
                handle.write(json.dumps({"last_event_id": event_id}))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, self.path)
        except BaseException:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
        self._last = event_id
