# Scheduled and User-Triggered Runs

This file owns strategy-run entry types, locking, health, error retries, repair,
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

Each trigger performs at most one strategy run and then exits. Never wait,
sleep, poll, loop, recurse, create another schedule, or start a background
process to imitate a cadence faster than the confirmed native schedule.

Every mode first acquires the same one-run-at-a-time project lock. The first
trigger owns the run. If another run is already active, record a skip and exit
before input collection, decision work, position and order checks, or orders.
Every trigger attempts recovery when Operational health is Degraded/Retrying.
Scheduler **Run now** and a chat run use the same recovery path. Neither can
override a user, update, deletion, or setup pause, and no run can send an order
until its current checks resolve every safety problem.

Never remove a leftover lock until checks prove that its owning run is not
active. Record that evidence before removing the lock and acquiring a new one.

Hold the lock through result evaluation and any repair attempted by that
run. Release it only after the result, repair state, and rollback state are
saved. When an operational error remains unresolved, save Operational health
as Degraded/Retrying with the exact next-trigger check before releasing the
lock. Do not change Automation state from Active.

## Strategy run

Follow the steps in [strategy implementation](implementation.md). Read fresh
files and state; do not recreate decisions from chat memory. Record scheduled
time, actual start time, run source, data cutoff time, decision, risk checks,
order outcome, health result, and notification result without secrets.

Missed runs do not catch up. A scheduled run that starts too late exits. A
stock run outside its confirmed accepted window because of a holiday, early
close, or late trigger is an expected no-order result. Do not carry its signal
forward unless `plan.md` explicitly defines persistent signal state. The next
trigger recomputes from current data and positions. A healthy scheduled or
user-triggered run creates project history but no success notification.

## Health evaluation

Evaluate whether the run followed `plan.md`:

- required inputs were available and fresh;
- AlphaInsider strategy and asset types matched;
- current positions, open orders, and saved state were checked and duplicate
  protection completed;
- decision and risk rules were applied;
- expected external results were confirmed or safely classified;
- state and lock integrity remained valid; and
- code and API wiring operated as planned.

Profit, loss, return, win rate, or a difference from a backtest is not a health
criterion. A large difference can start a correctness review. It becomes an
error only when evidence shows that implementation or data handling violates
the plan.

Classify an unexpected problem that did not make the run unsafe as a warning.
Classify a failure that prevents a safe run that follows the plan as an error.

Keep Automation state separate from run health:

- **Ready** means automation is active but no operational run has completed;
- **Healthy** means the latest completed run followed the plan, including an
  expected no-order result; and
- **Degraded/Retrying** means an error ended the latest run and the next trigger
  will diagnose and retry.

An operational error never pauses native automation automatically. Only the
user or an explicit update, deletion, or setup workflow can set Automation
state to Paused. A setup failure before activation remains a setup gate rather
than an operational retry.

## Error response

For every error that prevents a safe run that follows the plan:

1. keep the current lock;
2. end all order-capable work for this trigger;
3. compare current AlphaInsider positions and orders with saved state, then
   diagnose the cause;
4. apply the self-heal choice without retrying a strategy action in this
   trigger;
5. set Operational health to Degraded/Retrying while the problem remains; and
6. record every action, result, unresolved safety gate, and next scheduled
   retry.

Keep **Automation state** Active. For a project that completed creation, keep
**Creation state** and **Phase** Complete. An operational failure does not turn
the project back into incomplete creation. It also never authorizes a new order
while required inputs, identity, state, timing, or a prior order result remain
unverified.

Warnings, expected no-action results, skips because another run is active, and
a failure to send a notification are not run errors and do not set operational
health to Degraded/Retrying.

Authentication, ownership, AlphaInsider strategy mismatch, a possibly
submitted order with an unknown result, corrupt saved trading state, or a
required strategy-plan change can require user action. Do not repair around
those conditions. Keep scheduling safe reconciliation and diagnosis, but place
no order until the condition is resolved.

When an order might have reached AlphaInsider but its result is unknown, never
assume success or failure. Every later trigger first reconciles AlphaInsider
positions and open orders with saved state. It submits nothing while ambiguity
remains, keeps Operational health Degraded/Retrying, and tries reconciliation
again on the next trigger. It can continue only after the prior outcome is
proved.

## Self-healing

When self-healing is disabled, diagnose only. Keep automation Active, mark
Operational health Degraded/Retrying, and wait for the next trigger. Record the
diagnosis and send the matching Retrying or Error event when notifications are
enabled.

When enabled, automatic repair can change only implementation details that do
not change the confirmed strategy and are inside the confirmed repair scope.
Examples include compatible endpoint wiring, response parsing, bounded rate-limit
handling, caching, batching, dependency repair inside the selected dependency
set, and rebuildable operational state.

Never change:

- `plan.md`, `pending-update.md`, or intended strategy behavior;
- assets, selection rules, inputs, signals, entries, exits, sizing, exposure,
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

On later triggers, diagnose again but attempt another repair only when new
evidence supports a safe repair that was not already proved ineffective. Never
repeat the same failed repair only because another trigger occurred.

## Next-trigger recovery

After a repair passes every protected check:

1. repeat the AlphaInsider position, open order, and saved state checks;
2. record the completed repair and whether Operational health can return to
   Healthy;
3. perform no strategy or order retry in that trigger; and
4. wait for the next scheduled or user-triggered run.

At the next trigger, reconcile positions, open orders, saved state, and any
uncertain prior action before normal decision work. If the safety issue is
resolved, recompute from current inputs and positions and proceed through the
ordinary order gates. Never replay a missed signal or order. If the problem
remains, submit nothing, retain Degraded/Retrying, and record the next retry.

If repair cannot succeed, automation remains Active and Degraded/Retrying. An
interrupted repair must roll back before that trigger ends; the next trigger
verifies rollback before diagnosis. The user can use the native pause control
at any time. A user pause remains in force until the user explicitly resumes
it and is never cleared by operational recovery.

## Notifications

Classify notification events with exactly:

- `⚠️ Warning — No Action Required` for a useful warning that needs no user
  action;
- `🔄 Retrying — No Action Required` for an operational error that the next
  trigger will retry without user input;
- `🛠️ Self-Healed — No Action Required` after a completed repair and restored
  safe state; and
- `🚨 Error — Action Required` when the user must resolve an error or
  decision.

When notifications are enabled, the recommended **Errors only** choice sends
Retrying and Error events. The other choices also send Self-Healed events, or
Self-Healed and Warning events. Record every classified event and every failed
run in project history, including suppressed duplicate notifications.

Keep messages short and non-technical. State the project, strategy run, plain
cause, Automation state, Operational health, action already taken, and exact
next step. Send the first enabled notification for an unresolved incident and
again when its cause, severity, required action, or retry state materially
changes. Suppress an equivalent repeat while recording it. A later Healthy run
closes the incident so a future recurrence can notify again. Do not notify for
healthy runs, expected no-action results, or routine overlap skips.

Treat configured channels independently. Working channels send the original
event even when another channel fails. A notification failure never pauses
trading, the scheduler, or new orders by itself. Record the failure. Try a
limited channel repair or already confirmed backup only when self-healing is
enabled and notification repair is inside its confirmed scope; otherwise do
not repair the channel. Do not queue or resend the failed old message and do
not send an extra alert through a working channel solely about that failure. A
later new notification event tries the configured channel normally, including
on the next run.
