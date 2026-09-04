# Strategy Implementation

Read this file after **AlphaInsider setup status** is Authorized. It owns the
project build, one strategy run, AlphaInsider compatibility checks, and
order-free verification. `interview.md` owns phase transitions; `automation.md`
owns scheduler setup; and `scheduled-runs.md` owns entry modes, locks, health,
recovery, and strategy-run notifications.

## Build scope

1. Recheck the confirmed strategy, authorized setup, planned paths, and
   existing user changes.
2. Build the smallest source, state, documentation, scheduled-run instructions,
   and test set that follows the plan.
3. Run static checks and mocked or offline tests.
4. Return the evidence and any blocker to the interview. Do not create an
   AlphaInsider strategy or scheduler from this build procedure.

If the build needs an unplanned path, permission, change on AlphaInsider, or
behavior change, stop and return the affected stage to Draft. An implementation
fix that does not change the confirmed strategy needs no new interview.

Never run an order-capable strategy run during build or verification. Setup
calls can inspect or configure the authorized AlphaInsider strategy only in the
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

The scheduled AI obtains the confirmed inputs, makes the bounded decision,
applies risk checks, and uses project helpers for state and AlphaInsider
actions. It can use the calling model. Require a separate model API key only
when `plan.md` selects an external model service.

### Hybrid

Programs gather or calculate inputs and enforce mechanical limits. The
scheduled AI makes only the judgments assigned to it in `plan.md`.

For agent-led and hybrid projects, the scheduled-run instructions must define
allowed evidence, decision space, output shape, uncertainty behavior, hard risk
limits, and prohibited changes. Keep every decision prompt or rubric aligned
with the confirmed plan.

## One strategy run

The strategy-run workflow in `scheduled-runs.md` owns admission, the shared
lock, dry-run isolation, and post-run health handling. After it admits a
strategy run, execute these steps:

1. Read `plan.md` and `runtime/runbook.md` from disk.
2. Validate Strategy status Confirmed; require AlphaInsider setup status
   Authorized for order-free setup verification or Active for operation. Also
   validate AlphaInsider strategy identity, stock or cryptocurrency type,
   Automation state, Operational health, any user/update/deletion/setup pause,
   and unresolved prior action. Never allow an order unless setup and
   automation are Active and the current run clears every safety gate.
3. Compare current positions, open orders, and uncertain prior actions with
   saved state.
4. Run the shared AlphaInsider compatibility check for current availability.
5. Obtain fresh inputs under the confirmed data-cutoff and missing-data rules.
6. Calculate or make the confirmed decision.
7. Enforce asset, order-size, execution-specific exposure,
   total-position-value, loss, timing, and duplicate protections.
8. Repeat compatibility checks for the planned action and constraints that can
   change.
9. Submit only the confirmed AlphaInsider paper order when new orders are
   allowed, then persist a structured result.

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
otherwise return an error for the next-trigger retry flow.

The check must cover every applicable current AlphaInsider constraint,
including:

- market and operation availability under the session policy confirmed in
  `plan.md`, including current exchange status when authoritative guidance maps
  it. For stocks, use an explicit current AlphaInsider accepted-session rule
  when published. When no mapping is published, use the recorded Strategy
  Creator fallback for all AlphaInsider stocks: 09:30 until, but not including,
  16:00 `America/New_York` on a U.S. stock-market trading day, with holidays
  and early closes. Do not infer permission from an example exchange-status
  value. For cryptocurrency, treat order availability as 24/7. Newly
  documented support does not expand a confirmed schedule without a strategy
  update, while newly incompatible guidance reopens its timing decision;
- resolved instruments and strict `security` type compatibility;
- AlphaInsider strategy ownership, type, and current settings;
- positions, open orders, and uncertain prior submissions;
- the exact mapped execution behavior and side effects: direct-order amount or
  total selection, complete-target allocation cancellation and omitted-position
  closure, or signal-style webhook behavior as applicable;
- sizing and the confirmed maximum exposure under that operation's documented
  limits, using `getMaxOrderSize` for applicable direct orders and using `2×`
  only where the allocation or webhook contract defines it; and
- current endpoint permissions, operation-specific limits, account-tier
  dependencies, and side effects. Apply a tier limit only to an operation that
  its documentation explicitly names.

Never assume a missing `input_multiplier` is `1`. A failed external or strategy
action ends order-capable work for that trigger. Record it and wait for the next
scheduled or user-triggered run; never retry an order in the same trigger.

## Verification

Test whether the implementation follows the plan, not profitability or speed.
Cover the applicable strategy decisions, timestamps, freshness, the
stock-or-cryptocurrency limit, sizing, risk limits, position and order checks
against saved state, order mapping, and protection from future information.

Test the compatibility check at both checkpoints and on every order-capable
path, including supported, unavailable, invalid, and constraints that change
during a run. Test explicit accepted and rejected stock sessions, the
documentation-gap fallback, U.S. holidays and early closes, and 24/7
cryptocurrency availability. Also test the complete process in
`scheduled-runs.md`, including simultaneous triggers, single-run completion
without polling for a faster cadence, dry-run isolation, Active plus
Degraded/Retrying error handling, next-trigger recovery, ambiguous-order
reconciliation, no missed-order replay or same-trigger order retry, repair and
rollback, duplicate notification suppression, no notification for successful
runs, and notification delivery failure with self-healing both enabled and
disabled. Mock every notification channel; verification must not deliver a
setup or test notification. A failed channel can be repaired only when
notification repair is inside the enabled self-healing scope.

Mock external services. Tests must not submit or cancel an AlphaInsider paper
order. A performance difference from a backtest can start a correctness
review, but fails verification only when evidence proves the implementation
does not follow the plan.

## Build handoff

Use [generated project guidance](generated-project.md) for `README.md`,
`AGENTS.md`, and the scheduled-run instructions in `runtime/runbook.md`. Record
managed files, checks, and the current next step in `plan.md`. Return passed
evidence or the exact blocker to `interview.md`; it owns AlphaInsider strategy
setup, automation, and completion.
