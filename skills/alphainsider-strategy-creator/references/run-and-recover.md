# Run and Recover

Use this workflow for every scheduled trigger, scheduler **Run now**, chat run,
chat dry run, operational error, notification event, and confirmed self-heal
attempt. Project `plan.md` and `runtime/runbook.md` remain authoritative. A
generated project must perform this workflow without the installed skill.

## 1. Classify the trigger

1. Treat a scheduled run as an order-capable strategy run.
2. Treat scheduler **Run now** as the same order-capable strategy run.
3. Treat a chat request to run now as the same order-capable strategy run.
4. Treat only an explicit chat request for a dry run as order-free.

A dry run can use current inputs and write an isolated report, but it must not
submit, change, or cancel orders or alter saved portfolio or decision state.
Never schedule a dry run.

Each trigger performs at most one complete strategy run and exits. Never wait,
sleep, poll, loop, recurse, create another schedule, or start a background
process to imitate a faster cadence.

## 2. Acquire the shared lock

1. Every mode attempts the same one-run-at-a-time project lock before input
   collection, decision work, position checks, or order work.
2. If another run is active, record a routine overlap skip and exit.
3. Never remove a leftover lock until evidence proves its owning run is no
   longer active. Record that evidence before replacement.
4. Hold the lock through result evaluation and any repair or rollback attempted
   by this trigger.
5. Release it only after result, health, repair, rollback, notification state,
   and next-step records are durable.

Every trigger attempts recovery first when Operational health is
Degraded/Retrying. Neither Run now nor a chat run can override a user, setup,
update, or deletion pause. No mode can submit an order until every current
safety gate resolves.

## 3. Admit one strategy run

1. Read fresh `plan.md`, `runtime/runbook.md`, source, and runtime state from
   disk. Never recreate decisions from chat memory.
2. Validate Strategy status Confirmed.
3. Require AlphaInsider setup status Authorized only for order-free setup
   verification and Active for operation.
4. Validate public strategy identity, strict stock or cryptocurrency type,
   Automation state, Operational health, explicit pause state, and every
   unresolved prior action.
5. For an order-capable run, require setup and Automation state Active and clear
   every current safety gate.
6. Record scheduled time, actual start, trigger source, and admission result.

Missed runs never catch up. Exit when a scheduled run starts too late. A stock
run outside its confirmed window because of a holiday, early close, or late
trigger is an expected no-order result. Do not carry its signal forward unless
`plan.md` explicitly defines persistent signal state. The next trigger
recomputes from current data and positions.

## 4. Execute the confirmed strategy

After admission and while holding the lock:

1. Compare current AlphaInsider positions, open orders, and uncertain prior
   actions with saved state.
2. Run the shared compatibility gate for constraints that can stop work before
   input or decision processing.
3. Obtain fresh inputs under confirmed source, cutoff, and missing-data rules.
4. Calculate or make the confirmed decision according to code-led, agent-led,
   or hybrid responsibilities.
5. Enforce asset, order-size, operation-specific exposure, total-position-value,
   loss, timing, uncertainty, and duplicate protections.
6. Repeat compatibility checks for the planned action, its material side
   effects, and constraints that can change.
7. Submit only the confirmed AlphaInsider paper order when the run is
   order-capable and every gate permits it.
8. Persist a structured result and all safe run history.

The structured result must distinguish:

- an order with an unknown submission result;
- a confirmed order response;
- a confirmed failure before an order;
- a successful no-order result;
- a warning; and
- a run skipped because another run was active.

Record data cutoff, decision, risk and compatibility checks, order outcome,
health result, and notification result. Never record credentials or unnecessary
private response data.

## 5. Evaluate operational health

Evaluate only whether the run followed `plan.md`:

- required inputs were available and fresh;
- public strategy and asset types matched;
- positions, open orders, saved state, and duplicate protection were checked;
- decision and risk rules were applied;
- external results were confirmed or safely classified;
- state and lock integrity remained valid; and
- code and API wiring operated as planned.

Profit, loss, return, win rate, and divergence from a backtest are not health
criteria. A large difference can start a correctness review and becomes an
error only when evidence proves implementation or data handling violates the
plan.

Classify an unexpected safe problem as a warning. Classify a failure that
prevents a safe plan-compliant run as an error.

- **Ready** means automation is active but no operational run has completed.
- **Healthy** means the latest completed run followed the plan, including an
  expected no-order result.
- **Degraded/Retrying** means an error ended the latest run and the next trigger
  will diagnose and retry checks.

A healthy scheduled or user-triggered run writes history but sends no success
notification. Warnings, expected no-action results, routine overlap skips, and
notification delivery failures do not set health to Degraded/Retrying.

## 6. Respond to an operational error

1. Keep the current lock.
2. End every order-capable action for this trigger.
3. Compare current positions and open orders with saved state, then diagnose the
   cause.
4. Apply the confirmed self-heal choice without retrying a strategy or order
   action in this trigger.
5. Set Operational health Degraded/Retrying while the problem remains.
6. Record every action, result, unresolved gate, and exact next-trigger check.
7. Release the lock only after durable state and rollback verification.

Keep Automation state Active. For a completed project, keep Creation state and
Phase Complete. An operational error never automatically pauses the native
task or reopens creation. Only the user or an explicit setup, update, or
deletion workflow can set Automation state Paused.

Authentication, ownership, strategy mismatch, a possibly submitted order with
unknown result, corrupt saved trading state, or a required plan change can need
user action. Do not repair around them. Keep scheduled reconciliation and
diagnosis safe, but place no order until resolved.

When an order may have reached AlphaInsider but its result is unknown, never
assume success or failure. Each later trigger first reconciles positions and
open orders with saved state. Submit nothing while ambiguity remains, retain
Degraded/Retrying, and retry reconciliation on the next trigger. Continue only
after the prior outcome is proved.

A setup failure before activation is a setup gate, not an operational retry.

### When self-healing is enabled

1. Check positions, open orders, saved state, and confirmed repair scope before
   changing files.
2. Save a snapshot and journal the diagnosis, proposed scope, and rollback
   path.
3. Change only implementation details inside the confirmed scope that preserve
   strategy behavior.
4. Run only offline or technically enforced order-free checks.
5. Continue evidence-based repair while meaningful progress remains and the
   time limit permits it.
6. Restore the snapshot after an unsuccessful repair and verify rollback.

Permitted examples include compatible endpoint wiring, response parsing,
bounded rate-limit handling, caching, batching, dependency repair within the
selected dependency set, and rebuildable operational state.

Never change:

- `plan.md`, `pending-update.md`, or intended strategy behavior;
- assets, selection rules, inputs, signals, entries, exits, sizing, exposure,
  risk, timing, or AI-decision limits;
- credentials or permissions;
- public AlphaInsider strategy identity or core settings;
- native scheduler identity or frequency;
- the shared lock, protected tests, repair policy, or audit evidence; or
- saved orders, fills, trades, positions, or cash history.

Stop when no meaningful progress remains, a plan decision or user input is
needed, or 30 minutes have elapsed. Use a shorter platform execution limit when
applicable and reserve time to roll back. Never leave a partly applied repair
active.

Multiple repair and order-free check attempts are allowed inside the limit. A
failed check is not final while a new evidence-based repair can still make
progress. On later triggers, attempt another repair only when new evidence
supports a safe action not already proved ineffective; never repeat the same
failed repair merely because another trigger occurred.

### When self-healing is disabled

1. Diagnose without changing implementation.
2. Keep Automation state Active and Operational health Degraded/Retrying.
3. Record the diagnosis and next-trigger check.
4. Send the applicable Retrying or Error event when notifications are enabled.

## 7. Recover on a later trigger

After a repair passes every protected check:

1. Repeat position, open-order, and saved-state checks.
2. Record the completed repair, whether safe state was restored, and whether
   Operational health can return to Healthy.
3. Perform no strategy or order retry in that trigger.
4. Wait for the next trigger before ordinary strategy work.

At the next trigger:

1. Reconcile positions, open orders, saved state, rollback state, and any
   uncertain prior action before normal decision work.
2. If the safety issue is resolved, recompute from current inputs and positions
   and proceed through ordinary order gates.
3. If it remains, submit nothing, retain Degraded/Retrying, and record the next
   retry.

Never replay a missed signal or order. A user pause remains until the user
explicitly resumes it and is never cleared by operational recovery. An
interrupted repair must roll back before the trigger ends; the next trigger
verifies rollback before diagnosis.

If repair cannot succeed, keep Automation state Active and Operational health
Degraded/Retrying with the next safe retry or required user action.

## Send runtime notifications

Use the exact labels in [workflow contracts](workflow-contracts.md):

- `🚨 Error — Action Required` when the user must resolve an error or decision;
- `🔄 Retrying — No Action Required` when the next trigger can retry without
  user input;
- `🛠️ Self-Healed — No Action Required` after completed repair and restored safe
  state; and
- `⚠️ Warning — No Action Required` for a useful warning that needs no action.

Apply the selected event level:

- **Errors only** sends the first Retrying or Error event and material changes.
- **Errors and completed repairs** also sends Self-Healed events.
- **Errors, completed repairs, and warnings** also sends Warning events.

Record every classified event and failed run, including suppressed duplicates.
Keep messages short and nontechnical. State project, strategy run, plain cause,
Automation state, Operational health, action already taken, and exact next
step.

Send the first enabled notification for an unresolved incident and again only
when cause, severity, required action, or retry state materially changes.
Suppress equivalent repeats while recording them. A later Healthy run closes
the incident so a future recurrence can notify again. Do not notify for healthy
runs, expected no-actions, or routine overlap skips.

Treat channels independently. Working channels send the original event even
when another fails. A delivery failure never pauses trading, the scheduler, or
new orders and does not become a run error by itself. Record it without queuing
or resending the old message and without sending an extra alert through a
working channel solely about that failure.

Attempt limited channel repair or an already confirmed backup only when
self-healing is enabled and notification repair is inside its confirmed scope.
Otherwise, do not repair. A later new event tries every configured channel
normally.
