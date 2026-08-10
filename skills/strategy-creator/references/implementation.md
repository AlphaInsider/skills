# Strategy Implementation

Read this reference only after a complete plan is confirmed, when executing a
confirmed replacement, or when maintaining an implemented strategy.

## Contents

- [Execution gates](#execution-gates)
- [Replacement execution](#replacement-execution)
- [Project build](#project-build)
- [Generated documentation](#generated-documentation)
- [Completion and maintenance](#completion-and-maintenance)

## Execution gates

Read the sibling `alphainsider` skill and only the API references needed for
authentication, instruments, orders, sizing, and selected WebSockets. Before
writing, inventory every path again. Confirmation authorizes new files and
every exact overwrite recorded in the plan. If an unplanned path or collision
appears, return the plan to `draft` and reconfirm the complete updated plan
instead of requesting a one-off approval.

Keep project writes inside the selected project root; use absolute paths only
during the run and persist project-relative paths. The sole exception is one
exact confirmed user-level native background definition, installed only under
`background-operation.md` after all preceding gates pass.

For a `ready` target, complete **Confirmed provisioning** in
`alphainsider-target.md` before implementation files. For a `deferred` target,
make no remote calls, complete the local build with mocked external
interactions, install no background configuration, and leave the plan
`confirmed`.

## Replacement execution

For a confirmed replacement, perform only the recorded actions. Delete only
the exact attributable source, tests, copied AlphaInsider helpers,
dependencies, `.env.example`, `.gitignore`, `README.md`, `AGENTS.md`, and
background definition listed in the plan. Never recursively delete the project
root. Never delete `.env`, credentials, caches, unrelated files, or files whose
ownership is uncertain.

After those actions, replace `docs/plan.md` with
`docs/replacement-plan.md`, remove the temporary path, and build from the
promoted plan. Leave it `confirmed` unless every ready-target, remote,
verification, and applicable background gate succeeds.

## Project build

Build the smallest standalone project that satisfies the plan:

- Default to Python. Use another language only for a recorded ecosystem reason
  with equivalent AlphaInsider integration. Create `strategy/`, `tests/`,
  `.env.example`, dependency configuration, `.gitignore`, `README.md`, and
  `AGENTS.md` without a generic framework.
- For Python, read the sibling `scripts/alphainsider_request.py` as an immutable
  source and copy it to `strategy/alphainsider_request.py`. Copy
  `scripts/alphainsider_stream.py` only when the plan uses WebSockets. Pass
  `reconnect=True` to `stream_events` only for confirmed continuous recovery;
  retain one-session behavior when the plan stops on a stream error. Import
  generic request and calculation helpers, add only needed project-local
  endpoint functions, and modify only project copies.
- Put only names and safe examples in `.env.example`. Ignore `.env`, secrets,
  caches, and build outputs; keep plans, source, tests, and docs commit-ready.
  Follow `credentials.md` for missing values.
- Expose project-native commands for one decision cycle, continuous operation,
  tests, and a selected backtest. Do not add dry-run mode or an interactive
  confirmation before planned paper orders. Running either command is the
  user's execution action; never start either command automatically or during
  build and verification. For a deferred target, document the one-cycle and
  continuous commands but mark them unavailable until target readiness is
  resolved, and never run them.
- Implement the planned fixed, dynamic, or constrained-dynamic selection. For
  runtime candidates without exact IDs, use `search_stocks`; reject missing or
  ambiguous results and never guess a mapping. Validate resolved IDs with `get_stocks`,
  batch when practical, require the planned `security` type, and apply the
  freshness rule. Never order an invalid candidate; continue with valid
  candidates or abort as planned.
- Reconcile relevant AlphaInsider positions and open orders before decisions,
  validate target type at startup, and implement planned data, retry,
  duplicate, recovery, logging, sizing, and risk behavior. Never default a
  missing `input_multiplier` to `1`.
- Keep decisions testable. Backtests replay production logic chronologically
  without AlphaInsider calls or future information, reconstruct dynamic
  candidate sets without survivorship bias, and add portfolio accounting only
  with credible execution and cost assumptions.
- Add offline tests for signals, risk, order mapping, orchestration, and any
  backtest; mock external services. Verification must never submit an order or
  run an order-submitting command.

## Generated documentation

Write `README.md` for humans with purpose, behavior, prerequisites, setup,
environment names, commands, monitoring, limitations, and recovery. Apply the
target reference's API-key and cleanup requirements. Include a short `## Start`
section with ordered, copy-paste commands for dependency installation and
`.env` preparation. Label one decision cycle and continuous operation equally.
Match the selected language. For Python, place `source .venv/bin/activate`
immediately before the execution commands. For another language, use the
project's exact package-manager and runtime commands and omit Python steps.

For a deferred target, state that operational commands are unavailable until
the plan is reconfirmed with a ready target. For a ready target, warn that
either user-run command can submit paper orders immediately without another
prompt. When background operation is selected, include the manager-specific
install, lifecycle, management, logging, limitation, and start warnings from
`background-operation.md`.

Write `AGENTS.md` to make `docs/plan.md` authoritative, preserve credential and
remote-management boundaries, identify code/test entry points, and require the
installed-version workflow before behavior changes. Preserve deferred-target
restrictions, user invocation as execution consent, no second runtime prompt,
no automatic start, the background host-write exception, collision checks,
inactive installation, and stop-without-restart maintenance. Require agents to
use only the installed `set_env_value.py NAME VALUE` CLI with the value passed
as one safely quoted argument for agent-assisted entry, never show that command
to the user, import it, reproduce it, or edit `.env` directly, and fall back to
user editing when that argument cannot be passed safely.

## Completion and maintenance

Run all offline tests and static checks. For a ready target, complete
**Description synchronization**, then install and verify any confirmed
background definition without starting it. Set `implemented` only after the
remote and applicable background gates pass; a deferred target or failed
required installation remains `confirmed`. Exclude other deployment unless
separately requested. Before handoff, verify every changed path is in the
project or is the exact confirmed user-level definition, and neither skill
changed.

For behavior changes to an `implemented` plan, return it to `draft`, interview
only affected decisions, and reconfirm before code edits. Update code, tests,
`README.md`, and `AGENTS.md` together; regenerate the remote description and
restore `implemented` only after every gate passes. For a runtime-affecting
change, follow `background-operation.md`: the reconfirmed plan may stop and
disable an attributable service, but never restart it automatically. Report
the stopped state and exact user-run resume command.

To resume a confirmed deferred target, return the plan to `draft`, preserve the
offline implementation and unaffected decisions, resolve only target gaps,
and reconfirm before provisioning, synchronization, or other remote work.
