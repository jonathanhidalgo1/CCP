# Media (Core)

## Audio References
CCP Core uses `audio_ref` instead of streaming.

### Upload
- `POST /v1/media/audio`
- Returns: `{ "audio_ref": "aud_in_001" }`

### Use in turn
```json
{
  "ccp_version": "0.1",
  "type": "turn",
  "id": "m_000011",
  "payload": {
    "session_id": "ses_abc",
    "input": { "kind": "audio_ref", "audio_ref": "aud_in_001" }
  }
}
```

### Fetch
- `GET /v1/media/audio/{audio_ref}`

## Reasons
- Simple for constrained devices
- Enables cache and CDN
- Avoids streaming in v0.1
