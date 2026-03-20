"""Unit tests for the auth module."""


class TestAuth:
    def test_missing_header(self, client):
        resp = client.get("/api/users")
        assert resp.status_code == 401
        assert "Missing Authorization" in resp.json()["detail"]

    def test_malformed_header(self, client):
        resp = client.get("/api/users", headers={"Authorization": "Token abc"})
        assert resp.status_code == 401
        assert "Bearer" in resp.json()["detail"]

    def test_invalid_token(self, client):
        resp = client.get("/api/users", headers={"Authorization": "Bearer nope"})
        assert resp.status_code == 403
        assert "Invalid token" in resp.json()["detail"]

    def test_valid_token(self, client, auth_headers):
        resp = client.get("/api/users", headers=auth_headers)
        assert resp.status_code == 200
