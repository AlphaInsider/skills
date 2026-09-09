# Credentials

## Prepare protected access

- Store secrets in the selected project's `.env`; require root `plan.md`.
  - Never inspect or print existing API keys, `.env` values, or the process
    environment. Programs may load required values internally without exposure.
  - Exclude `.env` from version control and exports; use this boundary for
    notification and other project secrets too.
  - Public strategy IDs may be shown and recorded in `plan.md`.
- Resolve bundled CLI helpers from the installed skill directory.
  - [set_env_value.py](../scripts/set_env_value.py): non-echoing writes, preserved
    unrelated assignments, restricted permissions; required for deliberate
    chat-supplied secrets.
  - [alphainsider_setup_request.py](../scripts/alphainsider_setup_request.py):
    project `.env` configuration, redacted setup requests, and an allowlist
    excluding orders.

## Check existing access

- After implementation is chosen, verify access through the setup helper without
  opening `.env`.
  - If access works, continue without requesting the key again.

## Request a missing key

1. Create missing project `.env` and `.env.example` files
   containing `ALPHAINSIDER_API_KEY=`. Preserve existing files without reading
   them; never copy `.env` into `.env.example`.
2. Follow the [user action rule](workflow-contracts.md#resolve-the-current-decisions)
   and send:

   ```markdown
   👉 **Action — AlphaInsider API key:** Open the [AlphaInsider developer page](https://alphainsider.com/settings/developers),
   select the **AI Agent** preset permissions button, and create an API key.
   Paste it here. I'll save it in your project's `.env` without repeating it.

   ↪️ **Alternative:** Set `ALPHAINSIDER_API_KEY` in `<project>/.env`
   yourself, then tell me when it is saved.
   ```

3. Wait for the pasted key or confirmation of the direct edit before continuing.

## Save chat input

- Invoke the writer with the variable name and `--project-root`.
  - Supply the value through protected, non-echoing standard input.
  - Never put it in arguments, shell interpolation, logs, plans, or task prompts.
  - If input would echo, use direct editing.
  - Agent-only command shape:

    ```bash
    python <skill>/scripts/set_env_value.py --project-root <project> ALPHAINSIDER_API_KEY
    ```

## Verify access and continue

- Verify saved access with the setup helper before implementation questions.
  - Report only safe results.
  - Agent-only command shape:

    ```bash
    python <skill>/scripts/alphainsider_setup_request.py --project-root <project> GET /verifyToken
    ```

- Runtime code must load project `.env` privately and redact secrets from diagnostics.
  - Never expose existing secrets to wire API calls.
