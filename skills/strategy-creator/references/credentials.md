# Credential Setup

Read this reference only when a required credential or configuration value is
missing. Never inspect or print existing `.env` values.

For each missing value:

1. Name it and show the selected project's exact `.env` path without opening
   the file.
2. Recommend that the user add the values to `.env` themselves and tell you
   when ready.
3. If the user wants agent-assisted entry instead, they may paste the values in
   chat. Warn first that pasting credentials is less secure because the value
   is visible to the agent. Accept a bare value for one variable or one
   `NAME=value` line per variable for several.
4. Pasted values grant approval to update only those names. Never echo, quote,
   summarize, log, or record values in plans, `.env.example`, source, tests,
   documentation, or command arguments.
5. From the project root, launch this exact CLI-only helper in an interactive
   terminal, once per name:

   ```bash
   python /absolute/path/to/strategy-creator/scripts/set_env_value.py NAME
   ```

   Wait until its non-echoing prompt appears, then enter the deliberately
   pasted value. Never import the helper, call its functions, reproduce its
   write logic, or supply a value through a command argument, pipe, redirect,
   heredoc, inline script, environment or shell variable, command substitution,
   temporary file, or clipboard. Do not open `.env` before or after the update.
   Never pass a credential in a command argument. The helper preserves other
   entries.
6. If the pasted value remains available in the active task, use it once at the
   prompt without requesting another approval. If it is unavailable, ask the
   user to enter it again or edit `.env`; never recover it from `.env`. If a
   secure interactive terminal is unavailable, stop agent-assisted entry and
   have the user edit `.env` themselves. Do not improvise another write path.
7. Rerun the non-ordering check. For AlphaInsider configuration, use the sibling
   request helper and report only the result, never credentials. Strategy IDs
   and other non-secret values may be reported when the user supplied them,
   explicitly asks for them, or confirmed the plan that created them.

A missing API key is a setup gap, not a strategy decision. A non-deferred
`ALPHAINSIDER_API_KEY` must pass the target reference's permission gate before
remote work. If it cannot pass during forward-test setup, defer the target and
continue only with backtesting planning and local offline implementation. A
missing `ALPHAINSIDER_STRATEGY_ID` is not a credential failure; follow
`alphainsider-target.md`. Selecting an existing strategy authorizes writing its
ID through the non-echoing helper. Complete plan confirmation is the sole
authorization to write an ID returned by `newStrategy`.

A missing credential required by another selected data source pauses that
affected branch until the user supplies it or selects a feasible alternative.

Generated `README.md` and `AGENTS.md` files must preserve the CLI-only command,
interactive non-echoing prompt, prohibited bypasses, no-repeat-approval rule,
and manual-edit fallback above. `--remove NAME` may run without an interactive
terminal because it receives no value.
