# Strategy Implementation

Read this file after the applicable plan is Agreed. Build the smallest project
that follows `plan.md` and supports the selected code-led, agent-led, or hybrid
mode.

## Build order and boundaries

1. Recheck all planned paths and existing user changes.
2. Build source, state, docs, the runbook, and tests.
3. Run static checks and mocked or offline tests.
4. Set **Phase** to Configuring automation, then create or bind the
   AlphaInsider target only after those checks pass.
5. Validate the target and synchronize its description.
6. Create and activate the native AI schedule for its next normal occurrence.

If an unplanned path, permission, target mutation, or high-level behavior
change becomes necessary, stop and return the affected decision to Draft.
Routine plan-preserving implementation fixes need no new interview.

Never run an order-capable cycle during build or verification. AlphaInsider
setup calls can create or configure the agreed target, but must not submit or
cancel an order.

## Project structure

Use the core layout in `project-root.md`. Default to Python when no ecosystem
requirement favors another language. Add only needed dependency files. Keep
paths project-relative.

- `strategy/` contains reusable decision, data, risk, reconciliation, and
  AlphaInsider runtime code.
- `backtest/` contains historical replay code, data manifests, charts, and
  reports.
- `runtime/runbook.md` contains one finite AI-occurrence procedure.
- `runtime/` contains structured state, the shared lock, health, run history,
  repair journal, and snapshots.
- `tests/` contains order-free plan-conformance tests.

Put names and safe examples in `.env.example`. Ignore `.env`, caches, temporary
files, repair snapshots, and generated secrets. Keep `plan.md`, source, tests,
docs, and safe result summaries ready for source control.

## Decision modes

### Code-led

Implement deterministic rules in project code. The scheduled AI reads the plan
and runbook, invokes one finite cycle, evaluates its structured result, and
handles the agreed error policy.

### Agent-led

The scheduled AI reads the plan, obtains the agreed inputs, makes the bounded
decision itself, applies risk checks, and uses project helpers for safe state
and AlphaInsider actions. It can use the calling AI model. Do not require a
separate model API key unless `plan.md` explicitly selects an external model.

### Hybrid

Programs gather or calculate inputs and enforce mechanical limits. The
scheduled AI makes only the judgments that `plan.md` assigns to it.

For agent-led and hybrid projects, the runbook must state the allowed evidence,
decision space, output shape, uncertainty behavior, hard risk limits, and
prohibited changes. Keep any decision-affecting prompt or rubric aligned with
`plan.md`.

## One finite normal cycle

Every scheduled occurrence, scheduler **Run now**, and chat normal run uses the
same logical cycle:

1. acquire the project-wide atomic run lock before external work;
2. read `plan.md` and `runtime/runbook.md`;
3. verify Plan agreement, target identity, strict asset type, automation state,
   pause reason, and durable trading block;
4. reconcile relevant positions, open orders, and prior uncertain actions;
5. run the shared AlphaInsider compatibility preflight for cycle availability;
6. obtain fresh inputs with the agreed as-of and missing-data rules;
7. calculate or make the agreed decision;
8. enforce instrument, sizing, leverage, exposure, loss, timing, and duplicate
   protections;
9. rerun that preflight for the planned action and mutable constraints;
10. submit only the planned AlphaInsider paper action when normal trading is
   allowed; and
11. persist a structured result and release the lock.

Update **Current status** with the last completed step, next step, open error,
and UTC time without changing the agreed strategy.

The result must distinguish no-order success, confirmed order response,
confirmed pre-order failure, ambiguous possible order, warning, and skipped
overlap. Do not store credentials or unnecessary private response data.

Use one lock across every local or hosted runtime. The first occurrence runs.
Any overlapping occurrence records a skip and exits before data, decision, or
order work. Never remove a stale lock until liveness checks prove its owner is
not active.

## AlphaInsider compatibility

When `alphainsider-api` is installed, read its current instructions and only
the endpoint sections needed by this project. Otherwise, verify against current
AlphaInsider documentation.

Use one shared compatibility preflight for every order-capable entry path. Run
it before input and decision work for constraints that determine whether the
cycle can proceed. Immediately before an external action, rerun it with that
action's side effects and constraints that can change. If a required fact
cannot be verified, do not perform the action. Return a safe no-action result
only for an expected unavailable state; otherwise use error handling.

AlphaInsider stock orders are limited to regular market hours. Submit only when
the current status confirms that the regular market is open; otherwise use the
safe no-action or error result above.

- Resolve unknown instruments without guessing. Validate each result and its
  `security` type. Dynamic candidates must stay inside the planned asset type.
- Reconcile before deciding. Treat an uncertain prior submission as an error
  that blocks another possible duplicate.
- Never assume a missing `input_multiplier` is `1`.
- Use current AlphaInsider sizing and allocation rules. Enforce both the
  user's maximum leverage and the platform's `2×` ceiling.
- Use bounded in-cycle backoff for planned transient failures. Keep retries
  duplicate-safe.

## Verification

Test observable plan conformance, not profitability or speed. Include the
applicable cases:

- signal or agent-decision contract;
- timestamps, freshness, missing data, and strict asset type;
- sizing, leverage, exposure, and order mapping;
- positions, open orders, uncertain submissions, and reconciliation;
- overlapping normal and dry runs;
- dry-run prevention of orders and canonical state changes;
- the shared AlphaInsider compatibility preflight at both checkpoints,
  including supported and unsupported cases, endpoint side effects, and every
  order-capable entry path;
- scheduler pause and durable-block behavior;
- notification labels and failure handling;
- self-heal scope, snapshots, repeated dry checks, rollback, and time limit;
  and
- backtest logic and protection from future information.

Mock external services. Tests must not submit or cancel an AlphaInsider paper
order. Performance differences from the backtest can prompt a correctness
review, but they fail verification only when evidence shows plan
nonconformance.

## Documentation and completion

Follow `generated-project.md` for `README.md`, `AGENTS.md`, and the runbook.
Record the exact managed files, task identity, public target ID, checks, and
current next step in `plan.md`.

An incomplete target or scheduler gate does not discard the build. Preserve
the project, set the appropriate highest completed outcome, and identify the
next action. Set Automated strategy only after every completion condition in
`interview.md` passes.
