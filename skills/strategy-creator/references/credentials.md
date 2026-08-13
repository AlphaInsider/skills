# Credential Setup

Read this reference only when a required credential or configuration value is
missing. Never inspect or print existing `.env` values.

For each missing value:

1. Name it and show the selected project's exact `.env` path without opening
   the file.
2. Recommend that the user add the values to `.env` themselves and tell you
   when ready.
3. If the user wants agent-assisted entry instead, they may paste the values in
   chat. Warn once, before entry, that pasting credentials is less secure
   because the value is visible to the agent and may appear in tool metadata or
   a transient process listing. Accept a bare value for one variable or one
   `NAME=value` line per variable for several.
4. Pasted values grant approval to update only those names. Never echo, quote,
   summarize, log, or record values in plans, `.env.example`, source, tests,
   or documentation. Use each value in only the exact helper invocation below.
5. From the project root, launch this exact agent-only CLI, once per name:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py NAME VALUE
   ```

   Replace `NAME` and `VALUE`; pass the complete value as exactly one argument.
   Prefer a structured argument-array process call. When only a shell command
   is available, quote the value as one literal argument so its contents cannot
   be interpreted by the shell. Never show this command to the user or ask them
   to run it. Never import the helper, call its functions, reproduce its write
   logic, or supply a value through a shell pipeline, redirect, heredoc, inline
   script, environment or shell variable, command substitution, temporary
   file, patch, direct `.env` edit, or clipboard. Do not open `.env` before or
   after the update. The helper preserves other entries.
6. If the pasted value remains available in the active task, use it once at the
   helper without requesting another approval. If it is unavailable, ask the
   user to enter it again or edit `.env`; never recover it from `.env`. If a
   runtime cannot pass it as one safely quoted argument, return to the user-edit
   workflow. Do not improvise another write path. Defer the affected setup only
   when the user declines or cannot complete that workflow.
7. Rerun the non-ordering check. For AlphaInsider configuration, use the sibling
   request helper and report only the result, never credentials. Strategy IDs
   and other non-secret values may be reported when the user supplied them,
   explicitly asks for them, or confirmed the plan that created them.

A missing API key is a setup gap, not a strategy decision. A non-local-only
`ALPHAINSIDER_API_KEY` must pass the target reference's permission gate before
remote work. If it cannot pass during forward-test setup, record the target as
local-only and continue only with backtesting planning and local offline
implementation. A missing `ALPHAINSIDER_STRATEGY_ID` is not a credential
failure; follow `alphainsider-target.md`. Selecting an existing strategy
authorizes writing its ID through the non-echoing helper. Complete plan
confirmation is the sole authorization to write an ID returned by
`newStrategy`.

A missing credential required by another selected data source pauses that
affected branch until the user supplies it or selects a feasible alternative.

Generated `README.md` files must preserve user editing as the preferred setup
and identify chat entry and command transport as the less-secure agent-assisted
fallback, but never show the helper command. Generated `AGENTS.md` files must
point at the installed skill for the write path and never show the helper.
`--remove NAME` receives no value and is also agent-only. Removing a saved
strategy binding uses `--remove ALPHAINSIDER_STRATEGY_ID`.
