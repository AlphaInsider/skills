"""Reconcile current AlphaInsider state before generating paper orders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class StrategySnapshot:
    """Positions and open orders as AlphaInsider currently sees them.
    Amounts and totals are strategy-normalized."""

    positions: list[dict[str, Any]]
    open_orders: list[dict[str, Any]]

    @property
    def has_open_orders(self) -> bool:
        return bool(self.open_orders)

    def position_for(self, stock_id: str) -> dict[str, Any] | None:
        return next((p for p in self.positions if p.get("stock_id") == stock_id), None)

    def orders_for(self, stock_id: str) -> list[dict[str, Any]]:
        return [o for o in self.open_orders if o.get("stock_id") == stock_id]


def reconcile(client: Any, strategy_id: str | None = None) -> StrategySnapshot:
    """Fetch positions and open orders so each decision cycle starts from the
    strategy's actual state, not an assumed one."""
    return StrategySnapshot(
        positions=client.get_positions(strategy_id=strategy_id),
        open_orders=client.get_orders(strategy_id=strategy_id),
    )
