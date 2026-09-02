# Strategy Implementation

Read this file after the applicable plan is Agreed. It owns the project build,
one finite strategy cycle, AlphaInsider compatibility checks, and order-free
verification. `interview.md` owns phase transitions; `automation.md` owns
scheduler setup; and `scheduled-runs.md` owns entry modes, locks, health,
recovery, and runtime notifications.

## Build scope

1. Recheck the agreed plan, planned paths, and existing user changes.
2. Build the smallest source, state, documentation, runbook, and test set that
   follows the plan.
3. Run static checks and mocked or offline tests.
4. Return the evidence and any blocker to the interview. Do not provision a
   target or scheduler from this build procedure.

If the build needs an unplanned path, permission, remote mutation, or behavior
change, stop and return the affected decision to Draft. A plan-preserving
implementation fix needs no new interview.

Never run an order-capable cycle during build or verification. Setup calls can
inspect or configure the agreed target only in the later target workflow. They
must not submit or cancel an order.

Use the layout in [persistent project](project-root.md). Default to Python when
no ecosystem requirement favors another language. Add only needed dependencies
and keep paths project-relative. Put safe variable names and examples in
`.env.example`; ignore secrets, caches, temporary files, and repair snapshots.

## Decision modes

### Code-led

Implement deterministic rules in project code. The scheduled AI invokes one
finite cycle, evaluates its structured result, and applies the runtime policy.

### Agent-led

The scheduled AI obtains the agreed inputs, makes the bounded decision, applies
risk checks, and uses project helpers for state and AlphaInsider actions. It
can use the calling model. Require a separate model API key only when `plan.md`
selects an external model service.

### Hybrid

Programs gather or calculate inputs and enforce mechanical limits. The
scheduled AI makes only the judgments assigned to it in `plan.md`.

For agent-led and hybrid projects, the runbook must define allowed evidence,
decision space, output shape, uncertainty behavior, hard risk limits, and
prohibited changes. Keep every decision prompt or rubric aligned with the plan.

## Finite strategy cycle

The runtime controller in `scheduled-runs.md` owns admission, the shared lock,
dry-run isolation, and post-cycle health handling. After it admits a normal
run, execute this cycle:

1. Read `plan.md` and `runtime/runbook.md` from disk.
2. Validate Plan agreement, target identity, strict asset type, automation
   state, pause reason, and durable trading block.
3. Reconcile relevant positions, open orders, and uncertain prior actions.
4. Run the shared AlphaInsider compatibility preflight for cycle availability.
5. Obtain fresh inputs under the agreed as-of and missing-data rules.
6. Calculate or make the agreed decision.
7. Enforce instrument, sizing, leverage, exposure, loss, timing, and duplicate
   protections.
8. Rerun compatibility checks for the planned action and mutable constraints.
9. Submit only the planned AlphaInsider paper action when normal trading is
   allowed, then persist a structured result.

The result must distinguish no-order success, confirmed order response,
confirmed pre-order failure, ambiguous possible order, warning, and skipped
overlap. Record no credential or unnecessary private response data.

## AlphaInsider compatibility

When `alphainsider-api` is installed, use its current instructions and only the
endpoint sections needed by the project. Otherwise, verify current AlphaInsider
documentation.

Implement one shared preflight for every order-capable path. Run it before input
and decision work for constraints that can stop the cycle. Immediately before
an external action, rerun it for that action's side effects and mutable
constraints. If a required fact cannot be verified, do not act. Return a safe
no-action result only for an expected unavailable state; otherwise return an
error.

The preflight must cover every applicable current AlphaInsider constraint,
including:

- market and operation availability; stock orders are accepted only during
  regular market hours;
- resolved instruments and strict `security` type compatibility;
- target ownership, type, and current settings;
- positions, open orders, and uncertain prior submissions;
- sizing and allocation rules, the planned leverage maximum, and the platform
  `2×` ceiling; and
- current endpoint permissions, limits, and side effects.

Never assume a missing `input_multiplier` is `1`. Use bounded, duplicate-safe
in-cycle backoff only for planned transient failures.

## Verification

Test observable plan conformance, not profitability or speed. Cover the
applicable strategy decisions, timestamps, freshness, type boundary, sizing,
risk limits, reconciliation, order mapping, and protection from future
information.

Test the compatibility preflight at both checkpoints and on every
order-capable path, including supported, unavailable, invalid, and mutable
cases. Also test the complete operational contract in `scheduled-runs.md`,
including overlap, dry-run isolation, mandatory error pause, repair and
rollback, recovery, quiet success, and notification-only failure.

Mock external services. Tests must not submit or cancel an AlphaInsider paper
order. A performance difference from the backtest can start a correctness
review, but fails verification only when evidence proves plan nonconformance.

## Build handoff

Use [generated project guidance](generated-project.md) for `README.md`,
`AGENTS.md`, and `runtime/runbook.md`. Record managed files, checks, and the
current next step in `plan.md`. Return passed evidence or the exact blocker to
`interview.md`; it owns target provisioning, automation, and completion.
