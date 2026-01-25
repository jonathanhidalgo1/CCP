# Extensions (v0.x)

Extensions add optional features without breaking Core.

## Suggested namespaces
- `ccp.ext.audio_stream.v0`
- `ccp.ext.sensors.v0`
- `ccp.ext.motion.v0`
- `ccp.ext.display.v0`
- `ccp.ext.wakeword.v0`

## Rules
- Device advertises supported extensions in `hello`.
- Server must **not** require extensions to function in Core.
