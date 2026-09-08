# Run and Recover

Use this contract to generate the project's executable workflow and runbook.
Choose mechanisms appropriate to the scheduler and implementation, and verify
them before activation.

## Scheduled run

1. Read fresh `plan.md` and the project runbook. Respect saved pauses and
   unresolved incidents before order work. Acquire shared exclusivity covering
   the command, AI decisions, evaluation, repair, and any retry. All scheduled
   and manual entry points must respect it; an overlapping invocation exits.
2. Run the program command. When the strategy assigns judgment to the scheduled
   AI, follow its recorded role and pass decisions through the program's
   execution controls. Keep program entry points for execution and dry runs.
3. Evaluate the command's result against expected outcomes in `plan.md`, using
   saved evidence as well as exit status. A planned no-trade result is success;
   poor returns alone are not an implementation failure.
4. Record the outcome and apply the selected notification settings. Release
   exclusivity after evaluation and any recovery are complete.

The program must distinguish a known result from an uncertain order outcome
and prevent duplicate execution, including sequential duplicate triggers. A
dry run must be technically unable to submit, change, or cancel orders or
advance trading state. Choose and test these protections for the actual design.

## Error and recovery

1. Stop further order work. Save the incident and block new executions in
   project state, then pause the scheduler and verify it is paused. If pause
   cannot be verified, keep execution blocked and report the required action.
2. Diagnose the issue against the plan and saved evidence.
3. If self-healing is enabled, a fix preserves the plan's high-level decisions,
   and no human input or new authority is needed, repair the implementation.
   Any implementation issue is eligible under those conditions; there is no
   fixed list of repairable files or components. Update operational notes in
   `plan.md` without rewriting decisions to justify a repair. Otherwise leave
   automation paused, record what the user needs to resolve, and end recovery.
4. Dry-run the fix and run meaningful checks without AlphaInsider orders.
   Leave a coherent paused implementation if checks fail or recovery cannot
   finish within the available execution time.
5. After checks pass, reconcile uncertain previous actions before allowing
   orders; leave automation paused if an outcome remains unresolved. Use
   judgment to rerun now with current inputs or resume for the next suitable
   scheduled run. An immediate retry keeps the scheduler paused and admits
   only the recovery owner through this incident's execution block, under the
   same exclusivity and all other plan/order checks. If it fails, keep the
   scheduler paused and record the unresolved issue.
6. Clear this incident's execution block and resume the scheduler only after
   recovery succeeds. Verify and record the actual scheduler state. Never
   override a later user pause. Send the selected incident/recovery notification.

If self-healing is disabled, needs human input, fails, or the agent is
interrupted after pausing, leave automation paused. Save the diagnosis and
next action so the user can resume recovery in any chat. Do not rely on the
paused scheduler to launch another attempt or create a separate recovery task.

## Notifications

Use these strategy-run notification labels exactly, for selected events:

- `🚨 Error — Action Required` — recovery is waiting for the user; explain the
  issue, recommended next step, and any information or decision needed.
- `🔄 Retrying — No Action Required` — an automatic retry is underway or has an
  active scheduled trigger; explain what is being retried and what happens next.
- `🛠️ Self-Healed — No Action Required` — a repair has passed verification;
  safe operation is restored and no user action is needed. Explain what was
  restored and report the actual scheduler state and next run.
- `⚠️ Warning — No Action Required` — useful information that requires no
  user action.

Use the channels, destinations, and events agreed in `plan.md`. Keep messages
short and understandable: identify the strategy, explain the effect and current
automation state, and give the next step. Keep technical diagnostics in project
artifacts and secrets in `.env`. Record delivery failures honestly in the plan;
never claim that an unavailable channel notified the user.
