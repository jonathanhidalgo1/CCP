# CCP
Cortex Capsule Protocol (CCP) — v0.1 Draft

CCP standardizes communication between devices (robots, microcontrollers, gateways) and Cortex Capsule servers (local or cloud brain runtime).

## Contents
- Core specification
- HTTP mapping
- JSON schemas
- Message examples

## Structure
- [docs/](docs/README.md)
- [schemas/](schemas)
- [examples/](examples)

## Get started
1. Read the core spec: [docs/spec/ccp-core.md](docs/spec/ccp-core.md)
2. Check HTTP mapping: [docs/spec/http-binding.md](docs/spec/http-binding.md)
3. See schemas: [docs/spec/message-schemas.md](docs/spec/message-schemas.md)
4. See examples: [examples/](examples)

## How to use CCP
- This repo is the **specification**, not a dependency to install.
- Projects should depend on a **CCP SDK** (language/runtime specific) that implements the protocol.
- If you need JSON schemas in production, the SDK should bundle them or reference a published schema package.

## Python SDK (reference)

This repository now includes a minimal reference Python SDK that you can install with pip.

### Install (local dev)
From the repo root:

```bash
python -m pip install -e .
```

### Install (from PyPI)
After you publish it:

```bash
python -m pip install ccp-sdk
```

### Usage
See a runnable example in [examples/python_client.py](examples/python_client.py).

## ESP32 note
ESP32 (Arduino/ESP-IDF) does not run `pip` packages directly.

Typical architecture:
- ESP32 handles hardware (mic/speaker/LED/display) and sends events/audio to a gateway over Wi-Fi/serial.
- The gateway (Raspberry Pi / PC) runs the Python CCP SDK and talks to the CCP server over HTTP.

Practical mapping:
- Mic (I2S) -> capture audio -> upload to `/v1/media/audio` -> send `turn` with `audio_ref`
- Speaker (I2S) <- receive `turn_result.payload.reply.audio_ref` -> download audio -> play
- LED strip / display <- drive UI based on `turn_result.payload.state`, `safety`, or `actions`

## SDKs (planned)
- `ccp-python` — reference SDK for capsules/gateways
- `ccp-esp32` — thin device SDK for microcontrollers

## Version
CCP v0.1 (Draft)

## Roadmap
See [docs/roadmap.md](docs/roadmap.md).

## Community
Discord: invite link TBD.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes and submit PRs.

## Code of Conduct
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security
See [SECURITY.md](SECURITY.md).
