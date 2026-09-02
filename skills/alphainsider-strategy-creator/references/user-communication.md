# User Communication

Read this file before the first user-facing message. Use common words and
ASD-STE100-style technical English, but do not claim certified conformance.

## Plain language

Lead with the result or current status. Add only the context needed to
understand the next decision, action, risk, or effect. Use active voice, one
meaning per word, and one main idea per sentence. Define an unavoidable
technical or trading term the first time.

Keep internal stage names and exact `plan.md` status values inside project
instructions. Describe user-visible work plainly, such as testing with
historical data or setting up scheduled paper trading.

## Decisions and transitions

Each question and option must decide only its current subject. Do not mention a
later optional activity in its question, choices, or recommendation. Use
agreement labels such as **Agree to this strategy**, **Agree to this backtest
plan**, and **Agree to this implementation plan**. Put the work authorized by
an agreement in its question body, not its option label.

After a decision, record it and introduce the next applicable work separately.
State what completed, explain the next work in user terms, and give one clear
question or action.

## Interview rounds

Do not invoke another grilling or interview skill. Ask all currently available
decisions in one round. A decision becomes available only after its
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

Answer tangents and clarifications, then return to the next safe step. Never
leave the user to ask what happens next. Respect a request to pause, stop, or
change the goal.

Use these runtime-notification labels exactly:

- `⚠️ Warning — No Action Required`
- `🛠️ Self-Healed — No Action Required`
- `🚨 Error — Action Required`
