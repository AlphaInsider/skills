# AlphaInsider Target Setup

Use this reference after project preflight and before the strategy interview.
Never record a strategy ID in a plan, source file, test, README, or `AGENTS.md`.

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
included only so a user may separately approve cleanup of a strategy created
by a failed current run; it never authorizes routine or automatic deletion.

After the key is available, use the sibling request helper to call
`POST /verifyToken`. Read only the returned `user_id` and `scope`; never expose
the token. Compare `scope` with the complete bundle above. If any permission is
missing, list only the missing permission names, instruct the user to create or
replace the key, and pause all interview, remote creation, and implementation
work until the replacement key passes the same check. Accept extra permissions
without treating them as Strategy Creator requirements.

## Resolve the target

Run this flow only after the API key passes the permission gate.

1. If the helper resolves a configured strategy ID, validate it with
   `getStrategies` and `getStrategySubscriptions`. Require an owned strategy,
   its owner `input_value` and `input_multiplier`, and a strict `stock` or
   `cryptocurrency` type. Record the target source as `selected existing`.
2. If no ID is configured, use the verified token's `user_id` with
   `getUserStrategies`. Show safe distinguishing metadata without credentials
   and ask the user to select an owned strategy or explicitly create a new one.
   Never pick the first result or create a duplicate silently. Persist an
   approved selection with:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py \
     ALPHAINSIDER_STRATEGY_ID
   ```

   Then validate it as in step 1.
3. Before planning a new target, call `getAccountSubscription` and
   `getUserInfo`; stop if either eligibility check fails. Compare the owned
   strategy count with `limits.max_strategies` and stop creation at capacity,
   while still allowing selection of an existing strategy.
4. For a new target, resolve `stock` or `cryptocurrency`, propose a concise
   name from the goal, and require the user to choose the owner starting
   balance. Public access is always eligible. Offer private access only when
   `getAccountSubscription.level > 0`. Offer paid access only when the type is
   `cryptocurrency` and `getUserInfo.verified` is true. If neither enhanced
   mode is eligible, record public access without an extra access question.
   Never offer paid stock creation because its special approval cannot be
   verified through the documented API.
5. For paid cryptocurrency access, require one launch price from $10 through
   $1000 and convert the user-visible dollars to AlphaInsider's integer-cent
   `price`. Creation maps public to `private: false, price: 0`, private to
   `private: true, price: 0`, and paid to `private: false` with that approved
   price. Strategy Creator never changes the price later.
6. While the plan is `draft`, show the exact type, name, starting balance,
   access, and price when applicable. Obtain explicit core creation approval
   and record it without an ID. Changing any core field invalidates that
   approval. Do not call `newStrategy` before complete plan confirmation.
7. Generate the exact AlphaInsider description from the complete plan: one to
   three plain-language sentences covering the traded universe, signal and
   entry/exit behavior, cadence, and sizing or risk. Do not include performance
   claims, credentials, implementation paths, or unsupported promises. Plan
   confirmation approves this exact description separately from the earlier
   core creation fields.

## Confirmed provisioning

Before writing implementation files, reverify the API-key permission bundle.
For a new target, also recheck capacity and access eligibility, then call
`newStrategy` with only the approved type, name, owner `input_value`, access
mapping, price, and confirmed description. On success:

1. Capture the returned non-secret strategy ID, write it only to
   `ALPHAINSIDER_STRATEGY_ID` through the non-echoing helper, and report it once
   so the user can recover the target if later local work fails.
2. Validate the created strategy and owner subscription context through the
   sibling request helper. Do not continue if its type, ownership, starting
   value, or multiplier is unusable.
3. If ID persistence, validation, or any later work fails before the plan is
   `implemented`, report the failure and ask whether to delete this exact
   strategy. Never infer deletion approval, never offer deletion for a selected
   existing strategy, and never delete another strategy.

## Failed-creation cleanup

If the user approves cleanup, call `deleteStrategy` with the exact created ID.
Before deletion, confirm through the sibling helper that the configured default
still refers to that exact created ID. Only after deletion succeeds, and only
when that comparison matched, remove the saved default with:

```bash
python /absolute/path/to/strategy-creator/scripts/set_env_value.py \
  --remove ALPHAINSIDER_STRATEGY_ID
```

Never remove a default that now refers to another strategy. If deletion fails,
retain the ID and report the recoverable state. If the user declines, retain
the created strategy and resume it on the next run.

## Description synchronization

After offline tests and static checks, synchronize the confirmed remote
description for every selected existing target and for every subsequent
confirmed behavior change. Immediately before `updateStrategy`, re-fetch the
target metadata and owned subscription; send the current name and owner
`input_value` unchanged because the endpoint requires them, plus only the
confirmed description. Never use a stale plan value to overwrite either field.
If synchronization fails, leave the plan `confirmed`. Set `implemented` only
when code, tests, plan, docs, and remote description agree.

## Generated project documentation

The generated `README.md` API-key prerequisites must link to AlphaInsider
developer settings, list the complete permission bundle above exactly, explain
that `verifyToken` and stock REST lookups need no selectable permission, and
identify `deleteStrategy` as approval-gated failed-creation cleanup only.

The generated `AGENTS.md` must preserve these target rules. In particular,
agents never change strategy price and never delete a remote strategy except
through the exact failed-creation approval gate above.
