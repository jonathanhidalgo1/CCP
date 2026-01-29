from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from ccp_sdk import CCPClient

app = FastAPI(title="ESP32 CCP Gateway", version="0.1")

CCP_BASE_URL = os.environ.get("CCP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# In-memory session store: device_id -> session_id
_sessions: Dict[str, str] = {}


class ESP32Hello(BaseModel):
    device_id: str = Field(..., min_length=1)
    device_token: str = Field(..., min_length=1)
    firmware: str = Field(..., min_length=1)
    capabilities: Dict[str, Any] = Field(default_factory=dict)
    locale: Optional[str] = None


class ESP32SessionStart(BaseModel):
    device_id: str = Field(..., min_length=1)
    device_token: str = Field(..., min_length=1)


class ESP32TurnText(BaseModel):
    device_id: str = Field(..., min_length=1)
    device_token: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class ESP32SessionEnd(BaseModel):
    device_id: str = Field(..., min_length=1)
    device_token: str = Field(..., min_length=1)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


def _client(device_token: str) -> CCPClient:
    return CCPClient(base_url=CCP_BASE_URL, device_token=device_token)


@app.post("/esp32/hello")
async def esp32_hello(payload: ESP32Hello) -> Dict[str, Any]:
    try:
        with _client(payload.device_token) as ccp:
            return ccp.hello(
                device_id=payload.device_id,
                device_token=payload.device_token,
                firmware=payload.firmware,
                capabilities=payload.capabilities,
                locale=payload.locale,
            )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/esp32/session/start")
async def esp32_session_start(payload: ESP32SessionStart) -> Dict[str, Any]:
    try:
        with _client(payload.device_token) as ccp:
            msg = ccp.session_start(device_id=payload.device_id)
            session_id = msg["payload"]["session_id"]
            _sessions[payload.device_id] = session_id
            return {"session_id": session_id, "ccp": msg}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/esp32/turn/text")
async def esp32_turn_text(payload: ESP32TurnText) -> Dict[str, Any]:
    session_id = _sessions.get(payload.device_id)
    if not session_id:
        raise HTTPException(status_code=409, detail="No session for device_id; call /esp32/session/start")

    try:
        with _client(payload.device_token) as ccp:
            msg = ccp.turn_text(session_id=session_id, text=payload.text)
            reply = msg.get("payload", {}).get("reply", {}) if isinstance(msg, dict) else {}
            return {"reply": reply, "ccp": msg}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/esp32/turn/audio/{device_id}")
async def esp32_turn_audio(device_id: str, request: Request, device_token: str = Body(..., embed=True)) -> Dict[str, Any]:
    session_id = _sessions.get(device_id)
    if not session_id:
        raise HTTPException(status_code=409, detail="No session for device_id; call /esp32/session/start")

    content_type = request.headers.get("content-type", "application/octet-stream")
    audio_bytes = await request.body()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty body")

    try:
        with _client(device_token) as ccp:
            audio_ref = ccp.upload_audio(audio_bytes=audio_bytes, content_type=content_type)
            msg = ccp.turn_audio_ref(session_id=session_id, audio_ref=audio_ref)
            reply = msg.get("payload", {}).get("reply", {}) if isinstance(msg, dict) else {}
            return {"audio_ref": audio_ref, "reply": reply, "ccp": msg}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/esp32/session/end")
async def esp32_session_end(payload: ESP32SessionEnd) -> Dict[str, Any]:
    session_id = _sessions.get(payload.device_id)
    if not session_id:
        raise HTTPException(status_code=409, detail="No session for device_id")

    try:
        with _client(payload.device_token) as ccp:
            msg = ccp.session_end(session_id=session_id)
            _sessions.pop(payload.device_id, None)
            return msg
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
