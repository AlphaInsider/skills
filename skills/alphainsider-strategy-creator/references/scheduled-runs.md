# Scheduled and User-Triggered Runs

This file owns strategy-run entry types, locking, health, error pauses, repair,
recovery, and notifications. Read it for every scheduled run, scheduler **Run
now**, chat run, chat dry run, operational error, notification event, or
self-heal attempt. `plan.md` and the scheduled-run instructions in
`runtime/runbook.md` remain authoritative.

## Run types and lock

- A scheduled run is an order-capable strategy run.
- Scheduler **Run now** is the same strategy run.
- A chat request to run now is the same strategy run.
- A chat request for a dry run uses current inputs but must not submit, change,
  or cancel orders and must not change saved portfolio or decision state.
  It can write an isolated dry-run report.

A dry run is available only through an explicit chat request. Do not schedule
dry runs.

Every mode first acquires the same one-run-at-a-time project lock. The first
trigger owns the run. If another run is already active, record a skip and exit
before input collection, decision work, position and order checks, or orders.
An explicit scheduler **Run now** or chat run attempts recovery even while
future scheduled runs are paused because of an error. It cannot send an order
until the safety problem is resolved and project state no longer says that new
orders are paused.

Never remove a leftover lock until checks prove that its owning run is not
active. Record that evidence before removing the lock and acquiring a new one.

Hold the lock through result evaluation and any repair attempted by that
run. Release it only after the result, repair state, and rollback state are
saved. When an error remains unresolved, project state must continue to say
that new orders are paused after the lock is released.

## Strategy run

Follow the steps in [strategy implementation](implementation.md). Read fresh
files and state; do not recreate decisions from chat memory. Record scheduled
time, actual start time, run source, data cutoff time, decision, risk checks,
order outcome, health result, and notification result without secrets.

Missed runs do not catch up. A scheduled run that starts too late exits. A
healthy scheduled or user-triggered run creates project history but no success
notification.

## Health evaluation

Evaluate whether the run followed `plan.md`:

- required inputs were available and fresh;
- AlphaInsider strategy and asset types matched;
- current positions, open orders, and saved state were checked and duplicate
  protection completed;
- decision and risk rules were applied;
- expected external results were confirmed or safely classified;
- state and lock integrity remained valid; and
- code, API wiring, and notifications operated as planned.

Profit, loss, return, win rate, or a difference from a backtest is not a health
criterion. A large difference can start a correctness review. It becomes an
error only when evidence shows that implementation or data handling violates
the plan.

Classify an unexpected problem that did not make the run unsafe as a warning.
Classify a failure that prevents a safe run that follows the plan as an error.

## Error response

For every error that prevents a safe run that follows the plan:

1. keep the current lock;
2. save in project state that new orders are paused so another run cannot
   trade;
3. pause future native automation and verify its state when the platform
   allows it;
4. compare current AlphaInsider positions and orders with saved state, then
   diagnose the cause;
5. apply the self-heal choice; and
6. record every action and result.

Set **Automation state** to Paused and record the exact error pause reason.

Warnings, expected no-action results, skips because another run is active, and
a failure to send a notification are not run errors and do not start this
pause flow.

If native pause fails or needs a user-interface action, keep project state set
to prevent new orders. Later strategy runs must exit before order work. Send
the exact pause action when notifications are enabled.

Authentication, ownership, AlphaInsider strategy mismatch, a possibly
submitted order with an unknown result, corrupt saved trading state, or a
required strategy-plan change always needs user action. Do not repair around
those conditions or submit another possible duplicate.

## Self-healing

When self-healing is disabled, diagnose only. Leave automation paused and the
project state set to prevent new orders. Record and send the required user
action when notifications are enabled.

When enabled, automatic repair can change only implementation details that do
not change the agreed strategy and are inside the agreed repair scope. Examples
include compatible endpoint wiring, response parsing, bounded rate-limit
handling, caching, batching, dependency repair inside the selected dependency
set, and rebuildable operational state.

Never change:

- `plan.md`, `pending-update.md`, or intended strategy behavior;
- assets, selection rules, inputs, signals, entries, exits, sizing, leverage,
  risk, timing, or limits on AI decisions;
- credentials or their permissions;
- AlphaInsider strategy identity or core settings;
- scheduler identity or frequency;
- the lock, protected tests, repair policy, or audit evidence; or
- saved orders, fills, trades, positions, or cash history.

Before changing files, save a snapshot and journal the diagnosis, repair scope,
and rollback path. Check current positions, open orders, and saved state first.
Apply a bounded repair, then run only offline or technically enforced
order-free checks. If a check fails, continue repairing while evidence shows
progress.

Stop when no meaningful progress remains, a plan decision or user input is
needed, or 30 minutes have elapsed. Use a shorter platform execution limit and
reserve time to roll back. Restore the snapshot after an unsuccessful repair
and verify the rollback. Never leave a partly applied repair active.

Multiple repair and order-free check attempts are allowed inside that limit.
Do not count a failed check as final while a new evidence-based repair can
still make progress.

## Recovery and resume

After a repair passes every protected check:

1. repeat the AlphaInsider position, open order, and saved state checks;
2. allow new orders in project state only when the original safety issue is
   resolved;
3. use current data, duplicate risk, schedule, and market timing to decide
   whether one strategy retry now is safer than waiting;
4. perform at most one strategy retry when inputs remain fresh and no prior
   order can be duplicated; and
5. resume future automation automatically unless the pause reason is User.

An error pause never clears automatically for another reason. If the user
supplies required input, fixes an external problem, or agrees to a plan change,
keep scheduled runs and new orders paused until the position, order,
saved-state, and applicable order-free checks prove that the problem is
resolved. Then complete the user-directed resume.

When direct scheduler control is available, resume it and set **Automation
state** to Active. Otherwise, keep the strategy safe and give the user the
exact native resume action.

Wait for the next scheduled run when a retry would use stale evidence, run too
near that scheduled time, breach a rate limit, or risk a duplicate. Record the
reason.

If repair cannot succeed, leave scheduled runs and new orders paused. An
interrupted repair remains paused. The next chat run or scheduler **Run now**
must finish rollback or recovery before it can attempt a strategy run.

## Notifications

Classify notification events with exactly:

- `⚠️ Warning — No Action Required` for a useful warning that needs no user
  action;
- `🛠️ Self-Healed — No Action Required` after a completed repair and restored
  safe state; and
- `🚨 Error — Action Required` when the user must resolve an error or
  decision.

When notifications are enabled, the recommended **Errors only** choice sends
only Error events. The other choices also send Self-Healed events, or
Self-Healed and Warning events. Always record every classified event in project
history, so completed repairs and warnings remain available even when they are
not sent.

Keep messages short and non-technical. State the project, strategy run, plain
cause, automation state, action already taken, and exact next step. Do not
notify for healthy runs, expected no-action results, or routine overlap skips.

A notification failure never pauses trading by itself. Record the failure and
try a limited channel repair that follows the plan or an already agreed backup.
Do not queue or resend the failed old message. A later new notification event
tries the configured channel normally, including on the next run.
