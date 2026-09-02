---
name: alphainsider-strategy-creator
description: Create, resume, backtest, implement, automate, update, or explicitly delete one plan-driven AlphaInsider paper-trading strategy. Use for stock or cryptocurrency strategies that run through a native AI scheduler and may use code, the scheduled AI agent, or both.
---

# AlphaInsider Strategy Creator

Guide one strategy from an idea to an automated AlphaInsider paper strategy.
Keep this installed skill read-only. Put all user artifacts in one persistent
project.

## Core contract

- `plan.md` is the project's readable source of truth. Backtests, code, the
  AlphaInsider target, and automation must conform to it.
- One project contains one strategy with one strict `stock` or
  `cryptocurrency` type. Dynamic selection must stay inside that type.
- Check current applicable AlphaInsider constraints before proposing or
  performing an AlphaInsider action. Recheck mutable constraints immediately
  before the action.
- Send orders only to AlphaInsider paper strategies. Never create a broker
  client, connect a broker, or request broker credentials.
- Never inspect, print, or summarize an existing API key, secret store, or
  complete `.env`. Accept a value deliberately pasted in chat only through the
  non-echoing credential workflow.
- Use only the platform's native AI automation or scheduler. Never install a
  host scheduler, service, daemon, or background process.
- Make the generated plan and runbook sufficient for normal runs and agreed
  self-healing without this installed skill. Use this skill for creation,
  updates, deletion, and automation reconfiguration.
- Treat performance as information. Poor performance never makes a
  plan-conforming run unhealthy or authorizes a strategy change.
- Build and pass offline, order-free checks before creating a new target.
- Support create, resume, update, and explicit deletion. A different strategy
  belongs in another project. Deletion requires an explicit user request.

## Begin or resume

1. Read [user communication](references/user-communication.md) before the first
   user-facing message.
2. Read [persistent project](references/project-root.md). Select the safest
   persistent location without asking the user, unless the user already named
   one. Resume a clear match; otherwise create one dedicated project after its
   objective is known.
3. Read `plan.md` and its **Current status** when a project exists. Never open
   `.env` to discover configuration.
4. Route the requested work:
   - For creation or incomplete setup, read the
     [strategy interview](references/interview.md). It owns the creation order,
     agreements, transitions, stop behavior, and completion gates.
   - For any scheduled occurrence, scheduler **Run now**, chat normal run,
     chat dry run, operational error, notification, or repair, read
     [scheduled and user-triggered runs](references/scheduled-runs.md).
   - For an update, detected edit, external drift, or explicit deletion, read
     [changes and explicit deletion](references/changes-and-deletion.md).

Do not preload every reference. Follow links from the selected workflow only
when their stated phase or action begins.

## Agreement and authority

A Draft plan permits interviewing, feasibility research, read-only discovery,
and planning. Require the applicable plan to be Agreed before a backtest or
implementation build, remote mutation, order-capable run, or scheduler
activation. Keep `plan.md` current after each answer, material finding,
completed action, failure, or next-step change. Its status must let a new chat
or scheduled agent continue without this chat history.

If a backtest or implementation reveals that intended strategy behavior must
change, stop the affected work and return to the interview. Plan-preserving
mechanical fixes, such as compatible endpoint wiring or bounded rate-limit
handling, do not need a new strategy decision.

An agreed automation plan authorizes later plan-conforming AlphaInsider paper
orders through its normal-run paths without per-order confirmation. It does not
authorize an unlisted remote mutation, broker action, or strategy change.

## AlphaInsider API behavior

When `alphainsider-api` is installed, read its `SKILL.md` and only the API
sections needed for the current action. Otherwise, use the current
`https://api.alphainsider.com` index and contracts. Keep this skill
self-contained, but do not duplicate an API catalog here.
