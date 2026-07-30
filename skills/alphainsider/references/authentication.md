# Authentication Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Token verification for AlphaInsider API credentials.

## verifyToken - POST `/verifyToken`

Verify that an API token is valid.

Note: This endpoint sends the token in the JSON body as `token`; do not send an `Authorization` header.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| body | `token` | Yes | string (JWT) | AlphaInsider API token to verify. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.token_id` | string | Identifier for the verified API token. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.holder` | string | User or entity that holds the token. |
| `response.type` | string | Type or category for this object. |
| `response.name` | string | Display name. |
| `response.scope` | array of string | Permissions granted to the token. |

Example:

```bash
python scripts/alphainsider_request.py POST /verifyToken
```
