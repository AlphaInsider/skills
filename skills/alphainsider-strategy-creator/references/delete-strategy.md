# Delete Strategy Resources

Enter this workflow only after the user clearly asks to delete strategy
resources. Failure, stopping, supersession, retention cleanup, poor
performance, and completed creation never imply deletion authority.

## 1. Inventory attributable resources

1. Resolve the exact project and confirmed public strategy identity.
2. Inventory every resource created or used for this strategy:

   - native AI scheduler task;
   - AlphaInsider paper strategy and public strategy ID;
   - project source, `plan.md`, documentation, and tests;
   - backtest reports, visuals, historical data, recoverable source, and
     configuration;
   - saved run state, run history, logs, repair journal, and snapshots;
   - project `.env` or hosted secrets, without reading values; and
   - API-key revocation, which can require a user action in AlphaInsider
     developer settings.

3. Verify ownership and attribution rather than relying on a similar name.
4. Record safe labels and locations without exposing credentials or private
   destinations.

## 2. Select deletion scope

1. Use the decision-round format in
   [workflow contracts](workflow-contracts.md) to ask what to delete and retain.
2. Include **Delete everything** after a clear warning.
3. Recommend the scope that matches the user's explicit words.
4. When intent is broader than the evidence, recommend retaining historical
   and backtest material until the user confirms it is no longer needed.

Only an explicit selection can remove backtest source or configuration,
including Superseded or Failed evidence.

## 3. Review exact effects

Before final confirmation, show:

- exact project paths and selected data;
- exact native task name;
- public AlphaInsider strategy ID;
- secret locations without values;
- every retained item;
- irreversible effects and unresolved AlphaInsider behavior; and
- every user-operated revocation or platform action.

Before AlphaInsider strategy deletion, verify API permission, token user,
exact ID, ownership, subscriber count, open orders, and nonzero positions.
Explain that the current API might not define what deletion does to
subscribers, positions, or open orders. The user can still select deletion
after that warning.

## 4. Pause safely

1. Save in project state that new orders are paused for deletion.
2. Pause future native automation.
3. Wait for the shared run or repair lock to become idle.
4. Recheck the exact selected resources immediately before removal.

Do not change or delete run-owned files while lock ownership is unresolved.

## 5. Apply confirmed deletion

Perform only the confirmed actions in this order:

1. Delete the exact attributable native task and verify its absence.
2. Apply the selected AlphaInsider strategy action.
3. Remove selected secrets and explain any external key-revocation action.
4. Delete only the exact selected project data.
5. Report completed, retained, and failed items.

Deletion never cancels an order, liquidates a position, submits a trade, or
connects a broker. If AlphaInsider strategy deletion fails, keep the project
and public strategy ID required for recovery. Remove local recovery data after
that failure only if the user explicitly chooses to continue.

Prefer a recoverable local deletion mechanism when the platform supplies one.
Never recursively delete an uncertain path, persistent parent, repository root,
or installed skill directory.

## 6. Record the outcome

1. For partial deletion, update `plan.md` with retained resources, missing
   resources, Automation state, operational safety state, and any recovery
   action.
2. For full deletion, remove the entire exact selected project and leave no
   tombstone.
3. Never resume automation during or after deletion.
