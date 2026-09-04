# Update Strategy

Use this workflow for a requested change, a user edit, or external drift. It
owns proposed-change isolation, affected-decision review, evidence
supersession, rebuild, and safe restoration of automation. Use
[delete strategy](delete-strategy.md) only for explicit deletion.

The agent manages the dedicated project, but the user can edit any project
file.

## 1. Classify the change

1. Before writing project files or external state, detect user edits by
   comparing project files, native task, AlphaInsider paper strategy, and saved
   runtime state with the confirmed `plan.md`.
2. Determine whether each difference changes intended strategy behavior,
   implementation only, external-resource configuration, or documentation.
3. Preserve user changes that clearly conform to the plan.
4. Test and document compatible implementation improvements only within the
   confirmed implementation scope.
5. Ask the user when an edit changes or obscures intended behavior.

Never overwrite an unclear user change merely to restore generated text. An
implementation repair that preserves clear confirmed intent does not need a
strategy update. Performance alone never starts an automatic strategy change;
it can prompt a correctness review, but trading behavior changes only after the
user reviews and confirms them.

### External drift

1. Compare the native task, AlphaInsider strategy identity, description,
   access setting, and saved run state with `plan.md`.
2. When a mismatch can affect orders, immediately pause new orders in project
   state and pause native automation.
3. Reconcile ambiguous external results before any retry or replacement.
4. Repair compatible wiring only when it restores the confirmed plan within
   its confirmed implementation scope, without changing behavior or identity.
5. Route every material strategy, schedule, access, or identity decision
   through the affected update steps below.

## 2. Isolate a proposed behavior change

1. Preserve active confirmed `plan.md` as the authoritative current strategy.
2. Create root `pending-update.md` with the proposed change, affected
   decisions, dependent questions, prior automation state, and Draft status.
3. Save in project state that new orders are paused for the update.
4. Pause future native automation.
5. Wait for the shared run or repair lock to become idle.

If safe pause or idle state cannot be verified, do not change files used by a
strategy run. Preserve every unaffected choice and artifact and record the
exact next action.

## 3. Redefine only affected behavior

1. Use [define strategy](define-strategy.md) for changed and dependent
   decisions only.
2. Keep current Strategy status Confirmed in `plan.md` while the pending update
   remains Draft.
3. Show the revised strategy summary and ordinary next-step choices. A forward
   choice confirms the revision but does not broadly authorize later build or
   external work.
4. Preserve all unaffected strategy, setup, resource, and history decisions.

## 4. Reconcile affected backtests

1. Mark every affected Valid run Superseded with the exact update reason.
2. Preserve its methodology, recoverable source, configuration, data outputs,
   reports, and visuals.
3. Clear affected evidence as featured.
4. Set the pending Highest completed outcome to Strategy defined until another
   Valid run matches the revised strategy and current backtest plan.
5. Run each user-selected affected backtest only after its future-information
   disclosures and complete plan receive **Build and Run** authority through
   [backtest strategy](backtest-strategy.md).

Never delete evidence because it is Superseded, Failed, older, or no longer
featured.

## 5. Review and authorize implementation changes

1. Recompute affected source, state, permissions, AlphaInsider changes,
   scheduler settings, tests, documents, and runbook behavior.
2. Show the complete revised implementation scope.
3. Continue only after **Build, Configure, and Activate** authorizes those
   listed local and external actions.
4. Use [implement and activate](implement-and-activate.md) for credential,
   paper-strategy, build, verification, and scheduler rules.

An AlphaInsider strategy identity, schedule frequency, access mode, or strategy
behavior change always requires reviewed user confirmation. Repair only wiring
that follows the confirmed plan.

## 6. Apply and finalize the update

1. Update implementation, protected tests, documentation, and
   `runtime/runbook.md`.
2. Pass offline checks proving the revised implementation follows the revised
   plan.
3. Update the AlphaInsider description only when needed and authorized.
4. Merge the confirmed result from `pending-update.md` into `plan.md`.
5. Remove `pending-update.md` only after the merge and all required resource
   changes verify.
6. Clear the update order pause.
7. Resume native automation only when it was active before the update and the
   revised activation gates pass.
8. Record the new current state, evidence, resource identities, next run, and
   result.

Do not resume automatically when the user had already paused automation.
