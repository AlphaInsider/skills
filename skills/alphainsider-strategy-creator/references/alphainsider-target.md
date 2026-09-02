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
and permissions without showing the key. Require only permissions used by the
recorded setup and runtime plan. Recommend the **AI Agent** preset because it
supports later plan changes. Accept a sufficient narrower or broader key.

If required access is missing, list the missing permission names and give one
clear setup action. Preserve all earlier work. Do not make a remote mutation or
activate automation until the check passes.

## Choose a target

After token verification, call `getUserStrategies` with the verified user ID.
Show compatible owned strategies, including public, private, and paid
strategies when eligible. Display only useful public facts such as name, type,
access mode, public strategy ID, creation time, and whether it is already bound
to this project.

Ask the user to choose:

1. **Create a new strategy** — recommended for a new project because it keeps
   history and behavior separate.
2. A compatible owned strategy.

If many targets exist, first ask new versus existing, then present a short
searchable or paginated existing-target list. Never choose the first result.
Never bind a target whose type differs from the plan. A cryptocurrency target
cannot run a stock plan, and a stock target cannot run a cryptocurrency plan.

For an existing target:

- verify exact ownership, type, current strategy details, and owner
  `input_multiplier`;
- preserve all existing performance and trade history;
- do not reset, repurpose, rename, or change core settings unless the user
  separately adds that change to the plan; and
- persist the selected public ID through the safe configuration workflow.

## Plan a new target

Check current account eligibility and target limits. Ask only fields that the
API and current account permit:

- a concise strategy name;
- paper starting balance;
- public, private, or paid access when eligible; and
- the paid launch price when an eligible paid cryptocurrency strategy is
  selected.

Explain that the starting balance sets the paper strategy's display and sizing
scale. It is not real money, broker cash, a deposit, or the user's account
balance. Recommend `$100,000` when that value is within current platform
limits and no strategy-specific amount fits better.

Explain maximum leverage separately in the strategy interview. AlphaInsider
supports up to `2×`. Recommend `1×` unless the agreed strategy supports a
different maximum. Never treat the maximum as a target exposure.

Validate current public, private, and paid eligibility from the API and current
product rules. Never offer a mode that the account or strategy type cannot use.
Do not change a paid price after creation unless the user explicitly starts a
separate supported update.

Generate a concise remote description from `plan.md`. Include the universe,
decision approach, entry and exit behavior, cadence, and important sizing or
risk rules. Do not include performance promises, implementation paths,
credentials, or unsupported claims.

Record all fields and the exact `newStrategy` action before final agreement.
Do not ask for another creation approval after the user agrees to that complete
implementation plan.

## Provision after offline verification

Immediately before creation, recheck the key, account limit, eligibility, and
planned fields. Call `newStrategy` only after code, docs, static checks, and
mocked tests pass. Never run an order-capable cycle as a creation test.

After creation:

1. capture the returned public strategy ID;
2. store it through the safe configuration workflow;
3. record it in `plan.md`;
4. validate ownership, strict type, paper starting balance, and owner
   multiplier; and
5. verify the current public web route and record a working strategy URL.

For an existing target, revalidate the exact target and binding at the same
point.

Synchronize the generated description when the selected target does not
already have the agreed text. Preserve API-required current fields when an
update operation needs them. If description sync or later scheduling fails,
retain the target and saved ID. Report the exact next step; do not create a
duplicate on resumption.

Target creation, description updates, and deletion are setup mutations. They
never authorize orders. Orders are allowed only through an active agreed
normal-run contract.
