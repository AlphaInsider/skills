# Scheduled and User-Triggered Runs

Read this file for every scheduled occurrence, scheduler **Run now**, chat
normal run, chat dry run, operational error, notification event, or self-heal
attempt. `plan.md` and `runtime/runbook.md` remain authoritative.

## Entry modes and lock

- A scheduled occurrence is a normal order-capable run.
- Scheduler **Run now** is the same normal run.
- A chat request to run now is the same normal run.
- A chat request for a dry run uses current inputs but must not submit, change,
  or cancel orders and must not change canonical portfolio or decision state.
  It can write an isolated dry-run report.

A dry run is available only through an explicit chat request. Do not schedule
dry runs.

Every mode first acquires the same atomic project lock. The first trigger owns
the run. Every overlap records a skip and exits before input collection,
decision work, reconciliation, or orders. A user-triggered normal run should
attempt execution even while future automation is error-paused, but it must
first recheck the trading block and resolve the safety problem.

## Normal occurrence

Follow the finite cycle in `implementation.md`. Read fresh files and state; do
not reconstruct decisions from chat memory. Record scheduled time, actual start
time, run source, input as-of time, decision, risk checks, order outcome, health
result, and notification result without secrets.

Missed runs do not catch up. A late stale occurrence exits. A healthy scheduled
or user-triggered run creates normal project history but no success
notification.

## Health evaluation

Evaluate whether the run followed `plan.md`:

- required inputs were available and fresh;
- target and instrument types matched;
- reconciliation and duplicate protection completed;
- decision and risk rules were applied;
- expected external results were confirmed or safely classified;
- state and lock integrity remained valid; and
- code, API wiring, and notifications operated as planned.

Profit, loss, return, win rate, or divergence from a backtest is not a health
criterion. A large divergence can start a correctness review. It becomes an
error only when evidence shows that implementation or data handling violates
the plan.

Classify a recoverable degradation that did not make the run unsafe as a
warning. Classify a failure that prevents a safe plan-conforming run as an
error.

## Error response

For every error that prevents a safe plan-conforming run:

1. keep the current lock;
2. set a durable trading block so another occurrence cannot trade;
3. pause future native automation and verify its state when the platform
   allows it;
4. reconcile external state and diagnose the cause;
5. apply the self-heal choice; and
6. record every action and result.

Set **Automation state** to Paused and record the exact error pause reason.

Warnings, expected no-action results, routine overlap skips, and a
notification-only failure are not run errors and do not start this pause flow.

If native pause fails or needs a user-interface action, keep the durable block.
Later occurrences must exit. Send the exact pause action when notifications
are enabled.

Authentication, ownership, target mismatch, an ambiguous possible order,
corrupt canonical trading state, or a required strategy-plan change always
needs user action. Do not repair around those conditions or submit another
possible duplicate.

## Self-healing

When self-healing is disabled, diagnose only. Leave automation paused and the
trading block active. Record and send the required user action when
notifications are enabled.

When enabled, automatic repair can change only plan-preserving implementation
details inside the agreed repair scope. Examples include compatible endpoint
wiring, response parsing, bounded rate-limit handling, caching, batching,
dependency repair inside the selected dependency set, and rebuildable
operational state.

Never change:

- `plan.md`, `pending-update.md`, or intended strategy behavior;
- instruments, selection rules, inputs, signals, entries, exits, sizing,
  leverage, risk, timing, or agent-discretion boundaries;
- credentials or their permissions;
- AlphaInsider target identity or core settings;
- scheduler identity or cadence;
- the lock, protected tests, repair policy, or audit evidence; or
- canonical orders, fills, trades, positions, or cash history.

Before mutation, create a durable snapshot and journal the diagnosis, repair
scope, and rollback path. Reconcile first. Apply a bounded repair, then run only
offline or technically enforced order-free checks. If a check fails, continue
repairing while evidence shows progress.

Stop when no meaningful progress remains, a plan decision or user input is
needed, or 30 minutes have elapsed. Use a shorter platform execution limit and
reserve time to roll back. Restore the snapshot after an unsuccessful repair
and verify the rollback. Never leave a partly applied repair active.

Multiple repair and dry-check attempts are allowed inside that limit. Do not
count a failed dry check as final while a new evidence-based repair can still
make progress.

## Recovery and resume

After a repair passes every protected check:

1. reconcile AlphaInsider again;
2. clear the durable trading block only when the original safety issue is
   resolved;
3. use current data, duplicate risk, cadence, and market timing to decide
   whether one normal retry now is safer than waiting;
4. perform at most one normal retry when inputs remain fresh and no prior order
   can be duplicated; and
5. resume future automation automatically unless the pause reason is User.

An error pause never clears automatically for another reason. If the user
supplies required input, fixes an external problem, or agrees to a plan change,
keep the block and pause until reconciliation and all applicable order-free
checks prove that the problem is resolved. Then complete the user-directed
resume.

When direct scheduler control is available, resume it and set **Automation
state** to Active. Otherwise, keep the strategy safe and give the user the
exact native resume action.

Wait for the next scheduled occurrence when a retry would use stale evidence,
run too near the next occurrence, breach a rate limit, or risk a duplicate.
Record the reason.

If repair cannot succeed, leave automation paused and the trading block active.
An interrupted repair remains paused. The next chat normal run or scheduler
**Run now** must finish rollback or recovery before it can attempt a normal
cycle.

## Notifications

Classify notification events with exactly:

- `⚠️ Warning — No Action Required` for a useful warning that needs no user
  action;
- `🛠️ Self-Healed — No Action Required` after a completed repair and restored
  safe state; and
- `🚨 Error — Action Required` when the user must resolve an error or
  decision.

When notifications are enabled, the Essential policy sends Error and
Self-Healed events. The Expanded policy also sends Warning events. Always
record classified events in project history even when the selected policy does
not send them.

Keep messages short and non-technical. State the project, occurrence, plain
cause, automation state, action already taken, and exact next step. Do not
notify for healthy runs, expected no-action results, or routine overlap skips.

A notification failure never pauses trading by itself. Record the failure and
try bounded plan-compatible channel repair or an already agreed fallback.
Do not queue or resend the failed old message. A later new notification event
tries the configured channel normally, including on the next run.
