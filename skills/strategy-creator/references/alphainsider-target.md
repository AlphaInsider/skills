# AlphaInsider Target Setup

Use this reference after strategy, backtesting, implementation-contract, and
operation-and-scheduling planning as the final AlphaInsider forward-test setup
phase before confirmation. Record the non-secret strategy ID on the active or
replacement plan after the user selects an existing target or confirmation
creates one. Never record credentials. Follow `cleanup.md` for retirement or
outgoing replacement.

## Contents

- [API-key permission gate](#api-key-permission-gate)
- [Resolve the target](#resolve-the-target)
- [Target deferral](#target-deferral)
- [Confirmed provisioning](#confirmed-provisioning)
- [Post-creation cleanup](#post-creation-cleanup)
- [Description synchronization](#description-synchronization)
- [Generated project documentation](#generated-project-documentation)

## API-key permission gate

Before asking the user to set `ALPHAINSIDER_API_KEY`, link to
[AlphaInsider developer settings](https://alphainsider.com/settings/developers)
and instruct them to create one key by selecting the **AI Agent** preset. The
preset selects every required permission below; the user may alternatively
select the complete list individually:

```text
getUserInfo
getStrategies
getStrategyValues
getUserStrategies
getStrategyPerformance
getRecommendedStrategies
searchStrategies
newStrategy
updateStrategy
deleteStrategy
getStrategySubscriptions
getStrategyCalculation
getAccountSubscription
getTimelines
getStrategyTimelines
newPost
previewPost
deletePost
getPositions
getOrders
getMaxOrderSize
newOrder
newOrderAllocations
deleteOrder
wsStockPrice
wsStrategyValue
wsOrders
wsPositions
wsTimelines
```

Explain that `verifyToken` has no selectable permission and that AlphaInsider's
stock REST lookup endpoints require no API-key permission. `deleteStrategy` is
included for a separately confirmed retirement or outgoing replacement
cleanup. Token scope alone never authorizes deletion; the cleanup workflow
must verify exact identity and ownership and record the user's
retain-or-delete decision.

Timeline permissions allow reading, creating, previewing, and deleting posts;
`like` and `unlike` are not required. The subscription permissions are
read-only and never authorize starting, changing, or cancelling a subscription.

After the key is available, use the sibling request helper to call
`POST /verifyToken`. Read only the returned `user_id` and `scope`; never expose
the token. Compare `scope` with the complete bundle above. If any permission is
missing, list only the missing permission names, instruct the user to create or
replace the key with the **AI Agent** preset, and pause AlphaInsider target
setup and every remote action.
Record the target as local-only if the key cannot be corrected in the current
run; preserve every completed earlier planning decision. Accept extra
permissions without treating them as Strategy Creator requirements.

## Resolve the target

Run this flow only after the API key passes the permission gate.

1. If the helper resolves a configured strategy ID, validate it with
   `getStrategies` and `getStrategySubscriptions`. Require an owned strategy,
   its owner `input_value` and `input_multiplier`, and a strict `stock` or
   `cryptocurrency` type matching the planned asset class. Record the target
   source as `selected existing` only when it is compatible.
   If it is incompatible, preserve the strategy and offer a compatible owned
   target or a new target; also allow the user to reopen the affected strategy
   decisions. Never silently change the strategy or configured target.
2. If no ID is configured, use the verified token's `user_id` with
   `getUserStrategies`. Show safe distinguishing metadata without credentials
   and identify which owned strategies match the planned asset class. Ask the
   user to select a compatible strategy or explicitly create a new one. Never
   pick the first result or create a duplicate silently. Persist the user's
   selection by following the agent-only one-shot workflow in
   `credentials.md` with:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py \
     ALPHAINSIDER_STRATEGY_ID VALUE
   ```

   Replace `VALUE` with the selected ID as one safely quoted argument, then
   validate it as in step 1.
3. Before planning a new target, call `getAccountSubscription` and
   `getUserInfo`; stop if either eligibility check fails. Compare the owned
   strategy count with `limits.max_strategies` and stop creation at capacity,
   while still allowing selection of an existing strategy.
4. For a new target, use the plan's strict `stock` or `cryptocurrency` asset
   class, propose a concise name from the goal, and require the user to choose
   the owner starting balance. Public access is always eligible. Offer private
   access only when `getAccountSubscription.level > 0`. Offer paid access only
   when the type is `cryptocurrency` and `getUserInfo.verified` is true. If
   neither enhanced mode is eligible, record public access without an extra
   access question. Never offer paid stock creation because its special
   approval cannot be verified through the documented API.
5. For paid cryptocurrency access, require one launch price from $10 through
   $1000 and convert the user-visible dollars to AlphaInsider's integer-cent
   `price`. Creation maps public to `private: false, price: 0`, private to
   `private: true, price: 0`, and paid to `private: false` with that confirmed
   price. Strategy Creator never changes the price later.
6. While the plan is `draft`, show the exact type, name, starting balance,
   access, and price when applicable and record them without an ID. Do not ask
   for separate creation approval. Changing a core field before confirmation
   updates the draft; changing one after confirmation returns the plan to
   `draft` and requires complete plan reconfirmation. Do not call `newStrategy`
   before complete plan confirmation.
7. Generate the exact AlphaInsider description from the completed strategy
   design: one to three plain-language sentences covering the traded universe,
   signal and entry/exit behavior, cadence, and sizing or risk. Do not include
   performance claims, credentials, implementation paths, or unsupported
   promises. Normal confirmation of the active plan approves this exact
   description and the recorded core creation fields together. It is the sole
   authorization to call `newStrategy` and persist the returned strategy ID;
   do not ask again. Record that ID on the plan. A replacement plan's final
   confirmation also authorizes its exact recorded promotion actions under
   `interview.md` and `implementation.md`. If later work fails before
   `implemented`, retain the created target and saved ID and report how to
   resume. Never request another skill-level approval for that retain default.

## Target deferral

When permissions, eligibility, capacity, or compatible-target resolution
cannot complete in the current run, record target readiness as `local-only` and
record only a non-secret reason. Normalize every unavailable target field as
local-only rather than leaving a placeholder. Make no remote calls after
local-only readiness, but continue to plan confirmation.

A confirmed local-only plan authorizes a complete local build, including copied
AlphaInsider helpers, order mapping, documentation, backtests, and mocked
tests. It does not authorize provisioning, remote target validation,
synchronization, an order-submitting command, a native operation definition,
or an agent scheduled task. Mark operator commands unavailable, keep the plan
`confirmed`, and never set it to `implemented`.

When setup becomes possible, return the plan to `draft`, preserve unaffected
decisions and local artifacts, resolve only the target gaps, and reconfirm the
complete plan before any remote work. If target facts invalidate market,
execution, risk, cadence, or runner decisions, reopen only those affected
branches, rerun every dependent phase including Operation and scheduling when
needed, and return to target setup before confirmation.

## Confirmed provisioning

Run this section only for a confirmed plan whose target readiness is `ready`.
Before remote provisioning, reverify the API-key permission bundle.
For a new target, also recheck capacity and access eligibility, then call
`newStrategy` with only the confirmed type, name, owner `input_value`, access
mapping, price, and confirmed description. On success:

1. Capture the returned non-secret strategy ID, write it only to
   `ALPHAINSIDER_STRATEGY_ID` through the non-echoing helper, record it on the
   plan, and report it once so the user can recover the target if later local
   work fails.
2. Validate the created strategy and owner subscription context through the
   sibling request helper. Do not continue if its type, ownership, starting
   value, or multiplier is unusable.
3. If ID persistence, validation, or any later work fails before the plan is
   `implemented`, retain the created target and saved ID, report how to resume,
   and leave later cleanup of any verified owned target to the separately
   confirmed workflow in `cleanup.md`. Never request another skill-level
   approval for that retain default. Never remove a default that now refers to
   another strategy.

## Post-creation cleanup

For an explicit retirement or the outgoing side of a replacement, read and
follow `cleanup.md`. Stage the exact non-secret target ID and ownership
evidence on the active or replacement plan, offer retain-and-detach or
deletion for both Strategy Creator-created and selected existing owned
targets, and obtain the workflow's one final confirmation.

Immediately before deletion, reverify the API-key permission, token user,
exact target, and ownership. Use `getStrategies`, `getUserStrategies`,
`getStrategySubscriptions`, `getOrders`, and `getPositions` for read-only
metadata, owner-subscription context, subscriber, open-order, and nonzero-
position findings. Warn that the documented `deleteStrategy` operation does
not specify cascade behavior. The user may still confirm deletion; never cancel
orders, liquidate positions, or submit any trading action as cleanup.

Call `deleteStrategy` only with the plan's exact confirmed ID. Verify that it
no longer resolves before removing a matching configured default. Only after
deletion succeeds, and only when that comparison matched, remove the saved
default. For retention, make no deletion call and detach only an exact matching
binding. A replacement keeps its ready target binding. On failure, preserve the
confirmed plan and exact ID for an explicit retry; never retry during unrelated
work.

## Description synchronization

After offline tests and static checks, synchronize the confirmed remote
description for every selected existing target and for every subsequent
confirmed behavior change. Immediately before `updateStrategy`, re-fetch the
target metadata and owned subscription; send the current name and owner
`input_value` unchanged because the endpoint requires them, plus only the
confirmed description. Never use a stale plan value to overwrite either field.
If synchronization fails, leave the plan `confirmed`. Set `implemented` only
when code, tests, plan, docs, remote description, and every required operation
resource agree.

## Generated project documentation

The generated `README.md` API-key prerequisites must link to AlphaInsider
developer settings, tell the user they can select the **AI Agent** preset, list
the complete permission bundle above exactly, and explain that `verifyToken`
and stock REST lookups need no selectable permission. Identify
`deleteStrategy` as authorized only by a confirmed retirement or outgoing
replacement on the plan. Copy the permission list from this file at generation
time.

Generated `AGENTS.md` must point at the installed strategy-creator skill for
target, cleanup, and local-only rules. Keep only project-specific commands,
runner identity, and env names. Agents never change strategy price. Operational
commands must not prompt for confirmation before submitting planned paper
orders. A user-run command is the user's execution action; agents never
manually run a cycle, start a persistent process, or trigger a scheduled task
during build and verification.
