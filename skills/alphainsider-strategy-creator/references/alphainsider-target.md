# AlphaInsider Target

Read this file after the user chooses AlphaInsider forward testing and the API
key is available. Target discovery happens before final implementation
agreement. Creation happens only after the agreed implementation passes every
offline, order-free check.

Read the installed `alphainsider-api` skill for current endpoint behavior. If
it is unavailable, read the live AlphaInsider documentation index and relevant
OpenAPI sections. Do not copy a fixed API catalog into the project.

## Verify access

Use the setup wrapper from `credentials.md`. Verify the token type, user ID,
and permissions needed for read-only account and target discovery without
showing the key. Do not require permissions for setup or runtime operations
that are not known yet. Recommend the **AI Agent** preset because it supports
later plan changes. Accept a sufficient narrower or broader key.

If required access is missing, list the missing permission names and give one
clear setup action. Preserve all earlier work. Do not make a remote mutation or
activate automation until the check passes.

## Choose a target

After token verification, call `getUserStrategies` with the verified user ID.
Verify ownership and show only targets whose type matches `plan.md`. For each
one, display a concise set of useful facts: name, type, public or private state,
price when relevant, public strategy ID, creation time, current owner starting
scale when safely available, whether it has prior history or subscribers, and
whether it is already bound to this project. Do not show a complete API
response.

In one target-choice round, ask the user to choose:

1. **Create a new strategy** — recommended for a new project because it keeps
   history and behavior separate.
2. A compatible owned strategy.

If many targets exist, show the new-target option with a short searchable or
paginated existing-target list. Keep the choice open until the user selects an
exact target. Never choose the first result.
Do not ask a new-target name, scale, or access question until the user chooses
the new-target branch.
Never bind a target whose type differs from the plan. A cryptocurrency target
cannot run a stock plan, and a stock target cannot run a cryptocurrency plan.

For an existing target:

- verify exact ownership, type, current strategy details, and owner
  `input_multiplier`;
- show its apparent purpose and disclose that its prior results and subscribers
  remain attached;
- recommend a new target when its apparent purpose or history differs from the
  new plan, and record the user's explicit reuse confirmation before binding;
- preserve all existing performance and trade history;
- always preserve its public or private state and price in this reuse flow;
  preserve its name, starting scale, and description unless the user separately
  agrees to a supported change; and
- persist the selected public ID through the safe configuration workflow.

## Plan a new target

Check current account eligibility and target limits. Inherit the strict
`stock` or `cryptocurrency` type from the agreed plan; do not ask it again.

Ask these available decisions together:

- a concise strategy name, with a plan-derived name recommended;
- paper starting balance, with `$100,000` recommended when supported; and
- public or private access, with public recommended.

Before that recommendation, verify current product rules and briefly explain
the material visibility and access difference. State what other people can
discover, view, or use for each choice and what strategy information or results
become visible. Do not invent details that current documentation or the API
does not confirm. Recommend public for users who want its confirmed sharing or
discovery benefits; explain that private limits exposure under those same
rules.

Explain that the starting balance sets the paper strategy's display and sizing
scale. It is not real money, broker cash, a deposit, or the user's account
balance. An existing target keeps its current starting scale.

Always ask public or private and include the selected boolean explicitly in the
creation request. The API documents no default, and its current strategy update
operation does not accept this field. Never infer access from an API example or
silently apply the recommendation.

Price is separate from the public or private field. Offer paid behavior and ask
its launch price only when current account and product rules independently
confirm eligibility, supported combinations, units, and limits. Do not present
public, private, and paid as one fixed three-choice API field.

Explain maximum leverage separately in the strategy interview. AlphaInsider
supports up to `2×`. Recommend `1×` unless the agreed strategy supports a
different maximum. Never treat the maximum as a target exposure.

Generate a concise remote description from `plan.md`. Include the universe,
decision approach, entry and exit behavior, cadence, and important sizing or
risk rules. Do not include performance promises, implementation paths,
credentials, or unsupported claims. Show the generated text in the final
implementation agreement and let the user revise it; do not require a separate
description-writing question when it is accurate.

Record target choice, name, starting scale, public or private state, conditional
paid price, description, and the exact `newStrategy` action as separate plan
fields before final agreement. Do not create while an applicable field is
unresolved. The setup helper must reject a `newStrategy` body that omits type,
name, starting value, or the explicit public/private boolean. Do not ask for
another creation approval after the user agrees to the complete implementation
plan.

## Provision after offline verification

Immediately before creation, recheck the key, final setup permissions, account
limit, eligibility, and complete planned fields. Compare every applicable
creation-request field with the separate Agreed `plan.md` target fields,
including the selected public/private boolean and conditional paid price. The
setup helper checks request completeness and basic types; it does not prove
plan conformance. Stop on any mismatch. Call `newStrategy` only after code,
docs, static checks, and mocked tests pass. Never run an order-capable cycle as
a creation test.

Save the pre-call owned-target inventory. If `newStrategy` has an ambiguous
outcome, do not retry it. Refresh owned targets and compare the inventory and
all agreed creation fields. Bind the result only when exactly one new owned
match is proven. Otherwise, stop with an ambiguous error and the exact next
step. Never blindly create a replacement.

After creation:

1. capture the returned public strategy ID;
2. store it through the safe configuration workflow;
3. record it in `plan.md`;
4. validate ownership, strict type, paper starting balance, public or private
   state, conditional price, and owner multiplier; and
5. verify the current public web route and record a working strategy URL.

For an existing target, revalidate the exact target and binding at the same
point.

For a new target, synchronize the generated description when creation does not
produce the agreed text. For an existing target, update its description only
when that specific change was shown and agreed. Preserve API-required current
fields when an update operation needs them. If description sync or later
scheduling fails, retain the target and saved ID. Report the exact next step;
do not create a duplicate on resumption.

Target creation, description updates, and deletion are setup mutations. They
never authorize orders. Orders are allowed only through an active agreed
normal-run contract.
