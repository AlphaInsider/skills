# Timelines Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Strategy timeline events, posts, previews, likes, and unlikes.

The request helper can supply a default strategy ID for endpoints that accept `strategy_id` when the user has not supplied an explicit ID.

Timeline trade/order `data.amount`, `data.total`, and `data.strategy_value` fields are normalized. Read `input-multiplier.md` before displaying timeline trades, holdings changes, fees, totals, or percent fallback.

## getTimelines - GET `/getTimelines`

Get timeline events.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `timeline_id[]` | Yes | array of string (max 100) | One or more timeline event IDs. Repeat this query parameter for multiple timelines. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].timeline_id` | string | Timeline event identifier. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].name` | string | Display name. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].likes` | string | Like count. |
| `response[].liked` | boolean | Whether the authenticated user liked the event. |
| `response[].type` | string | Type or category for this object. |
| `response[].data` | object | Timeline event-specific payload. |
| `response[].data.history_id` | string | Trade history identifier. |
| `response[].data.action` | string | Order or signal action. |
| `response[].data.price` | string | Price or execution price, depending on context. |
| `response[].data.amount` | string | Amount. |
| `response[].data.fee_total` | string | Total fee for a trade event. |
| `response[].data.total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].data.new_holdings` | string | Holdings after the trade event. |
| `response[].data.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].data.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].data.figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].data.symbol` | string | Ticker or asset symbol. |
| `response[].data.name` | string | Display name. |
| `response[].data.sector` | string | Sector or asset category. |
| `response[].data.security` | string | Security type, such as stock or cryptocurrency. |
| `response[].data.exchange` | string | Exchange code. |
| `response[].data.stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].data.peg` | string | Peg or quote currency. |
| `response[].data.provider` | string | External provider or data provider. |
| `response[].data.slippage` | string | Slippage value or configured slippage fraction. |
| `response[].data.fee` | string | Fee value. |
| `response[].data.links` | object | External research and market-data links. |
| `response[].data.stock_status` | string | Current stock status. |

Example:

```bash
python scripts/alphainsider_request.py GET /getTimelines \
  --query "timeline_id[]=timeline_123"
```

## getStrategyTimelines - GET `/getStrategyTimelines`

Get strategy timeline events.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id[]` | Yes | array of string (max 100) | One or more strategy IDs. Repeat this query parameter for multiple strategies. |
| query | `type[]` | No | array of string | Array of timeline types to filter by. |
| query | `is_notification` | No | boolean | If true, only show timelines you receive notifications from. |
| query | `start_date` | No | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |
| query | `limit` | Yes | number | Number of results to return. |
| query | `offset_id` | No | string | Offet by ID. Used for pagination. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].timeline_id` | string | Timeline event identifier. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].name` | string | Display name. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].likes` | string | Like count. |
| `response[].liked` | boolean | Whether the authenticated user liked the event. |
| `response[].type` | string | Type or category for this object. |
| `response[].data` | object | Timeline event-specific payload. |
| `response[].data.history_id` | string | Trade history identifier. |
| `response[].data.action` | string | Order or signal action. |
| `response[].data.price` | string | Price or execution price, depending on context. |
| `response[].data.amount` | string | Amount. |
| `response[].data.fee_total` | string | Total fee for a trade event. |
| `response[].data.total` | string | Total value; for positions/orders this is strategy-normalized unless documented otherwise. |
| `response[].data.new_holdings` | string | Holdings after the trade event. |
| `response[].data.strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].data.stock_id` | string | AlphaInsider stock identifier, or `SYMBOL:EXCHANGE` in requests. |
| `response[].data.figi_composite` | null or value | Composite FIGI identifier when available. |
| `response[].data.symbol` | string | Ticker or asset symbol. |
| `response[].data.name` | string | Display name. |
| `response[].data.sector` | string | Sector or asset category. |
| `response[].data.security` | string | Security type, such as stock or cryptocurrency. |
| `response[].data.exchange` | string | Exchange code. |
| `response[].data.stock` | string | Stock symbol as stored by AlphaInsider. |
| `response[].data.peg` | string | Peg or quote currency. |
| `response[].data.provider` | string | External provider or data provider. |
| `response[].data.slippage` | string | Slippage value or configured slippage fraction. |
| `response[].data.fee` | string | Fee value. |
| `response[].data.links` | object | External research and market-data links. |
| `response[].data.stock_status` | string | Current stock status. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategyTimelines \
  --query "limit=20"
```

## newPost - POST `/newPost`

Create a new timeline post.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `description` | No | string | Post description. |
| body | `url` | No | string (url) | Post url. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.timeline_id` | string | Timeline event identifier. |
| `response.created_at` | string | Creation timestamp. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.name` | string | Display name. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.likes` | string | Like count. |
| `response.liked` | boolean | Whether the authenticated user liked the event. |
| `response.type` | string | Type or category for this object. |
| `response.data` | object | Timeline event-specific payload. |
| `response.data.post_id` | string | Post identifier. |
| `response.data.description` | string | Human-readable description. |
| `response.data.url` | string | Related URL. |
| `response.data.content` | object | Preview metadata for a linked URL. |
| `response.data.content.site` | string | Website host for preview content. |
| `response.data.content.type` | string | Type or category for this object. |
| `response.data.content.image` | string | Preview image URL. |
| `response.data.content.title` | string | Preview title. |
| `response.data.content.description` | string | Human-readable description. |

Example:

```bash
python scripts/alphainsider_request.py POST /newPost \
  --json '{"description":"Weekly update"}'
```

## previewPost - POST `/previewPost`

Preview a new timeline post.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `description` | No | string | Post description. |
| body | `url` | No | string (url) | Post url. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.created_at` | string | Creation timestamp. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.likes` | string | Like count. |
| `response.liked` | boolean | Whether the authenticated user liked the event. |
| `response.type` | string | Type or category for this object. |
| `response.data` | object | Timeline event-specific payload. |
| `response.data.description` | string | Human-readable description. |
| `response.data.url` | string | Related URL. |
| `response.data.content` | object | Preview metadata for a linked URL. |
| `response.data.content.site` | string | Website host for preview content. |
| `response.data.content.type` | string | Type or category for this object. |
| `response.data.content.title` | string | Preview title. |
| `response.data.content.description` | string | Human-readable description. |
| `response.data.content.image` | string | Preview image URL. |

Example:

```bash
python scripts/alphainsider_request.py POST /previewPost \
  --json '{"url":"https://example.com/research"}'
```

## deletePost - POST `/deletePost`

Delete timeline post.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `timeline_id` | Yes | string | Timeline ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py POST /deletePost \
  --json '{"timeline_id":"timeline_123"}'
```

## like - POST `/like`

Like timeline event.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `timeline_id` | Yes | string | Timeline ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py POST /like \
  --json '{"timeline_id":"timeline_123"}'
```

## unlike - POST `/unlike`

Unlike timeline event.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `timeline_id` | Yes | string | Timeline ID. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | string | Endpoint-specific response payload, or an error message when `success` is false. |

Example:

```bash
python scripts/alphainsider_request.py POST /unlike \
  --json '{"timeline_id":"timeline_123"}'
```
