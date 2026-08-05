# Users Endpoints

REST base URL: `https://alphainsider.com/api`.

Public user lookup and authenticated user profile settings.

## getUsers - GET `/getUsers`

Get public user information.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| query | `user_id[]` | Yes | array of string (max 100) | Array of user IDs. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].info` | object | Profile information object. |
| `response[].info.bio` | string | User profile biography. |
| `response[].info.x` | string | X/Twitter profile URL. |
| `response[].info.website` | string | Website URL. |
| `response[].info.youtube` | string | YouTube profile URL. |
| `response[].info.telegram` | string | Telegram profile URL. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].post_count` | string | Number of public posts. |
| `response[].like_count` | string | Number of likes. |
| `response[].subscriber_count` | string | Number of subscribers. |
| `response[].strategy_count` | string | Number of strategies. |

Example request:

```http
GET /getUsers?user_id[]=user_1
```

## getUserInfo - GET `/getUserInfo`

Get private user information.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.email` | string | User email address. |
| `response.info` | object | Profile information object. |
| `response.info.bio` | string | User profile biography. |
| `response.info.x` | string | X/Twitter profile URL. |
| `response.info.website` | string | Website URL. |
| `response.info.youtube` | string | YouTube profile URL. |
| `response.info.telegram` | string | Telegram profile URL. |
| `response.commission` | integer | User commission percentage or amount as returned by AlphaInsider. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.payments_enabled` | boolean | Whether payments are enabled for the user. |
| `response.verified` | boolean | Whether the user is verified. |
| `response.ref_id` | string | Referral identifier. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
GET /getUserInfo
Authorization: <API_TOKEN>
```

## updateUserInfo - POST `/updateUserInfo`

Update user profile information.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `bio` | No | string | Bio description. |
| body | `youtube` | No | string (url) | Youtube link. |
| body | `x` | No | string (url) | X link. |
| body | `telegram` | No | string (url) | Telegram link. |
| body | `website` | No | string (url) | Website link. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.email` | string | User email address. |
| `response.info` | object | Profile information object. |
| `response.info.bio` | string | User profile biography. |
| `response.info.x` | string | X/Twitter profile URL. |
| `response.info.website` | string | Website URL. |
| `response.info.youtube` | string | YouTube profile URL. |
| `response.info.telegram` | string | Telegram profile URL. |
| `response.commission` | integer | User commission percentage or amount as returned by AlphaInsider. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.payments_enabled` | boolean | Whether payments are enabled for the user. |
| `response.verified` | boolean | Whether the user is verified. |
| `response.ref_id` | string | Referral identifier. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateUserInfo
Authorization: <API_TOKEN>
Content-Type: application/json

{"bio":"Systematic long-term strategies","website":"https://example.com"}
```

## updateUserNotifications - POST `/updateUserNotifications`

Update user notification settings.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `notifications` | Yes | array of string | Array of notification settings. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.email` | string | User email address. |
| `response.info` | object | Profile information object. |
| `response.info.bio` | string | User profile biography. |
| `response.info.x` | string | X/Twitter profile URL. |
| `response.info.website` | string | Website URL. |
| `response.info.youtube` | string | YouTube profile URL. |
| `response.info.telegram` | string | Telegram profile URL. |
| `response.commission` | integer | User commission percentage or amount as returned by AlphaInsider. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.payments_enabled` | boolean | Whether payments are enabled for the user. |
| `response.verified` | boolean | Whether the user is verified. |
| `response.ref_id` | string | Referral identifier. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example request:

```http
POST /updateUserNotifications
Authorization: <API_TOKEN>
Content-Type: application/json

{"notifications":["subscription","subscription_email"]}
```
