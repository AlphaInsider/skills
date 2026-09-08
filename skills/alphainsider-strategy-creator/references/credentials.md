# Credentials

Secrets belong in the selected project's `.env`. Agents never inspect or print
existing API keys, `.env` values, or the process environment. Programs may load
required values internally without exposing them. Public strategy IDs may be
shown and recorded in `plan.md`.

Use the bundled helpers as CLI tools; they keep secret handling out of the
agent's output. Resolve their paths from the installed skill directory:

- [set_env_value.py](../scripts/set_env_value.py) writes a value through
  non-echoing input, preserving unrelated assignments and restricting file
  permissions. Use it for all deliberate chat-supplied secret values.
- [alphainsider_setup_request.py](../scripts/alphainsider_setup_request.py)
  loads configuration from the selected project's `.env`, makes supported
  setup requests, and redacts credentials. Its allowlist excludes orders.

On resume, use the setup helper to verify configured access without opening
`.env`; do not ask for a key again if access works. When a key is needed, follow
the [user action rule](workflow-contracts.md#interview-and-communication) and send:

```markdown
👉 **Action — AlphaInsider API key:** Create an API key in AlphaInsider's
Developer settings with the access needed for this strategy, and paste it
here. I'll save it in your project's `.env` without repeating it.

↪️ **Alternative:** Add `ALPHAINSIDER_API_KEY=your_key` to `<project>/.env`
yourself, then tell me when it is saved.
```

Wait for the pasted key or confirmation of the direct edit. Save chat input
as below and verify access before continuing with implementation questions.

For chat entry, run the writer with the variable name and `--project-root`,
supplying the value through protected, non-echoing standard input. Never put
it in command arguments, shell interpolation, logs, plans, or task prompts.
If the tool cannot supply input without echoing, use direct editing instead.

Agent-only command shapes (the writer receives the secret separately):

```bash
python <skill>/scripts/set_env_value.py --project-root <project> ALPHAINSIDER_API_KEY
python <skill>/scripts/alphainsider_setup_request.py --project-root <project> GET /verifyToken
```

The project must already contain `plan.md`. Keep `.env` out of version control
and exports. Validate access through the helper, reporting only safe results.
Use the same storage boundary for notification and other project secrets.
Generated runtime code must load project `.env` privately and redact secret
values from diagnostics; never expose an existing value to the agent to wire
an API call.
