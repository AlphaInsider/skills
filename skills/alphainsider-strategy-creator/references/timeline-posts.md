# Timeline Posts

Short updates on the strategy's AlphaInsider timeline after live runs that placed
orders. Off by default; use only when the user or calling agent opts in.

## Enable or disable posts

1. Ask while creating or updating the strategy; recommend based on the user's
   goals. Record the decision and any style changes in `plan.md`.
   - Updating the strategy can change the decision.
2. Create the config. It starts off and never overwrites an existing file:

   ```bash
   python <skill>/scripts/alphainsider_strategy_post.py init --project-root <project>
   ```

3. Set `"post_updates": true` in `<project>/post_updates.json` to enable posts.
   - Set `false` to turn them off; a missing file also means off.
   - `banned_words` and `allowed_terms` replace the defaults when present; edit
     them to change the style rules `check` enforces.
4. [Verify access](credentials.md#verify-access-and-continue) with the setup
   helper's `GET /verifyToken`.
   - Its `scope` must include `newPost`, `getOrders`, `getPositions`,
     `getStrategyValues`, and `getStrategyTimelines`.
   - The key's account must own the strategy.

- When enabled, put these commands with resolved paths and the drafting rules in
  the runbook so scheduled runs need no chat history.

## Post after a run

- Post only after a live run that placed orders, such as a signal or settings
  change. Never post for no-trade runs, dry runs, failed or uncertain runs, or
  strategy creation alone.
- A posting failure never affects trading or triggers recovery. Record it with
  the run outcome and continue; optionally send a `⚠️ Warning — No Action Required`
  notification.

1. After the run's order work and evaluation, inside the run's exclusivity,
   prepare a facts file. Pass every order ID the run placed. Optionally pass a JSON
   object of strategy-specific facts, such as signal readings, reasons, schedule,
   or rule parameters; its numbers and tickers may be used in the draft.

   ```bash
   python <skill>/scripts/alphainsider_strategy_post.py prepare --project-root <project> \
     --strategy-id <strategy-id> --run-id <run-id> --order-id <order-id> \
     [--order-id <order-id> ...] [--context <project>/posts/<run-id>.context.json]
   ```

   - It waits up to `--max-wait` seconds (default 300) for those orders to leave
     the open-order list, then reads positions and strategy value. It sends GET
     requests only.
   - `<run-id>` must match `[A-Za-z0-9._-]{1,100}` and be unique per run.
2. Write `<project>/posts/<run-id>.draft.txt` from `<project>/posts/<run-id>.facts.json`
   following [write the draft](#write-the-draft).
3. Check the draft. Fix every listed problem and recheck until it passes:

   ```bash
   python <skill>/scripts/alphainsider_strategy_post.py check \
     --facts <project>/posts/<run-id>.facts.json --text <project>/posts/<run-id>.draft.txt
   ```

4. Post it:

   ```bash
   python <skill>/scripts/alphainsider_strategy_post.py post --project-root <project> \
     --facts <project>/posts/<run-id>.facts.json --text <project>/posts/<run-id>.draft.txt
   ```

## Write the draft

- Write at least 3 sentences and at most 1,200 characters. Explain what changed
  and why in plain language that fits the strategy.
- Use only numbers and tickers from the facts file, including `context`; `check`
  rejects others. Rounded values and fractions shown as percentages pass.
  - `pct_of_strategy` is each position's signed share of current strategy value;
    shorts are negative. `gross_pct` and `cash_pct` use the same base.
  - Orders that left the open-order list are no longer open, which does not prove
    a fill. Describe the resulting positions instead of claiming fills.
- Default style, which the user may change; record changes in `plan.md` and the
  config:
  - Write in a "we" voice as the strategy's team.
  - Do not mention AI, bots, agents, or automation.
  - Add no disclaimers and mention no other strategies.
- Make each post specific to its run. An identical recent post counts as already
  posted.

## Results and limits

| Exit | Meaning |
| --- | --- |
| 0 | Success. `post` prints a JSON summary; `already_posted: true` means the text was already on the timeline. |
| 1 | `check` found problems, listed one per line. |
| 2 | Invalid arguments, files, configuration, or missing API key. |
| 3 | `no post: <reason>`: posts are off, the run placed no orders, or this run already posted or attempted. |
| 4 | An AlphaInsider request failed; for `post`, after at most one retry. |

- `post` writes `<project>/posts/<run-id>.result.json` and appends a line to
  `<project>/posts/posts.log`.
- `<run-id>.lock` is kept after any send attempt so a run never posts twice, and
  removed when nothing was sent. Do not delete it to retry.
- It retries once only after an ambiguous failure, such as a timeout or server
  error, and only after confirming the text is not already on the timeline.
- AlphaInsider allows 100 successful `/newPost` requests per strategy per day;
  `post` refuses once `posts.log` records 100 in the last 24 hours.
