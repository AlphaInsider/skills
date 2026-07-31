# Strategies Endpoints

REST base URL: `https://alphainsider.com/api`.

Credential boundary: Authentication fields below describe API wire format. Agents should not read `ALPHAINSIDER_API_KEY` from environment variables or `.env`, and should use `scripts/alphainsider_request.py` so the helper injects private credentials.

Strategy lookup, search, creation, updates, pricing, values, and performance.

The request helper can supply a default strategy ID for endpoints that accept `strategy_id` when the user has not supplied an explicit ID.

Read `input-multiplier.md` before displaying `strategy_value`, timeframe values, or performance gain/loss to users.

## getStrategies - GET `/getStrategies`

Get strategy information.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id[]` | Yes | array of string (max 100) | One or more strategy IDs. Repeat this query parameter for multiple strategies. |
| query | `timeframe` | No | string: `day`, `week`, `month`, `year`, `five_year` (default `month`) | Gets strategy values based on timeframe. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Strategy security type: `stock` or `cryptocurrency`. |
| `response[].private` | boolean | Whether the strategy is private. |
| `response[].name` | string | Display name. |
| `response[].description` | string | Human-readable description. |
| `response[].categories` | array of string | Strategy category labels. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].subscriber_count` | string | Number of subscribers. |
| `response[].timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response[].timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response[].timeframes[].rank_performance` | string | Performance rank for the timeframe. |
| `response[].timeframes[].rank_popular` | string | Popularity rank for the timeframe. |
| `response[].timeframes[].rank_trending` | string | Trending rank for the timeframe. |
| `response[].timeframes[].rank_top` | string | Overall top rank for the timeframe. |
| `response[].timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response[].timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategies \
  --query "timeframe=month"
```

## getStrategyValues - GET `/getStrategyValues`

Get current strategy value.

Note: `strategy_value` is normalized. Use `input-multiplier.md` to display user-facing USD values or percent fallback.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id[]` | Yes | array of string (max 100) | One or more strategy IDs. Repeat this query parameter for multiple strategies. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategyValues
```

## getUserStrategies - GET `/getUserStrategies`

Get user strategies.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `user_id` | Yes | string | User ID. |
| query | `timeframe` | No | string: `day`, `week`, `month`, `year`, `five_year` (default `month`) | Gets strategy values based on timeframe. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Strategy security type: `stock` or `cryptocurrency`. |
| `response[].private` | boolean | Whether the strategy is private. |
| `response[].name` | string | Display name. |
| `response[].description` | string | Human-readable description. |
| `response[].categories` | array of string | Strategy category labels. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].subscriber_count` | string | Number of subscribers. |
| `response[].timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response[].timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response[].timeframes[].rank_performance` | string | Performance rank for the timeframe. |
| `response[].timeframes[].rank_popular` | string | Popularity rank for the timeframe. |
| `response[].timeframes[].rank_trending` | string | Trending rank for the timeframe. |
| `response[].timeframes[].rank_top` | string | Overall top rank for the timeframe. |
| `response[].timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response[].timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py GET /getUserStrategies \
  --query "user_id=user_1" \
  --query "timeframe=year"
```

## getStrategyPerformance - GET `/getStrategyPerformance`

Get strategy performance data.

Note: Performance `strategy_value` points are normalized. Use `input-multiplier.md` for calculation-date baselines, dollar gain/loss display, and percent fallback.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id` | Yes | string | Strategy ID. |
| query | `frequency` | No | number (default `1`) | The number of intervals per tick. |
| query | `interval` | No | string: `hour`, `day`, `week` (default `hour`) | The timeframe per tick. |
| query | `start_date` | Yes | string (date-time) | Start date. |
| query | `end_date` | No | string (date-time) | End date. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].strategy_value` | string | Normalized strategy value. Convert before displaying user-facing USD values. |
| `response[].activity` | string | Trade activity label for a performance interval. |
| `response[].trade_count` | string | Number of trades in the interval. |

Example:

```bash
python scripts/alphainsider_request.py GET /getStrategyPerformance \
  --query "start_date=2026-01-01T00:00:00Z" \
  --query "interval=day"
```

## getRecommendedStrategies - GET `/getRecommendedStrategies`

Get recommended strategies.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| query | `strategy_id[]` | Yes | array of string (max 100) | One or more strategy IDs. Repeat this query parameter for multiple strategies. |
| query | `timeframe` | No | string: `day`, `week`, `month`, `year`, `five_year` (default `month`) | Gets strategy values based on timeframe. |
| query | `limit` | No | number | Number of results to return. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Strategy security type: `stock` or `cryptocurrency`. |
| `response[].private` | boolean | Whether the strategy is private. |
| `response[].name` | string | Display name. |
| `response[].description` | string | Human-readable description. |
| `response[].categories` | array of string | Strategy category labels. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].subscriber_count` | string | Number of subscribers. |
| `response[].timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response[].timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response[].timeframes[].rank_performance` | string | Performance rank for the timeframe. |
| `response[].timeframes[].rank_popular` | string | Popularity rank for the timeframe. |
| `response[].timeframes[].rank_trending` | string | Trending rank for the timeframe. |
| `response[].timeframes[].rank_top` | string | Overall top rank for the timeframe. |
| `response[].timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response[].timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py GET /getRecommendedStrategies \
  --query "limit=10"
```

## searchStrategies - POST `/searchStrategies`

Search strategies.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | No | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `search` | No | string | Term to search for. |
| body | `type` | No | object | Filter by strategy security type. |
| body | `type.includes` | No | array of string | Must ***include*** these types. |
| body | `type.excludes` | No | array of string | Must ***exclude*** these types. |
| body | `categories` | No | object | Filter by category. |
| body | `categories.includes` | No | array of string | Must ***include*** these categories. |
| body | `categories.excludes` | No | array of string | Must ***exclude*** these categories. |
| body | `max_drawdown` | No | number | Filter by max drawdown. |
| body | `positions` | No | object | Filter by current stock positions. |
| body | `positions.includes` | No | array of string (max 100) | Must ***include*** these stock positions. `["stock:exchange"]` or `["stock_id"]` |
| body | `positions.excludes` | No | array of string (max 100) | Must ***exclude*** these stock positions. `["stock:exchange"]` or `["stock_id"]` |
| body | `sectors` | No | object | Filter by sector. |
| body | `sectors.includes` | No | array of string | Must ***include*** these sectors. |
| body | `sectors.excludes` | No | array of string | Must ***exclude*** these sectors. |
| body | `trade_count_min` | No | number | Filter by minimum trade count. |
| body | `trade_count_max` | No | number | Filter by maximum trade count. |
| body | `price_min` | No | number | Filter by minimum price. |
| body | `price_max` | No | number | Filter by maximum price. |
| body | `created_min` | No | string (date-time) | Filter by minimum strategy created date. |
| body | `created_max` | No | string (date-time) | Filter by maximum strategy created date. Must be greater than or equal to created_min. |
| body | `timeframe` | No | string: `day`, `week`, `month`, `year`, `five_year` (default `month`) | Gets strategy values based on timeframe. |
| body | `sort` | No | string: `top`, `trending`, `performance`, `popular`, `newest` (default `top`) | Sort results by. |
| body | `limit` | No | number | Number of results to return. |
| body | `offset_id` | No | string | Offet by ID. Used for pagination. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | array of object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response[].strategy_id` | string | AlphaInsider strategy identifier. |
| `response[].product_id` | string | Billing product identifier. |
| `response[].user_id` | string | AlphaInsider user identifier. |
| `response[].type` | string | Strategy security type: `stock` or `cryptocurrency`. |
| `response[].private` | boolean | Whether the strategy is private. |
| `response[].name` | string | Display name. |
| `response[].description` | string | Human-readable description. |
| `response[].categories` | array of string | Strategy category labels. |
| `response[].updated_at` | string | Last update timestamp. |
| `response[].created_at` | string | Creation timestamp. |
| `response[].price` | integer | Price or execution price, depending on context. |
| `response[].subscriber_count` | string | Number of subscribers. |
| `response[].timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response[].timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response[].timeframes[].rank_performance` | string | Performance rank for the timeframe. |
| `response[].timeframes[].rank_popular` | string | Popularity rank for the timeframe. |
| `response[].timeframes[].rank_trending` | string | Trending rank for the timeframe. |
| `response[].timeframes[].rank_top` | string | Overall top rank for the timeframe. |
| `response[].timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response[].timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py POST /searchStrategies \
  --json '{"search":"momentum","type":"stock","sort":"performance","limit":10}'
```

## newStrategy - POST `/newStrategy`

Create new strategy.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `type` | Yes | string: `stock`, `cryptocurrency` | Strategy security type. |
| body | `private` | No | boolean | Whether strategy is public or private. |
| body | `name` | Yes | string | Strategy name. |
| body | `description` | No | string | Strategy description. |
| body | `input_value` | Yes | number | Strategy owner's starting balance. AlphaInsider uses it to establish the owner's display calculation and `input_multiplier`. |
| body | `price` | No | number | Monthly subscription price. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.name` | string | Display name. |
| `response.description` | string | Human-readable description. |
| `response.categories` | array | Strategy category labels. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |
| `response.price` | integer | Price or execution price, depending on context. |
| `response.subscriber_count` | string | Number of subscribers. |
| `response.timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response.timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response.timeframes[].rank_performance` | null or value | Performance rank for the timeframe. |
| `response.timeframes[].rank_popular` | null or value | Popularity rank for the timeframe. |
| `response.timeframes[].rank_trending` | null or value | Trending rank for the timeframe. |
| `response.timeframes[].rank_top` | null or value | Overall top rank for the timeframe. |
| `response.timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response.timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py POST /newStrategy \
  --json '{"type":"stock","name":"Example Strategy","input_value":"100000","private":true}'
```

## updateStrategy - POST `/updateStrategy`

Update existing strategy.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `name` | Yes | string | Strategy name. |
| body | `description` | No | string | Strategy description. |
| body | `input_value` | Yes | number | Strategy owner's starting balance. AlphaInsider uses it to update the owner's display calculation and `input_multiplier`. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.name` | string | Display name. |
| `response.description` | string | Human-readable description. |
| `response.categories` | array of string | Strategy category labels. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |
| `response.price` | integer | Price or execution price, depending on context. |
| `response.subscriber_count` | string | Number of subscribers. |
| `response.timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response.timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response.timeframes[].rank_performance` | null or value | Performance rank for the timeframe. |
| `response.timeframes[].rank_popular` | null or value | Popularity rank for the timeframe. |
| `response.timeframes[].rank_trending` | null or value | Trending rank for the timeframe. |
| `response.timeframes[].rank_top` | null or value | Overall top rank for the timeframe. |
| `response.timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response.timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py POST /updateStrategy \
  --json '{"name":"Updated Strategy","input_value":"100000"}'
```

## updateStrategyPrice - POST `/updateStrategyPrice`

Update existing strategy price.

Inputs:

| Location | Name | Required | Type / values | Description |
| --- | --- | --- | --- | --- |
| header | `Authorization` | Yes | string (JWT) | AlphaInsider API token sent exactly as the header value; do not prepend `Bearer`. |
| body | `strategy_id` | Yes | string | Strategy ID. |
| body | `price` | Yes | number | Monthly subscription price. |

Outputs:

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | True when the request succeeded. |
| `response` | object | Endpoint-specific response payload, or an error message when `success` is false. |
| `response.strategy_id` | string | AlphaInsider strategy identifier. |
| `response.product_id` | string | Billing product identifier. |
| `response.user_id` | string | AlphaInsider user identifier. |
| `response.type` | string | Type or category for this object. |
| `response.private` | boolean | Whether the strategy is private. |
| `response.name` | string | Display name. |
| `response.description` | string | Human-readable description. |
| `response.categories` | array of string | Strategy category labels. |
| `response.updated_at` | string | Last update timestamp. |
| `response.created_at` | string | Creation timestamp. |
| `response.price` | integer | Price or execution price, depending on context. |
| `response.subscriber_count` | string | Number of subscribers. |
| `response.timeframes` | array of object | Per-timeframe ranking and historical value data. |
| `response.timeframes[].timeframe` | string | Time window used for ranking or performance data. |
| `response.timeframes[].rank_performance` | null or value | Performance rank for the timeframe. |
| `response.timeframes[].rank_popular` | null or value | Popularity rank for the timeframe. |
| `response.timeframes[].rank_trending` | null or value | Trending rank for the timeframe. |
| `response.timeframes[].rank_top` | null or value | Overall top rank for the timeframe. |
| `response.timeframes[].max_drawdown` | string | Maximum drawdown for the timeframe. |
| `response.timeframes[].past_value` | string | Strategy value at the start of the timeframe. |

Example:

```bash
python scripts/alphainsider_request.py POST /updateStrategyPrice \
  --json '{"price":"10"}'
```

## deleteStrategy - POST `/deleteStrategy`

Delete strategy.

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
python scripts/alphainsider_request.py POST /deleteStrategy
```
