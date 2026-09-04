# Workflow Contracts

Use these contracts in every Strategy Creator workflow. They own user
communication, decision authority, lifecycle status, stopping, resumption, and
AlphaInsider documentation routing. Phase files point here instead of defining
another copy.

## Apply confirmation and action authority

1. A Draft strategy permits interviewing and read-only discovery.
2. A reviewed forward choice confirms the strategy. Require Strategy status
   Confirmed before planning a backtest or AlphaInsider setup.
3. Only **Build and Run** changes the reviewed backtest plan to Authorized for
   its listed local build and data access. At results review, a displayed
   mechanical correction and rerun can receive the same bounded authority.
4. Only **Build, Configure, and Activate** changes the reviewed AlphaInsider
   setup to Authorized for its listed local and external work, scheduler
   activation, and later plan-compliant AlphaInsider paper orders.
5. Immediately before an authorized action, verify that the plan still lists
   it and recheck every material fact that can change.

- Future paper-order authority never permits an unlisted AlphaInsider change,
  broker action, strategy change, cancellation, or another external action.
- AlphaInsider strategy creation, description updates, and deletion never
  authorize orders.
- A strategy run can submit an order only through an Active, confirmed,
  plan-compliant process.
- If a build reveals a required strategy, permission, schedule, or
  AlphaInsider change, return the affected stage to Draft and review it again.
- Apply a mechanical compatible fix without reopening unaffected decisions.

## Maintain the plan and lifecycle state

1. Update `plan.md` after every answer, material finding, completed action,
   failure, next-step change, and external-resource change.
2. Keep Strategy status Draft while an open decision can change intended
   behavior. Keep a confirmed strategy authoritative while a later backtest or
   setup plan is Draft.
3. Preserve unaffected answers when an earlier choice changes; reopen every
   dependent decision and invalidate only dependent authority.
4. Keep all earlier backtest evidence unless explicit deletion selects it.

Use conservative defaults for routine technical choices. After an authorized
build choice, give concise progress updates and interrupt only for a material
decision or blocker.

- **Creation state** describes the guided creation lifecycle.
- **Phase** identifies its current workflow position.
- **Strategy status**, **Backtest status**, and **AlphaInsider setup status**
  record separate confirmation and authority gates.
- **Highest completed outcome** records durable progress, not the best result.
- **Automation state** records whether the native task is configured, Active,
  or deliberately Paused.
- **Operational health** records Ready, Healthy, or Degraded/Retrying without
  changing Automation state.

Poor profit, loss, return, win rate, or deviation from a backtest is not a
lifecycle or health transition. Evidence of a plan violation can start the
applicable correction workflow.

## Ask each available decision round

1. Research facts from the project, market data, scheduler, storage, and
   AlphaInsider before asking the affected questions. Never ask the user for a
   fact that can be discovered safely.
2. Determine the current frontier: every decision whose prerequisites are
   settled.
3. Ask the entire frontier in one round. Defer a question that depends on an
   answer still open in that round.
4. Record each actual answer in `plan.md`; preserve partial answers and repeat
   only unanswered or newly affected questions.

Use the platform's multiple-choice control when it can hold the complete round.
Otherwise, use:

```markdown
❓ **Q1 — Short title:** Short question

A. First choice
B. Second choice

➡️ **Recommended:** A — Short reason.
```

- Filter recommendations through known constraints before showing them.
- Explain every material tradeoff between offered choices.
- Make each question and option decide only its current subject.
- Give two or three clear choices when possible and put the recommendation
  first in a question control.
- Recommend an answer unless only the user can know it.
- Bundle settings that must work together, such as cadence, data cutoff, clock,
  timezone, and order window, into complete compatible choices.
- Challenge future-data use, hidden costs, unavailable inputs, execution
  ambiguity, and unnecessary complexity.
- Keep material limits and side effects in the review summary even when they
  need no decision.
- Do not mention a later optional activity before its prerequisites are
  settled.
- Explain limitations and offer solutions only after the user requests a
  conflicting outcome. Do not ask how to handle a hypothetical failure of the
  recommended compatible choice.
- Do not invoke another grilling or interview skill.

`Recommended` accepts the pending question's recommendation. `Recommended all`
accepts every explicit recommendation in the current round. Neither supplies a
personal fact nor authorizes an unlisted action.

## Review and advance a decision stage

1. Show one concise summary after every decision in the stage is resolved.
2. In the same prompt, introduce destination-specific next-step choices with
   `❓ **Next step:** What would you like to do?` and explain what happens at
   each destination.
3. Treat a forward choice as confirmation of the reviewed summary; never add a
   separate agreement question.
4. Update `plan.md`, state what completed, explain the chosen destination in
   user terms, and continue with its next available decisions.

- **Revise** returns only affected and dependent decisions to Draft.
- **Save and Stop** preserves resumable work and authorizes no later build or
  external action.
- **Save This Strategy and Stop** at the Define summary confirms the reviewed
  strategy but leaves creation incomplete.
- A save at a backtest or AlphaInsider setup summary leaves that plan Draft.

## Stop, block, and resume creation

1. Respect a request to pause, stop, or change the goal at any time. If an
   external action cannot be interrupted, let only that action resolve and
   verify its result before stopping.
2. Preserve the current nonterminal Phase. Never set Phase or Creation state to
   Complete for a stop or blocker.
3. Set Creation state to Stopped for a user stop or Blocked for a technical,
   access, or capability gate that prevents the expected next action until it
   is remediated.
4. Record the reason, last completed step, exact resume step, what is waiting,
   what remains safe, whether scheduled runs and new orders are paused, and
   every local or external resource already created.
5. Use the **Creation incomplete** handoff in
   [project contract](project-contract.md).
6. On explicit resume, set Creation state to In progress, reconcile partial or
   ambiguous external results, recheck applicable state, and continue from the
   recorded safe checkpoint.

Waiting for an ordinary answer, a requested API key, or a supported
user-operated control is not a technical blocker. Keep Creation state In
progress and put the exact action under Waiting for.

- No stop or blocker authorizes deletion.
- A stop during partial setup pauses any active schedule, prevents new orders
  in project state, and retains all recovery identities.
- A stop after a matching Valid backtest preserves its methodology,
  limitations, Completed status, evidence, and Backtest outcome.
- A stop after a Failed backtest preserves diagnostic evidence without
  advancing the outcome.
- **Save This Strategy and Stop** preserves a Confirmed strategy and Highest
  completed outcome Strategy defined.
- A stop before the Define summary preserves a Draft strategy.

Never imply that a stop or blocker canceled an open order or sold a position.

## Resolve AlphaInsider API behavior

1. When installed, read `alphainsider-api` and only the sections needed for the
   current action.
2. Otherwise, read the current `https://api.alphainsider.com` documentation
   index, focused prose, and applicable OpenAPI or AsyncAPI contract sections.
3. During Define, also inspect live schedule-critical guidance.
4. Follow stricter compatible focused prose, record every relevant
   discrepancy, and never infer a rule from an example response or status.
5. Recheck changeable limits, permissions, identity, settings, and side effects
   immediately before the affected action.

Do not copy a fixed AlphaInsider endpoint catalog into a generated project.
Route each action to current installed guidance or live contracts instead.

Explicit current session guidance overrides the Strategy Creator stock
fallback for new or revised timing. Newly supported hours never silently
expand a confirmed schedule; newly incompatible guidance reopens its affected
timing decision.

## Request a user action

1. Keep a required action separate from an interview round.
2. Put the easiest supported method first.
3. State exactly what the user must provide or say when finished.

```markdown
👉 **Action — Short title:** Direct instruction.
```

Use `↪️ **Alternative:**` for another supported method. Do not use the required
action marker for an optional next step.

## Communicate outcomes and notifications

Use these strategy-run notification labels exactly:

- `🚨 Error — Action Required`
- `🔄 Retrying — No Action Required`
- `🛠️ Self-Healed — No Action Required`
- `⚠️ Warning — No Action Required`

After completed automation, mark a useful but non-required recommendation as:

```markdown
💡 **Optional next step — Short title:** Concise recommendation.
```

Phase-specific result order, evidence, warnings, and handoff content live in
the phase file or [project contract](project-contract.md).

## Prepare each user-facing turn

1. Read this file before the first user-facing message.
2. Lead with the result or current status.
3. Add only the context needed for the next decision, action, risk, or effect.
4. After answering a tangent or clarification, return to the next safe workflow
   step.

- Use common words and ASD-STE100-style technical English, but do not claim
  certified conformance.
- Use plain labels in questions, summaries, plans, results, and notifications.
- Use active voice, one meaning per word, and one main idea per sentence.
- Define an unavoidable technical or trading term the first time.
- Keep exact API fields, filenames, and internal status values out of questions
  unless they are necessary.
- Describe completed work and the next decision in user terms.
