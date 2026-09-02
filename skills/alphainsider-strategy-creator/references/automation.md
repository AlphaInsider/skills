# Native AI Automation

This file owns native-scheduler capability discovery, schedule configuration,
task instructions, notification setup, and activation. Use only the current
platform's native AI automation or scheduler. Never install or recommend cron,
systemd, launchd, Windows Task Scheduler, a daemon, or a background process.

## Discover capabilities

Inspect current platform tools and official documentation. Do not assume that
a web, desktop, or command-line product has the same controls. Record:

- create, inspect, edit, pause, resume, **Run now**, and delete support;
- schedule frequency limits, precision, timezone, daylight-saving, missed-run,
  scheduler-retry, overlap, history, notification, and duration behavior;
- access to the persistent project, exact code revision, saved state, and
  one-run-at-a-time lock;
- non-prompt secret and required network access; and
- whether the agent or only the user can operate each control.

Use native user-interface instructions when a required control is unavailable
as an agent tool. Do not activate unless create, pause, resume, status, and
removal controls exist, even when some are user-operated. Future runs must be
able to read and write the same project, state, and secrets. Otherwise,
preserve the implementation and record one exact blocker and user action.

## Plan the schedule

Offer only supported schedule frequencies. If the requested frequency is
unavailable, explain the nearest useful alternatives and ask the user to select
one. Record the exact timezone and daylight-saving behavior. For stocks,
configure order-capable schedules only during AlphaInsider's regular market
hours.

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

## Configure notifications

Discover native or already authorized channels before asking. Ask enabled or
disabled first and recommend enabled. If enabled, ask these available
decisions together in the next round:

- which events to send, with these choices in order:
  1. **Errors only** — recommended; completed repairs and warnings remain in
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

Attempt a non-trading delivery check before activation when supported. The
notification service accepting the message without an immediate error is
sufficient; do not require the user to confirm receipt. If no outbound channel
exists, ask whether native task history is acceptable. Do not create an
unagreed account, connector, or secret.

## Activate

Activate only after the AlphaInsider strategy, agreed description, final
strategy-run permissions, implementation, scheduled-run instructions, offline
tests, saved state, lock, and notification check are ready. Record the
scheduled task name and next scheduled run. Do not trigger an order-capable run
to verify activation.

For a user stop during setup, return to `interview.md`. For pause and resume
behavior during strategy runs, use
[scheduled and user-triggered runs](scheduled-runs.md). When the agent cannot
operate a required native control, keep project state set to prevent new orders
and give the exact user-interface action. Never substitute another scheduler.
