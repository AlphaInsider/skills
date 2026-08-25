# Authentication Endpoints

REST base URL: `https://alphainsider.com/api`.

Token verification for AlphaInsider API credentials.

## verifyToken - POST `/verifyToken`

Verify that an API token is valid.

Provide the API token as the exact `Authorization` header value. Do not add a `Bearer` prefix.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token to verify, sent exactly as the header value. |

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

Example request:

```http
POST /verifyToken
Authorization: <API_TOKEN>
```
