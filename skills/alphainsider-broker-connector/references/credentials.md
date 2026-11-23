# Credentials

## Prepare protected access

- Reuse working credentials through the current runtime's supported storage and
  access mechanism. When a credential is missing or needs replacement, use the
  easiest supported secure entry method, such as a masked secret card or settings
  form. A protected input displayed within chat is appropriate when the value
  stays outside the conversation transcript and model context. Never request the
  value in an ordinary chat message.
  - Keep one authoritative storage location for each credential. Prefer secure,
    persistent storage that future chats and scheduled runs can access.
  - Record storage references and access methods in `plan.md` and the runbook in
    `connection.md`, never secret values. Verify access in the current chat and
    confirm from the runtime's guidance that future chats and scheduled runs can
    use the same storage; the first scheduled run confirms it.
  - Use supported credential injection or private runtime loading without
    creating additional persistent copies.
  - Use a protected project `.env` only when no suitable supported credential
    storage and access method is available. Create fallback files only when that
    method is selected.
  - Never inspect or print existing API keys, passwords, tokens, `.env` values,
    or the process environment. Programs may load required values internally
    without exposure.
  - Keep secrets out of arguments, shell interpolation, URLs, logs,
    `connection.db`, plans, task prompts, version control, and exports; preserve
    unrelated credentials.
  - Restrict access to fallback `.env` files and exclude them from version
    control and exports.
  - Public strategy IDs and non-secret broker account identifiers may be shown
    and recorded.

## Broker credentials and sessions

The user chooses the access method from the
[broker research](broker-contract.md#access). Store what that method needs:

- API keys and secrets, or OAuth client details with access and refresh tokens.
- Login credentials (username and password) when the runtime offers secure
  persistent storage. When it does, store and use them. Never put passwords in a
  `.env` fallback; without secure storage, a re-login needs the user.
- An authenticator (TOTP) secret only if the user chooses to provide one, in
  secure storage only.

Fill login forms through supported secure autofill or a program that loads the
secret privately; never place a secret in model-visible tool arguments.

For browser logins, keep one dedicated persistent browser profile shared by the
agent and any scripts, protected like a credential. Scripts reuse its session
and stop with a clear "login needed" result at a login or challenge page; the
agent then completes the login in that same profile and continues the run.

Keep the connection running without the user whenever possible. When access
fails:

1. Reuse the current session or access token if it is still valid.
2. Refresh it the way the broker's own web or app client does, such as a refresh
   token or session renewal.
3. Log in again with the stored credentials and complete any MFA the stored
   credentials allow.
4. Only when every option is exhausted (for example a push or SMS approval,
   CAPTCHA, new-device check, locked account, or changed password), pause the
   connection and send `🚨 Error — Action Required` following
   [recovery](run-and-recover.md#recover-from-an-error).

Store refreshed tokens back to the same authoritative storage. Record only the
outcome and time in `connection.db`.

## Check existing access

- After the access method is chosen, [verify access](#verify-access-and-continue)
  without opening `.env`.
  - If access works and the account is confirmed, continue without requesting
    credentials again.
  - Verify broker access privately through its configured runtime and report only
    safe results, such as account type and non-secret account identifier.

## Request missing credentials

1. Choose the supported entry method and persistent storage for each missing
   secret. Give the user the actual entry method, storage location, required
   variable name, and completion signal.
   - Only when `.env` fallback is selected, create missing `.env` and
     `.env.example` files with empty assignments for the required names. Preserve
     existing files without reading them; never copy `.env` into `.env.example`.
2. Follow the [user action rule](workflow-contracts.md#resolve-the-current-decisions).
   For a missing AlphaInsider key, adapt this message to the chosen secure entry
   method. Offer project `.env` only when fallback is needed:

   ```markdown
   👉 **Action — AlphaInsider API key:** Open the [AlphaInsider developer page](https://alphainsider.com/settings/developers),
   select the **AI Agent** preset permissions button, and create an API key.
   Use <selected entry method> to paste it into <selected persistent storage>.
   Tell me when it is saved.
   ```

   For broker credentials, give the broker's own steps for creating keys or
   approving the login, then the same entry method and completion signal.
3. Wait for completion, then verify saved access before continuing.

## Verify access and continue

- Call the AlphaInsider API directly with curl or any HTTP client at
  `https://alphainsider.com/api`. Send the raw `ALPHAINSIDER_API_KEY` in the
  `Authorization` header, with no `Bearer` prefix. Follow the hosted
  [API skill](https://api.alphainsider.com/skill.md) and
  [authentication guide](https://api.alphainsider.com/resources/introduction.md#authentication-and-requests).
- Verify saved access with `GET /verifyToken`, which shows the key's scopes,
  before allocation questions. Report only safe results.
  - Show the returned `user_id` and token `name`, and have the user confirm the
    account is theirs before continuing. Record the confirmed `user_id` in `plan.md`.
  - In later chats and scheduled runs, compare the returned `user_id` with the
    recorded one. If they differ, stop before any AlphaInsider action and ask the
    user; scheduled runs pause and send the action-required notification.
  - Load the key from the runtime's injected environment without printing it or
    putting it in arguments, for example:

    ```bash
    printf 'Authorization: %s\n' "$ALPHAINSIDER_API_KEY" |
      curl -sS -H @- https://alphainsider.com/api/verifyToken
    ```

  - With `.env` fallback, load it in a subshell:
    `(set -a; . <project>/.env; set +a; <command>)`.
- Gotchas:
  - `/getStrategyValues` and `/getStrategyTimelines` take `strategy_id[]`;
    `/getPositions` takes a single `strategy_id`.
  - Absence from `/getOrders` does not prove a fill.
- Runtime code must use only required credentials through the recorded injection
  or private loading method, without additional persistent copies, and redact
  diagnostics.

## Rotate credentials

- For a requested rotation, replace the credential through its authoritative
  store's supported entry method. Refresh or restart the affected runtime as
  required, then verify replacement access in the actual runtime before
  continuing. Retire the previous credential after the next scheduled run
  succeeds.
  - Keep the plan and runbook limited to storage references, access methods, and
    verification status; do not synchronize credential copies.
