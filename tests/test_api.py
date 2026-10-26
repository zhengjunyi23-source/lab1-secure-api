"""Functional tests for the API: auth, protection, injection & XSS behaviour."""
import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def _login(client, username="alice", password="S3cure#Passw0rd"):
    return client.post(
        "/auth/login", json={"username": username, "password": password}
    )


def test_login_success(client):
    resp = _login(client)
    assert resp.status_code == 200
    body = resp.get_json()
    assert "token" in body
    assert body["token_type"] == "Bearer"


def test_login_wrong_password(client):
    resp = client.post(
        "/auth/login", json={"username": "alice", "password": "wrong-password"}
    )
    assert resp.status_code == 401
    assert "token" not in resp.get_json()


def test_data_requires_token(client):
    resp = client.get("/api/data")
    assert resp.status_code == 401


def test_data_with_token(client):
    token = _login(client).get_json()["token"]
    resp = client.get("/api/data", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert "data" in body
    assert any(u["username"] == "alice" for u in body["data"])


def test_invalid_token_rejected(client):
    resp = client.get(
        "/api/data", headers={"Authorization": "Bearer not.a.valid.token"}
    )
    assert resp.status_code == 401


def test_xss_escaped_on_output(client):
    """The stored <script> tag in mallory's 'about' must be escaped on output."""
    token = _login(client).get_json()["token"]
    resp = client.get("/api/data", headers={"Authorization": f"Bearer {token}"})
    body = resp.get_json()
    mallory = next(u for u in body["data"] if u["username"] == "mallory")
    assert "<script>" not in mallory["about"]
    assert "&lt;script&gt;" in mallory["about"]


def test_sqli_parameterised(client):
    """A malicious username must NOT bypass authentication via SQL injection."""
    resp = client.post(
        "/auth/login",
        json={"username": "' OR '1'='1' --", "password": "anything"},
    )
    assert resp.status_code == 401
