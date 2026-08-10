# AlphaInsider Target Setup

Use this reference after strategy design and background-operation planning and
before backtesting as the AlphaInsider forward-test setup phase.
Never record a strategy ID in a plan, source file, test, README, or `AGENTS.md`.

## Contents

- [API-key permission gate](#api-key-permission-gate)
- [Resolve the target](#resolve-the-target)
- [Target deferral](#target-deferral)
- [Confirmed provisioning](#confirmed-provisioning)
- [Failed-creation cleanup](#failed-creation-cleanup)
- [Description synchronization](#description-synchronization)
- [Generated project documentation](#generated-project-documentation)

## API-key permission gate

Before asking the user to set `ALPHAINSIDER_API_KEY`, link to
[AlphaInsider developer settings](https://alphainsider.com/settings/developers)
and instruct them to create one key with every permission below:

```text
getUserInfo
getStrategies
getStrategyValues
getUserStrategies
getStrategyPerformance
newStrategy
updateStrategy
deleteStrategy
getStrategySubscriptions
getAccountSubscription
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
```

Explain that `verifyToken` has no selectable permission and that AlphaInsider's
stock REST lookup endpoints require no API-key permission. `deleteStrategy` is
included only for the confirmed cleanup policy of a strategy created by a
failed current run; it never authorizes routine deletion or deletion of a
selected existing strategy.

After the key is available, use the sibling request helper to call
`POST /verifyToken`. Read only the returned `user_id` and `scope`; never expose
the token. Compare `scope` with the complete bundle above. If any permission is
missing, list only the missing permission names, instruct the user to create or
replace the key, and pause AlphaInsider target setup and every remote action.
Record the target as deferred if the key cannot be corrected in the current
run; backtesting planning may continue. Accept extra permissions without
treating them as Strategy Creator requirements.

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
7. Ask whether a strategy created by this run should be deleted or retained if
   later work fails before `implemented`. Explain that deletion applies only to
   that exact newly created strategy and removes the saved default only when it
   still matches. Record the cleanup policy in the draft; final complete-plan
   confirmation authorizes that conditional action without a failure-time
   approval prompt.
8. Generate the exact AlphaInsider description from the completed strategy
   design: one to three plain-language sentences covering the traded universe,
   signal and entry/exit behavior, cadence, and sizing or risk. Do not include
   performance claims, credentials, implementation paths, or unsupported
   promises. Normal confirmation of the active plan approves this exact
   description and the recorded core creation fields together. It is the sole
   authorization to call `newStrategy` and persist the returned strategy ID;
   do not ask again. A replacement plan's final confirmation also authorizes
   its exact recorded promotion actions under `interview.md` and
   `implementation.md`.

## Target deferral

When permissions, eligibility, capacity, or compatible-target resolution
cannot complete in the current run, record target readiness as `deferred` and
record only a non-secret reason. Normalize every unavailable target field as
deferred rather than leaving a placeholder. Make no remote calls after
deferral, but continue through backtesting and plan confirmation.

A confirmed deferred plan authorizes a complete local build, including copied
AlphaInsider helpers, order mapping, documentation, backtests, and mocked
tests. It does not authorize provisioning, remote target validation,
synchronization, or an order-submitting command. Mark those operator commands
unavailable, install no background definition, keep the plan `confirmed`, and
never set it to `implemented`.

When setup becomes possible, return the plan to `draft`, preserve unaffected
decisions and local artifacts, resolve only the target gaps, and reconfirm the
complete plan before any remote work. If target facts invalidate market,
execution, or risk decisions, reopen those affected branches and their
downstream decisions as well.

## Confirmed provisioning

Run this section only for a confirmed plan whose target readiness is `ready`.
Before remote provisioning, reverify the API-key permission bundle.
For a new target, also recheck capacity and access eligibility, then call
`newStrategy` with only the confirmed type, name, owner `input_value`, access
mapping, price, and confirmed description. On success:

1. Capture the returned non-secret strategy ID, write it only to
   `ALPHAINSIDER_STRATEGY_ID` through the non-echoing helper, and report it once
   so the user can recover the target if later local work fails.
2. Validate the created strategy and owner subscription context through the
   sibling request helper. Do not continue if its type, ownership, starting
   value, or multiplier is unusable.
3. If ID persistence, validation, or any later work fails before the plan is
   `implemented`, report the failure and immediately apply the confirmed
   failed-current-run cleanup policy. Never delete a selected existing strategy
   or another strategy.

## Failed-creation cleanup

When the confirmed policy is `delete`, call `deleteStrategy` with the exact
created ID. Before deletion, confirm through the sibling helper that the
configured default still refers to that exact created ID. If it does not,
retain the strategy and report the mismatch. Only after deletion succeeds, and
only when that comparison matched, remove the saved default with:

```bash
python /absolute/path/to/strategy-creator/scripts/set_env_value.py \
  --remove ALPHAINSIDER_STRATEGY_ID
```

Run this as the agent-only helper; removal receives no value argument.

Never remove a default that now refers to another strategy. If deletion fails,
retain the ID and report the recoverable state. When the confirmed policy is
`retain`, keep the created strategy and saved ID and report how to resume it on
the next run. Never request another skill-level approval for either confirmed
policy.

## Description synchronization

After offline tests and static checks, synchronize the confirmed remote
description for every selected existing target and for every subsequent
confirmed behavior change. Immediately before `updateStrategy`, re-fetch the
target metadata and owned subscription; send the current name and owner
`input_value` unchanged because the endpoint requires them, plus only the
confirmed description. Never use a stale plan value to overwrite either field.
If synchronization fails, leave the plan `confirmed`. Set `implemented` only
when code, tests, plan, docs, remote description, and any required background
installation agree.

## Generated project documentation

The generated `README.md` API-key prerequisites must link to AlphaInsider
developer settings, list the complete permission bundle above exactly, explain
that `verifyToken` and stock REST lookups need no selectable permission, and
identify `deleteStrategy` as final-plan-authorized failed-current-run cleanup
only and state the confirmed retain-or-delete policy.

The generated `AGENTS.md` must preserve these target rules. In particular,
agents never change strategy price, never delete a remote strategy except
through the exact confirmed cleanup policy above, make no remote call for
a deferred target, and return a deferred plan to `draft` for target completion
and full reconfirmation. The one-cycle and continuous commands must not prompt
for confirmation before submitting planned paper orders. Running either
command is the user's execution action; agents never start either command
automatically or during build and verification.
