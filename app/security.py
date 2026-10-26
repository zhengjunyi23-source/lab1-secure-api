"""Security helpers: JWT issuing/verification, XSS escaping, auth middleware.

- JWT (PyJWT, HMAC-SHA256) is signed with the application secret; protected
  endpoints verify it on every request (protection against Broken Auth).
- Every string returned in JSON is HTML-escaped so a stored/reflected payload
  cannot be executed in a victim's browser (protection against XSS).
"""
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

ALGORITHM = "HS256"


def _secret():
    return current_app.config["SECRET_KEY"]


def create_token(user_id: int) -> str:
    """Issue a signed JWT for the given user id."""
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=current_app.config["JWT_EXPIRES_MINUTES"]
    )
    payload = {
        "sub": str(user_id),          # subject: the authenticated user
        "iat": datetime.now(timezone.utc),
        "exp": exp,                    # expiration
        "iss": "secure-api",           # issuer
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def xss_safe(obj):
    """Recursively HTML-escape every string in a JSON-serialisable structure.

    This is the single output-serialisation gate: any user-controlled text
    stored in the database is escaped before it is returned to the client.
    """
    if isinstance(obj, str):
        # quote=True also escapes characters that could break attribute context
        from html import escape
        return escape(obj, quote=True)
    if isinstance(obj, list):
        return [xss_safe(item) for item in obj]
    if isinstance(obj, dict):
        return {key: xss_safe(value) for key, value in obj.items()}
    return obj


def require_token(f):
    """Middleware: verify a Bearer JWT before allowing the wrapped endpoint.

    Requests without a valid token are rejected with 401, which is exactly
    the behaviour the manual expects for "access without a token is denied".
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify(error="missing bearer token"), 401

        token = auth[7:].strip()
        try:
            payload = jwt.decode(
                token, _secret(), algorithms=[ALGORITHM], issuer="secure-api"
            )
        except jwt.ExpiredSignatureError:
            return jsonify(error="token expired"), 401
        except jwt.InvalidTokenError:
            return jsonify(error="invalid token"), 401

        g.user_id = int(payload["sub"])
        return f(*args, **kwargs)

    return wrapper
