# Reusable Python runtime

Use `scripts/runtime/` when an integration needs importable REST and WebSocket
clients rather than one-off requests through `alphainsider_request.py`.

- `client.py` provides `AlphaInsiderClient`, normalized-value conversion,
  response-envelope validation, rate-limit errors, positions, orders,
  allocations, timelines, stock lookup, and strategy calculations.
- `stream.py` provides `AlphaInsiderStream` for strategy value, order,
  position, and timeline channels.
- `client.py` also owns environment loading: process values win and missing
  values may be filled from a working-directory `.env`.

The package is self-contained. A generator may copy and rename these modules,
but must preserve the credential boundary and update relative imports. Never
run network calls from automated tests; inject mock HTTP and WebSocket
transports instead.
