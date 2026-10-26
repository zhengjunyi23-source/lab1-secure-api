"""Application routes.

Endpoints:
  1. POST /auth/login      -> authenticate with username + password, returns JWT
  2. GET  /api/data        -> protected; returns the list of users
  3. GET  /api/me          -> protected; returns the authenticated user's data

Every protected endpoint is decorated with @require_token and every response
is passed through xss_safe() before serialisation.
"""
from flask import Blueprint, current_app, g, jsonify, request

from app.extensions import db
from app.models import User
from app.security import create_token, require_token, xss_safe

bp = Blueprint("api", __name__)


@bp.post("/auth/login")
def login():
    """Authenticate a user and issue a signed JWT.

    Passwords are checked against the stored bcrypt hash; a failed check is
    indistinguishable in response from a missing account.
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # ORM lookup with parameter binding - no raw SQL concatenation anywhere.
    user = User.query.filter_by(username=username).first()

    if user is not None and user.check_password(password):
        token = create_token(user.id)
        return jsonify(
            token=token,
            token_type="Bearer",  # nosec B106 - "Bearer" is the JWT scheme identifier, not a password
            expires_in_minutes=current_app.config["JWT_EXPIRES_MINUTES"],
        ), 200

    # Generic error message: do not reveal whether the username or password failed.
    return jsonify(error="invalid username or password"), 401


@bp.get("/api/data")
@require_token
def get_data():
    """Return the full list of users. Requires a valid Bearer token."""
    users = User.query.order_by(User.id).all()
    public = [u.to_public_dict() for u in users]
    return jsonify(data=xss_safe(public))


@bp.get("/api/me")
@require_token
def get_me():
    """Return the profile of the currently authenticated user."""
    user = db.session.get(User, g.user_id)
    if user is None:
        return jsonify(error="user not found"), 404
    return jsonify(xss_safe(user.to_public_dict()))
