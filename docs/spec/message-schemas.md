# Message Schemas

JSON schemas (Draft 2020-12) are in [schemas/](../../schemas).

## Core
- `ccp-message.json` — base envelope
- `hello.json`
- `hello-ack.json`
- `session-start.json`
- `session-started.json`
- `turn.json`
- `turn-result.json`
- `session-end.json`
- `session-ended.json`
- `error.json`

## Rules
- Unknown fields must be ignored by devices.
- Only additive changes are allowed in v0.x.
