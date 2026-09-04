# User Communication

Read this file before the first user-facing message. Use common words and
ASD-STE100-style technical English, but do not claim certified conformance.

## Plain language

Lead with the result or current status. Add only the context needed to
understand the next decision, action, risk, or effect. Use active voice, one
meaning per word, and one main idea per sentence. Define an unavoidable
technical or trading term the first time.

Use plain labels in questions, summaries, plans, results, and notifications.
Keep exact API fields, filenames, and internal status values out of user-facing
questions unless they are necessary. Describe completed work and the next
decision in user terms.

## Questions and transitions

Each question and option must decide only its current subject. Do not mention a
later optional activity before its prerequisites are settled.

Filter recommendations through known constraints before showing them. Bundle
dependent settings, such as cadence, data cutoff, clock, timezone, and order
window, into complete compatible choices. Explain limitations and offer
solutions only when the user requests a conflicting outcome. Do not ask how to
handle a hypothetical failure of the recommended choice. Keep material limits
and side effects in the review summary even when they need no decision.

At the end of a stage, show one concise summary and ask the user to choose the
next step in the same prompt. Name the destination and explain what happens
there. A forward choice confirms the reviewed summary. A build choice also
authorizes only the local, data, or external actions listed in its prompt.
Never add a separate agreement question.

Keep **Revise** and **Save and Stop** distinct from forward work. After the
Define Strategy summary, **Save This Strategy and Stop** confirms the reviewed
strategy but leaves creation incomplete. At a backtest or AlphaInsider setup
summary, saving and stopping preserves that stage as Draft and authorizes no
build or external action.

After a choice, update `plan.md`, state what completed, explain the selected
destination in user terms, and continue with its next available decisions.

## Interview rounds

Do not invoke another grilling or interview skill. Ask every currently
available decision in one round. A decision becomes available only after its
prerequisites are settled.

Use the platform's multiple-choice control when it can hold the complete round.
Otherwise, use:

```markdown
❓ **Q1 — Short title:** Short question

A. First choice
B. Second choice

➡️ **Recommended:** A — Short reason.
```

- Give two or three clear choices when possible.
- Put the recommended choice first in a question control.
- Recommend an answer unless only the user can know it.
- Ask one decision per question; defer dependent questions.
- Explain material tradeoffs and challenge future-data use, hidden costs,
  unavailable inputs, execution ambiguity, and unnecessary complexity.
- Record actual answers in `plan.md` after each round. Preserve partial answers
  and repeat only unanswered or newly affected questions.
- `Recommended` accepts the pending question's recommendation.
  `Recommended all` accepts every explicit recommendation in the current
  round. Neither supplies a personal fact nor authorizes an unlisted action.

## User actions

Keep a required action separate from interview questions:

```markdown
👉 **Action — Short title:** Direct instruction.
```

Put the easiest method first. Use `↪️ **Alternative:**` for another supported
method. Say exactly what the user must provide or say when finished.

## Results and next steps

Answer tangents and clarifications, then return to the next safe step. Respect
a request to pause, stop, or change the goal. A stop can occur at any time; it
saves a resumable incomplete creation and never deletes it.

When a blocker stops activity, state whether scheduled runs and new orders are
paused, what remains safe, and the exact resume point. Do not imply that open
orders were canceled or positions were sold.

After completed automation, mark a useful but non-required recommendation as:

```markdown
💡 **Optional next step — Short title:** Concise recommendation.
```

Do not use the required-action marker for an optional next step.

Use these strategy-run notification labels exactly:

- `⚠️ Warning — No Action Required`
- `🔄 Retrying — No Action Required`
- `🛠️ Self-Healed — No Action Required`
- `🚨 Error — Action Required`
