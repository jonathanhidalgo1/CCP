from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict

from jsonschema import Draft202012Validator
from jsonschema.validators import RefResolver

from .errors import CCPSchemaError


_MESSAGE_TYPE_TO_SCHEMA = {
    "hello": "hello.json",
    "hello_ack": "hello-ack.json",
    "session_start": "session-start.json",
    "session_started": "session-started.json",
    "turn": "turn.json",
    "turn_result": "turn-result.json",
    "session_end": "session-end.json",
    "session_ended": "session-ended.json",
    "error": "error.json",
}


def _load_all_schemas() -> Dict[str, Dict[str, Any]]:
    schema_pkg = resources.files("ccp_sdk.schemas")
    schemas: Dict[str, Dict[str, Any]] = {}
    for entry in schema_pkg.iterdir():
        if entry.name.endswith(".json"):
            schemas[entry.name] = json.loads(entry.read_text(encoding="utf-8"))
    return schemas


_ALL_SCHEMAS = _load_all_schemas()


def _make_resolver(schema: Dict[str, Any]) -> RefResolver:
    store: Dict[str, Any] = {}
    for filename, schema_obj in _ALL_SCHEMAS.items():
        store[filename] = schema_obj
        schema_id = schema_obj.get("$id")
        if isinstance(schema_id, str):
            store[schema_id] = schema_obj

    return RefResolver.from_schema(schema, store=store)


def validate_message(message: Dict[str, Any]) -> None:
    msg_type = message.get("type")
    if not isinstance(msg_type, str) or not msg_type:
        raise CCPSchemaError("Missing or invalid message.type")

    schema_filename = _MESSAGE_TYPE_TO_SCHEMA.get(msg_type)
    if schema_filename is None:
        raise CCPSchemaError(f"Unknown message type: {msg_type}")

    schema = _ALL_SCHEMAS.get(schema_filename)
    if schema is None:
        raise CCPSchemaError(f"Schema not bundled: {schema_filename}")

    validator = Draft202012Validator(schema, resolver=_make_resolver(schema))
    errors = sorted(validator.iter_errors(message), key=lambda e: e.path)
    if errors:
        first = errors[0]
        loc = "/".join(str(p) for p in first.path) or "<root>"
        raise CCPSchemaError(f"Invalid CCP message at {loc}: {first.message}")
