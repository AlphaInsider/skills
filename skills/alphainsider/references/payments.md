# Payments Endpoints

REST base URL: `https://alphainsider.com/api`.

Payment sources, invoices, invoice PDFs, invoice line items, and invoice retries.

## getPaymentSources - GET `/getPaymentSources`

Get payment sources.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].source_id` | string | Payment source identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Type or category for this object. |
| `response[].direction` | string | Direction. |
| `response[].primary` | boolean | Primary. |
| `response[].description` | string | Human-readable description. |
| `response[].name` | string | Display name. |
| `response[].city` | string | City. |
| `response[].country` | string | Country. |
| `response[].line_one` | string | Line one. |
| `response[].line_two` | string | Line two. |
| `response[].district` | string | District. |
| `response[].postal` | string | Postal. |
| `response[].status` | string | Current status. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |

Example request:

```http
GET /getPaymentSources
Authorization: <API_TOKEN>
```

## getUpcomingInvoice - GET `/getUpcomingInvoice`

Get upcoming invoice.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.invoice_id` | null or value | Invoice identifier, when one exists. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.description` | string | Human-readable description. |
| `response.status` | string | Current status. |
| `response.updated_at` | null or value | Last update timestamp. |
| `response.created_at` | null or value | Creation timestamp. |
| `response.amount` | string | Amount. |
| `response.amount_refunded` | string | Amount refunded. |
| `response.source` | object | Source. |
| `response.source.source_id` | string | Payment source identifier. |
| `response.source.user_id` | string | AlphaInsider user identifier. |
| `response.source.type` | string | Type or category for this object. |
| `response.source.direction` | string | Direction. |
| `response.source.primary` | boolean | Primary. |
| `response.source.description` | string | Human-readable description. |
| `response.source.name` | string | Display name. |
| `response.source.city` | string | City. |
| `response.source.country` | string | Country. |
| `response.source.line_one` | string | Line one. |
| `response.source.line_two` | string | Line two. |
| `response.source.district` | string | District. |
| `response.source.postal` | string | Postal. |
| `response.source.status` | string | Current status. |
| `response.source.updated_at` | string | Last update timestamp. |
| `response.source.created_at` | string | Creation timestamp. |
| `response.retryable` | boolean | Retryable. |

Example request:

```http
GET /getUpcomingInvoice
Authorization: <API_TOKEN>
```

## getInvoices - GET `/getInvoices`

Get invoices.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `invoice_id[]` | No | array of string (max 100) | One or more invoice IDs. Repeat this query parameter for multiple invoices. |
| query | `source_id` | No | string | Source ID. |
| query | `status` | No | string: `pending`, `paid`, `failed`, `chargeback` | Invoice status. |
| query | `limit` | No | number (default `10`) | Number of results to return. |
| query | `offset_id` | No | string | Offet by ID. Used for pagination. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].invoice_id` | string | Invoice identifier, when one exists. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].description` | string | Human-readable description. |
| `response[].status` | string | Current status. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].amount` | string | Amount. |
| `response[].amount_refunded` | string | Amount refunded. |
| `response[].source` | object | Source. |
| `response[].source.source_id` | string | Payment source identifier. |
| `response[].source.user_id` | string | AlphaInsider user identifier. |
| `response[].source.type` | string | Type or category for this object. |
| `response[].source.direction` | string | Direction. |
| `response[].source.primary` | boolean | Primary. |
| `response[].source.description` | string | Human-readable description. |
| `response[].source.name` | string | Display name. |
| `response[].source.city` | string | City. |
| `response[].source.country` | string | Country. |
| `response[].source.line_one` | string | Line one. |
| `response[].source.line_two` | string | Line two. |
| `response[].source.district` | string | District. |
| `response[].source.postal` | string | Postal. |
| `response[].source.status` | string | Current status. |
| `response[].source.updated_at` | string | Last update timestamp. |
| `response[].source.created_at` | string | Creation timestamp. |
| `response[].retryable` | boolean | Retryable. |

Example request:

```http
GET /getInvoices?status=paid&limit=20
Authorization: <API_TOKEN>
```

## getInvoicePdf - GET `/getInvoicePdf`

Get invoice PDF.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `invoice_id` | Yes | string | Invoice ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | PDF file | Invoice PDF file payload, or an error message when `success` is false. |

Example request:

```http
GET /getInvoicePdf?invoice_id=invoice_123
Authorization: <API_TOKEN>
```

## retryInvoice - POST `/retryInvoice`

Retry failed invoice.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `invoice_id` | Yes | string | Invoice ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].invoice_id` | string | Invoice identifier, when one exists. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].description` | string | Human-readable description. |
| `response[].status` | string | Current status. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].amount` | string | Amount. |
| `response[].amount_refunded` | string | Amount refunded. |
| `response[].source` | object | Source. |
| `response[].source.source_id` | string | Payment source identifier. |
| `response[].source.user_id` | string | AlphaInsider user identifier. |
| `response[].source.type` | string | Type or category for this object. |
| `response[].source.direction` | string | Direction. |
| `response[].source.primary` | boolean | Primary. |
| `response[].source.description` | string | Human-readable description. |
| `response[].source.name` | string | Display name. |
| `response[].source.city` | string | City. |
| `response[].source.country` | string | Country. |
| `response[].source.line_one` | string | Line one. |
| `response[].source.line_two` | string | Line two. |
| `response[].source.district` | string | District. |
| `response[].source.postal` | string | Postal. |
| `response[].source.status` | string | Current status. |
| `response[].source.updated_at` | string | Last update timestamp. |
| `response[].source.created_at` | string | Creation timestamp. |
| `response[].retryable` | boolean | Retryable. |

Example request:

```http
POST /retryInvoice
Authorization: <API_TOKEN>
Content-Type: application/json

{"invoice_id":"invoice_123"}
```

## getUpcomingInvoiceItems - GET `/getUpcomingInvoiceItems`

Get upcoming invoice items.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].item_id` | null or value | Item id. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].invoice_id` | null or value | Invoice identifier, when one exists. |
| `response[].amount` | integer | Amount. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].start_date` | string | Start date. |
| `response[].end_date` | string | End timestamp for the current period or range. |
| `response[].updated_at` | null or value | Last update timestamp. |
| `response[].created_at` | null or value | Creation timestamp. |
| `response[].amount_refunded` | string | Amount refunded. |
| `response[].name` | string | Display name. |
| `response[].type` | string | Type or category for this object. |

Example request:

```http
GET /getUpcomingInvoiceItems
Authorization: <API_TOKEN>
```

## getInvoiceItems - GET `/getInvoiceItems`

Get invoice items.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `invoice_id` | Yes | string | Invoice ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].item_id` | string | Item id. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].invoice_id` | string | Invoice identifier, when one exists. |
| `response[].amount` | string | Amount. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].start_date` | string | Start date. |
| `response[].end_date` | string | End timestamp for the current period or range. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].amount_refunded` | string | Amount refunded. |
| `response[].name` | string | Display name. |
| `response[].type` | string | Type or category for this object. |
| `response[].type_id` | null or value | Type id. |

Example request:

```http
GET /getInvoiceItems?invoice_id=invoice_123
Authorization: <API_TOKEN>
```
