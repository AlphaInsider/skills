"""Generic strategy loop: ``run_once`` and continuous ``run`` with graceful
shutdown and exponential backoff on errors (covers stream reconnection).

External tooling is responsible for hosting; this runner only drives cycles.
"""

from __future__ import annotations

import logging
import signal
import threading
from typing import Any, Callable

logger = logging.getLogger(__name__)


class StrategyRunner:
    """Drives a strategy ``step`` callable. One step is a full decision cycle:
    reconcile AlphaInsider state, fetch market data, decide, submit orders."""

    def __init__(
        self,
        step: Callable[[], Any],
        *,
        poll_interval: float = 60.0,
        initial_backoff: float = 1.0,
        max_backoff: float = 300.0,
        sleep: Callable[[float], Any] | None = None,
        on_error: Callable[[Exception], Any] | None = None,
    ):
        self._step = step
        self._poll_interval = poll_interval
        self._initial_backoff = initial_backoff
        self._max_backoff = max_backoff
        self._on_error = on_error
        self.shutdown_event = threading.Event()
        # Default sleep waits on the shutdown event so signals interrupt it.
        self._sleep = sleep or (lambda seconds: self.shutdown_event.wait(seconds))

    def request_shutdown(self, *_args: Any) -> None:
        self.shutdown_event.set()

    def install_signal_handlers(self) -> None:
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, self.request_shutdown)

    def run_once(self) -> Any:
        """Execute exactly one decision cycle; exceptions propagate."""
        return self._step()

    def run(self) -> None:
        """Loop until shutdown. A failing step (network drop, API error) is
        retried with exponential backoff; success resets the backoff."""
        backoff = self._initial_backoff
        while not self.shutdown_event.is_set():
            try:
                self._step()
                backoff = self._initial_backoff
                wait = self._poll_interval
            except Exception as exc:
                if self._on_error is not None:
                    self._on_error(exc)
                else:
                    logger.warning("strategy step failed; retrying in %.1fs: %s", backoff, exc)
                wait = backoff
                backoff = min(backoff * 2, self._max_backoff)
            if self.shutdown_event.is_set():
                break
            self._sleep(wait)
