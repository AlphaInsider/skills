# Native AI Automation

Read this file after the user chooses AlphaInsider forward testing. Use the
current platform's native AI automation or scheduler only. Do not install or
recommend cron, systemd, launchd, Windows Task Scheduler, a daemon, or a
background process.

## Discover capabilities

Inspect current platform tools and current official documentation. Do not
assume that a web app, desktop app, or command-line app has the same controls.
Record:

- create, inspect, edit, pause, resume, **Run now**, and delete support;
- recurrence limits, minimum and maximum cadence, precision, timezone, and
  daylight-saving-time behavior;
- missed-run, scheduler-retry, overlap, history, and notification behavior;
- maximum occurrence duration;
- access to the persistent project and exact code revision;
- durable read/write state and atomic lock support;
- non-prompt secret access;
- required network access; and
- whether the agent or only the user can operate each lifecycle control.

Use provider-native user-interface instructions when a required control is not
available as an agent tool. Never claim that a control exists without current
evidence. Do not activate unless the native platform provides create, pause,
resume, status, and removal controls, even when some controls are user-interface
only. If future scheduled runs cannot read the same project, state, or secrets,
do not activate automation. Preserve the implementation and record the specific
blocker and next user action.

## Plan the schedule

Offer only cadences supported by the selected scheduler. If the desired cadence
is unsupported, explain the nearest useful alternatives and ask the user to
select one. Record the exact timezone and how daylight-saving changes affect
local run times.

Use these defaults unless the plan needs another supported choice:

- each occurrence is one finite normal run;
- missed occurrences are skipped and never caught up;
- scheduler-level automatic retries are disabled;
- the project-wide lock rejects overlap;
- healthy runs remain quiet; and
- the schedule starts at its next normal occurrence, not with an
  order-capable setup test.

If scheduler retries or catch-up cannot be disabled, require the project lock,
scheduled-for-time check, and durable trading block to reject duplicates and
stale occurrences. Record the provider limitation.

Derive a unique, stable task name from the project name. Check for a collision
without opening secret stores or arbitrary run output. Never overwrite an
unrelated task.

## Task instruction

Save a short instruction that gives the persistent project identity and tells
each scheduled AI instance to:

1. read the installed Strategy Creator skill;
2. read project `plan.md` and `runtime/runbook.md`;
3. perform exactly one normal occurrence under `scheduled-runs.md`;
4. use the project lock and current scheduled-for time;
5. make only plan-conforming AlphaInsider paper actions;
6. apply the recorded evaluation, self-heal, and notification rules;
7. update project status and history without exposing secrets; and
8. finish without creating another schedule.

Do not put an API key, secret, broker detail, or unnecessary private data in
the task prompt or metadata. A public strategy ID can remain in `plan.md` and
project configuration instead of the task prompt.

For agent-led or hybrid strategies, the occurrence can use the scheduled AI's
reasoning directly. Project programs can collect inputs, enforce mechanical
limits, and submit the final paper action.

## Run and dry-run controls

The scheduler's **Run now** control performs a normal order-capable occurrence.
A user can also ask an AI chat to perform the same normal run. An explicit
`dry run` request in chat performs the dry-run branch. Do not teach the user
to invoke the strategy program manually in a terminal as the normal control.

All entry paths share the same lock. If a scheduled and user-triggered run
overlap, the first lock owner continues and the other records a skip.

## Notifications

When notifications are enabled, discover available native or already
authorized channels and record the exact non-secret destination. Attempt a
non-trading delivery check before activation when supported. Provider
acceptance without an immediate error is sufficient; do not require the user
to confirm receipt.

When no outbound channel exists, explain the limitation and ask whether task
history is acceptable. Never create an account, connector, or secret outside
the user's agreed setup.

## Activation and lifecycle

Activate only after the target, description, implementation, runbook, offline
tests, durable state, lock, and notification check are ready. Record the exact
task identity and next normal occurrence. Do not trigger an order-capable run
for activation verification.

The project must distinguish:

- a user pause, which only the user or an explicit user request clears;
- an error pause, which successful plan-conforming recovery can clear;
- an update pause, which clears after the agreed update passes; and
- a deletion block, which never clears automatically.

When automatic scheduler pause is unavailable, the durable trading block must
make later occurrences exit before external trading work. Notify the user to
pause the native task through its UI. Never substitute another scheduler.
