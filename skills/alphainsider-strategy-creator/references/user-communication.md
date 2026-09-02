# User Communication

Read this file before the first user-facing message. Apply it throughout the
project. Use common, simple words and ASD-STE100-style technical English. Do
not claim certified ASD-STE100 conformance.

## Give useful context

Lead with the result or current status. Add one short context sentence when it
helps the user understand a choice, risk, prerequisite, or effect. Do not add
background that does not change the next decision or action.

Use active voice. Give each word one meaning. Define an unavoidable technical
or trading term the first time. Prefer one main idea per sentence. Use short
sentences, specific nouns, and vertical lists when they are easier to scan.

## Internal grill interview

Do not invoke another grilling or interview skill. Ask all currently available
decisions in one round. A decision is available only when its prerequisites
are settled.

Use the platform's multiple-choice question control when it can present the
complete round. Otherwise, use:

```markdown
❓ **Q1 — Short title:** Short question

A. First choice
B. Second choice

➡️ **Recommended:** A — Short reason.
```

- Give two or three clear choices when possible.
- Put the recommended choice first in a question control.
- Give a recommended answer unless only the user can know the answer.
- Ask one decision per question. Put dependent questions in a later round.
- Explain material tradeoffs. Challenge future-data use, hidden costs,
  unavailable inputs, execution ambiguity, and unnecessary complexity.
- Record the user's actual answer in `plan.md` after each round.
- `Recommended` accepts the recommended answer to the pending question.
  `Recommended all` accepts each explicit recommendation in the current round.
  Neither phrase supplies a personal fact or authorizes an unlisted action.
- Preserve partial answers. Repeat only unanswered or newly affected questions.

## User actions

Separate actions from interview questions. When the user must supply a value,
open a platform setting, or complete another prerequisite, use:

```markdown
👉 **Action — Short title:** Direct instruction.
```

Put the easiest recommended method first. Use
`↪️ **Alternative:**` for another supported method. State exactly what the user
must provide or say when complete. Do not put a numbered Q&A round in the same
message.

## Keep the journey moving

After each result, tangent, clarification, or blocker:

1. answer the immediate point;
2. state the current phase when useful; and
3. continue with the next safe step, or clearly identify the next user action.

Never leave the user to ask what happens next. Respect a request to pause,
stop, or change the goal.

Use these runtime-notification labels exactly:

- `⚠️ Warning — No Action Required`
- `🛠️ Self-Healed — No Action Required`
- `🚨 Error — Action Required`
