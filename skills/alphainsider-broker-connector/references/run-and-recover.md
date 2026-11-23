# Run and Recover

## Operational data

Use `connection.db` (SQLite, through Python's standard `sqlite3` module or the
`sqlite3` command) for everything that changes during runs. It is a local file
in the project and needs no server or third-party service. `connection.md` only
shows a status view of it.

- Store decimals as text to keep full precision.
- Change state in transactions; a failed run must leave the previous baseline
  and checkpoints intact.
- Never store secrets.
- Start from this schema and extend it as the connection needs:

```sql
CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT);
-- applied leverage, fee, slippage; status (active, paused, blocked); block reason; run lock
CREATE TABLE allocations (
  strategy_id TEXT PRIMARY KEY,
  target_percent TEXT,  -- plan.md target when last applied
  percent TEXT,         -- weight at the last baseline (p_i)
  baseline_value TEXT,  -- strategy value at the last baseline (V0_i)
  baseline_at TEXT,
  checkpoint_at TEXT,   -- created_at of the last processed trade event
  checkpoint_id TEXT    -- timeline_id of the last processed trade event
);
CREATE TABLE symbols (stock_id TEXT PRIMARY KEY, broker_symbol TEXT, status TEXT, note TEXT, updated_at TEXT);
CREATE TABLE runs (run_id INTEGER PRIMARY KEY, started_at TEXT, finished_at TEXT,
  trigger TEXT, result TEXT, broker_value TEXT, note TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, run_id INTEGER, broker_symbol TEXT, type TEXT,
  quantity TEXT, est_price TEXT, status TEXT, broker_order_id TEXT, updated_at TEXT);
CREATE TABLE incidents (incident_id INTEGER PRIMARY KEY, run_id INTEGER, opened_at TEXT,
  closed_at TEXT, summary TEXT, repair TEXT, status TEXT);
```

## Prepare the runtime workflow

- Write the runbook in `connection.md` so a fresh scheduled agent without chat
  history or this skill can complete a run. Either scripts implement the
  [rebalance math](rebalance-math.md), or the runbook carries the formulas it needs.
- Link the runbook from `plan.md` and the scheduled task.
- Use credentials through the recorded injection or private loading methods
  without additional persistent copies; the first scheduled run confirms access.
- Make dry runs technically unable to submit or cancel orders or to advance
  baselines and checkpoints.
- Distinguish known results from uncertain order outcomes and prevent duplicate
  execution, including sequential duplicate triggers.

## Run the connection

Once the user agrees to go live during setup, scheduled and manual runs place
orders without asking the user.

1. Read fresh `plan.md` and the runbook; respect pauses and unresolved incidents.
2. Acquire exclusivity before any broker work, for example a lock row in
   `connection.db` with an expiry.
   - Cover the run, evaluation, repair, and retries.
   - All scheduled and manual entry points participate; overlapping invocations exit.
3. Verify the AlphaInsider account matches `plan.md` following
   [credentials](credentials.md). Check `getStrategySubscriptions` for an active
   subscription of the chosen asset type for each allocation. If any is missing
   or cannot be verified, pause for resolution before touching broker orders.
4. Find what triggers a rebalance.
   - New trades: for each allocation, read `getStrategyTimelines` with
     `type[]=trade` since its checkpoint, paging until complete. Ignore events
     already processed.
   - Edits: `plan.md` targets or leverage differ from the applied values in
     `connection.db`.
   - A manual request, rebalance on start, or a recovery rerun.
   - A deposit or withdrawal, if the user enabled deposit rebalancing in
     `plan.md`: the broker reports a transfer since the last run, or the account
     value changed more than its holdings explain. Otherwise the change spreads
     across allocations at the next rebalance.
   - Without a trigger, record a no-op run and exit.
5. Check that the market for the connection's asset type is open at
   AlphaInsider and the broker. If closed, record the pending trigger without
   advancing checkpoints and exit.
6. Verify broker access. On a live rebalance, cancel open orders in the selected
   account. On a dry run, list the orders that would be cancelled.
7. Read the broker's value, capacity, and positions, and AlphaInsider strategy
   values, positions, and quotes.
8. Compute weights, targets, and orders with the [rebalance math](rebalance-math.md).
9. Record order intents, then place decreases followed by increases. Record each
   result.
10. Re-read broker positions and compare them with the targets, allowing for
    exposure deliberately left in cash.
11. Read strategy values again. In one transaction, save
    [baselines](rebalance-math.md#baselines) from them, advance checkpoints to
    the newest processed trade, record applied targets and leverage, and finish
    the run record. Then refresh the status view in `connection.md`.
12. Apply selected notifications and release exclusivity.

On any error, follow [recovery](#recover-from-an-error).

## Dry run

- Run steps 1–8 with current data and save the proposed orders and a dry-run
  record in `connection.db`.
- Never submit or cancel orders, and never change baselines or checkpoints.
- Required during setup and after every self-heal.
  - During setup, show the user the orders, the resulting weights, and any
    exposure left in cash.
  - After a self-heal, evaluate the result as part of the recovery checks
    without waiting for the user, and summarize it in the notification.

## Recover from an error

1. Stop order work, save the incident, and block new runs in `connection.db`.
2. Pause the scheduler and verify the pause.
   - If unverified, keep runs blocked and report the required action.
3. Diagnose against `plan.md` and the saved evidence in `connection.db`.
4. Decide whether to self-heal and repair when eligible.
   - Require self-healing enabled, preservation of `plan.md` decisions, and no
     human input or new authority.
   - Repair only the implementation: scripts, runbook steps, symbol mapping, and
     broker facts. Never change allocations, leverage, credentials, the
     access method, or `plan.md` decisions.
   - Exhaust the [session recovery steps](credentials.md#broker-credentials-and-sessions)
     before asking the user to log in.
   - Otherwise leave paused, record what the user must resolve, and end recovery.
5. [Dry-run](#dry-run) the fix and run meaningful checks without orders.
   - If checks fail or available execution time runs out, leave a coherent paused
     implementation and save the diagnosis and next action.
6. After checks pass, reconcile uncertain previous orders against the broker's
   orders and positions before placing new ones.
   - Leave paused if an outcome remains unresolved.
7. Choose an immediate rerun or the next scheduled run.
   - An immediate rerun keeps the scheduler paused and admits only the recovery
     owner through this incident's block, under the same exclusivity and checks.
   - If the rerun fails, keep paused and record the unresolved issue.
8. After recovery succeeds, clear this incident's block and resume the scheduler.
   - Never override a later user pause.
   - Verify and record actual scheduler state.
9. Record the outcome and send the selected notification.
   - Hand off unfinished recovery for any later user chat.
   - Leave paused when self-healing is disabled, needs human input, fails, or the
     agent is interrupted after pausing; preserve diagnosis and next action.

## Send selected notifications

- Use the events, channels, and destinations agreed in `plan.md`.
- Select the exact label:
  - `🚨 Error — Action Required`
    - The connection is paused until the user acts: explain the issue,
      recommended next step, and required information or decision.
  - `🔄 Retrying — No Action Required`
    - An automatic retry is underway or scheduled: explain what is retried and
      what happens next.
  - `🛠️ Self-Healed — No Action Required`
    - The repair passed verification and runs resumed: explain what changed,
      scheduler state, and next run.
  - `⚠️ Warning — No Action Required`
    - Useful information, such as exposure left in cash or a detected deposit or
      withdrawal.
  - `✅ Rebalanced — No Action Required`
    - A rebalance completed: summarize orders and resulting weights.
- Send a short, understandable message identifying the connection, effect,
  automation state, and next step.
  - Keep technical diagnostics in `connection.db` and secrets in the selected
    authoritative storage following [credentials](credentials.md).
- Record delivery failures honestly. Never claim an unavailable channel notified
  the user.
