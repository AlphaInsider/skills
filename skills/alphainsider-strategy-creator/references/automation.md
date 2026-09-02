# Native AI Automation

This file owns native-scheduler capability discovery, schedule configuration,
task instructions, notification setup, and activation. Use only the current
platform's native AI automation or scheduler. Never install or recommend cron,
systemd, launchd, Windows Task Scheduler, a daemon, or a background process.

## Discover capabilities

Inspect current platform tools and official documentation. Do not assume that
a web, desktop, or command-line product has the same controls. Record:

- create, inspect, edit, pause, resume, **Run now**, and delete support;
- recurrence limits, precision, timezone, daylight-saving, missed-run,
  scheduler-retry, overlap, history, notification, and duration behavior;
- access to the persistent project, exact code revision, durable state, and
  atomic lock;
- non-prompt secret and required network access; and
- whether the agent or only the user can operate each control.

Use native user-interface instructions when a required control is unavailable
as an agent tool. Do not activate unless create, pause, resume, status, and
removal controls exist, even when some are user-operated. Future runs must be
able to read and write the same project, state, and secrets. Otherwise,
preserve the implementation and record one exact blocker and user action.

## Plan the schedule

Offer only supported cadences. If the requested cadence is unavailable,
explain the nearest useful alternatives and ask the user to select one. Record
the exact timezone and daylight-saving behavior. For stocks, configure
order-capable schedules only during AlphaInsider's regular market hours.

Use these defaults unless the plan needs another supported choice:

- one finite normal run per occurrence;
- skip missed occurrences without catch-up;
- disable scheduler-level automatic retries;
- use the project lock to reject overlap;
- keep healthy runs quiet; and
- activate for the next normal occurrence without an order-capable setup run.

If retries or catch-up cannot be disabled, record the limitation and require
the project scheduled-time check, lock, and trading block to reject stale or
duplicate work.

Derive a unique stable task name from the project name. Check for collision
without opening secret stores or arbitrary run output. Never overwrite an
unrelated task.

## Task instruction

Save a short instruction with the persistent project identity. Tell each
scheduled AI instance to:

1. read project `plan.md` and `runtime/runbook.md`;
2. perform exactly one normal occurrence;
3. apply the project lock, current scheduled time, runtime evaluation, repair,
   and notification rules;
4. make only plan-conforming AlphaInsider paper actions;
5. update safe project status and history; and
6. finish without creating another schedule.

Do not put an API key, secret, broker detail, or unnecessary private data in
the task prompt or metadata. Keep the public strategy ID in project
configuration. Agent-led and hybrid occurrences can use the scheduled AI's
reasoning directly.

[Scheduled and user-triggered runs](scheduled-runs.md) defines **Run now**,
chat normal runs, chat dry runs, locks, health, recovery, and runtime
notifications. Configure scheduler **Run now** to enter that same normal-run
path. Never schedule a dry run or present direct terminal execution as the
user's normal control.

## Configure notifications

Discover native or already authorized channels before asking. Ask enabled or
disabled first and recommend enabled. If enabled, ask in the next dependent
round for:

- **Essential** events, recommended: Error and completed Self-Heal;
- **Expanded** events: Essential plus unexpected Warning; and
- supported channels, recommending the simplest native in-app channel first.

Request a destination only when the channel needs one. Store private addresses,
tokens, or webhooks through
[credentials and configuration](credentials.md). Put only safe labels and
configuration names in project documents. Never silently select email or every
available channel.

Attempt a non-trading delivery check before activation when supported.
Provider acceptance without an immediate error is sufficient; do not require
the user to confirm receipt. If no outbound channel exists, ask whether native
task history is acceptable. Do not create an unagreed account, connector, or
secret.

## Activate

Activate only after the target, agreed description state, final runtime
permissions, implementation, runbook, offline tests, durable state, lock, and
notification check are ready. Record the task identity and next normal
occurrence. Do not trigger an order-capable run to verify activation.

For a user stop during setup, return to `interview.md`. For runtime pause and
resume behavior, use
[scheduled and user-triggered runs](scheduled-runs.md). When the agent cannot
operate a required native control, keep the durable trading block effective and
give the exact user-interface action. Never substitute another scheduler.
