---
name: alphainsider-strategy-creator
description: Create, resume, backtest, implement, automate, run, update, or explicitly delete one plan-driven AlphaInsider stock or cryptocurrency strategy that uses native AI scheduling.
---

# AlphaInsider Strategy Creator

Guide one strategy to verified AlphaInsider paper automation. Keep this skill
read-only; create and change artifacts only in the selected persistent project.

## Contract

- Send orders only to AlphaInsider paper strategies. Never create or connect a
  broker client, request broker credentials, or treat future order authority as
  authority for another external action.
- Treat project `plan.md` as the readable source of truth. Tests, code, the
  AlphaInsider strategy, and automation must conform to it.
- Keep one strategy with one strict `stock` or `cryptocurrency` type in each
  project.
- Never inspect or expose an existing API key, complete `.env`, process
  environment, or secret store. Use only the protected credential workflow.
- Use only the platform's native AI automation or scheduler. Never install a
  host scheduler or keep a run alive to simulate a faster cadence.
- Check applicable AlphaInsider and scheduler constraints before proposing an
  action; recheck changeable facts immediately before acting.
- Keep active automation running through operational errors. Withhold unsafe
  orders, set health to Degraded/Retrying, and retry checks on the next trigger.
  Only the user or an explicit setup, update, or deletion workflow may pause it.
- Treat poor performance as information, never as permission to change a plan
  or as proof that a plan-compliant run is unhealthy.
- Call creation Complete only after the AlphaInsider strategy validates and its
  native automation is active. A stop or blocker remains resumable and never
  authorizes deletion.

Read [workflow contracts](references/workflow-contracts.md) for authority,
status, communication, evidence, and API-source rules.

Follow links from the selected workflow only when their phase begins.

## 1. Start or resume

1. Read [start or resume](references/start-or-resume.md).
2. Resolve one safe persistent project without opening `.env`.
3. Read `plan.md` and **Current status** when the project already exists.
4. Route the request from the recorded state and the user's current words.

## 2. Route the request

1. Compare the user's current words with the recorded project state.
2. Select one branch below without presenting unrelated later work.

### Create or complete a strategy

1. Follow [define strategy](references/define-strategy.md) for a new strategy,
   incomplete definition, or definition reopened by drift or revision.
2. Follow [backtest strategy](references/backtest-strategy.md) only after the
   user selects **Backtest Strategy**.
3. Follow [implement and activate](references/implement-and-activate.md) after
   the user skips backtesting or chooses implementation from reviewed results.
4. Use [project contract](references/project-contract.md) whenever the workflow
   creates, migrates, or hands off project artifacts. New plans use the
   [plan template](references/plan-template.md).

### Operate the strategy

1. Read [run and recover](references/run-and-recover.md) for every scheduled
   run, scheduler **Run now**, chat run, dry run, operational error,
   notification event, or confirmed self-heal attempt.
2. Perform at most one run per trigger through the shared lock.
3. Let generated project instructions run and self-heal without this installed
   skill; use this skill again for strategy or automation changes.

### Update the strategy

1. Read [update strategy](references/update-strategy.md) for a requested
   change, detected user edit, or external drift.
2. Preserve the confirmed plan while proposed behavior remains Draft.
3. Reopen and reauthorize only affected decisions and work.

### Delete strategy resources

1. Read [delete strategy](references/delete-strategy.md) only after an explicit
   deletion request.
2. Inventory and confirm exact resources before removing anything.
3. Never infer deletion from failure, supersession, stopping, or poor results.
