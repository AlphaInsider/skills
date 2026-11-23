# Connection Plan

## Current state

- Keep enough context to resume.
  - Never include secret values.
  - Host/runtime, project location, scheduler binding, and
    [access status/evidence](workflow-contracts.md#check-platform-and-automation-access).
  - Current phase, last completed action, open questions, what is waiting, next
    step, and last update.
  - Actual scheduler state, pause reasons, and unresolved incidents.

## Broker

- Broker, non-secret account identifier, paper or live, and asset type.
- Accounts offered and why the user chose this one.
- Chosen access method and why; link broker facts in `connection.md`.
- Confirmed AlphaInsider `user_id`.
- Each credential's authoritative storage reference and runtime access method,
  verification status, and missing access; never secret values.

## Allocations

- Strategies with name, ID, and target percent as the user set them. Current
  drifted weights live in `connection.db`; editing a target here applies it at
  the next run following [baselines](rebalance-math.md#baselines).
- Leverage `L` and the account's `L_max` when chosen; fee and slippage reserves.
- Rebalance on start, deposit/withdrawal rebalancing, and close-on-stop choices.
- Account-wide scope confirmation and holdings the user expected to close.

## Automation

- Polling cadence, scheduler task identity, and next run.
- Live test trade: allowed or declined, and its result.
- Self-healing enabled or disabled and relevant user decisions.
- Notification events, channels, and safe destination references; delivery
  status and limitations.

## Decisions

- Settled answers from setup and later changes, with dates. Distinguish
  agreements from proposals.
