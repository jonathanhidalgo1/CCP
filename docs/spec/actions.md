# Actions (Core)

Actions are **hints** from the server. The device may ignore unknown actions.

## Core Actions
- `led`: `{ "pattern": "happy|sparkle|sleepy|error" }`
- `sound`: `{ "sfx": "chime|pop" }`

## Example
```json
{
  "actions": [
    { "type": "led", "pattern": "sparkle" },
    { "type": "sound", "sfx": "chime" }
  ]
}
```
