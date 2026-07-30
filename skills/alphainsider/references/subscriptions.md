# Subscriptions Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Strategy subscriptions, relative calculations, account tiers, and account subscription changes.

Read `input-multiplier.md` for how `input_value`, `input_date`, `input_multiplier`, and `strategy_value` control user-facing strategy values, positions, orders, and performance.

## getStrategySubscriptions - GET `/getStrategySubscriptions`

Get strategy subscriptions.

Note: `input_multiplier` from this response is the preferred value for converting normalized strategy values to user-facing USD or user-visible share/crypto amounts.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id[]` | No | array of string (max 100) | One or more strategy IDs. Repeat this query parameter for multiple strategies. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].strategy_owner` | string | User ID of the strategy owner. |
| `response[].type` | string | Type or category for this object. |
| `response[].private` | boolean | Whether the strategy is private. |
| `response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].invoice_id` | null or value | Invoice identifier, when one exists. |
| `response[].end_date` | null or value | End timestamp for the current period or range. |
| `response[].subscription_id` | string | Strategy subscription identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].input_value` | string | User-provided starting value for relative strategy calculations. |
| `response[].input_date` | string | Starting timestamp for relative strategy calculations. |
| `response[].input_multiplier` | string | Multiplier for converting normalized strategy units to user-facing USD values. |
| `response[].notifications` | array | Enabled notification types. |
| `response[].renew` | boolean | Whether the subscription renews. |
| `response[].status` | string | Current status. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategySubscriptions
```

## newStrategySubscription - POST `/newStrategySubscription`

New strategy subscription.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.strategy_owner` | string | User ID of the strategy owner. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.strategy_value` | null or value | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response.invoice_id` | null or value | Invoice identifier, when one exists. |
| `response.end_date` | null or value | End timestamp for the current period or range. |
| `response.subscription_id` | string | Strategy subscription identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.input_value` | null or value | User-provided starting value for relative strategy calculations. |
| `response.input_date` | null or value | Starting timestamp for relative strategy calculations. |
| `response.input_multiplier` | null or value | Multiplier for converting normalized strategy units to user-facing USD values. |
| `response.notifications` | array | Enabled notification types. |
| `response.renew` | boolean | Whether the subscription renews. |
| `response.status` | string | Current status. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py POST /newStrategySubscription
```

## deleteStrategySubscription - POST `/deleteStrategySubscription`

Unsubscribe from strategy.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py POST /deleteStrategySubscription
```

## updateStrategySubscriptionNotifications - POST `/updateStrategySubscriptionNotifications`

Set which notifications to receive from a strategy.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `notifications` | Yes | array of string | Which notification types to receive. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.strategy_owner` | string | User ID of the strategy owner. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response.invoice_id` | null or value | Invoice identifier, when one exists. |
| `response.end_date` | null or value | End timestamp for the current period or range. |
| `response.subscription_id` | string | Strategy subscription identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.input_value` | string | User-provided starting value for relative strategy calculations. |
| `response.input_date` | string | Starting timestamp for relative strategy calculations. |
| `response.input_multiplier` | string | Multiplier for converting normalized strategy units to user-facing USD values. |
| `response.notifications` | array of string | Enabled notification types. |
| `response.renew` | boolean | Whether the subscription renews. |
| `response.status` | string | Current status. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py POST /updateStrategySubscriptionNotifications \
  --json '{"notifications":["trade","post"]}'
```

## getStrategyCalculation - GET `/getStrategyCalculation`

Get relative strategy calculations.

Note: Use this to calculate `input_multiplier` from a user-provided starting value and date. See `input-multiplier.md` before using the result for display or order sizing.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id` | Yes | string | Strategy ID. |
| query | `input_value` | Yes | number | Relative starting balance. |
| query | `input_date` | Yes | string (date-time) | Input value starting date. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.input_value` | string | User-provided starting value for relative strategy calculations. |
| `response.input_date` | string | Starting timestamp for relative strategy calculations. |
| `response.input_multiplier` | string | Multiplier for converting normalized strategy units to user-facing USD values. |
| `response.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategyCalculation \
  --query "input_value=10000" \
  --query "input_date=2026-01-01T00:00:00Z"
```

## updateStrategyCalculation - POST `/updateStrategyCalculation`

Update relative strategy calculations.

Note: Use this to persist a relative calculation for a subscribed strategy. The returned `input_multiplier` is the saved conversion value for user-facing display.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `input_value` | Yes | number | Relative starting balance. |
| body | `input_date` | Yes | string (date-time) | Input value starting date. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.strategy_owner` | string | User ID of the strategy owner. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response.invoice_id` | null or value | Invoice identifier, when one exists. |
| `response.end_date` | null or value | End timestamp for the current period or range. |
| `response.subscription_id` | string | Strategy subscription identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.input_value` | string | User-provided starting value for relative strategy calculations. |
| `response.input_date` | string | Starting timestamp for relative strategy calculations. |
| `response.input_multiplier` | string | Multiplier for converting normalized strategy units to user-facing USD values. |
| `response.notifications` | array | Enabled notification types. |
| `response.renew` | boolean | Whether the subscription renews. |
| `response.status` | string | Current status. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py POST /updateStrategyCalculation \
  --json '{"input_value":"10000","input_date":"2026-01-01T00:00:00Z"}'
```

## deleteStrategyCalculation - POST `/deleteStrategyCalculation`

Delete relative strategy calculation.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py POST /deleteStrategyCalculation
```

## getAccountTiers - GET `/getAccountTiers`

Get all account subscription tiers.

Note: Use this to inspect account-level limits and prices before creating strategies, bots, or many orders.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| - | - | - | - | No inputs. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].timeframe` | string | Time window used for ranking or performance data. |
| `response[].level` | integer | Subscription tier level. |
| `response[].name` | string | Display name. |
| `response[].apiTokenExpire` | integer | API token expiration period in milliseconds. |
| `response[].limits` | object | Account or tier operational limits. |
| `response[].limits.new_order` | integer | Maximum successful `/newOrder` requests per day per strategy. |
| `response[].limits.max_strategies` | integer | Maximum number of strategies the account can create. |
| `response[].limits.max_subscriptions` | integer | Maximum number of strategy subscriptions. |
| `response[].limits.max_bots` | integer | Maximum number of bots. |
| `response[].price` | integer | Price or execution price, depending on context. |

Example:

```bash
python scripts/alphainsider_request.py GET /getAccountTiers
```

## getAccountSubscription - GET `/getAccountSubscription`

Get account subscription.

Note: The `limits` object is the authenticated account's active operational limits.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.account_subscription_id` | string | Account subscription identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.status` | string | Current status. |
| `response.product_id` | string | Billing product identifier. |
| `response.type` | string | Type or category for this object. |
| `response.timeframe` | string | Time window used for ranking or performance data. |
| `response.level` | integer | Subscription tier level. |
| `response.name` | string | Display name. |
| `response.next_product_id` | string | Next billing product identifier after a pending change. |
| `response.next_type` | string | Next account subscription type after a pending change. |
| `response.next_timeframe` | string | Next subscription billing timeframe after a pending change. |
| `response.next_level` | integer | Next subscription tier level after a pending change. |
| `response.next_name` | string | Next account subscription display name after a pending change. |
| `response.invoice_id` | null or value | Invoice identifier, when one exists. |
| `response.limits` | object | Account or tier operational limits. |
| `response.limits.new_order` | integer | Maximum successful `/newOrder` requests per day per strategy. |
| `response.limits.new_post` | integer | Maximum successful `/newPost` requests per day per strategy. |
| `response.limits.like` | integer | Maximum successful `/like` requests per day. |
| `response.limits.max_sessions` | integer | Maximum number of active sessions. |
| `response.limits.max_api_tokens` | integer | Maximum number of API tokens. |
| `response.limits.max_strategies` | integer | Maximum number of strategies the account can create. |
| `response.limits.max_subscriptions` | integer | Maximum number of strategy subscriptions. |
| `response.limits.max_open_orders` | integer | Maximum number of open orders per strategy. |
| `response.limits.max_bots` | integer | Maximum number of bots. |
| `response.end_date` | null or value | End timestamp for the current period or range. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py GET /getAccountSubscription
```

## updateAccountSubscription - POST `/updateAccountSubscription`

Update account subscription.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `type` | Yes | string: `standard`, `pro`, `premium` | Account subscription tier. |
| body | `timeframe` | Yes | string: `month`, `year` | Account subscription timeframe. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.account_subscription_id` | string | Account subscription identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.status` | string | Current status. |
| `response.product_id` | string | Billing product identifier. |
| `response.type` | string | Type or category for this object. |
| `response.timeframe` | string | Time window used for ranking or performance data. |
| `response.level` | integer | Subscription tier level. |
| `response.name` | string | Display name. |
| `response.next_product_id` | string | Next billing product identifier after a pending change. |
| `response.next_type` | string | Next account subscription type after a pending change. |
| `response.next_timeframe` | string | Next subscription billing timeframe after a pending change. |
| `response.next_level` | integer | Next subscription tier level after a pending change. |
| `response.next_name` | string | Next account subscription display name after a pending change. |
| `response.invoice_id` | string | Invoice identifier, when one exists. |
| `response.limits` | object | Account or tier operational limits. |
| `response.limits.new_order` | integer | Maximum successful `/newOrder` requests per day per strategy. |
| `response.limits.new_post` | integer | Maximum successful `/newPost` requests per day per strategy. |
| `response.limits.like` | integer | Maximum successful `/like` requests per day. |
| `response.limits.max_sessions` | integer | Maximum number of active sessions. |
| `response.limits.max_api_tokens` | integer | Maximum number of API tokens. |
| `response.limits.max_strategies` | integer | Maximum number of strategies the account can create. |
| `response.limits.max_subscriptions` | integer | Maximum number of strategy subscriptions. |
| `response.limits.max_open_orders` | integer | Maximum number of open orders per strategy. |
| `response.limits.max_bots` | integer | Maximum number of bots. |
| `response.end_date` | null or value | End timestamp for the current period or range. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py POST /updateAccountSubscription \
  --json '{"type":"pro","timeframe":"month"}'
```
