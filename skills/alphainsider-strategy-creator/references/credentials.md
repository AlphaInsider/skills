# Credentials

## Prepare protected access

- For every API key or secret needed during setup, find the easiest supported way
  for the user to paste it in. Prefer secure, persistent storage that future chats
  and scheduled runs can access. If no suitable storage or easy paste-in method
  is available, ask the user to add it under the required variable name in the
  strategy project's `.env`. Reuse saved credentials without requesting them
  again while access works.
  - Require root `plan.md`; record storage references and access methods there
    and in the runbook, never secret values. Verify protected access from future
    chats and scheduled runs.
  - Never inspect or print existing API keys, `.env` values, or the process
    environment. Programs may load required values internally without exposure.
  - Use supported entry and storage without echoing values. Keep secrets out of
    arguments, shell interpolation, logs, plans, task prompts, version control,
    and exports; preserve unrelated credentials.
  - Restrict access to fallback `.env` files and exclude them from version
    control and exports.
  - Public strategy IDs may be shown and recorded in `plan.md`.
- Resolve bundled CLI helpers from the installed skill directory.
  - [alphainsider_setup_request.py](../scripts/alphainsider_setup_request.py):
    privately injected `ALPHAINSIDER_API_KEY` with project `.env` fallback,
    redacted setup requests, and an allowlist excluding orders.

## Check existing access

- After implementation is chosen, verify access through the setup helper without
  opening `.env`.
  - If access works, continue without requesting the key again.
  - For other services, verify access privately through their configured runtime.

## Request missing credentials

1. Choose the supported entry method and persistent storage for each missing
   secret. Give the user the actual entry method, storage location, required
   variable name, and completion signal.
   - For `.env` fallback, create missing `.env` and `.env.example` files with
     empty assignments for the required names. Preserve existing files without
     reading them; never copy `.env` into `.env.example`.
2. Follow the [user action rule](workflow-contracts.md#resolve-the-current-decisions).
   For a missing AlphaInsider key, adapt this message to the chosen method:

   ```markdown
   👉 **Action — AlphaInsider API key:** Open the [AlphaInsider developer page](https://alphainsider.com/settings/developers),
   select the **AI Agent** preset permissions button, and create an API key.
   Use <selected entry method> to paste it into <selected persistent storage>.
   Tell me when it is saved.

   ↪️ **Alternative:** Set `ALPHAINSIDER_API_KEY` in `<project>/.env`
   yourself, then tell me when it is saved.
   ```

3. Wait for completion, then verify saved access before continuing.

## Verify access and continue

- Verify saved access with the setup helper before implementation questions.
  - Report only safe results.
  - Agent-only command shape:

    ```bash
    python <skill>/scripts/alphainsider_setup_request.py --project-root <project> GET /verifyToken
    ```

- Runtime code must load only required secrets privately through the recorded
  access method, with project `.env` as fallback, and redact diagnostics.
  - Resolve authentication inside the request process without exposing secrets.
