from __future__ import annotations

from ccp_sdk import CCPClient


def main() -> None:
    # This matches the FastAPI example in examples/ccp_api
    base_url = "http://127.0.0.1:8000"

    device_id = "esp32-devkit"
    device_token = "devtok_example"

    capabilities = {
        "audio_in": {"codecs": ["pcm16"], "sample_rates": [16000], "channels": 1},
        "audio_out": {"codecs": ["pcm16"], "sample_rates": [16000], "channels": 1},
        "io": {"button": True, "led": True, "screen": True},
    }

    with CCPClient(base_url=base_url, device_token=device_token) as ccp:
        hello_ack = ccp.hello(
            device_id=device_id,
            device_token=device_token,
            firmware="0.0.1",
            capabilities=capabilities,
            locale="pt-BR",
        )
        print("hello_ack:", hello_ack)

        session_started = ccp.session_start(device_id=device_id)
        session_id = session_started["payload"]["session_id"]
        print("session_started:", session_started)

        turn_result = ccp.turn_text(session_id=session_id, text="Olá! Teste CCP.")
        print("turn_result:", turn_result)

        session_ended = ccp.session_end(session_id=session_id)
        print("session_ended:", session_ended)


if __name__ == "__main__":
    main()
