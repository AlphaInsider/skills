# Limits Reference

Source material: AlphaInsider public limits documentation and OpenAPI examples.

Use this file before creating high-volume workflows, orders, posts, likes, bots, strategies, subscriptions, withdrawals, or stock catalog sync jobs.

## General Limits

| ID                    | Limit        | Description                                                             |
| --------------------- | ------------ | ----------------------------------------------------------------------- |
| new\_post             | 100/d        | Maximum successful requests to `/newPost` per day each strategy.        |
| like                  | 100/d        | Maximum successful requests to `/like` per day.                         |
| max\_sessions         | 100          | Maximum number of sessions. Drops oldest session once limit is reached. |
| max\_api\_tokens      | 50           | Maximum number of API tokens you can create.                            |
| max\_open\_orders     | 100          | Maximum number of open orders per strategy.                             |
| min\_withdraw\_amount | 1,000 (\$10) | Minimum USD withdrawal amount.                                          |

## Account Tier Limits

### Standard Account Limits

| ID                     | Limit | Description                                                       |
| ---------------------- | ----- | ----------------------------------------------------------------- |
| new\_order             | 50/d  | Maximum successful requests to `/newOrder` per day each strategy. |
| max\_strategies        | 5     | Maximum number of strategies you can create.                      |
| max\_subscriptions     | 10    | Maximum number of subscriptions you can have.                     |
| max\_bots              | 0     | Maximum number of bots you can have.                              |
| api\_token\_expiration | 1,000 | Years until API tokens expire.                                    |

### Pro Account Limits

| ID                     | Limit | Description                                                       |
| ---------------------- | ----- | ----------------------------------------------------------------- |
| new\_order             | 500/d | Maximum successful requests to `/newOrder` per day each strategy. |
| max\_strategies        | 50    | Maximum number of strategies you can create.                      |
| max\_subscriptions     | 100   | Maximum number of subscriptions you can have.                     |
| max\_bots              | 2     | Maximum number of bots you can have.                              |
| api\_token\_expiration | 1,000 | Years until API tokens expire.                                    |

### Premium Account Limits

| ID                     | Limit   | Description                                                       |
| ---------------------- | ------- | ----------------------------------------------------------------- |
| new\_order             | 5,000/d | Maximum successful requests to `/newOrder` per day each strategy. |
| max\_strategies        | 500     | Maximum number of strategies you can create.                      |
| max\_subscriptions     | 1,000   | Maximum number of subscriptions you can have.                     |
| max\_bots              | 4       | Maximum number of bots you can have.                              |
| api\_token\_expiration | 1,000   | Years until API tokens expire.                                    |

## Endpoint-Specific Notes

| Endpoint / field | Limit | Agent guidance |
| --- | --- | --- |
| `/newOrder` | Tiered: 50/d standard, 500/d pro, 5,000/d premium per strategy | Check `getAccountSubscription.response.limits.new_order` before automated order bursts. |
| `/newPost` | 100/d per strategy | Avoid posting loops; inspect `new_post` limits from the account subscription when available. |
| `/like` | 100/d | Avoid like automation loops. |
| `max_open_orders` | 100 open orders per strategy | Call `getOrders` before placing many new open orders. |
| `/getAllStocks` | 20 requests/hour | Prefer `searchStocks` for lookup and cache full catalog responses. |
| `/newPayout` | Minimum 1,000 cents ($10) | Call `getPayoutFees` and ensure the requested payout meets the minimum. |
| Bot count | 0 standard, 2 pro, 4 premium | Check `max_bots` before creating bots. |
| Strategy count | 5 standard, 50 pro, 500 premium | Check `max_strategies` before creating strategies. |
| Subscription count | 10 standard, 100 pro, 1,000 premium | Check `max_subscriptions` before creating subscriptions. |
| API tokens | 50 | Avoid generating extra tokens for automation. |
| Sessions | 100 | Oldest session is dropped after the limit is reached. |

## 429 Rate Limit Handling

OpenAPI defines HTTP 429 as `{ "success": false, "response": "Rate limit reached." }`. On 429, stop the current burst, back off, and retry later only if the workflow is safe to repeat.
