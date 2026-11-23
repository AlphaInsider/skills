# Connection

Slow-changing operating guidance and a status view for the user. Data that
changes during runs lives in `connection.db`; see
[operational data](run-and-recover.md#operational-data).

## Runbook

- Steps for a fresh scheduled agent to complete a run, following
  [run the connection](run-and-recover.md#run-the-connection).
- Script commands and entry points, including the dry-run entry point.
- How to load credentials privately and recover sessions, by storage reference.
- How to pause, resume, and take the run lock.
- Where `plan.md` and `connection.db` are.

## Broker facts

- Each [broker contract](broker-contract.md) fact with its source and date.
- Unknowns and how the connection handles them.

## Status

Refreshed after each rebalance; read-only. Edit settings through `plan.md`.

- Connection state and next scheduled run.
- Allocations with target and current weights.
- Last rebalance: time, orders, account value.
- Exposure left in cash and why.
- Open incidents and required user actions.
