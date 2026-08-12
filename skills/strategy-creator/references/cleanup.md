# Strategy Cleanup and Retirement

Use this reference only when the user explicitly asks to retire, delete, clean
up, or replace a recognized Strategy Creator project. Cleanup is a lifecycle
branch, not a Strategy Plan interview phase. Never run it during unrelated
maintenance or a version-only upgrade.

## Contents

- [Recognition and staging](#recognition-and-staging)
- [Interview and confirmation](#interview-and-confirmation)
- [Operation shutdown](#operation-shutdown)
- [AlphaInsider disposition](#alphainsider-disposition)
- [Local retirement](#local-retirement)
- [Replacement ordering](#replacement-ordering)
- [Failures and resumption](#failures-and-resumption)
- [Generated project guidance](#generated-project-guidance)

## Recognition and staging

Recognize the project through the valid authoritative `docs/plan.md`, its
contract version and lifecycle status, and the exact managed-artifact and
operation-resource inventory. Perform read-only checks for every project path,
native definition, agent task, runtime lock or marker, process state, and
AlphaInsider target before proposing a destructive action.

Refuse to infer ownership from a filename, process name, target name, or
schedule name alone. Do not remove a path or resource unless the plan and live
state attribute the exact identity to this strategy. If attribution is missing
or conflicts, leave the item untouched and record the blocker.

Create or resume `docs/cleanup-plan.md` from `cleanup-plan-template.md`. It may
use only `draft` or `confirmed`. It is the sole plan allowed to record the exact
non-secret AlphaInsider strategy ID so a failed deletion remains resumable.
Active plans, replacement plans, source, tests, scheduler definitions, task
prompts, logs, `README.md`, and `AGENTS.md` must still omit strategy IDs.

Permit only one unresolved cleanup plan in a project. Never overwrite a
collision. A pending cleanup may be resumed only when the user explicitly asks
for cleanup; do not retry it during unrelated work. Resolve it or revise its
remote disposition to retain before staging another replacement or retirement.

## Interview and confirmation

Ask exactly one decision per turn. For an explicit retirement, ask whether the
verified owned AlphaInsider strategy should be `retain and detach` or `delete`.
Recommend retention when the request does not already state deletion because
remote deletion is irreversible. The local result is always a retired record:
remove only attributable implementation and operation resources while
preserving the project root, `.env`, `.gitignore`, credentials, historical
data, and every user-authored, unrelated, or uncertain path.

For a replacement, ask the same remote-disposition decision for the outgoing
target while `docs/replacement-plan.md` and `docs/cleanup-plan.md` are draft.
The replacement's one final complete-plan confirmation confirms both plans and
authorizes their exact recorded actions. An explicit retirement uses one final
cleanup-plan confirmation. Never request action-by-action approval afterward.

Immediately before confirmation, show the target's exact non-secret ID, name,
asset class, source, verified ownership, subscriber count, open-order and
nonzero-position findings, every operation resource, every local path action,
the binding action, and the ordered failure behavior. If any item changes after
confirmation, return the cleanup plan to `draft` and reconfirm the complete
inventory rather than requesting a one-off approval.

## Operation shutdown

Prevent future cycles before remote or local deletion. Use the runner's exact
confirmed lifecycle controls and remain agent-vendor neutral:

- For a recurring native or agent task, pause or disable recurrence, verify the
  inactive state, allow an attributable active occurrence to finish, delete the
  exact definition or task, and verify absence.
- For a native persistent service, disable future starts, request a graceful
  stop at a safe cycle boundary, remove the exact attributable definition,
  reload or unregister the user manager when required, and verify absence.
- For a foreground persistent process, use the generated runtime lock or marker
  plus process identity and command path to establish attribution. Request a
  graceful stop. If the controlling session requires user action, provide the
  exact visible stop instruction and wait; never force-kill an uncertain
  process.
- For a finite foreground cycle, wait for the attributable runtime lock to
  release. Never interrupt it mid-cycle or start another cycle as a test.
- For a remote or web agent task, require the current environment to expose the
  exact task identity, runtime location, active-run state, pause or disable,
  history, and deletion capabilities. If it cannot, leave the task untouched
  and provide the recorded provider-neutral lifecycle information.

All generated operational entry points must acquire one fail-closed
process-lifetime lock or equivalent shared remote lock before external data or
order work. Its non-secret marker may contain project identity, invocation
model, PID or run identity, and start time for attribution. Remove a stale
marker only after proving no matching process or remote occurrence is active.

If an active cycle cannot reach safe completion or any required runner cannot
be disabled and removed, stop cleanup. Leave future execution inactive when
possible, record the exact recovery action, and perform no AlphaInsider or
local deletion. Never resume or reactivate an outgoing runner automatically.

## AlphaInsider disposition

Use the sibling request helper and never open `.env`. Reverify `deleteStrategy`
permission, the token's user ID, the exact target through `getStrategies`, and
ownership through `getUserStrategies` and owner-subscription context. Selected
existing and Strategy Creator-created targets are both eligible when ownership
and exact identity are verified and the user chose deletion.

Before deletion, use read-only calls to record the current subscriber count and
subscription context, open orders, and nonzero positions. Explain that the
documented `deleteStrategy` operation does not state whether or how those
resources cascade. The user may still confirm deletion with any of those
findings present. Cleanup never calls `newOrder`, `newOrderAllocations`, or a
liquidation action. It never calls `deleteOrder` or any other trading endpoint.

Immediately before `deleteStrategy`, re-fetch the exact target and ownership.
Stop on a missing target, ID mismatch, ownership mismatch, or changed material
metadata. Send only the confirmed cleanup-plan strategy ID. After success,
verify that the target no longer resolves. Remove `ALPHAINSIDER_STRATEGY_ID`
only when the configured binding was confirmed to match the deleted target;
never remove a binding that points to a replacement or another target.

For `retain and detach`, make no deletion call. Reverify the exact binding and
remove only matching `ALPHAINSIDER_STRATEGY_ID` through the installed
agent-only helper. Preserve `ALPHAINSIDER_API_KEY`. For a replacement, persist
the ready replacement target as the active binding instead of removing it.

## Local retirement

After operation shutdown, remove only the exact attributable generated source,
tests, copied helpers, dependency configuration, `.env.example`, generated
`README.md`, generated `AGENTS.md`, and operation definitions listed in the
confirmed cleanup plan. Never recursively delete the project root. Preserve
`.env`, `.gitignore`, credentials, caches, historical logs, persistent strategy
state, backtest outputs, user-authored files, unrelated resources, and every
item with uncertain ownership. Remove a verified stale runtime lock only after
the running-state checks above.

For explicit retirement, update `docs/plan.md` to `status: retired` and record
the local, operation, and target disposition results in its existing fields;
do not add a new Strategy Plan section. For replacement, move the outgoing plan
to `docs/retired/YYYYMMDDTHHMMSSZ-<slug>.md` before promoting
`docs/replacement-plan.md`. Use a portable UTC timestamp and normalized strategy
slug. Stop rather than overwrite an archive collision.

After every selected remote and local action is resolved, update the retired
record with safe target disposition and UTC completion data without the
strategy ID, then remove `docs/cleanup-plan.md`. A retired plan remains
recognizable as an audit record but cannot operate a strategy.

## Replacement ordering

Keep the outgoing strategy intact while the replacement and cleanup plans are
draft. After their joint confirmation:

1. If the replacement target is deferred, stop and leave the outgoing strategy,
   binding, implementation, and resources unchanged.
2. Pause or disable the outgoing runner and wait for its active cycle to finish.
3. Resolve, provision when applicable, validate, and persist the ready
   replacement target before deleting the outgoing AlphaInsider target.
4. Remove and verify the outgoing operation resources, then apply its remote
   disposition.
5. Remove attributable local artifacts, archive the outgoing plan, and promote
   the replacement.
6. Build, verify, synchronize, and install the replacement resources under the
   normal confirmed lifecycle. Never trigger an immediate run.

If outgoing remote deletion alone fails, keep `docs/cleanup-plan.md` confirmed
with the exact ID and recovery result. Continue the ready replacement and allow
its confirmed future activation with a prominent pending-cleanup warning. A
shutdown, operation-removal, archive, promotion, or local-cleanup failure blocks
replacement activation.

## Failures and resumption

Record each completed action before advancing so a confirmed cleanup can resume
without repeating successful destructive work. Revalidate every remaining
identity and precondition on resumption. If target metadata, ownership, paths,
resources, or running state changed materially, return the cleanup plan to
`draft` and require one new complete confirmation.

Remote deletion failure does not recreate, cancel, or alter orders or
positions. Complete the safe local retirement when operation shutdown and local
attribution succeeded, retain the confirmed cleanup plan for retry, and report
the remote strategy as still present. If remote deletion succeeded but a later
local action failed, record the partial state and never recreate the target.

Never execute a confirmed cleanup merely because it exists. Resume only in
response to an explicit cleanup request. After the user revises a failed delete
to retain, detach the matching binding as applicable, record the retained
disposition, and finish the normal retirement flow.

## Generated project guidance

Generated `README.md` files must identify the exact project-local retirement
request, runner lifecycle, safe-stop behavior, preserved data, remote
retain-or-delete choice, live-state warning, and recovery path. Do not include
the target ID or credentials.

Generated `AGENTS.md` files must tell future agents to read this installed
cleanup workflow, recognize `docs/cleanup-plan.md` and retired records, perform
read-only attribution first, ask one decision per turn, require one final
confirmation, disable execution before deletion, remain provider-neutral for
agent tasks, and never cancel orders, liquidate positions, force-kill uncertain
processes, retry during unrelated work, or delete unconfirmed resources.
