# Backtesting

This file owns feasibility assessment, methodology disclosures, design,
execution, and results. Read it only after the user selects **Backtest
Strategy** from the Define Strategy summary. A backtest never authorizes a
strategy change or submits an AlphaInsider order.

## Assess feasibility and disclose limitations

Assess feasibility as the first Backtest Strategy activity. Do not use this
assessment to hide or withdraw the earlier backtest choice.

Determine whether each decision can be recreated from information available at
that historical time. Check:

- timestamped historical signal inputs;
- the assets eligible on each date, including assets that later stopped
  trading or failed;
- the confirmed implementable native-scheduler cadence, market calendar,
  documented-or-fallback stock session policy or 24/7 cryptocurrency policy,
  and decision timing;
- the mapped AlphaInsider order operation and its material side effects;
- credible price, fee, execution-delay, fill, and slippage assumptions; and
- later revisions, later index membership, survivorship bias, or other future
  information.

For an AI-led decision, determine whether the historical prompt context and
permitted evidence can be recreated. Record model and reasoning differences.
Do not claim fixed code exactly represents decisions made by scheduled AI.

For every planned and completed backtest, record these methodology facts:

- **Uses information unavailable at the historical decision time: Yes | No**;
  and
- every difference from intended automated execution and every other
  limitation, including substituted data, behavior, cadence, or execution
  assumptions. Record `None known` rather than leaving the field ambiguous.

Use **Yes** when any decision, eligible-asset universe, later revision, or
other input would not have been available at its historical decision time. Use
**No** only when every decision uses contemporaneously available information.
The answer may remain **Not assessed** during feasibility work but must be
**Yes** or **No** before Backtest status becomes Authorized.

These methodology facts describe what the backtest can support, not whether a
run completed correctly. Give every attempted run one separate disposition:

- **Valid** — its measurements and recoverable evidence are complete and its
  correctness checks pass; a recorded result-visual rendering failure alone
  does not change this disposition;
- **Superseded** — a retained Valid run is no longer the featured evidence
  because a later Valid run, strategy revision, or backtest-plan revision replaced
  it; or
- **Failed** — it stopped early or a defect makes its results untrustworthy.

Valid describes run integrity, not predictive credibility.

For status purposes, a run matches the current strategy when it evaluates the
confirmed rules under its authorized backtest plan without silently revising
intended strategy behavior. Disclosed future-information use or a backtest-only
substitute for unavailable data, behavior, or execution does not by itself make
the run evidence for a different strategy. A newly intended signal, asset
selection rule, sizing rule, or other trading behavior does.

Record a plain reason whenever a run is Superseded or Failed. Never feature a
Failed run. Preserve it as diagnostic evidence rather than silently replacing
it.

If a faithful backtest is straightforward, briefly state that finding and
continue to backtest questions without another confirmation. Otherwise,
explain the issue, recommend the most informative method, and let the user
choose or suggest any safe, technically possible, order-free backtest.
Challenge a misleading method before execution, but run it when the user still
chooses it and its access, cost, licensing, and technical requirements are
satisfied. Never conceal future information or imply that a backtest recreated
the automated strategy when its data, behavior, or execution differs.

A signal-focused backtest is often more useful than false portfolio precision.
If no proposed method is technically possible, explain the exact blocker and
return to the interview for revision, implementation without a backtest, or
Save and Stop. Implementation without a backtest marks it Skipped; saving
keeps it Draft and resumable.

Use the confirmed implementable cadence and mapped execution behavior for the
primary backtest. A user-requested backtest at another cadence or with another
execution method can still run after its warning; record the exact difference
and set future-information use to **Yes** when applicable. Never present a
backtest at a cadence the native scheduler cannot run as direct evidence for
the automated strategy.

## Plan and authorize the backtest

Ask only about choices that can change the backtest:

- backtest dates and any final period kept separate until the strategy is set;
- simulated starting value and maximum exposure under the confirmed
  execution-specific rule;
- decision and execution timestamps;
- order-fill, fee, slippage, delay, and missing-data assumptions;
- an appropriate comparison investment; and
- the exact results and result visuals that will make the backtest
  understandable.

Normally plan two to four data-derived visuals. For a portfolio backtest,
include the equity curve against the comparison investment and drawdown. For a
signal-only backtest that cannot honestly produce portfolio results, propose
two suitable substitutes, such as a signal-and-price timeline, outcome
distribution, or data-coverage view. Explain why the portfolio views do not
apply. Put the exact substitutes in the reviewed plan before **Build and Run**;
do not choose them only after seeing results. Add more than four visuals only
when needed to prevent a misleading summary.

Every performance visual must come from the saved backtest data. An explanatory
diagram can come from the confirmed plan. Never use decorative or invented
imagery as backtest evidence.

Ask before using a paid source, new credential, or scraping. Define correctness
checks for logic and data timing. Show the future-information answer, upfront
warning when it is **Yes**, known or expected differences from intended
automated execution, other limitations, unresolved implementation-dependent
differences, data access, and planned local work in the backtest summary.

Only the user's **Build and Run** choice initially makes Backtest status
Authorized and permits that displayed local build and data access. Revise
returns to affected questions. Skip continues to AlphaInsider implementation.
Save and Stop keeps the backtest plan Draft.

## Build and run

Reuse production decision logic or a shared pure decision module when the
backtest claims to reproduce it. Keep every backtest entry point unable to call
AlphaInsider ordering endpoints and mock all trading actions.

Process historical data in chronological order when future-information use is
**No**. When it is **Yes**, use future information or nonchronological
processing only as the authorized plan discloses. Persist every run rather
than replacing earlier evidence. Record:

- the run's future-information answer and exact limitations;
- strategy, plan, code, and dataset fingerprints;
- data identity, retrieval time, cutoff time, and any permitted future
  information;
- assumptions and exact differences from automated runs;
- changes from earlier backtests;
- run disposition and its reason;
- exact command and random seed when applicable;
- results, limitations, report and visual artifact paths, visual-rendering
  failures and repairs; and
- an immutable snapshot of the run's source and configuration, or an exact
  durable commit that contains both. A fingerprint without recoverable source
  is not sufficient. Exclude `.env`, secret values, private destinations,
  caches, and unrelated files from every snapshot.

Keep with the run the saved outputs needed to reproduce its visuals. If a
planned visual does not render, make one safe mechanical repair attempt from
those outputs. A remaining rendering failure does not by itself make otherwise
trustworthy evidence Failed or prevent the matching run from being Valid. Keep
the exact failure and repair attempt in the run history. A later repair renders
from the same saved outputs, preserves that history, and never reruns the
trading logic or changes the measurements.

Keep every run's recoverable source and configuration until the user explicitly
selects it for deletion through `changes-and-deletion.md`. Retention cleanup,
supersession, a newer Valid run, or completed creation never authorizes its
removal.

Users may change backtest assumptions and run more backtests after seeing
results. Preserve each run and identify the change. A strategy-behavior change
returns to Define Strategy and invalidates dependent authorization; correcting
a backtest does not silently change the strategy. Mark affected Valid evidence
Superseded before applying a strategy or backtest-plan revision. If no other
Valid result matches the revised strategy and current backtest plan, clear the
featured result, set the backtest plan to Draft, and return Highest completed
outcome to Strategy defined.

When a newer matching Valid run becomes featured, mark the prior featured run
Superseded with that reason. This disposition change never alters or removes
its methodology disclosures, source, configuration, report, or artifacts.

At results review, a user can authorize a displayed mechanical correction and
rerun under the same backtest plan. Set Backtest status to Authorized and
preserve earlier evidence. A change to the backtest plan returns it to Draft
and needs a new summary and **Build and Run** choice.

## Present results

Identify each result as `Backtest <date or ID> — Valid | Superseded | Failed`.
Then state whether it used information unavailable at the historical decision
time and give a plain conclusion about what it did and did not reproduce. When
the answer is **Yes**, begin with a warning that the backtest cannot demonstrate
real-time strategy performance and repeat that warning beside every affected
measurement. The warning is mandatory even when the user requested the method.
Put other differences and disclaimers before headline performance and beside
every affected measurement. State that results do not guarantee future
performance.

When several backtests exist, feature the latest Valid run that matches the
current strategy. List every earlier, Superseded, and Failed backtest with its
date or ID, disposition, future-information use, limitations, link, and reason.
Do not select the best-performing result as primary.

Show the main comparison in a compact Markdown table. Define each standard
financial term the first time. Include, when applicable:

- equity curve and comparison investment;
- drawdown, meaning the fall from a prior high;
- returns by period, total return, and annualized return;
- volatility and a risk-adjusted return measure;
- trade count, win rate, turnover, fees, and time invested; and
- important assumptions, future information, and data limits.

Supplement the table and written interpretation with the exact saved result
visuals from the authorized plan. Usually show two to four. A portfolio result
includes the equity curve against its comparison investment and drawdown. A
signal-only result includes its two authorized substitutes. Show other result
or diagnostic visuals only when they materially improve understanding. For
multiple runs, feature the visuals for the latest Valid run that matches the
current strategy; include an earlier, Superseded, or Failed run's diagnostic
visual only when useful.

Make every visual understandable as a standalone artifact. Include the
backtest identity and period, labels and units, the comparison investment when
relevant, descriptive alternative text or a caption, and a one-sentence
takeaway. When future information or another material limitation affects a
visual, put a short warning inside the artifact and repeat it beside the visual
in the response. Derive charts only from saved run data and diagrams only from
the confirmed plan.

Embed the saved images when the response supports them. Otherwise, link
directly to each named image; a link to the detailed report alone is not a
substitute. Keep the visuals with the compact table, limitations, warnings, and
plain-language interpretation rather than replacing them. End with a separate
direct link to the detailed report.

If a planned visual remains unavailable after the safe repair attempt, state
only that some planned visuals are unavailable. Show any available visuals and
the rest of the results normally. This presentation failure does not by itself
invalidate trustworthy evidence. Separate whether the backtest followed
`plan.md` from profitability. Poor returns do not make a backtest or strategy
fail.

Record all runs under `backtest/` and in `plan.md`. A Valid completed run of any
methodology advances Backtest status to Completed and Highest completed
outcome to Backtest only while it matches the current strategy and backtest
plan. When no Valid run matches, a Failed run sets Backtest status to Failed,
leaves the stage resumable, and does not claim a completed Backtest outcome.
When an earlier matching Valid run exists, keep Completed and record the later
failed attempt separately. Return to `interview.md` for the results summary and
next-step choices.
