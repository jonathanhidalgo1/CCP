from __future__ import annotations


class CCPError(Exception):
    """Base error for the CCP SDK."""


class CCPSchemaError(CCPError):
    """Raised when a message fails JSON Schema validation."""


class CCPHTTPError(CCPError):
    """Raised when an HTTP call fails (non-2xx or invalid payload)."""

    def __init__(self, status_code: int, body: object | None = None):
        super().__init__(f"CCP HTTP error: {status_code}")
        self.status_code = status_code
        self.body = body
