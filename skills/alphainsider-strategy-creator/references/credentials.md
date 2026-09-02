# Credentials and Configuration

Read this file only when a required value is missing. Never inspect, print, or
summarize an existing API key, complete `.env`, process environment, or hosted
secret store.

Require this skill's `scripts/set_env_value.py` and
`scripts/alphainsider_setup_request.py` before project-file credential or
target setup. If either is missing, stop only that phase and reinstall Strategy
Creator. Do not improvise another secret-write or setup-request path.

Do not request `ALPHAINSIDER_API_KEY` before the user chooses AlphaInsider
forward testing. Link to
[AlphaInsider developer settings](https://alphainsider.com/settings/developers).
Recommend the **AI Agent** permission preset because future plan changes can
need additional AlphaInsider functions. A narrower key is acceptable when its
current permissions cover every planned setup and runtime operation.

## Choose secret storage

Use the project `.env` when both the current agent and scheduled runtime can
load it. Use the platform's secure non-prompt secret storage when a hosted
runtime cannot access the project `.env`. Never place a secret in a scheduler
instruction, plan, source file, example, test, log, or notification.

`ALPHAINSIDER_STRATEGY_ID` is public configuration, but store it through the
same helper or the selected hosted configuration facility.

## Chat-first setup

For project `.env` storage, use one standalone action:

```markdown
👉 **Action — Add AlphaInsider API key:** Paste the API key in this chat.

Pasting gives this active chat and agent access so the key can be stored
without displaying it.

↪️ **Alternative:** Add `ALPHAINSIDER_API_KEY` directly to the announced
project `.env`, then reply `ready`.
```

Request only missing names. Accept a bare value when one name is pending, or
clear `NAME=value` entries for several names. If the mapping is unclear, ask
one focused clarification. Do not echo or restate any value.

Pasted values authorize updates only to the requested names. Write each value
with the installed `scripts/set_env_value.py` helper. Pass:

```text
python /absolute/skill/path/scripts/set_env_value.py --project-root /absolute/project NAME
```

Supply the value through protected standard input or the helper's non-echoing
prompt. Never put it in a command argument, shell variable, environment
assignment, pipeline, redirect, heredoc, temporary file, patch, or another
write path. Do not show the helper command to the user. If protected input is
not available, use direct user editing or hosted secret storage.

The helper must:

- require the exact project root with a root `plan.md`;
- reject installed-skill directories and symbolic-link `.env` files;
- atomically preserve unrelated entries;
- enforce owner-only `0600` permissions; and
- reveal only the updated variable name and file path.

Never open `.env` before or after the write. Do not import or reproduce the
helper's write logic.

## Safe AlphaInsider setup requests

Use `scripts/alphainsider_setup_request.py` only for the setup operations
allowed by that helper. Always pass the exact `--project-root`. It can load the
API key privately from process injection or project `.env` and can print only
the public `ALPHAINSIDER_STRATEGY_ID` configuration value.

Use request bodies through protected standard input when they contain a private
value. Report only the redacted result. Never use this setup helper for an
order, allocation, cancellation, or another trading action.

Verify `GET /verifyToken` and require an API token with the plan's needed
permissions. List only missing permission names. Accept extra permissions
without requiring replacement or rotation. Deliberate chat entry is not by
itself a reason to rotate the key.

If a value is no longer available to the active chat, ask for it again or use
the direct-edit method. Never recover it by reading `.env`. A hosted secret
facility remains user-managed; give exact platform steps and wait for the
completion signal when the agent cannot write it safely.
