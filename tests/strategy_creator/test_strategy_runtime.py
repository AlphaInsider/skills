import json

import pytest

from scripts.strategy_runtime import EventCheckpoint, StrategyRunner, StrategySnapshot, reconcile


class FakeAlphaClient:
    def __init__(self, positions=None, orders=None):
        self.positions = positions or []
        self.orders = orders or []

    def get_positions(self, strategy_id=None):
        return self.positions

    def get_orders(self, strategy_id=None):
        return self.orders


# -- EventCheckpoint ---------------------------------------------------------


def test_checkpoint_marks_and_reloads_from_disk(tmp_path):
    path = tmp_path / "state" / "checkpoint.json"
    checkpoint = EventCheckpoint(path)
    assert checkpoint.last_event_id is None
    assert checkpoint.is_new("bar-2026-07-28T20:00")

    checkpoint.mark("bar-2026-07-28T20:00")
    assert not checkpoint.is_new("bar-2026-07-28T20:00")

    reloaded = EventCheckpoint(path)
    assert reloaded.last_event_id == "bar-2026-07-28T20:00"
    assert not reloaded.is_new("bar-2026-07-28T20:00")
    assert reloaded.is_new("bar-2026-07-28T20:05")


def test_checkpoint_write_is_atomic_and_leaves_no_temp_files(tmp_path):
    path = tmp_path / "checkpoint.json"
    checkpoint = EventCheckpoint(path)
    for event_id in ("e1", "e2", "e3"):
        checkpoint.mark(event_id)
    assert json.loads(path.read_text()) == {"last_event_id": "e3"}
    assert [entry.name for entry in tmp_path.iterdir()] == ["checkpoint.json"]


def test_checkpoint_prevents_duplicate_submissions(tmp_path):
    checkpoint = EventCheckpoint(tmp_path / "checkpoint.json")
    submitted = []
    for event_id in ["e1", "e1", "e2"]:  # replayed event after a reconnect
        if checkpoint.is_new(event_id):
            submitted.append(event_id)
            checkpoint.mark(event_id)
    assert submitted == ["e1", "e2"]


# -- reconcile ---------------------------------------------------------------


def test_reconcile_snapshots_positions_and_orders():
    client = FakeAlphaClient(
        positions=[{"stock_id": "SPY:ARCX", "amount": "8"}],
        orders=[{"stock_id": "SPY:ARCX", "order_id": "o1"}],
    )
    snapshot = reconcile(client)
    assert isinstance(snapshot, StrategySnapshot)
    assert snapshot.has_open_orders
    assert snapshot.position_for("SPY:ARCX")["amount"] == "8"
    assert snapshot.position_for("MSFT:XNAS") is None
    assert snapshot.orders_for("SPY:ARCX") == [{"stock_id": "SPY:ARCX", "order_id": "o1"}]


# -- StrategyRunner ----------------------------------------------------------


def test_run_once_executes_single_cycle():
    calls = []
    runner = StrategyRunner(lambda: calls.append(1))
    runner.run_once()
    assert calls == [1]


def test_run_once_propagates_errors():
    def step():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        StrategyRunner(step).run_once()


def test_run_stops_on_shutdown_request():
    calls = []

    def step():
        calls.append(1)
        if len(calls) == 3:
            runner.request_shutdown()

    runner = StrategyRunner(step, poll_interval=0, sleep=lambda seconds: None)
    runner.run()
    assert len(calls) == 3


def test_run_backs_off_exponentially_and_recovers():
    attempts = []
    waits = []
    errors = []

    def step():
        attempts.append(1)
        if len(attempts) <= 2:
            raise ConnectionError("stream dropped")

    def sleeping(seconds):
        waits.append(seconds)
        if len(attempts) == 3:
            runner.request_shutdown()

    runner = StrategyRunner(
        step,
        poll_interval=60,
        initial_backoff=1,
        max_backoff=300,
        sleep=sleeping,
        on_error=errors.append,
    )
    runner.run()

    assert waits == [1, 2, 60]  # backoff, doubled backoff, then normal polling
    assert len(errors) == 2
    assert all(isinstance(error, ConnectionError) for error in errors)


def test_backoff_is_capped():
    waits = []

    def step():
        raise ConnectionError("still down")

    def sleeping(seconds):
        waits.append(seconds)
        if len(waits) == 3:
            runner.request_shutdown()

    runner = StrategyRunner(
        step, initial_backoff=100, max_backoff=150, sleep=sleeping, on_error=lambda exc: None
    )
    runner.run()
    assert waits == [100, 150, 150]


def test_signal_handlers_trigger_shutdown():
    runner = StrategyRunner(lambda: None)
    assert not runner.shutdown_event.is_set()
    runner.request_shutdown(15, None)  # signature matches signal handlers
    assert runner.shutdown_event.is_set()
