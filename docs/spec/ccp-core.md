# CCP Core v0.1 — Draft

## 1) Purpose
CCP standardizes communication between:
- Device clients (robots, microcontrollers, gateways)
- Cortex Capsule servers (local or cloud brain runtime)

Defines:
- Message types and schemas
- Pairing and authentication
- Capability negotiation
- Session lifecycle
- Turn processing (text/audio)
- Actions (LED/screen/sound)
- Errors and reliability rules
- Optional extensions

## 2) Design Principles
- **Capabilities, not hardware**: devices declare what they can do.
- **Thin devices**: safety, memory, and reasoning live in Cortex.
- **Graceful degradation**: devices may ignore unsupported actions.
- **Stable contracts**: additive and versioned changes.
- **Kid-safe by default**: server enforces safety; device is untrusted.

## 3) Versioning
All messages include:
- `ccp_version`: "0.1"
- `type`: message type
- `id`: unique id (uuid or device monotonic id)
- `ts`: ISO timestamp (optional for constrained devices)

Example:
```json
{
  "ccp_version": "0.1",
  "type": "hello",
  "id": "m_000001",
  "ts": "2026-01-23T18:10:00Z",
  "payload": {}
}
```

## 4) Core Message Types
- `hello` → auth + capabilities
- `hello_ack` → accept + negotiation
- `session_start` / `session_started`
- `turn` / `turn_result`
- `session_end` / `session_ended`
- `error`

Schema details: [message-schemas.md](message-schemas.md)

## 5) Session
- `session_start`: opens logical context
- `session_started`: returns `session_id` and metadata
- `session_end`: closes

## 6) Turn
- Input is text or audio reference (`audio_ref`)
- Response can include `text`, `audio_ref`, `actions`, and `state`

## 7) Media
Core uses audio references (refs). Upload/Fetch via HTTP.

See [media.md](media.md).

## 8) Actions
Actions are **hints**; device may ignore.

See [actions.md](actions.md).

## 9) Errors and Reliability
- Standardized errors (`error`)
- Retry and idempotency rules

See [errors.md](errors.md) and [reliability.md](reliability.md).

## 10) Extensions
Optional namespaces without breaking Core.

See [extensions.md](extensions.md).
