# Security & Privacy

## Pairing
- `pair_code` expiry 5–10 min
- Exchange for long-lived `device_token`
- Tokens are revocable and rotatable

## Authentication
- WS: `device_token` in `hello`
- HTTP: `Authorization: Device <token>`

## Principles
- Device is untrusted
- Server applies kid-safe policies
- Minimal logs on device
