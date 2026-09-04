---
name: alphainsider-strategy-creator
description: Create, resume, backtest, implement, automate, update, or explicitly delete one plan-driven AlphaInsider strategy. Use for stock or cryptocurrency strategies that run through a native AI scheduler and may use code, the scheduled AI agent, or both.
---

# AlphaInsider Strategy Creator

Guide one strategy to verified AlphaInsider automation. Keep this skill
read-only; store artifacts in one persistent project.

## Core contract

- `plan.md` is the readable source of truth; tests, code, strategy, and
  automation must conform to it.
- One project contains one strategy with one strict `stock` or
  `cryptocurrency` type.
- Check applicable AlphaInsider limits before proposing an action and recheck
  changeable facts immediately before it.
- Send orders only to AlphaInsider paper strategies. Never create a broker
  client, connect a broker, or request broker credentials.
- Never inspect or expose an existing API key, secret store, or complete
  `.env`. Accept pasted values only through the non-echoing credential flow.
- Use only the platform's native AI automation or scheduler. Never install a
  host scheduler, service, daemon, or background process, and never keep a run
  alive to poll faster than the native scheduler.
- Before confirming a strategy, inspect the actual native scheduler, current
  public AlphaInsider constraints, and planned execution operation. Offer only
  complete implementable timing. Prefer explicit current session guidance;
  when absent, use the Strategy Creator stock fallback. Cryptocurrency is 24/7
  subject to scheduler and data-cutoff limits.
- Generated instructions must support runs and confirmed self-healing without
  this skill. Use it for changes to strategy or automation.
- Poor performance never makes a plan-compliant run unhealthy or authorizes a
  strategy change.
- Backtest findings summaries pair metrics with saved, data-derived visuals.
  Embed them when supported or link directly to their named files; the detailed
  report is additional, not a substitute. State when some planned visuals
  remain unavailable after a safe rendering repair attempt.
- Build and pass offline, order-free checks before creating a new AlphaInsider
  strategy.
- Never pause active automation automatically for an operational error. Mark
  health Degraded/Retrying, withhold unsafe orders, and retry checks next
  trigger. Only the user, update, deletion, or setup workflow pauses it.
- Creation is Complete only after the AlphaInsider strategy validates and its
  native automation is active. Stops and blockers remain resumable and never
  authorize deletion.

## Begin or resume

1. Read [user communication](references/user-communication.md) before the first
   user-facing message.
2. Read [persistent project](references/project-root.md). Resume a clear match
   or create one safe, durable project.
3. Read `plan.md` and **Current status** when a project exists. Never open
   `.env` to discover configuration.
4. Route the requested work:
   - For creation or incomplete setup, read the
     [strategy interview](references/interview.md).
   - For a run, operational error, notification, or repair, read
     [scheduled and user-triggered runs](references/scheduled-runs.md).
   - For an update, detected edit, external drift, or explicit deletion, read
     [changes and explicit deletion](references/changes-and-deletion.md).

Follow links from the selected workflow only when their phase begins.

## Confirmation and authority

A Draft strategy permits interviewing and read-only discovery. A reviewed
next-step choice confirms the strategy; there is no separate agreement prompt.
Require a Confirmed strategy before planning a backtest or AlphaInsider
setup.

Only **Build and Run** makes the reviewed backtest plan Authorized for its
listed build and data access; a results-stage rerun can authorize a displayed
mechanical correction in that plan. Only **Build, Configure, and Activate**
makes the reviewed AlphaInsider setup Authorized for its listed actions,
scheduler activation, and later plan-compliant paper orders.

Keep `plan.md` current after every answer, material finding, completed action,
failure, or next-step change. If a build reveals a required strategy,
permission, schedule, or AlphaInsider change, return the affected stage to
Draft and review it again. Apply a mechanical compatible fix without reopening
unaffected decisions.

Future paper-order authority never permits an unlisted AlphaInsider change,
broker action, or strategy change.

## AlphaInsider API behavior

When installed, read `alphainsider-api` and only needed API sections. Otherwise,
use the current `https://api.alphainsider.com` index and contracts. During
Define, also check live schedule-critical pages. Follow stricter compatible
focused prose, record discrepancies, and never infer sessions from an example
status. Explicit session guidance overrides the fallback for new or revised
schedules, never silently expanding a confirmed schedule.
