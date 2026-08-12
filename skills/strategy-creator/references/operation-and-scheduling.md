# Operation and Scheduling

Use this phase after backtesting and implementation planning and before final
AlphaInsider target setup. Separate how long the strategy operates from how
long one process lives:

- a `single run` executes one decision cycle;
- a `persistent process` stays visible or managed and performs cycles itself;
- a `recurring schedule` invokes the finite one-cycle command at each planned
  interval until the schedule is paused, disabled, or deleted.

## Contents

- [Interview branch](#interview-branch)
- [Capability and safety gates](#capability-and-safety-gates)
- [Collision and running-state checks](#collision-and-running-state-checks)
- [Native user-system runners](#native-user-system-runners)
- [Agent scheduled tasks](#agent-scheduled-tasks)
- [Installation and lifecycle](#installation-and-lifecycle)
- [Generated project guidance](#generated-project-guidance)

## Interview branch

Ask exactly one decision per turn. First derive the compatible invocation
models from the confirmed cadence, data dependencies, and worst-case cycle
duration. Then perform read-only discovery and offer only usable runners:

1. Always offer `foreground`. It supports a user-run single cycle or a visible
   persistent process that performs repeated cycles. A foreground process
   stops with its controlling session or machine. A cron-like recurrence is
   managed operation, not foreground operation.
2. Offer `native user-system` when the current host provides a supported
   user-level manager. Linux systemd and macOS launchd may run a persistent
   process or recurring finite cycles. Windows Task Scheduler supports only
   recurring finite cycles.
3. Offer `agent scheduled task` only when the current agent environment can
   create and manage a recurring standalone task with the required runtime.
   Each occurrence runs exactly one finite strategy cycle; the schedule itself
   provides continuous operation over time.

Recommend a compatible native user-system runner before an agent scheduled
task. Keep foreground available even when managed runners exist. When more
than one invocation model is compatible, recommend the simplest model that
meets the strategy cadence and let the user choose.

For managed operation, derive a stable lowercase ASCII slug from the project
directory, collapse other runs to one hyphen, and prefix it with
`alphainsider-`. Ask for an identifier only when normalization is empty or an
unrelated collision requires a different value. Resolve, one decision at a
time, the runner, exact recurrence and timezone when scheduled, missed-run
behavior, initial activation, logs or run history, and notifications. Record
the manager or provider, execution environment, resource identity, exact
native paths or task name, and capability result without recording secrets.

Ask whether each managed resource should initially be `inactive` or `active`
and recommend inactive. Active means eligible for future planned occurrences
or next-login startup after installation; it never authorizes a manual or
immediate strategy run. State the next scheduled occurrence when known and
warn that a future active occurrence can submit AlphaInsider paper orders
without another prompt.

## Capability and safety gates

Discover system and provider facts instead of asking the user. Do not install a
manager, request elevation, configure a system-wide or pre-login service, or
enable systemd lingering. Before offering a runner, verify all applicable
facts:

- The exact one-cycle command exists for recurring execution, or the exact
  persistent command exists for foreground or native persistent execution.
- The schedule precision, timezone behavior, and market-hours support satisfy
  the strategy cadence. A recurring runner is incompatible unless the
  worst-case cycle duration is shorter than the interval.
- The runner's missed-run or catch-up behavior is known. Explain whether a
  delayed or missed occurrence is skipped, coalesced, or run later, and require
  the user's acceptance. Record the configurable choice when one exists; omit
  the runner when its fixed behavior is unacceptable.
- Recurring one-cycle execution cannot overlap. Configure the runner to reject
  another occurrence while one is active and require the generated one-cycle
  command to acquire a fail-closed process-lifetime lock before external data
  or order work. A remote runtime needs an equivalent lock shared by every
  instance that can run the strategy.
- Every finite-cycle and persistent entry point must expose the same
  attributable process-lifetime lock or equivalent remote run identity for
  cleanup. Its non-secret marker may contain project identity, invocation
  model, PID or run identity, and start time, but no strategy ID or credential.
- Scheduler-level retries and task-level restart-on-failure are disabled for
  every recurring one-cycle runner. Existing confirmed in-cycle retry,
  reconciliation, and next scheduled occurrence behavior remain unchanged.
  A persistent service's separately confirmed failure-restart policy is not a
  retry of a finite scheduled occurrence.
- Status, pause or disable, update, delete, and logs or run history are
  available. Record notification support and default agent-task notifications
  to failures only; offer every-run notifications only when supported.

Never put credentials, `.env` values, or strategy IDs in a native definition,
task prompt, task metadata, command argument, log instruction, or output.
Local commands load the project `.env`; remote tasks use only an existing
non-prompt secret mechanism.

## Collision and running-state checks

Before confirmation, inspect only resource identity, path existence, status,
and attributable running state. Do not inspect environment values, task-secret
stores, or arbitrary task output.

- Update a native definition or agent task only when the current plan and
  project documentation attribute its exact identity to this strategy.
- Never overwrite an active unrelated resource. For an unrelated inactive
  collision, explain the consequences and record either a unique identity or
  the exact overwrite while the plan is draft.
- For a runtime-affecting update, record pause or disable actions before
  implementation. Prevent new cycles, allow an active cycle to reach a safe
  completion, and stop a persistent process at a safe cycle boundary. If safe
  completion cannot be verified, do not change runtime files.
- Never resume or reactivate a runner after an update. Report its state and the
  exact user-run resume or activation action.
- Replacement confirmation covers only the recorded pause, disable, deletion,
  and removal of the outgoing strategy's attributable resources.
- Retirement and replacement cleanup follow `cleanup.md`: disable future
  execution first, wait for an attributable active cycle, gracefully stop a
  persistent process, delete only exact confirmed resources, and verify
  absence. Never force-kill an uncertain process or remove a stale lock until
  liveness checks prove no matching process or remote occurrence exists.

## Native user-system runners

Render absolute project and executable paths only in the confirmed native
definitions. Keep plans, project documentation, state, and log paths
project-relative. Generate no project-local manager wrapper.

### Linux systemd

For a persistent process, install one user service at
`~/.config/systemd/user/<identifier>.service` using the project directory and
exact persistent command. Preserve a separately confirmed bounded
`Restart=on-failure` policy or use `Restart=no`; never apply service restart to
a recurring one-cycle service.

For a recurring schedule, install an attributable pair:
`~/.config/systemd/user/<identifier>.service` as `Type=oneshot` with
`Restart=no`, and `~/.config/systemd/user/<identifier>.timer` with the exact
calendar recurrence. Map accepted catch-up behavior to `Persistent`, record
timer precision, and rely on service-unit activity plus the runtime lock to
prevent overlap.

Reload the user manager after installation. Apply only the confirmed enabled
or disabled state and never manually start the service or use a manager command
that can trigger an immediate cycle. Verify definitions, state, and the next
timer occurrence. Generated instructions use `systemctl --user` and
`journalctl --user -u` for lifecycle, status, and native logs.

### macOS launchd

Install only `~/Library/LaunchAgents/<identifier>.plist`. A persistent agent
uses the exact persistent command. A recurring agent uses the exact one-cycle
command with `StartCalendarInterval`. Keep `KeepAlive` false for recurring
execution, do not use `RunAtLoad` to trigger a cycle, and disclose that calendar
events missed during sleep may be coalesced while powered-off events are not
replayed.

Validate the plist before installation. Register it only when doing so cannot
start the strategy before the confirmed future occurrence; otherwise leave it
inactive and report the activation command. Never kickstart or manually start
it during build or verification. Document `launchctl` lifecycle and the
selected standard-output, standard-error, or rotating project logs.

### Windows Task Scheduler

Create only a current-user task with the exact one-cycle command and confirmed
recurrence. Do not store a password, request elevation, or offer Task Scheduler
as a persistent-service substitute. Set `MultipleInstancesPolicy` to reject a
new occurrence while one is active, disable restart-on-failure, and map the
accepted catch-up choice to `StartWhenAvailable` when supported. Never invoke
the task during installation or verification. Document status, enable,
disable, run history, and deletion commands.

## Agent scheduled tasks

Keep selection vendor-neutral. Do not require a named agent product,
proprietary task schema, or vendor-specific conversation type. Discover the
current environment's capabilities and record a provider name only when the
user selects that available runner.

Use an independent recurring scheduled task whose saved instruction and
lifecycle do not depend on the planning conversation. Require read-only
discovery to verify recurring schedules, timezone and precision, task creation
and update, pause or disable, deletion, status, run history, notifications,
sandbox or approval limits, and the execution environment.

For a local task, select the confirmed persistent project rather than an
ephemeral or isolated copy. Verify that the scheduler can access its code,
`.env`, dependencies, and persistent state, and document every requirement for
the machine, agent runtime, or project to remain available.

For a remote or web task, require an already available durable runtime with the
confirmed code version, dependencies, persistent state, non-prompt secrets,
network access, and exact one-cycle invocation. Do not provision cloud
infrastructure, upload local secrets, reconstruct the strategy from chat
context, or offer the runner when any requirement is missing.

Save a durable task instruction that tells each occurrence to run the exact
confirmed one-cycle invocation once, make no code or plan changes, create no
nested schedule, perform no scheduler retry, expose no secrets, and report the
result through task history. Configure the recurring schedule until explicitly
paused or deleted. Never manually trigger a run during creation or validation.

## Installation and lifecycle

Complete plan confirmation is the sole authorization for every recorded native
definition and external task create, update, pause, disable, activation, or
deletion. Apply those actions only after a ready target is provisioned, the
local build and offline checks pass, and the remote description is synchronized.
Never manually run a one-cycle command, start a persistent process, or trigger
a scheduled task during build or verification.

For a deferred target, retain normalized operation decisions but create no
native definition or agent task and keep all operational commands unavailable.
If required installation or activation fails, leave the plan `confirmed` and
the runner stopped or paused. Set the plan to `implemented` only when every
selected resource is installed, its confirmed active or inactive state is
verified, and any active schedule's next occurrence is reported.

An explicit cleanup plan may instead authorize attributable pause, disable,
graceful stop, deletion, and verification under `cleanup.md`. A current agent
that cannot manage the recorded native or external resource must leave it
untouched, preserve it in the pending cleanup plan, and report the exact
provider-neutral lifecycle information. Never treat lack of task visibility as
proof that a local, remote, or web task no longer exists.

An active resource may run at a later confirmed occurrence or login. The final
plan confirmation authorizes those future executions, not an immediate test
run. If a path, identity, capability, status, or required action differs from
the confirmed inventory, return the plan to `draft`, resolve only affected
decisions, and require one new complete-plan confirmation.

## Generated project guidance

The generated `README.md` must distinguish a single run, persistent process,
and recurring schedule. Identify the selected runner, environment, definitions
or task name, cadence, timezone, precision, missed-run behavior, activation,
next occurrence, overlap and retry policy, logs or history, notifications, and
runtime-location limitations. Provide exact install or create, activate,
pause, resume, status, log or history, update, and uninstall or delete actions.
Warn immediately before every manual activation or start action that it may
submit paper orders without another prompt.

The generated `AGENTS.md` must preserve the plan fields, credential boundary,
native host-write and external-task exceptions, collision rules, installation
ordering, no-immediate-run rule, and single-final-confirmation boundary. It must
require runtime-affecting updates to pause future cycles, wait for safe cycle
completion, leave the runner inactive afterward, and report the exact user-run
resume action. It must also route explicit retirement or replacement cleanup
through the installed `cleanup.md`, require exact resource attribution and
safe-cycle completion, and forbid automatic resumption or cleanup retries
during unrelated work.
