

class TestCreateUser:
    def test_create_user(self, client, auth_headers):
        resp = client.post(
            "/api/users",
            json={"email": "alice@example.com", "name": "Alice"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "alice@example.com"
        assert data["name"] == "Alice"
        assert data["id"] is not None

    def test_create_user_duplicate_email(self, client, auth_headers):
        payload = {"email": "dup@example.com", "name": "First"}
        client.post("/api/users", json=payload, headers=auth_headers)
        resp = client.post("/api/users", json=payload, headers=auth_headers)
        assert resp.status_code == 409

    def test_create_user_no_auth(self, client):
        resp = client.post("/api/users", json={"email": "x@x.com", "name": "X"})
        assert resp.status_code == 401

    def test_create_user_bad_token(self, client):
        resp = client.post(
            "/api/users",
            json={"email": "x@x.com", "name": "X"},
            headers={"Authorization": "Bearer wrong-token"},
        )
        assert resp.status_code == 403


class TestListUsers:
    def test_list_users_empty(self, client, auth_headers):
        resp = client.get("/api/users", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_users_returns_created(self, client, auth_headers):
        client.post("/api/users", json={"email": "a@b.com", "name": "A"}, headers=auth_headers)
        resp = client.get("/api/users", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestGetUser:
    def test_get_user(self, client, auth_headers):
        create_resp = client.post(
            "/api/users",
            json={"email": "get@test.com", "name": "Get"},
            headers=auth_headers,
        )
        user_id = create_resp.json()["id"]
        resp = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "get@test.com"

    def test_get_user_not_found(self, client, auth_headers):
        resp = client.get("/api/users/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestUpdateUser:
    def test_update_user(self, client, auth_headers):
        create_resp = client.post(
            "/api/users",
            json={"email": "upd@test.com", "name": "Old"},
            headers=auth_headers,
        )
        user_id = create_resp.json()["id"]
        resp = client.put(
            f"/api/users/{user_id}",
            json={"name": "New"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New"
        assert resp.json()["email"] == "upd@test.com"  # unchanged

    def test_update_user_not_found(self, client, auth_headers):
        resp = client.put("/api/users/99999", json={"name": "X"}, headers=auth_headers)
        assert resp.status_code == 404


class TestDeleteUser:
    def test_delete_user(self, client, auth_headers):
        create_resp = client.post(
            "/api/users",
            json={"email": "del@test.com", "name": "Del"},
            headers=auth_headers,
        )
        user_id = create_resp.json()["id"]
        resp = client.delete(f"/api/users/{user_id}", headers=auth_headers)
        assert resp.status_code == 204

        resp = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert resp.status_code == 404

    def test_delete_user_not_found(self, client, auth_headers):
        resp = client.delete("/api/users/99999", headers=auth_headers)
        assert resp.status_code == 404
