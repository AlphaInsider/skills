# Implement and Activate

Enter this workflow after the user skips backtesting or chooses implementation
from reviewed results. It owns protected configuration, AlphaInsider paper
strategy selection and creation, implementation planning and build, native
automation setup, offline verification, and creation completion. Runtime
execution and recovery live in [run and recover](run-and-recover.md).

## 1. Enter implementation planning

1. Require Strategy status Confirmed.
2. Set Phase Planning implementation and AlphaInsider setup status Draft.
3. Read the confirmed strategy, all backtest disclosures, existing project
   files, and current user changes.
4. Recheck the native scheduler surface, confirmed timing, project access, and
   safe non-prompt secret options before requesting an API key or asking setup
   questions.
5. If platform or AlphaInsider drift changes confirmed timing, return only that
   decision to [define strategy](define-strategy.md). Preserve every unaffected
   answer and later show a revised setup summary.

Do not select new timing during implementation. Newly compatible hours never
silently expand a confirmed schedule.

## 2. Establish protected configuration

This subflow owns secret-storage selection, credential collection, private
verification, and safe setup requests. Never inspect, print, or summarize an
existing API key, complete `.env`, process environment, hosted secret store,
notification token, webhook URL, or private destination.

Never place a secret in a scheduler instruction, plan, source file, example,
test, log, notification, task prompt, or metadata.

Require both installed helpers:

- `scripts/set_env_value.py`
- `scripts/alphainsider_setup_request.py`

If either helper is missing, stop only this phase and instruct the user to
reinstall Strategy Creator. Do not improvise another secret writer or
AlphaInsider setup-request path.

### 2.1 Select secret storage

1. Inspect whether current and future scheduled agents can load project `.env`
   without prompting.
2. If they can, select project `.env`.
3. Otherwise, select the platform's secure secret facility only when scheduled
   runs can access it safely.
4. If neither works, do not request a key. Record a technical blocker and give
   the exact platform action needed to enable safe access.

This is a read-only implementation preflight, not an interview question.

Use the same protected facility for notification credentials and private
destinations. `ALPHAINSIDER_STRATEGY_ID` is public, but store it through the
same helper or hosted configuration facility for consistent runtime access.
Project documents record only configuration names and safe labels.

For a resumed project, privately verify an already configured key with the
setup helper. Never request it again when verification succeeds. If it is
missing, inaccessible, invalid, or insufficient, make key entry the first
user-facing implementation action and do not ask setup questions first.

Waiting for a requested key is ordinary implementation work. Keep Creation
state In progress and record the action under Waiting for. Use Blocked only
when safe storage or access cannot function until a technical problem is
remediated.

### 2.2 Collect a missing API key

Do not request `ALPHAINSIDER_API_KEY` before storage is selected. Link to
[AlphaInsider developer settings](https://alphainsider.com/settings/developers).
Recommend the **AI Agent** permission preset because later confirmed strategy
changes can require additional functions. A narrower key is initially
acceptable when it supports token verification and required read-only
discovery.

For project `.env`, use one standalone action without setup questions:

```markdown
👉 **Action — Add AlphaInsider API key:** Paste the API key in this chat.

Pasting gives this active chat and agent access so the key can be stored
without displaying it.

↪️ **Alternative:** Add `ALPHAINSIDER_API_KEY` directly to the announced
project `.env`, then reply `ready`.
```

Request only missing names. Accept a bare value when exactly one name is
pending, or clear `NAME=value` entries for several names. Ask one focused
clarification when mapping is unclear. Never echo, restate, log, or summarize a
value.

Pasted values authorize updates only to the requested names. Invoke:

```text
python /absolute/skill/path/scripts/set_env_value.py --project-root /absolute/project NAME
```

Supply the value through protected standard input or the helper's non-echoing
prompt. Never put it in a command argument, shell variable, environment
assignment, pipeline, redirect, heredoc, temporary file, patch, or another
write path. Do not show the helper command to the user. When protected input is
unavailable, use direct user editing or supported hosted secret storage.

The helper must:

- require the exact project root with a root `plan.md`;
- reject installed-skill directories and symbolic-link `.env` files;
- preserve unrelated entries atomically;
- enforce owner-only `0600` permissions; and
- reveal only the updated variable name and resolved file path.

Never open `.env` before or after a write and never reproduce the helper's
write logic. Do not import either CLI-only helper.

### 2.3 Verify API access privately

1. Use `scripts/alphainsider_setup_request.py` with the exact
   `--project-root`.
2. At the initial gate, verify `GET /verifyToken`, token user identity, and only
   permissions needed for read-only account and strategy discovery.
3. Resolve insufficient discovery access before strategy discovery.
4. Verify current account tier and applicable account-specific limits after
   access succeeds.
5. If the account cannot support a recorded higher-tier timing dependency,
   return that timing to Define instead of inventing a workaround.
6. After strategy and implementation design are settled, derive exact setup
   and runtime operations, record their required permissions in `plan.md`, and
   reverify the key.
7. List only missing permission names. Accept sufficient extra permissions
   without requiring replacement or rotation.

Use request bodies through protected standard input when they contain a
private value. The helper may load the key privately from process injection or
project `.env` and may print only the non-secret
`ALPHAINSIDER_STRATEGY_ID` configuration value. Report only redacted results.
Use it only for operations in its fixed setup allowlist. Never use it for an
order, allocation, cancellation, webhook trade, or another trading action.

Deliberate chat entry alone is not a reason to rotate a key. If a replacement
value is no longer available to the active chat, request it again or use direct
editing; never recover it by reading `.env`. For a user-managed hosted secret
facility, give exact platform steps and wait for the completion signal when the
agent cannot write safely.

## 3. Select an AlphaInsider paper strategy

Complete discovery after initial read access and before the AlphaInsider setup
summary. Actual creation or final reuse validation occurs only after every
offline order-free check passes.

### 3.1 Discover compatible owned strategies

1. Use the safe setup wrapper to call `getUserStrategies` for the verified user
   ID.
2. Verify ownership and filter to the strict strategy type in `plan.md`.
3. Show **Create a new AlphaInsider strategy** first and recommend it for a new
   project because it separates history and behavior.
4. Show each compatible owned strategy with only useful facts: name, type,
   public or private state, relevant price, public strategy ID, creation time,
   current simulated starting value, prior history or subscribers, and whether
   this project already uses it.
5. In one choice round, ask the user to select one exact option. For many
   results, use a short
   searchable or paginated list.

Never display a complete API response, select the first result automatically,
or use a strategy whose type differs from the plan. Do not ask for a new
strategy's settings until the user chooses creation.

### 3.2 Resolve the selected path

#### Reuse an owned strategy

1. Verify exact ownership, strict type, current details, and owner
   `input_multiplier` without assuming a missing value is `1`.
2. Explain the apparent purpose and disclose that prior results and subscribers
   remain attached.
3. Recommend a new strategy when prior purpose or history differs from the
   confirmed plan.
4. Record explicit reuse confirmation before use when purpose or history
   differs.
5. Persist the selected public strategy ID through the protected configuration
   workflow.

Preserve all existing performance and trade history. In this reuse flow,
always preserve public/private state and price. Preserve name, simulated
starting value, and description unless a separately displayed supported change
is confirmed.

#### Create a new paper strategy

1. Recheck current account eligibility, product rules, and strategy limits.
2. Inherit the strict stock or cryptocurrency type from the confirmed plan; do
   not ask it again.
3. Ask these available decisions together:

   - concise name, recommending a plan-derived name;
   - simulated starting value, recommending `$100,000` when supported; and
   - public or private access, recommending public when its confirmed sharing
     or discovery benefits match the user's goal.

4. Before recommending access, explain only visibility and use differences
   verified by current product rules or the API. State what other people can
   discover, view, or use and what strategy information or results become
   visible. Explain that private limits access under those same rules.
5. Explain that simulated starting value controls displayed strategy value and
   order-size scale. It is not real money, broker cash, a deposit, or an account
   balance. An existing strategy retains its current value.
6. Generate a concise description from the confirmed plan: assets, decision
   method, entry and exit behavior, schedule, and important sizing or risk
   rules. Show it in the setup summary and let the user revise it.

Always ask public or private and include the selected boolean explicitly in
`newStrategy`; the API documents no default and the current update operation
does not accept this field. Never infer it from an example or silently apply a
recommendation.

Price is separate from public/private state. Offer paid access and ask price
only when current account and product rules independently confirm eligibility,
supported combinations, units, and limits. Do not present public, private, and
paid as one fixed three-choice field.

Do not include performance promises, implementation paths, credentials, or
unsupported claims in the description. Do not require a separate description
question when generated text is accurate.

Record choice, type, name, starting value, public/private state, conditional
price, description, and exact `newStrategy` action as separate plan fields.
Leave no applicable field unresolved before review. The setup helper must
reject a `newStrategy` body that omits type, name, `input_value`, or explicit
`private` boolean. Its completeness and basic-type checks do not prove that a
request follows the Authorized plan.

## 4. Design implementation and native automation

1. Map the confirmed decision mode to the smallest project-specific source,
   state, documentation, runbook, and tests.
2. Derive exact setup and runtime API permissions.
3. Recheck scheduler capabilities, durable project access, secrets, and
   controls.
4. Configure self-healing and notifications in dependency order.
5. Compare final data, decision, sizing, and execution behavior with every
   backtest disclosure.

Default to Python when no ecosystem requirement favors another language. Add
only needed dependencies and keep paths project-relative.

### 4.1 Map the decision mode

- **Code-led:** implement deterministic rules in code. Scheduled AI invokes one
  run, evaluates its structured result, and applies runtime policy.
- **Agent-led:** scheduled AI obtains confirmed inputs, makes the bounded
  decision, applies risk checks, and uses project helpers for state and
  AlphaInsider actions. Require a separate model key only for a confirmed
  external model service.
- **Hybrid:** programs gather or calculate inputs and enforce mechanical
  limits; scheduled AI makes only judgments assigned in `plan.md`.

For agent-led and hybrid designs, generated instructions must define allowed
evidence, decision space, output shape, uncertainty behavior, hard risk limits,
and prohibited changes. Keep prompts and rubrics aligned with the confirmed
plan.

### 4.2 Recheck the native scheduler

Inspect:

- create, inspect, edit, pause, resume, **Run now**, status, and delete support;
- project, exact code revision, saved-state, and shared-lock access;
- non-prompt secret and network access; and
- whether the agent or only the user can operate each control.

Use native user-interface instructions when a required control is not available
as an agent tool. Do not activate unless create, pause, resume, status, and
removal controls exist, even when some are user-operated. Otherwise preserve
the implementation and record one exact blocker and action.

Derive a unique stable task name from the project name. Check collisions
without opening secret stores or arbitrary run output. Never overwrite an
unrelated task.

### 4.3 Configure self-healing

1. Ask whether self-healing is enabled and recommend enabled.
2. If enabled, show the proposed implementation-only repair scope, protected
   files and state, snapshot and rollback behavior, and time limit.
3. Ask explicitly whether notification-channel repair is included. It remains
   disabled unless self-healing and that scope are both confirmed.

Never put strategy behavior, credentials, AlphaInsider strategy identity,
scheduler identity or frequency, saved trading history, the shared lock,
protected tests, or repair evidence inside automatic repair scope. Detailed
runtime limits live in [run and recover](run-and-recover.md).

### 4.4 Configure notifications

1. Discover native or already authorized channels using only non-sending
   capability and configuration checks. Never send a setup or test message.
2. Ask enabled or disabled and recommend enabled.
3. If enabled, ask the next available decisions together:

   - **Errors only** — recommended; sends the first Retrying or Action Required
     event and material changes while repairs and warnings remain in history.
   - **Errors and completed repairs**.
   - **Errors, completed repairs, and warnings**.
   - Which supported channels to use, recommending the simplest native in-app
     channel first.

4. Request a destination only when the selected channel needs one and store it
   through protected configuration.
5. Record each channel as **supported** when non-sending evidence proves it, or
   **user-selected, unverified** when support cannot be checked without
   delivery.

Never silently select email or every available channel. If a non-sending check
proves a selection unsupported, explain it while the user is present and ask
whether to fix it, remove that channel, or disable notifications; preserve
other channels independently. If no outbound channel exists, offer native task
history. Do not create an unconfirmed account, connector, or secret.

Notification delivery is not an activation gate. Never claim a channel
delivered anything during setup or infer delivery merely because a channel is
supported or configured. Operational delivery and repair rules live in [run
and recover](run-and-recover.md).

### 4.5 Reconcile backtest disclosures

Compare final data, decision, timing, sizing, and execution behavior with every
backtest. Resolve formerly unknown differences and update reports and plan
disclosures without rewriting measurements. Show any material new difference
in the setup summary. Offer another backtest when useful, but never make
performance or another run an implementation gate.

## 5. Review and authorize setup

1. Show the selected or planned paper strategy and all settings.
2. Show implementation design, exact API access, schedule, task controls,
   self-healing and notification-repair scope, notification events/channels and
   support status, every planned AlphaInsider change, and future paper-order
   authority.
3. Show listed local files, data access, and external actions.
4. Offer:

   - **Build, Configure, and Activate** — authorizes only the displayed local
     and external work, native scheduler activation, and later scheduled or
     user-triggered paper orders that follow the confirmed plan without another
     prompt.
   - **Revise Setup** — returns to affected setup questions.
   - **Save and Stop** — keeps setup Draft and authorizes nothing.

Do not ask for another creation approval after **Build, Configure, and
Activate**. On Build, set AlphaInsider setup status Authorized and Phase
Building implementation.

## 6. Build the authorized implementation

1. Recheck the confirmed strategy, authorized setup, planned paths, and user
   changes.
2. Build the smallest source, state, documentation, runbook, and test set that
   follows the plan.
3. Implement every runtime entry and safety gate in
   [run and recover](run-and-recover.md).
4. Generate the project artifacts required by
   [project contract](project-contract.md).
5. Run static checks and mocked or offline tests.
6. Record managed files, checks, evidence, and next step in `plan.md`.

Do not create an AlphaInsider strategy or native task during this build step.
Never run an order-capable strategy run for build or verification. Setup calls
may inspect only the authorized paper strategy in the later setup step and may
never submit or cancel an order.

If the build needs an unplanned path, permission, AlphaInsider change, schedule
change, or behavior change, stop and return the affected stage to Draft. A
mechanical implementation fix that preserves the plan needs no new interview.

## 7. Implement the shared compatibility gate

1. Build one shared compatibility check used by every order-capable entry.
2. Run it before input and decision work for constraints that can stop a run.
3. Immediately before an external action, repeat it for that action's side
   effects and changeable constraints.
4. If a required fact cannot be verified, prohibit action. Return a safe
   no-action result only for an expected unavailable state; otherwise return an
   error for next-trigger recovery.

The check must cover:

- accepted market and operation availability under the confirmed session
  policy, using explicit guidance or the recorded stock fallback and treating
  cryptocurrency availability as 24/7, including current exchange status when
  authoritative guidance maps that status to permission;
- resolved instruments and strict `security` type compatibility;
- strategy ownership, strict type, current settings, and owner multiplier;
- positions, open orders, saved state, and uncertain prior submissions;
- exact mapped execution behavior and material side effects;
- confirmed sizing and exposure under operation-specific limits, including
  `getMaxOrderSize` for applicable direct orders and `2×` only where allocation
  or webhook contracts define it; and
- current permissions, account-tier dependencies, operation-specific limits,
  and side effects.

Do not assume missing `input_multiplier` is `1`. Newly documented support does
not expand a confirmed schedule. Incompatible guidance reopens timing. A failed
external action ends order work for that trigger and never permits a same-run
order retry.

## 8. Pass offline, order-free verification

Test whether implementation follows the plan, never whether it is profitable
or fast. Mock every external service and notification channel. Tests must not
submit or cancel an AlphaInsider paper order or deliver a setup/test
notification.

Cover:

- every applicable strategy decision, timestamp, freshness rule, strict asset
  type, sizing rule, risk limit, saved-state comparison, order mapping, and
  protection from future information;
- both compatibility checkpoints on every order-capable path, including
  supported, unavailable, invalid, and mid-run changed constraints;
- explicit accepted and rejected stock sessions, documentation-gap fallback,
  U.S. holidays and early closes, and 24/7 cryptocurrency availability;
- simultaneous triggers, one-run completion without faster-cadence polling,
  dry-run isolation, shared-lock behavior, and structured results;
- Active plus Degraded/Retrying error handling, next-trigger recovery,
  ambiguous-order reconciliation, no missed-order replay, and no same-trigger
  retry;
- repair scope, snapshot, rollback, protected resources, and time limits;
- duplicate-notification suppression, silence for healthy runs, independent
  channel failure, and notification delivery failure with self-healing enabled
  and disabled; and
- the rule that a failed channel is repaired only when notification repair is
  inside confirmed enabled self-healing scope.

A difference from backtest performance can start a correctness review but
fails verification only when evidence proves implementation or data handling
violates the plan.

## 9. Create or revalidate the paper strategy

1. Recheck key validity, final setup and runtime permissions, token user,
   account eligibility and limits, and every complete planned field.
2. Compare every request field with the Authorized setup plan, including the
   explicit public/private boolean and conditional price. Stop on any mismatch.
3. Confirm all code, documentation, static checks, and mocked tests passed.
4. For reuse, revalidate the exact choice and project configuration.
5. For creation, save the pre-call owned-strategy inventory, then call
   `newStrategy` exactly once.

Never run an order-capable strategy action as a setup test.

If `newStrategy` has an ambiguous outcome, do not retry. Refresh owned
strategies and compare the prior inventory with every authorized creation
field. Accept the result only when exactly one new owned match is proven;
otherwise stop with an ambiguous error and exact next step. Never blindly
create a replacement.

After a confirmed creation:

1. Capture the returned public strategy ID.
2. Store it through protected configuration.
3. Record it in `plan.md`.
4. Validate ownership, strict type, starting value, public/private state,
   conditional price, and owner multiplier.
5. Verify and record a working strategy URL.
6. Synchronize the generated description when creation did not produce the
   confirmed text.

For reuse, update description only when that exact change was displayed and
authorized. Preserve API-required current fields when an update operation
needs them. If description sync or scheduling later fails, retain the strategy
and saved ID, report the resume step, and never create a duplicate.

## 10. Configure and activate native automation

1. Set Phase Configuring automation.
2. Recheck the scheduler surface, project revision, persistent read/write
   access, secrets, network, task-name uniqueness, and user-operated controls.
3. Create the native task with the confirmed schedule. Put the stable
   persistent project identity in its instruction before these run directives:

   1. Open the persistent project at the recorded stable identity.
   2. Read project `plan.md` and `runtime/runbook.md`.
   3. Perform exactly one strategy run.
   4. Apply the shared lock, scheduled-time, run-evaluation, repair, and
      notification rules.
   5. Submit only AlphaInsider paper orders that follow the plan.
   6. Update safe project status and history.
   7. Finish without creating another schedule.

4. Configure scheduler **Run now** to enter the same strategy-run path. Never
   schedule a dry run or present terminal execution as the usual control.
5. If only the user can activate, provide the exact native-interface action,
   keep project state preventing new orders, wait, and verify the result.
6. Activate for the next scheduled run without executing an order-capable setup
   run.

Do not put an API key, secret, broker detail, public strategy ID, or unnecessary
private data in task prompt or metadata; keep the public strategy ID in project
configuration. Agent-led and hybrid runs can use scheduled AI reasoning
directly.

Activation requires the confirmed strategy description, final permissions,
implementation, runbook, offline tests, saved state, shared lock, and recorded
notification choices/support. Notification delivery is not a gate. Record task
name and next run, set Automation state Active, and set Operational health
Ready until the first operational run.

## 11. Complete creation

Set Phase and Creation state Complete, AlphaInsider setup status Active,
Highest completed outcome Automated strategy, Automation state Active, and
Operational health Ready only after:

- implementation and generated documents conform to `plan.md`;
- offline tests prove complete order-capable and dry-run paths;
- public strategy ID, ownership, strict type, settings, and link validate;
- a new strategy has the generated description, or an existing description is
  preserved unless its update was authorized; and
- the native scheduler is active for the next scheduled run.

Do not send a setup notification or require delivery verification. Record each
selected channel as supported or user-selected, unverified. If any gate remains
open, use **Creation incomplete** with the exact blocker and resume step.

Only after every gate passes, use the adaptive informational success handoff in
[project contract](project-contract.md). It asks for no approval.
