# Reliability (Core)

## Devices SHOULD
- Request timeout: 5–10s
- Retry only on `SERVER_BUSY`, `RATE_LIMIT` (after delay), and network errors
- Recreate session on `CONFLICT`

## Devices MUST
- Unique `id` per message
- Handle duplicate `turn_result` (idempotency)

## Servers SHOULD
- Return `retry_after_ms` when relevant
- Include `request_id` for tracing
