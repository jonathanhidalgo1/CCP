from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="CCP API Example", version="0.1")


def now_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseEnvelope(BaseModel):
    ccp_version: Literal["0.1"] = "0.1"
    type: str
    id: str = Field(..., min_length=1)
    ts: Optional[str] = None


class HelloPayload(BaseModel):
    device_id: str
    device_token: str
    firmware: str
    capabilities: Dict[str, Any]
    locale: Optional[str] = None


class HelloMessage(BaseEnvelope):
    type: Literal["hello"]
    payload: HelloPayload


class HelloAckPayload(BaseModel):
    accepted: bool
    device_id: str
    session_supported: bool = True
    negotiated: Optional[Dict[str, Any]] = None
    limits: Optional[Dict[str, Any]] = None


class HelloAckMessage(BaseEnvelope):
    type: Literal["hello_ack"]
    payload: HelloAckPayload


class SessionStartPayload(BaseModel):
    device_id: str


class SessionStartMessage(BaseEnvelope):
    type: Literal["session_start"]
    payload: SessionStartPayload


class SessionStartedPayload(BaseModel):
    session_id: str
    active_capsule_id: Optional[str] = None
    kid_safe_applied: Optional[bool] = True


class SessionStartedMessage(BaseEnvelope):
    type: Literal["session_started"]
    payload: SessionStartedPayload


class TurnInput(BaseModel):
    kind: Literal["text", "audio_ref"]
    text: Optional[str] = None
    audio_ref: Optional[str] = None


class TurnPayload(BaseModel):
    session_id: str
    input: TurnInput


class TurnMessage(BaseEnvelope):
    type: Literal["turn"]
    payload: TurnPayload


class TurnReply(BaseModel):
    text: Optional[str] = None
    audio_ref: Optional[str] = None


class TurnResultPayload(BaseModel):
    session_id: str
    reply: Optional[TurnReply] = None
    state: Optional[Dict[str, Any]] = None
    safety: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    meta: Optional[Dict[str, Any]] = None


class TurnResultMessage(BaseEnvelope):
    type: Literal["turn_result"]
    payload: TurnResultPayload


class SessionEndPayload(BaseModel):
    session_id: str


class SessionEndMessage(BaseEnvelope):
    type: Literal["session_end"]
    payload: SessionEndPayload


class SessionEndedPayload(BaseModel):
    session_id: str


class SessionEndedMessage(BaseEnvelope):
    type: Literal["session_ended"]
    payload: SessionEndedPayload


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/ccp/hello", response_model=HelloAckMessage)
async def hello(message: HelloMessage) -> HelloAckMessage:
    negotiated = {
        "audio_codec": "pcm16",
        "sample_rate": 16000,
        "preferred_transport": "http",
    }
    return HelloAckMessage(
        type="hello_ack",
        id=str(uuid4()),
        ts=now_ts(),
        payload=HelloAckPayload(
            accepted=True,
            device_id=message.payload.device_id,
            negotiated=negotiated,
            limits={"turns_per_min": 30, "tts_seconds_per_min": 120},
        ),
    )


@app.post("/ccp/session/start", response_model=SessionStartedMessage)
async def session_start(message: SessionStartMessage) -> SessionStartedMessage:
    return SessionStartedMessage(
        type="session_started",
        id=str(uuid4()),
        ts=now_ts(),
        payload=SessionStartedPayload(session_id=str(uuid4())),
    )


@app.post("/ccp/turn", response_model=TurnResultMessage)
async def turn(message: TurnMessage) -> TurnResultMessage:
    reply_text = None
    reply_audio_ref = None
    if message.payload.input.kind == "text":
        reply_text = f"echo: {message.payload.input.text or ''}".strip()
    else:
        reply_text = "audio received"
        reply_audio_ref = message.payload.input.audio_ref

    return TurnResultMessage(
        type="turn_result",
        id=str(uuid4()),
        ts=now_ts(),
        payload=TurnResultPayload(
            session_id=message.payload.session_id,
            reply=TurnReply(text=reply_text, audio_ref=reply_audio_ref),
            safety={"blocked": False, "kid_safe_applied": True, "reason": None},
            actions=[],
            meta={"source": "ccp_api_example"},
        ),
    )


@app.post("/ccp/session/end", response_model=SessionEndedMessage)
async def session_end(message: SessionEndMessage) -> SessionEndedMessage:
    return SessionEndedMessage(
        type="session_ended",
        id=str(uuid4()),
        ts=now_ts(),
        payload=SessionEndedPayload(session_id=message.payload.session_id),
    )
