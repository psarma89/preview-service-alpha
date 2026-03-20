"""Minimal token-based authentication.

Expects: Authorization: Bearer <API_TOKEN>

The token is validated against the API_TOKEN environment variable.
This is intentionally simple for a preview-environments demo —
a production system would use JWT/OAuth2.
"""

from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status

from ..settings import Settings, get_settings


@dataclass
class AuthContext:
    token: str


def get_auth_context(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> AuthContext:
    """Extract and validate Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must be: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    if token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

    return AuthContext(token=token)
