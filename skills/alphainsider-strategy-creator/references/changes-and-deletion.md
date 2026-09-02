# Changes and Explicit Deletion

This file owns updates, checks of user edits or external changes, and explicit
deletion. Use only create, resume, update, and explicit deletion paths.

## Update an agreed strategy

Preserve the active agreed `plan.md` while an update is being decided. Record
the proposed change, affected decisions, open questions, and prior automation
state in root `pending-update.md`. Mark the pending update Draft while keeping
the current plan Agreed and authoritative for any allowed current operation.

For a behavior-changing update:

1. save in project state that new orders are paused;
2. pause future native automation;
3. wait for the shared run or repair lock to become idle;
4. use the [strategy interview](interview.md) for only changed and dependent
   decisions;
5. show a concise summary of the change and obtain agreement;
6. run every affected credible backtest;
7. update implementation, protected tests, docs, and scheduled-run
   instructions;
8. pass offline checks that prove the implementation follows the plan;
9. update the AlphaInsider description when needed;
10. merge the agreed result into `plan.md` and remove `pending-update.md`; and
11. allow new orders and resume automation when it was active before the
    update.

If safe pause or idle state cannot be verified, do not change files used by
strategy runs. Keep unaffected choices and artifacts. An implementation repair
that does not change the agreed strategy does not need a strategy update.

Performance alone never starts an automatic strategy change. It can prompt a
correctness review. Change trading behavior only when the user chooses and
agrees to that change.

## Review user edits

The AI manages the dedicated project, but the user can edit any file. Detect
changes before writing:

- retain changes that clearly conform to `plan.md`;
- test and document compatible improvements;
- ask the user when an edit changes or obscures intended behavior; and
- never overwrite an unclear user change just to restore generated text.

If a user edit changed behavior, use `pending-update.md` and the normal update
flow. If it broke only implementation while preserving clear intent, repair it
within the agreed scope.

## Detect external changes

Compare the native scheduler, AlphaInsider strategy, description, access
setting, and saved run state with `plan.md`. A mismatch that can affect orders
must pause new orders in project state and pause automation. Repair only wiring
that follows the plan. AlphaInsider strategy identity, schedule frequency,
access mode, or strategy behavior require user agreement.

## Explicit deletion interview

Start deletion only when the user clearly asks. Inventory everything created
or used for this strategy:

- native AI scheduler task;
- AlphaInsider strategy and AlphaInsider strategy ID;
- project source, plan, docs, and tests;
- backtest reports and historical data;
- saved run state, run history, logs, repair journal, and snapshots;
- project `.env` or hosted secrets; and
- API key revocation, which may require a user action in AlphaInsider settings.

Use the interview-round format in `user-communication.md` to ask what to delete
or retain.
Include **Delete everything** as an allowed choice after a clear warning.
Recommend a scope that matches the user's words; otherwise recommend retaining
historical and backtest evidence until the user confirms it is no longer
needed.

Before final confirmation, show exact paths, scheduled task name, AlphaInsider
strategy ID, secret locations without values, retained items, irreversible
effects, and any action the user must complete. Do not infer ownership from a
similar name alone.

## Delete safely

Apply the agreed deletion actions in this order:

1. save in project state that new orders are paused for deletion;
2. pause future automation and wait for the shared lock to become idle;
3. delete the exact attributable scheduler task and verify absence;
4. apply the chosen AlphaInsider strategy action;
5. remove selected secrets and explain any external key-revocation action;
6. delete only the exact selected project data; and
7. report completed, retained, and failed items.

Before AlphaInsider strategy deletion, verify API permission, token user, exact
ID, ownership, subscriber count, open orders, and nonzero positions. Explain
that the current API might not define what deletion does to subscribers,
positions, or open orders. The user can still choose deletion after that
warning.

Deletion cleanup never cancels an order, liquidates a position, submits a
trade, or connects a broker. If AlphaInsider strategy deletion fails, keep the
project and AlphaInsider strategy ID needed for recovery. Delete local recovery
data only when the user explicitly chooses to continue after that failure.

Prefer a recoverable local deletion method when the platform provides one.
Never recursively delete an uncertain path, persistent parent, repository
root, or installed skill directory.

For partial deletion, update `plan.md` with the new resource and automation
state. For full deletion, remove the entire selected project and leave no
tombstone. Do not resume automation during or after deletion.
