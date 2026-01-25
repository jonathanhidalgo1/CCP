# HTTP Mapping (v0.1)

## Goal
Guarantee parity between WebSocket and HTTP. Each CCP message has an equivalent endpoint.

## General Rules
- `Content-Type: application/json`
- Auth via `Authorization: Device <token>`
- Responses are always a **CCP message**

## Core Endpoints

### POST /ccp/hello
**Request body:** `hello` message

**Response:** `hello_ack` or `error`

### POST /ccp/session/start
**Request body:** `session_start` message

**Response:** `session_started` or `error`

### POST /ccp/turn
**Request body:** `turn` message

**Response:** `turn_result` or `error`

### POST /ccp/session/end
**Request body:** `session_end` message

**Response:** `session_ended` or `error`

## Media

### POST /v1/media/audio
- Audio upload
- **Response:** `{ "audio_ref": "aud_xxx" }`

### GET /v1/media/audio/{audio_ref}
- Audio download

## Example Headers
```
Authorization: Device devtok_xxx
Content-Type: application/json
```

## Notes
- WS and HTTP must behave the same for CCP Core.
- Errors use the same `error` format.
