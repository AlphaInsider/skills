# Native AI Automation

This file owns Define-time native-scheduler discovery, schedule constraints,
implementation-time rechecks, task instructions, notification setup, and
activation. Use only the current platform's native AI automation or scheduler.
Never install or recommend cron, systemd, launchd, Windows Task Scheduler, a
daemon, or a background process.

## Discover schedule capabilities during Define Strategy

Before asking strategy timing questions, inspect the actual current platform's
tools and official scheduler documentation. Do not assume that web, desktop,
and command-line products have the same controls. Resolve the native surface
without a user question when current context makes it clear. Record its source,
checked time, and schedule-critical capabilities:

- schedule frequency limits, precision, timezone, daylight-saving, missed-run,
  scheduler-retry, overlap, history, notification, and duration behavior;
- whether one invocation can perform exactly one complete strategy run; and
- whether the documented surface can ultimately create, inspect, edit, pause,
  resume, run now, and remove a task, including user-operated controls.

Ask only about the strategy's timing intent. Present complete compatible timing
choices that bundle decision and data-cutoff time, useful cadence, run clock,
timezone, daylight-saving behavior, and order window. Filter recommendations
through the discovered scheduler and AlphaInsider session policy before showing
them. If the requested cadence is unavailable, explain the conflict and offer
the nearest complete supported alternatives, then ask the user to choose among
them. Do not ask a hypothetical fallback question for a compatible choice. Do
not ask who will operate controls, where secrets will live, or another
implementation question during Define Strategy.

Never simulate a faster cadence by keeping a scheduled run alive, sleeping,
polling, looping, recursively scheduling, or starting a background process.
One trigger performs at most one strategy run and finishes. If the native
scheduler cannot supply a useful cadence, keep timing unresolved and preserve
the resumable Define Strategy stage as a technical blocker.

For stock timing, read the installed `alphainsider-api` guidance and the current
live `llms.txt`, any indexed session guidance, the focused `getExchangeStatus`
and selected order-operation pages, and the OpenAPI operations. Use an explicit
current accepted-session rule when one exists. An exchange-status name or
example is not proof. When the sources publish no mapping, use the Strategy
Creator fallback for every AlphaInsider stock: 09:30 until, but not including,
16:00 `America/New_York` on a U.S. stock-market trading day, with the U.S.
holiday and early-close calendar. Record the missing mapping and identify the
fallback as Strategy Creator policy rather than API documentation.

Treat AlphaInsider cryptocurrency order availability as 24/7. Do not ask a
cryptocurrency market-session question. Still constrain recommendations by the
native scheduler, required data boundary and timezone, and when completed data
becomes available.

Explicit session guidance overrides the fallback for a new or revised
schedule. Added support does not silently expand an existing confirmed
schedule. Guidance that invalidates a confirmed schedule reopens only the
affected Define Strategy timing decision.

Apply public AlphaInsider limits only to the operations they explicitly name.
Do not request a key, inspect the user's account tier, or ask an account setup
question here. When the confirmed cadence would require a higher documented
tier for its mapped operation, use maximum planned calls per run and runs per
day to record that dependency for implementation and explain it with the
strategy timing choices.

Record the selected implementable schedule, exact timezone, daylight-saving
behavior, applicable documented-or-fallback session policy, native surface,
capability source, and checked time in the strategy plan before its review.

Use these defaults unless the plan needs another supported choice:

- one strategy run per scheduler trigger;
- skip missed scheduled runs without catch-up;
- disable scheduler-level automatic retries;
- use the project lock to reject overlap;
- keep healthy runs quiet; and
- activate for the next scheduled run without an order-capable setup run.

If retries or catch-up cannot be disabled, record the limitation and require
the project scheduled-time check and lock to reject stale or duplicate work.
Every run must also exit when project state says that new orders are paused.

A stock trigger outside its confirmed window because of a holiday, early
close, or late start is an expected no-order result. Do not submit, flatten, or
carry a stale signal by default. The next trigger recomputes from current data.

## Recheck capabilities during implementation

Before API-key collection and again before activation, recheck the same native
surface and confirmed schedule. Inspect:

- create, inspect, edit, pause, resume, **Run now**, status, and delete support;
- access to the persistent project, exact code revision, saved state, and
  one-run-at-a-time lock;
- non-prompt secret and required network access; and
- whether the agent or only the user can operate each control.

Use native user-interface instructions when a required control is unavailable
as an agent tool. Do not activate unless create, pause, resume, status, and
removal controls exist, even when some are user-operated. Future runs must be
able to read and write the same project, state, and secrets. Otherwise,
preserve the implementation and record one exact blocker and user action.

Do not reselect timing during implementation. If capability or AlphaInsider
documentation drift makes the confirmed schedule unavailable, return the
schedule decision to Draft in Define Strategy, preserve other answers, and show
a revised strategy summary after the user chooses a supported alternative.

Derive a unique stable task name from the project name. Check for collision
without opening secret stores or arbitrary run output. Never overwrite an
unrelated task.

## Task instruction

Save a short instruction with the persistent project identity. Tell each
scheduled AI instance to:

1. read project `plan.md` and `runtime/runbook.md`;
2. perform exactly one strategy run;
3. apply the project lock, current scheduled time, run evaluation, repair, and
   notification rules;
4. submit only AlphaInsider paper orders that follow the plan;
5. update safe project status and history; and
6. finish without creating another schedule.

Do not put an API key, secret, broker detail, or unnecessary private data in
the task prompt or metadata. Keep the AlphaInsider strategy ID in project
configuration. Agent-led and hybrid strategy runs can use the scheduled AI's
reasoning directly.

[Scheduled and user-triggered runs](scheduled-runs.md) defines **Run now**,
chat runs, chat dry runs, locks, health, recovery, and strategy-run
notifications.
Configure scheduler **Run now** to enter that same strategy-run path. Never
schedule a dry run or present direct terminal execution as the user's usual
run control.

## Configure self-healing

Ask whether self-healing is enabled and recommend enabled. If enabled, show the
proposed implementation-only repair scope, protected files and state, snapshot
and rollback behavior, and time limit. Ask explicitly whether notification
channel repair is inside that scope. It is disabled unless both self-healing
and that scope are confirmed. Never include strategy behavior, credentials,
AlphaInsider strategy identity, scheduler identity or frequency, saved trading
history, the lock, protected tests, or repair evidence.

## Configure notifications

Discover native or already authorized channels before asking. Use only
non-sending capability and configuration checks; never send a setup or test
notification. Ask enabled or disabled first and recommend enabled. If enabled,
ask these available decisions together in the next round:

- which events to send, with these choices in order:
  1. **Errors only** — recommended; sends the first Retrying or Action Required
     event and material changes, while completed repairs and warnings remain in
     project history;
  2. **Errors and completed repairs**; and
  3. **Errors, completed repairs, and warnings**; and
- which supported channels to use, recommending the simplest native in-app
  channel first.

Request a destination only when the channel needs one. Store private addresses,
tokens, or webhooks through
[credentials and configuration](credentials.md). Put only safe labels and
configuration names in project documents. Never silently select email or every
available channel.

For each selected channel, record whether current platform information proves
that it is supported. If a non-sending check proves that a channel or its
configuration is unsupported, explain the issue while the user is present and
ask whether to fix it, remove that channel, or disable notifications. Preserve
other selected channels independently.

When support cannot be checked without sending, accept the user's selection
and record it as **user-selected, unverified**. Do not claim that a supported or
configured channel delivered anything. If no outbound channel is available,
offer native task history. Do not create an unconfirmed account, connector, or
secret.

Setup does not send a notification. During later operation, delivery is best
effort. A failed channel never pauses the strategy, scheduler, or new orders;
working channels still send the original event. Record each failure. Attempt a
bounded channel repair or confirmed backup only when self-healing is enabled
and notification repair is inside its confirmed scope. Otherwise, make no
repair. Do not queue or resend the old message; try the configured channel
normally on the next new event.

## Activate

Activate only after the AlphaInsider strategy, confirmed description, final
strategy-run permissions, implementation, scheduled-run instructions, offline
tests, saved state, lock, and notification choices and support status are
recorded. Notification delivery is not an activation gate. Record the scheduled
task name and next scheduled run, keep Automation state Active, and set
Operational health to Ready until the first operational run. Do not trigger an
order-capable run to verify activation.

For a user stop during setup, return to `interview.md`. For pause and resume
behavior during strategy runs, use
[scheduled and user-triggered runs](scheduled-runs.md). When the agent cannot
operate a required native control, keep project state set to prevent new orders
and give the exact user-interface action. Never substitute another scheduler.
