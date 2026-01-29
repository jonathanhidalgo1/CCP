from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


def now_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def envelope(
    *,
    type: str,
    payload: Dict[str, Any],
    ccp_version: str = "0.1",
    id: Optional[str] = None,
    ts: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "ccp_version": ccp_version,
        "type": type,
        "id": id or str(uuid4()),
        "ts": ts or now_ts(),
        "payload": payload,
    }


def hello(
    *,
    device_id: str,
    device_token: str,
    firmware: str,
    capabilities: Dict[str, Any],
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "device_id": device_id,
        "device_token": device_token,
        "firmware": firmware,
        "capabilities": capabilities,
    }
    if locale is not None:
        payload["locale"] = locale
    return envelope(type="hello", payload=payload)


def session_start(*, device_id: str) -> Dict[str, Any]:
    return envelope(type="session_start", payload={"device_id": device_id})


def turn_text(*, session_id: str, text: str) -> Dict[str, Any]:
    return envelope(
        type="turn",
        payload={"session_id": session_id, "input": {"kind": "text", "text": text}},
    )


def turn_audio_ref(*, session_id: str, audio_ref: str) -> Dict[str, Any]:
    return envelope(
        type="turn",
        payload={
            "session_id": session_id,
            "input": {"kind": "audio_ref", "audio_ref": audio_ref},
        },
    )


def session_end(*, session_id: str) -> Dict[str, Any]:
    return envelope(type="session_end", payload={"session_id": session_id})
