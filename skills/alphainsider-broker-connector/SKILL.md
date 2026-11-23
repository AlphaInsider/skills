---
name: alphainsider-broker-connector
description: Connect a user's existing brokerage account to AlphaInsider strategies and keep it rebalanced across chosen allocations with scheduled agent runs, a persistent connection plan, and optional self-healing.
---

# AlphaInsider Broker Connector

Version: 1.2.0

## Updates

1. On first interactive use per conversation, inspect installed versions of this
   repository's `alphainsider`, `alphainsider-strategy-creator`, and
   `alphainsider-broker-connector` skills, and read
   all pages of [public GitHub releases](https://api.github.com/repos/AlphaInsider/skills/releases?per_page=100)
   without authentication. Compare numerically with the highest published stable
   `vX.Y.Z`; ignore drafts, prereleases, bare tags, and Latest. For older/unknown
   copies, show installed/available versions, label unknowns, and pause:
   **Update all** or **Continue**. Share results/choices across skills; recheck
   on request. Skip unattended runs. Continue quietly on automatic lookup failure
   or no releases; explain explicit-check failures. The hosted API skill is
   maintained by Mintlify and is excluded from this GitHub release check.

2. On **Update all**, use available capabilities to update existing older/unknown
   copies from the selected release, preserving installation scope. Keep current/newer
   copies; install no missing skills. Reload updated instructions when supported
   and resume. If unable to update, report outcomes, link the release, and give
   suitable manual instructions; continue with available versions.

## Purpose

The agent acts as the AlphaInsider bot for a brokerage account the user already
has. It mirrors the user's allocated AlphaInsider strategies in that account using
AlphaInsider's [allocation math](references/rebalance-math.md) and the broker's
real limits. The user chose to run this through the agent; do not offer
AlphaInsider's native bots instead.

- One project manages one broker account (or sub-account) and one asset type:
  stocks or cryptocurrency.
- The connection owns the whole account. Sizing follows the live account value,
  so deposits and withdrawals spread across allocations, and holdings outside the
  targets are closed.
- Use judgment for broker mechanics, scripts, order handling, and checks. The
  only fixed rules are in [Boundaries](#boundaries).

## Start or resume

1. Run the [platform and automation access check](references/workflow-contracts.md#check-platform-and-automation-access)
   before [project setup](references/workflow-contracts.md#start-or-resume-the-project).
   - Resume from the project's `plan.md`, `connection.md`, and `connection.db`
     before new work; keep generated files outside this skill repository.
2. Continue from recorded state.
   - Handle modify, stop, and resume requests whenever asked.
   - Number required sequences; use bullets for other notes, ranked by importance
     at each level.

## AlphaInsider API

- Read the live [AlphaInsider API skill](https://api.alphainsider.com/skill.md),
  then follow its navigation, prerequisite guides, and exact operation pages. Use
  this source even if an older GitHub API skill is installed.
- Use it to find, filter, and subscribe to strategies, and to read strategy
  values, positions, trade timelines, stock details, quotes, and exchange status.
- If required API guidance cannot be fetched, pause the dependent API work and
  report the missing source.

## Set up a connection

Interview the user in rounds and record decisions in `plan.md`, following
[resolve the current decisions](references/workflow-contracts.md#resolve-the-current-decisions).
End each phase with a [next-step question](references/workflow-contracts.md#choose-the-next-phase).

1. **Access:** confirm persistent storage, SQLite, and scheduling.
2. **Broker:** research the [broker contract](references/broker-contract.md),
   let the user choose the access method, set up [credentials](references/credentials.md),
   and let the user choose the account from those available, recommending a
   sub-account.
3. **Allocations:** choose subscribed strategies and targets, leverage,
   reserves, and start, stop, and deposit/withdrawal behavior.
4. **Build:** write the runbook and any broker scripts, initialize
   `connection.md` and `connection.db`, and complete a dry run.
5. **Activate:** offer a live test trade, then schedule runs and set
   notifications and self-healing.

Phase details are in [setup phases](references/workflow-contracts.md#setup-phases).

## Run and recover

- Scheduled and manual runs follow `plan.md`, the runbook in `connection.md`,
  and [run and recover](references/run-and-recover.md): detect strategy trades,
  rebalance, record state in `connection.db`, self-heal when enabled, and notify.

## Boundaries

- Follow [credentials](references/credentials.md): never inspect, print, or log
  secrets.
- Before the first live orders, the user reviews a dry run and agrees to go
  live. This happens once, during setup; after that,
  [runs](references/run-and-recover.md#run-the-connection) place orders without
  asking.
- Before the first rebalance, confirm the user understands that holdings outside
  the targets will be closed.
- Allocate only to strategies of the selected asset type with an active subscription
  for the user, including owned strategies. Free and paid stock or crypto
  strategies are eligible. The agent submits orders directly to the chosen broker.

## References

- [`references/workflow-contracts.md`](references/workflow-contracts.md) — access check, interview, phases, schedule, modify/stop/resume
- [`references/broker-contract.md`](references/broker-contract.md) — broker facts to research before sizing orders
- [`references/rebalance-math.md`](references/rebalance-math.md) — allocation drift, targets, and orders
- [`references/run-and-recover.md`](references/run-and-recover.md) — `connection.db`, runs, dry runs, recovery, notifications
- [`references/credentials.md`](references/credentials.md) — AlphaInsider and broker credentials, sessions, and re-login
- [`references/plan-template.md`](references/plan-template.md) — `plan.md` outline
- [`references/connection-template.md`](references/connection-template.md) — `connection.md` outline
