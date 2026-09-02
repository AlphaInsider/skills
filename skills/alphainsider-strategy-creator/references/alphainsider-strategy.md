# AlphaInsider Strategy

This file owns AlphaInsider strategy discovery, selection, settings, use, and
creation. Read it after `credentials.md` verifies API access. Discovery happens
before the final AlphaInsider setup agreement. Creation happens only after the
agreed implementation passes every offline, order-free check.

Read the installed `alphainsider-api` skill for current endpoint behavior. If
it is unavailable, read the live AlphaInsider documentation index and relevant
OpenAPI sections. Do not copy a fixed API catalog into the project.

## Choose an AlphaInsider strategy

Use the safe setup wrapper defined in `credentials.md`. Call
`getUserStrategies` with the verified user ID. Verify ownership and show only
strategies whose type matches `plan.md`. For each one, display a concise set of
useful facts: name, type, public or private state, price when relevant,
AlphaInsider strategy ID, creation time, current simulated starting value,
whether it has prior history or subscribers, and whether this project already
uses it. Do not show a complete API response.

In one choice round, ask the user to choose:

1. **Create a new AlphaInsider strategy** — recommended for a new project
   because it keeps history and behavior separate.
2. A compatible owned AlphaInsider strategy.

If many strategies exist, show the create-new option with a short searchable or
paginated list. Keep the choice open until the user selects an exact strategy.
Never choose the first result. Do not ask for a new strategy's name, simulated
starting value, or access setting until the user chooses to create one.

Never use an AlphaInsider strategy whose type differs from the plan. A
cryptocurrency strategy cannot run a stock plan, and a stock strategy cannot
run a cryptocurrency plan.

For an existing AlphaInsider strategy:

- verify exact ownership, type, current strategy details, and owner
  `input_multiplier`;
- show its apparent purpose and disclose that its prior results and subscribers
  remain attached;
- recommend a new strategy when its apparent purpose or history differs from
  the new plan, and record the user's explicit reuse confirmation before use;
- preserve all existing performance and trade history;
- always preserve its public or private state and price in this reuse flow;
  preserve its name, simulated starting value, and description unless the user
  separately agrees to a supported change; and
- persist the selected AlphaInsider strategy ID through the safe configuration
  workflow.

## Plan a new AlphaInsider strategy

Check current account eligibility and strategy limits. Inherit the strict
`stock` or `cryptocurrency` type from the agreed plan; do not ask it again.

Ask these available decisions together:

- a concise strategy name, with a plan-derived name recommended;
- a simulated starting value, with `$100,000` recommended when supported; and
- public or private access, with public recommended.

Before that recommendation, verify current product rules and briefly explain
the important visibility and access difference. State what other people can
discover, view, or use for each choice and what strategy information or results
become visible. Do not invent details that current documentation or the API
does not confirm. Recommend public for users who want its confirmed sharing or
discovery benefits; explain that private limits who can access it under those
same rules.

Explain that the simulated starting value sets the strategy's displayed value
and order-size scale. It is not real money, broker cash, a deposit, or the
user's account balance. An existing strategy keeps its current value.

Always ask public or private and include the selected boolean explicitly in the
creation request. The API documents no default, and its current strategy update
operation does not accept this field. Never infer access from an API example or
silently apply the recommendation.

Price is separate from the public or private field. Offer paid access and ask
its access price only when current account and product rules independently
confirm eligibility, supported combinations, units, and limits. Do not present
public, private, and paid as one fixed three-choice API field.

Generate a concise AlphaInsider description from `plan.md`. Include the
assets the strategy can trade, how decisions are made, entry and exit behavior,
schedule, and important sizing or risk rules. Do not include performance
promises, implementation paths, credentials, or unsupported claims. Show the
generated text in the final AlphaInsider setup agreement and let the user
revise it; do not require a separate description-writing question when it is
accurate.

Record the AlphaInsider strategy choice, name, simulated starting value, public
or private state, conditional access price, description, and exact
`newStrategy` action as separate plan fields before final agreement. Do not
create while an applicable field is unresolved. The setup helper must reject a
`newStrategy` body that omits type, name, starting value, or the explicit
public/private boolean. Do not ask for another creation approval after the user
agrees to the complete AlphaInsider setup.

## Create or use after offline verification

Immediately before creation, recheck the key, final setup permissions, account
limit, eligibility, and complete planned fields. Compare every applicable
creation-request field with the separate Agreed `plan.md` AlphaInsider
strategy fields, including the selected public/private boolean and conditional
access price. The setup helper checks request completeness and basic types; it
does not prove that the request follows the plan. Stop on any mismatch. Call
`newStrategy` only after code, docs, static checks, and mocked tests pass. Never
run an order-capable strategy run as a creation test.

Save the pre-call owned-strategy inventory. If `newStrategy` has an ambiguous
outcome, do not retry it. Refresh owned strategies and compare the inventory
and all agreed creation fields. Use the result only when exactly one new owned
match is proven. Otherwise, stop with an ambiguous error and the exact next
step. Never blindly create a replacement.

After creation:

1. capture the returned AlphaInsider strategy ID;
2. store it through the safe configuration workflow;
3. record it in `plan.md`;
4. validate ownership, stock or cryptocurrency type, simulated starting value,
   public or private state, conditional access price, and owner multiplier; and
5. verify and record a working AlphaInsider strategy URL.

For an existing AlphaInsider strategy, revalidate the exact choice and project
configuration at the same point.

For a new AlphaInsider strategy, synchronize the generated description when
creation does not produce the agreed text. For an existing strategy, update its
description only when that specific change was shown and agreed. Preserve
API-required current fields when an update operation needs them. If description
sync or later scheduling fails, retain the strategy and saved AlphaInsider
strategy ID. Report the exact next step; do not create a duplicate on
resumption.

AlphaInsider strategy creation, description updates, and deletion never
authorize orders. AlphaInsider paper orders are allowed only through an active,
agreed strategy-run process.
