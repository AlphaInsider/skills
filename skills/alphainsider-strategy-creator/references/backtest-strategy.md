# Backtest Strategy

Use this workflow only after the user selects **Backtest Strategy** from the
reviewed Define summary. It owns feasibility, disclosures, design authority,
execution, evidence, disposition, results, and results-stage choices. A
backtest never authorizes a strategy change or an AlphaInsider order.

## 1. Enter backtesting

1. Require Strategy status Confirmed and Backtest choice Selected.
2. Set Backtest status Draft and Phase Assessing backtest.
3. Assess feasibility before asking any backtest-design question.
4. Keep the confirmed strategy unchanged while the backtest plan remains
   Draft.

Do not use feasibility assessment to hide or withdraw the backtest choice that
the user already selected.

## 2. Assess feasibility

1. Determine whether every decision can be recreated from information that was
   available at its historical decision time.
2. Check the complete evidence and execution boundary:

   - timestamped historical signal inputs;
   - assets eligible on each date, including assets that later stopped trading
     or failed;
   - confirmed native-scheduler cadence, calendar, decision time, and
     documented-or-fallback stock session or 24/7 cryptocurrency policy;
   - mapped AlphaInsider operation and its material side effects;
   - credible price, fee, fill, execution-delay, and slippage assumptions; and
   - later revisions, later index membership, survivorship bias, and any other
     future information.

3. For an AI-led decision, determine whether the historical prompt context and
   permitted evidence can be recreated. Record model and reasoning
   differences; never claim fixed code exactly represents a scheduled AI
   judgment.
4. Record a feasibility finding and recommended approach in `plan.md`.

Every planned and completed run must record:

- **Uses information unavailable at the historical decision time: Yes | No**;
  and
- every difference from intended automated execution and every other
  limitation, including substituted data, behavior, cadence, or execution
  assumptions. Use `None known` when none are known.

Use **Yes** when any decision, eligible universe, later revision, or other
input was unavailable at the historical decision time. Use **No** only when
every decision uses contemporaneously available information. The value can be
Not assessed during feasibility but must be Yes or No before Backtest status
becomes Authorized.

### 2.1 Choose a feasible method

1. If a faithful backtest is straightforward, state that finding and continue
   directly to planning without another confirmation.
2. Otherwise, explain the material limitation before results can anchor the
   user and recommend the most informative technically possible method.
3. Let the user choose or suggest any safe, order-free method whose access,
   cost, licensing, and technical requirements can be met.
4. Challenge a misleading method before execution, but run it when the user
   still selects it and every prerequisite is satisfied.
5. If no proposed method can run, explain the exact blocker and offer strategy
   revision, implementation without a backtest, or Save and Stop.

For this no-method branch, implementation sets Backtest choice and status
Skipped, sets Phase Planning implementation, and continues to [implement and
activate](implement-and-activate.md). Save and Stop keeps the assessed backtest
Draft and uses the incomplete handoff in [project contract](project-contract.md).

A signal-focused test is often more useful than false portfolio precision.
Never conceal future information or imply that substituted data, behavior, or
execution recreated the automated strategy exactly.

A warning permits an imperfect user-directed backtest; it never permits
undisclosed future information, a false claim, unauthorized data access, or an
order.

Use the confirmed cadence and mapped execution behavior for the primary
backtest. A user-requested alternative can run after a clear warning; record
the exact difference and mark future-information use Yes when applicable.
Never present an unsupported higher-frequency test as direct evidence for the
scheduled implementation.

## 3. Plan the backtest

1. Set Phase Planning backtest when an approach is ready.
2. Settle only choices that can change the backtest:

   - dates and any final period held separate until the strategy is fixed;
   - exact dataset, source, access, cost, retrieval, and data cutoff;
   - simulated starting value and maximum exposure under the confirmed
     execution-specific rule;
   - decision and execution timestamps;
   - fill, fee, slippage, delay, and missing-data assumptions;
   - an appropriate comparison investment;
   - exact result measurements and visuals; and
   - correctness checks for strategy logic and data timing.

3. Ask before using a paid source, new credential, or scraping.
4. Resolve future-information use to Yes or No.
5. Record known, expected, and implementation-dependent differences from
   intended automation.

### 3.1 Plan result visuals

- Normally plan two to four data-derived visuals.
- For a portfolio backtest, include an equity curve against the comparison
  investment and drawdown, meaning the fall from a prior high.
- For a signal-only backtest that cannot honestly produce portfolio results,
  explain why those views do not apply and choose two useful substitutes, such
  as a signal-and-price timeline, outcome distribution, or data-coverage view.
- Put exact substitutes in the reviewed plan before **Build and Run**. Do not
  choose them after seeing results.
- Use more than four visuals only when needed to prevent a misleading summary.
- Derive every performance visual from saved backtest data. An explanatory
  diagram may come from the confirmed plan. Never use decorative or invented
  imagery as evidence.

## 4. Review and authorize the plan

1. Show the complete backtest plan, planned local work and data access,
   future-information answer, known or expected execution differences, other
   limitations, and unresolved implementation-dependent differences.
2. When the future-information answer is Yes, lead with the warning that this
   backtest cannot demonstrate real-time strategy performance. Omit that
   warning only when the answer is No.
3. Offer:

   - **Build and Run** — authorizes only the displayed local build and data
     access.
   - **Revise the Backtest** — returns to affected questions.
   - **Skip Backtesting and Implement on AlphaInsider** — marks backtesting
     Skipped and enters implementation.
   - **Save and Stop** — preserves a Draft plan without authority to build.

4. Apply the selected transition:

   - Build and Run sets Backtest status Authorized and Phase Building backtest.
   - Skip sets Backtest choice and status Skipped, Phase Planning
     implementation, and continues to
     [implement and activate](implement-and-activate.md).
   - Save keeps Backtest status Draft and uses the incomplete handoff in
     [project contract](project-contract.md).

Only **Build and Run** authorizes initial execution of the reviewed plan.

## 5. Build and execute an authorized run

1. Reuse production decision logic or a shared pure decision module when the
   backtest claims to reproduce it.
2. Keep every backtest entry point technically unable to call an AlphaInsider
   order or cancellation operation; mock all trading actions.
3. Process historical data chronologically when future-information use is No.
   When it is Yes, use future information or nonchronological processing only
   as the authorized plan discloses.
4. Run the planned correctness checks.
5. Persist the attempt and its recoverable evidence without replacing an
   earlier run.

For every attempt, save:

- future-information answer and exact limitations;
- strategy, plan, code, and dataset fingerprints;
- dataset identity, retrieval time, cutoff, and any authorized future input;
- assumptions and differences from automated runs;
- changes from earlier backtests;
- exact command and random seed when applicable;
- results, report, visual paths, and visual-rendering failures or repairs;
- disposition and plain reason; and
- either an immutable snapshot of source and configuration or an exact durable
  commit containing both. A fingerprint without recoverable source is
  insufficient.

Exclude `.env`, secret values, private destinations, caches, and unrelated
files from every snapshot. Retain recoverable source, configuration, data
outputs, reports, and visuals until explicit deletion selects them.

### 5.1 Classify the run

Methodology describes what a run can support. Disposition separately describes
whether the run completed correctly:

- **Valid** — measurements and recoverable evidence are complete and
  correctness checks pass. A recorded visual-rendering failure alone does not
  change this disposition.
- **Superseded** — a retained Valid run is no longer featured because a later
  Valid run, strategy revision, or backtest-plan revision replaced it.
- **Failed** — the run stopped early or a defect makes its results
  untrustworthy.

Valid means run integrity, not predictive credibility. Record a plain reason
for Superseded or Failed and never feature Failed evidence.

A run matches the current strategy when it evaluates the confirmed rules under
its authorized plan without silently revising intended behavior. Disclosed
future-information use or a backtest-only substitute does not by itself make
it a different strategy. A newly intended signal, asset rule, sizing rule, or
other trading behavior does.

### 5.2 Preserve and repair visuals

1. Save the outputs required to reproduce every planned visual with the run.
2. If a planned visual fails, make one safe mechanical rendering repair from
   those saved outputs.
3. Record the exact failure and repair attempt whether or not it succeeds.
4. A later repair must use the same outputs, preserve history, and never rerun
   trading logic or change measurements.

A remaining rendering failure does not by itself make trustworthy evidence
Failed or prevent a matching run from becoming Valid.

### 5.3 Manage later runs and revisions

1. Preserve every run and identify assumptions or corrections changed after
   earlier results.
2. When a newer matching Valid run becomes featured, mark the prior featured
   run Superseded with that reason without altering its disclosures or
   artifacts.
3. Before a strategy or backtest-plan revision, mark affected Valid evidence
   Superseded and preserve all of it.
4. If no other Valid result matches the revised strategy and current backtest
   plan, clear the featured result, set the affected backtest plan Draft, and
   return Highest completed outcome to Strategy defined.
5. Treat a strategy-behavior change as a return to
   [define strategy](define-strategy.md), not as a backtest correction.

At results review, the user can authorize a displayed mechanical correction
and rerun inside the same plan. Set Backtest status Authorized, set Phase
Building backtest, and preserve earlier evidence. A plan change returns status
to Draft and requires another review and **Build and Run** choice.

## 6. Present results

1. Set Phase Reviewing results.
2. Identify each attempt as `Backtest <date or ID> — Valid | Superseded |
   Failed` and give its disposition reason.
3. State whether it used information unavailable at the historical decision
   time and what it did and did not reproduce.
4. Put differences and limitations before headline performance and beside
   every affected measurement.
5. Feature the latest Valid run that matches the current strategy; never choose
   the best-performing result.
6. List every earlier, Superseded, and Failed run with its date or ID,
   disposition, future-information use, limitations, link, and reason.
7. State that results do not guarantee future performance.

When future-information use is Yes, begin with the mandatory warning that the
backtest cannot demonstrate real-time strategy performance. Repeat that warning
beside every affected measurement and inside each affected visual, even when
the user requested the method.

### 6.1 Show measurements

Use a compact Markdown table for the main comparison. Define each standard
financial term the first time. Include when applicable:

- equity curve and comparison investment;
- drawdown;
- returns by period, total return, and annualized return;
- volatility and a risk-adjusted return measure;
- trade count, win rate, turnover, fees, and time invested; and
- important assumptions, future information, and data limits.

Separate whether the run followed `plan.md` from profitability. Poor returns do
not make a backtest or strategy fail.

### 6.2 Show saved visual evidence

1. Show the exact planned visuals for the featured run alongside the table,
   limitations, warnings, and plain-language interpretation.
2. Embed saved images when supported; otherwise link directly to each named
   image. A detailed report link alone is not a substitute.
3. Include an earlier diagnostic visual only when it materially improves
   understanding.
4. End with a separate direct link to the detailed report.

Every visual must stand alone with the backtest identity and period, labels and
units, comparison investment when relevant, descriptive alternative text or a
caption, and a one-sentence takeaway. Put each material warning inside the
artifact and beside it in the response.

If a planned visual remains unavailable after its safe repair attempt, state
only that some planned visuals are unavailable. Show all available visuals and
other results normally.

## 7. Record status and choose the next step

1. Record every run under `backtest/` and in `plan.md`.
2. For a matching Valid run, set Backtest status Completed and Highest
   completed outcome Backtest.
3. For a Failed run with no matching Valid evidence, set Backtest status Failed
   without advancing the outcome.
4. When an earlier matching Valid run exists, keep Completed and record the
   later failure separately.
5. Show the reviewed results and offer:

   - **Implement Strategy on AlphaInsider** — enters API access, paper-strategy
     selection, implementation, and automation.
   - **Correct and Rerun the Backtest** — authorizes only a displayed mechanical
     correction inside the same plan, or returns to planning when the plan
     changes.
   - **Revise Strategy and Retest** — returns to affected Define decisions and
     supersedes affected evidence without deleting it.
   - **Save and Stop** — preserves all evidence while creation remains
     incomplete.

Choosing implementation preserves Completed when matching Valid evidence
exists and Failed when none does, then sets Phase Planning implementation and
continues to [implement and activate](implement-and-activate.md).
