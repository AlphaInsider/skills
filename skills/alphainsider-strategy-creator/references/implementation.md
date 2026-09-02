# Strategy Implementation

Read this file after the applicable plan is Agreed. It owns the project build,
one strategy run, AlphaInsider compatibility checks, and order-free
verification. `interview.md` owns phase transitions; `automation.md` owns
scheduler setup; and `scheduled-runs.md` owns entry modes, locks, health,
recovery, and strategy-run notifications.

## Build scope

1. Recheck the agreed plan, planned paths, and existing user changes.
2. Build the smallest source, state, documentation, scheduled-run instructions,
   and test set that follows the plan.
3. Run static checks and mocked or offline tests.
4. Return the evidence and any blocker to the interview. Do not create an
   AlphaInsider strategy or scheduler from this build procedure.

If the build needs an unplanned path, permission, change on AlphaInsider, or
behavior change, stop and return the affected decision to Draft. An
implementation fix that does not change the agreed strategy needs no new
interview.

Never run an order-capable strategy run during build or verification. Setup
calls can inspect or configure the agreed AlphaInsider strategy only in the
later AlphaInsider setup workflow. They must not submit or cancel an order.

Use the layout in [persistent project](project-root.md). Default to Python when
no ecosystem requirement favors another language. Add only needed dependencies
and keep paths project-relative. Put safe variable names and examples in
`.env.example`; ignore secrets, caches, temporary files, and repair snapshots.

## Decision modes

### Code-led

Implement deterministic rules in project code. The scheduled AI invokes one
strategy run, evaluates its structured result, and applies the run policy.

### Agent-led

The scheduled AI obtains the agreed inputs, makes the bounded decision, applies
risk checks, and uses project helpers for state and AlphaInsider actions. It
can use the calling model. Require a separate model API key only when `plan.md`
selects an external model service.

### Hybrid

Programs gather or calculate inputs and enforce mechanical limits. The
scheduled AI makes only the judgments assigned to it in `plan.md`.

For agent-led and hybrid projects, the scheduled-run instructions must define
allowed evidence, decision space, output shape, uncertainty behavior, hard risk
limits, and prohibited changes. Keep every decision prompt or rubric aligned
with the plan.

## One strategy run

The strategy-run workflow in `scheduled-runs.md` owns admission, the shared
lock, dry-run isolation, and post-run health handling. After it admits a
strategy run, execute these steps:

1. Read `plan.md` and `runtime/runbook.md` from disk.
2. Validate Plan agreement, AlphaInsider strategy identity, the plan's stock or
   cryptocurrency type, automation state, pause reason, and whether project
   state says new orders are paused.
3. Compare current positions, open orders, and uncertain prior actions with
   saved state.
4. Run the shared AlphaInsider compatibility check for current availability.
5. Obtain fresh inputs under the agreed data-cutoff and missing-data rules.
6. Calculate or make the agreed decision.
7. Enforce asset, order-size, leverage, total-position-value, loss, timing, and
   duplicate protections.
8. Repeat compatibility checks for the planned action and constraints that can
   change.
9. Submit only the planned AlphaInsider paper order when new orders are allowed,
   then persist a structured result.

The result must distinguish no-order success, confirmed order response,
confirmed failure before an order, an order with an unknown submission result,
warning, and a run skipped because another run was active. Record no credential
or unnecessary private response data.

## AlphaInsider compatibility

When `alphainsider-api` is installed, use its current instructions and only the
endpoint sections needed by the project. Otherwise, verify current AlphaInsider
documentation.

Implement one shared compatibility check for every order-capable path. Run it
before input and decision work for constraints that can stop the strategy run.
Immediately before an external action, repeat it for that action's side effects
and constraints that can change. If a required fact cannot be verified, do not
act. Return a safe no-action result only for an expected unavailable state;
otherwise return an error.

The check must cover every applicable current AlphaInsider constraint,
including:

- market and operation availability; stock orders are accepted only during
  regular market hours;
- resolved instruments and strict `security` type compatibility;
- AlphaInsider strategy ownership, type, and current settings;
- positions, open orders, and uncertain prior submissions;
- sizing and allocation rules, the planned leverage maximum, and the platform
  `2×` ceiling; and
- current endpoint permissions, limits, and side effects.

Never assume a missing `input_multiplier` is `1`. Wait and retry only within
one strategy run, only for planned temporary failures, and only when doing so
cannot create a duplicate.

## Verification

Test whether the implementation follows the plan, not profitability or speed.
Cover the applicable strategy decisions, timestamps, freshness, the
stock-or-cryptocurrency limit, sizing, risk limits, position and order checks
against saved state, order mapping, and protection from future information.

Test the compatibility check at both checkpoints and on every order-capable
path, including supported, unavailable, invalid, and constraints that change
during a run. Also test the complete process in `scheduled-runs.md`, including
simultaneous triggers, dry-run isolation, mandatory error pause, repair and
rollback, recovery, no notification for successful runs, and failure to send a
notification.

Mock external services. Tests must not submit or cancel an AlphaInsider paper
order. A performance difference from the backtest can start a correctness
review, but fails verification only when evidence proves the implementation
does not follow the plan.

## Build handoff

Use [generated project guidance](generated-project.md) for `README.md`,
`AGENTS.md`, and the scheduled-run instructions in `runtime/runbook.md`. Record
managed files, checks, and the current next step in `plan.md`. Return passed
evidence or the exact blocker to `interview.md`; it owns AlphaInsider strategy
setup, automation, and completion.
