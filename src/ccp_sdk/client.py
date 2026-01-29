from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .errors import CCPHTTPError
from .messages import hello as hello_msg
from .messages import session_end as session_end_msg
from .messages import session_start as session_start_msg
from .messages import turn_audio_ref as turn_audio_ref_msg
from .messages import turn_text as turn_text_msg
from .validator import validate_message


class CCPClient:
    def __init__(
        self,
        *,
        base_url: str,
        device_token: Optional[str] = None,
        timeout_s: float = 10.0,
        validate: bool = True,
    ):
        self._base_url = base_url.rstrip("/")
        self._device_token = device_token
        self._timeout_s = timeout_s
        self._validate = validate
        self._client = httpx.Client(timeout=timeout_s)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CCPClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._device_token:
            headers["Authorization"] = f"Device {self._device_token}"
        return headers

    def _post_ccp(self, path: str, message: Dict[str, Any]) -> Dict[str, Any]:
        if self._validate:
            validate_message(message)

        url = f"{self._base_url}{path}"
        resp = self._client.post(url, headers=self._headers(), json=message)
        if resp.status_code < 200 or resp.status_code >= 300:
            body: Any
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise CCPHTTPError(resp.status_code, body)

        data = resp.json()
        if self._validate and isinstance(data, dict):
            validate_message(data)
        return data

    def hello(
        self,
        *,
        device_id: str,
        device_token: str,
        firmware: str,
        capabilities: Dict[str, Any],
        locale: Optional[str] = None,
    ) -> Dict[str, Any]:
        msg = hello_msg(
            device_id=device_id,
            device_token=device_token,
            firmware=firmware,
            capabilities=capabilities,
            locale=locale,
        )
        return self._post_ccp("/ccp/hello", msg)

    def session_start(self, *, device_id: str) -> Dict[str, Any]:
        return self._post_ccp("/ccp/session/start", session_start_msg(device_id=device_id))

    def turn_text(self, *, session_id: str, text: str) -> Dict[str, Any]:
        return self._post_ccp("/ccp/turn", turn_text_msg(session_id=session_id, text=text))

    def turn_audio_ref(self, *, session_id: str, audio_ref: str) -> Dict[str, Any]:
        return self._post_ccp(
            "/ccp/turn", turn_audio_ref_msg(session_id=session_id, audio_ref=audio_ref)
        )

    def session_end(self, *, session_id: str) -> Dict[str, Any]:
        return self._post_ccp("/ccp/session/end", session_end_msg(session_id=session_id))

    def upload_audio(self, *, audio_bytes: bytes, content_type: str = "audio/wav") -> str:
        url = f"{self._base_url}/v1/media/audio"
        resp = self._client.post(
            url,
            headers={k: v for k, v in self._headers().items() if k.lower() != "content-type"},
            content=audio_bytes,
        )
        if resp.status_code < 200 or resp.status_code >= 300:
            body: Any
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise CCPHTTPError(resp.status_code, body)

        data = resp.json()
        audio_ref = data.get("audio_ref") if isinstance(data, dict) else None
        if not isinstance(audio_ref, str) or not audio_ref:
            raise CCPHTTPError(resp.status_code, data)
        return audio_ref

