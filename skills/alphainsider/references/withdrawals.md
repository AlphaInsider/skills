# Withdrawals Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Balances, payouts, payout fees, income, and Stripe account links.

## getUserBalance - GET `/getUserBalance`

Get user balance.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.balance` | string | Available balance data. |
| `response.amount_on_hold` | string | Amount on hold. |
| `response.amount_available` | string | Amount available. |

Example:

```bash
python scripts/alphainsider_request.py GET /getUserBalance
```

## getPayouts - GET `/getPayouts`

Get payouts.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `limit` | No | number | Number of results to return. |
| query | `offset_id` | No | string | Offet by ID. Used for pagination. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].payout_id` | string | Payout identifier. |
| `response[].provider` | string | External provider or data provider. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].amount` | string | Amount. |
| `response[].fee` | string | Fee value. |
| `response[].destination` | object | Payout destination details. |
| `response[].status` | string | Current status. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py GET /getPayouts \
  --query "limit=20"
```

## newPayout - POST `/newPayout`

New payout.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `amount` | Yes | number (int) | Order amount, position amount, or withdrawal amount depending on endpoint. See endpoint notes. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.payout_id` | string | Payout identifier. |
| `response.provider` | string | External provider or data provider. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.type` | string | Type or category for this object. |
| `response.amount` | string | Amount. |
| `response.fee` | string | Fee value. |
| `response.destination` | object | Payout destination details. |
| `response.status` | string | Current status. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |

Example:

```bash
python scripts/alphainsider_request.py POST /newPayout \
  --json '{"amount":1000}'
```

## getPayoutFees - GET `/getPayoutFees`

Get withdrawal payout fees.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `amount` | Yes | number (int) | Order amount, position amount, or withdrawal amount depending on endpoint. See endpoint notes. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py GET /getPayoutFees \
  --query "amount=1000"
```

## getIncome - GET `/getIncome`

Get income.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `interval` | Yes | string: `year`, `month`, `week`, `day` | Graph data intervals. |
| query | `start_date` | Yes | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].referrer` | string | Referrer. |
| `response[].strategy_owner` | string | User ID of the strategy owner. |
| `response[].promotion` | string | Promotion. |

Example:

```bash
python scripts/alphainsider_request.py GET /getIncome \
  --query "interval=month" \
  --query "start_date=2026-01-01T00:00:00Z"
```

## getStripeAccountLink - GET `/getStripeAccountLink`

Get stripe account link for managing withdrawal details.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `country` | No | string | Country of residence in ISO 3166-1 alpha-2 format. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStripeAccountLink \
  --query "country=US"
```
