# Errors (Core)

## Error message
```json
{
  "ccp_version": "0.1",
  "type": "error",
  "id": "m_900001",
  "payload": {
    "code": "RATE_LIMIT",
    "message": "Too many requests.",
    "retry_after_ms": 1000,
    "request_id": "req_123"
  }
}
```

## Core codes
- `INVALID_REQUEST`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `NOT_FOUND`
- `CONFLICT`
- `RATE_LIMIT`
- `SERVER_BUSY`
- `MEDIA_TOO_LARGE`
- `UNSUPPORTED_CAPABILITY`
