# Capabilities (Core)

## Capability Object
Example:
```json
{
  "audio_in": { "codecs": ["pcm16", "opus"], "sample_rates": [16000], "channels": 1 },
  "audio_out": { "codecs": ["pcm16"], "sample_rates": [16000], "channels": 1 },
  "io": { "button": true, "led": true, "screen": false },
  "actions": ["led"],
  "streaming": { "supported": false },
  "network": { "type": "wifi", "metered": false }
}
```

## Negotiation
Server responds with:
- `audio_codec`
- `sample_rate`
- `max_audio_seconds`
- `preferred_transport`

## Rules
- Unknown fields must be ignored.
- Adding new capabilities must be backward compatible.
